---
name: hindsight-troubleshooting
description: Hindsight 本地嵌入模式排错指南 — 从模块缺失到 glibc 不兼容的完整诊断链路。
version: 1.0.0
author: 上河一号
metadata:
  hermes:
    tags: [hindsight, memory, debugging, glibc, pgvector, pg0]
    priority: normal
---

# Hindsight 本地模式排错指南

## 环境前提

Hindsight 本地嵌入模式需要：
1. Python 包：`hindsight-all-slim`（或 `hindsight-all`）+ `hindsight-client` + `hindsight-embed` + `hindsight-api-slim`
2. 嵌入式 PostgreSQL：`pg0`（由 `hindsight-embed` 自动管理）
3. pgvector 扩展：随 pg0 安装，但 **要求 glibc ≥ 2.38**
4. LLM API key：用于记忆提取和反思

## 故障诊断链路

### 症状 1：`No module named 'hindsight'`

**根因：** `hindsight-all-slim` 不提供 `hindsight` 顶层命名空间。Hermes plugin 代码做 `from hindsight import HindsightEmbedded`，但 slim 包只有 `hindsight_client`、`hindsight_api`、`hindsight_embed` 等子包。

**修复：** 安装 `hindsight-all`（非 slim），或手动补上缺失模块：

```bash
# 方案 A：安装完整包（pip 可能超时，包依赖大）
pip install hindsight-all==0.5.4

# 方案 B：手动提取（更快，只需 12KB 的命名空间包装）
pip download hindsight-all==0.5.4 --no-deps -d /tmp/hindsight-tmp
cd /tmp/hindsight-tmp && unzip hindsight_all-0.5.4-py3-none-any.whl -d extracted
cp -r extracted/hindsight/ <hermes-venv>/lib/python3.11/site-packages/hindsight/

# 验证
<hermes-venv>/bin/python3 -c "from hindsight import HindsightEmbedded; print('OK')"
```

**关键发现：** `hindsight-all` 包只有 12KB，就是 `hindsight/__init__.py` + `embedded.py` + `client_wrapper.py` + `server.py` 的薄包装。`HindsightEmbedded` = `DaemonEmbedManager`（管 daemon 进程）+ `Hindsight` client（连 localhost daemon）的组合。

### 症状 2：`Database migration failed`

**根因：** pg0 内置的 PostgreSQL 18.1 附带的 pgvector 扩展需要 glibc ≥ 2.38，但 Ubuntu 22.04 只有 glibc 2.35。

**错误信息特征：**
```
sqlalchemy.exc.OperationalError: (psycopg2.errors.UndefinedFile) 
could not load library "/home/hangskf/.pg0/installation/18.1.0/lib/vector.so": 
/lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.38' not found
```

**诊断命令：**
```bash
ldd --version | head -1  # 查看当前 glibc 版本
# Ubuntu 22.04 = glibc 2.35 (不够)
# Ubuntu 24.04 = glibc 2.39 (够)
```

**修复方案（优先级排序）：**

| 方案 | 可行性 | 代价 |
|------|--------|------|
| 升级 Ubuntu 到 24.04 | ✅ 最干净 | 系统升级约 30-60 分钟，服务中断 |
| Docker 跑 pgvector/pgvector 容器 | ✅ 可行 | 多一个容器依赖，需手动管理 |
| 切 Hindsight Cloud 模式 | ✅ 最轻量 | 需要 API key，数据存云端 |

**Docker 替代方案步骤：**
```bash
# 1. 启动 pgvector 容器
docker run -d --name hindsight-pg \
  -e POSTGRES_PASSWORD=hindsight -e POSTGRES_DB=hindsight \
  -p 5432:5432 pgvector/pgvector:pg17

# 2. 修改 ~/.hermes/hindsight/config.json
# mode: "local_external"
# api_url: "http://localhost:9177"

# 3. 启动 hindsight-api daemon（指向 Docker PostgreSQL）
export HINDSIGHT_API_DATABASE_URL=postgresql://postgres:hindsight@localhost:5432/hindsight
export HINDSIGHT_API_LLM_PROVIDER=openai
export HINDSIGHT_API_LLM_API_KEY=<your-key>
export HINDSIGHT_API_LLM_MODEL=deepseek-v4-flash
export HINDSIGHT_API_LLM_BASE_URL=https://api.deepseek.com/v1
hindsight-api --daemon --idle-timeout 0 --port 9177
```

### 症状 3：`RuntimeError: Failed to start daemon for profile 'hermes'`

**错误特征：**
```
RuntimeError: Failed to start daemon for profile 'hermes'
RuntimeError: Cannot use HindsightEmbedded after it has been closed
WARNING plugins.memory.hindsight: Hindsight retain failed: Failed to start daemon for profile 'hermes'
```

**根因分析：**
1. HindsightEmbedded 数据库损坏或锁文件残留
2. `.env` 中 `API_SERVER_KEY` 缺失或无效（导致 401 认证失败，进而 daemon 启动失败）
3. 嵌入模式进程异常退出后未正确清理
4. **config.yaml 中 hindsight provider 缺少模型配置**（仅 `provider: hindsight`，无 model/base_url/api_key）

**修复流程（按顺序执行）：**

```bash
# Step 1: 彻底停止 gateway
systemctl --user stop hermes-gateway.service
sleep 5

# Step 2: 清理 hindsight 数据库和锁文件（关键）
rm -rf ~/.hermes/hindsight/*
rm -f ~/.hermes/*.lock ~/.cache/hermes/*.lock

# Step 3: 检查并修复 .env（最常见根因）
# 用 cat > 覆盖，不要用 cat >> 追加
PASS=$(openssl rand -base64 32 | tr -d '\n')
cat > ~/.hermes/.env << EOF
API_SERVER_ENABLED=true
API_SERVER_PORT=8642
API_SERVER_KEY=$PASS
EOF

# 验证写入
cat ~/.hermes/.env

# Step 3b: 检查 config.yaml 中 hindsight 是否有模型配置
# 如果只有 "provider: hindsight" 而无 model/base_url/api_key，需补充：
# memory:
#   provider: hindsight
#   model: <主模型名>
#   provider: custom
#   base_url: <主模型base_url>
#   api_key_env: MAIN_API_KEY

# Step 4: 重启
systemctl --user start hermes-gateway.service
sleep 5

# Step 5: 验证
hermes gateway status
journalctl --user -u hermes-gateway.service -n 30 --no-pager
```

**关键陷阱：`.env` 写入方式**

| 命令 | 效果 | 风险 |
|------|------|------|
| `cat >> ~/.hermes/.env` | **追加**，可能产生重复/无效配置 | ❌ 常见错误 |
| `cat > ~/.hermes/.env` | **覆盖**，确保内容完整 | ✅ 正确做法 |

**验证要点：**
- `cat ~/.hermes/.env` 必须显示完整的三行配置
- `API_SERVER_KEY=` 后面必须有值，不能为空
- 密码不能包含未闭合的引号或换行

### 症状 4：Daemon 启动但 9177 端口不监听

**可能原因：**
1. API key 未传入（daemon 用 uv 独立环境，不读 hermes 的 `.env`）
2. pg0 初始化卡住（首次需要下载嵌入模型，~200MB）
3. HuggingFace 网络不可达（嵌入模型加载重试中）

**检查方法：**
```bash
# 看 daemon 进程
ps aux | grep hindsight-api

# 看 daemon stderr（关键排错信息在这里）
cat /proc/<pid>/fd/2 | tail -30

# 看 profile 日志
cat ~/.hindsight/profiles/hermes.log | tail -50

# 看 pg0 日志
tail -20 ~/.pg0/instances/hindsight-embed-hermes/data/log/postgresql*.log
```

**API key 修复：** 确保 `~/.hindsight/profiles/hermes.env` 包含正确 key：
```
HINDSIGHT_API_LLM_PROVIDER=openai
HINDSIGHT_API_LLM_API_KEY=<your-deepseek-key>
HINDSIGHT_API_LLM_MODEL=deepseek-v4-flash
HINDSIGHT_API_LLM_BASE_URL=https://api.deepseek.com/v1
```

## 配置要点

### DeepSeek 作为 LLM 后端

**模型选择：必须用 `deepseek-chat`，不能用 `deepseek-v4-flash`/`deepseek-reasoner`。**

`deepseek-reasoner` 系列模型不支持 `tool_choice` 参数，Hindsight 的 reflect 功能内部会传 `tool_choice`，导致 400 错误：

```
API error: HTTP 400: "deepseek-reasoner does not support this tool_choice"
```

**现象：** recall/retain 正常，但 reflect 超时或报错。daemon 日志可见 `APIConnectionError` 后跟 400 错误。

`hindsight/config.json` 中 `llm_provider` 必须设为 `openai_compatible`（DeepSeek 兼容 OpenAI API），但 daemon 的 env 文件中需要映射为 `openai`（因为 daemon 内部把 `openai_compatible` 映射为 `openai`）：

```json
// config.json（hermes 视角）
{
  "llm_provider": "openai_compatible",
  "llm_base_url": "https://api.deepseek.com/v1",
  "llm_model": "deepseek-chat"
}
```

```
# hermes.env（daemon 视角）
HINDSIGHT_API_LLM_PROVIDER=openai
HINDSIGHT_API_LLM_BASE_URL=https://api.deepseek.com/v1
HINDSIGHT_API_LLM_MODEL=deepseek-chat
```

| DeepSeek 模型 | Hindsight 兼容 | 原因 |
|--------------|---------------|------|
| `deepseek-chat` | ✅ | 标准 chat 模型，支持 tool_choice |
| `deepseek-v4-flash` | ❌ | reasoner 模型，不支持 tool_choice |
| `deepseek-reasoner` | ❌ | 同上 |

| `deepseek-reasoner` | ❌ | 同上 |

### 切换 LLM 后端（实操流程）

Hindsight 的 LLM 配置全在 `~/.hindsight/profiles/hermes.env`，改完需重启 hindsight-api 生效。

**关键陷阱 1：API Key 脱敏**

Hermes 的 `~/.hermes/config.yaml` 中的 `api_key` 字段做了**存储时脱敏**——文件里存的就是 `sk-XDO...HI2b`（省略号是真实存储内容），不是显示遮掩。无论用 `cat`、`hexdump`、`python read()` 都只能拿到脱敏后的值。

**关键陷阱 2：env 文件中的 Key 也可能被脱敏**

用户在终端用 `sed` 或 `echo` 写入 API Key 时，某些 shell 环境或工具会自动脱敏 key 值。**必须验证文件里存的是真实完整 key**：

```bash
# 用 python 读原始内容验证（cat 会脱敏显示）
python3 -c "print(open('/home/hangskf/.hindsight/profiles/hermes.env').read())"
# 确认 API_KEY 行是完整的 sk-xxx，不是 sk-xxx...xxx
```

如果 key 被脱敏了，用 python 重写整个 env 文件（最可靠，不被 shell 脱敏）：

```python
python3 -c "
env = '''HINDSIGHT_API_LLM_PROVIDER=openai
HINDSIGHT_API_LLM_API_KEY=粘贴完整key
HINDSIGHT_API_LLM_MODEL=英伟达/z-ai/glm5
HINDSIGHT_API_LOG_LEVEL=info
HINDSIGHT_API_LLM_BASE_URL=https://api.xinjianya.top/
HF_HUB_OFFLINE=true
TRANSFORMERS_OFFLINE=true'''
with open('/home/hangskf/.hindsight/profiles/hermes.env','w') as f:
    f.write(env)
"
```

**关键陷阱 3：huggingface 离线模式**

VPS 网络不通 huggingface.co 时，hindsight-api 启动会卡在嵌入模型/重排序模型的 HEAD 请求验证上，重试5次后报 `RuntimeError: Cannot send a request, as the client has been closed` 退出。

**修复：** 在 env 文件中加入离线环境变量（模型已在本地缓存，不需要联网）：

```
HF_HUB_OFFLINE=true
TRANSFORMERS_OFFLINE=true
```

**关键陷阱 4：hindsight-api 启动参数**

- `hindsight-api` **不认 `--profile` 参数**，它靠环境变量驱动（读取 `~/.hindsight/profiles/hermes.env`）
- `hindsight-worker` 也**没有 `restart` 子命令**，它只接受 `--worker-id` 等参数
- 正确的重启方式：先 kill 进程，再用环境变量启动

```bash
# 1. 杀掉旧进程
pkill -f "hindsight-api" 2>/dev/null

# 2. 启动（必须传入离线环境变量）
HF_HUB_OFFLINE=true TRANSFORMERS_OFFLINE=true hindsight-api --port 9177

# 3. 验证启动成功
sleep 10 && head -10 ~/.hindsight/profiles/hermes.log
# 应看到：OpenAI-compatible client initialized: provider=openai, model=你的模型名, base_url=...
```

**一键切换脚本：** `~/switch-hindsight-llm.sh` 已创建，自动写入模型名+base_url+离线标志，用户只需提供 API Key 参数：

```bash
bash ~/switch-hindsight-llm.sh sk-你的完整key
```

**注意：** 如果 `hindsight-api --port 9177` 报 `LLM API key is required`，说明 env 文件未被自动加载。需手动 export 所有变量后再启动：

```bash
export $(cat ~/.hindsight/profiles/hermes.env | xargs)
hindsight-api --port 9177
```

**通用要求：** 无论换什么 LLM 后端，模型必须支持 `tool_choice` 参数，否则 reflect 功能会 400 报错。

### 不重启 Gateway 的限制

Hermes agent 进程在启动时加载 Hindsight 模块。修复 `import` 问题后必须重启 gateway 才能生效：
```bash
hermes gateway restart  # 或重启服务
```

## 排错优先级

```
1. 验证 import → python3 -c "from hindsight import HindsightEmbedded"
2. 验证 glibc → ldd --version
3. 验证 pg0 → ls ~/.pg0/instances/
4. 验证 daemon → ss -tlnp | grep 9177
5. 验证 API → curl http://localhost:9177/health (如可用)
6. 验证 recall → python3 -c "from hindsight_client import Hindsight; c=Hindsight('http://localhost:9177'); print(c.recall('hermes','test','low'))"
```

### 症状 5：`No module named 'pg0'` — `pg0-embedded` 缺失

**错误特征：**
```
ImportError: pg0-embedded is required for embedded PostgreSQL.
Install it with: pip install 'hindsight-api-slim[embedded-db]'
```

**根因：** `hindsight-api-slim` 是精简版，**不包含** `pg0-embedded` 依赖。嵌入式 PostgreSQL 需要单独安装 `[embedded-db]` 额外依赖。

**修复：**
```bash
# 在 hermes-agent 的 venv 中安装
cd ~/.hermes/hermes-agent
venv/bin/pip install 'hindsight-api-slim[embedded-db]'
```

**验证：**
```bash
# 测试 pg0 可导入
venv/bin/python -c "from hindsight_api.pg0 import EmbeddedPostgres; print('OK')"

# 测试 daemon 启动
venv/bin/hindsight-embed daemon start -p hermes
```

**注意：** `hindsight` 包（PyPI 上的 0.1.7 版本）因 `use_2to3` 已废弃无法构建，但 Hermes 实际使用的是 `hindsight-api-slim` + `hindsight_client` 组合，这两个包正常安装即可，无需 `hindsight` 顶层包。

## 参考文件

- `references/hindsight-daemon-failure.md` — Daemon 启动失败的完整故障日志与修复流程
- `references/pg0-embedded-missing.md` — pg0-embedded 缺失的诊断与修复（2026-05-05）
- `references/hindsight-embed-cli.md` — `hindsight-embed` CLI 工具使用指南（2026-05-05）

## `hindsight-embed` CLI 工具

`hindsight-api-slim` 安装后提供 `hindsight-embed` CLI，用于管理 profile 和 daemon：

```bash
# Profile 管理
hindsight-embed profile list          # 列出所有 profile
hindsight-embed profile show          # 显示当前活跃 profile
hindsight-embed profile show -p hermes  # 显示指定 profile
hindsight-embed profile set-active hermes  # 设置活跃 profile

# Daemon 管理
hindsight-embed daemon start -p hermes   # 启动 daemon
hindsight-embed daemon stop -p hermes    # 停止 daemon
hindsight-embed daemon status -p hermes  # 检查 daemon 状态
hindsight-embed daemon logs -p hermes    # 查看 daemon 日志

# Memory 操作
hindsight-embed memory recall hermes "query" -p hermes  # 检索记忆
hindsight-embed memory retain hermes "content" -p hermes  # 存储记忆
hindsight-embed bank list -p hermes  # 列出记忆库
```

**注意：** `hindsight-embed` 不认 `--profile` 全局参数，profile 通过 `-p` 子命令参数指定。

## `.env` 配置恢复机制

当 `.env` 被 `cat >` 意外覆盖时，系统会生成备份：

| 备份文件 | 内容 | 用途 |
|---|---|---|
| `~/.hermes/.env.current.bak` | 覆盖前的 `.env` 内容（仅被覆盖的那次） | 恢复被覆盖的配置 |
| `~/.hermes/state-snapshots/<timestamp>/.env` | 完整 `.env` 快照 | 恢复整个配置 |

**恢复 API_SERVER 配置示例：**
```bash
# 从 .env.current.bak 提取 API_SERVER 配置
grep "API_SERVER" ~/.hermes/.env.current.bak

# 追加到当前 .env
cat ~/.hermes/.env.current.bak | grep "API_SERVER" >> ~/.hermes/.env

# 或从 state-snapshots 恢复
cp ~/.hermes/state-snapshots/20260503-012828-pre-update/.env ~/.hermes/.env
```

**验证 API Server 是否正常运行：**
```bash
# 健康检查
curl -s http://127.0.0.1:8642/health
# 应返回: {"status": "ok", "platform": "hermes-agent"}

# 模型列表
curl -s http://127.0.0.1:8642/v1/models -H "Authorization: Bearer <API_SERVER_KEY>"
# 应返回: {"object": "list", "data": [{"id": "hermes-agent", ...}]}

# 端口监听检查
ss -tlnp | grep 8642
```
