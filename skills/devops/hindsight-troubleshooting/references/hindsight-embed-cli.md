# hindsight-embed CLI 使用指南

## 工具来源

`hindsight-api-slim` 安装后提供以下 CLI 工具：

| 命令 | 功能 |
|---|---|
| `hindsight-embed` | Profile 和 daemon 管理 |
| `hindsight-api` | API 服务器（直接运行） |
| `hindsight-worker` | 后台 worker 进程 |
| `hindsight-admin` | 管理工具 |

## Profile 管理

Hindsight 支持多 profile，每个 profile 有独立的配置和数据库：

```bash
# 列出所有 profile
hindsight-embed profile list

# 显示当前活跃 profile
hindsight-embed profile show

# 显示指定 profile 详情
hindsight-embed profile show -p hermes

# 设置活跃 profile
hindsight-embed profile set-active hermes

# 创建新 profile
hindsight-embed profile create newprofile --port 9178

# 删除 profile
hindsight-embed profile delete oldprofile
```

每个 profile 的配置文件位置：`~/.hindsight/profiles/<name>.env`

## Daemon 管理

```bash
# 启动 daemon
hindsight-embed daemon start -p hermes

# 停止 daemon
hindsight-embed daemon stop -p hermes

# 检查 daemon 状态
hindsight-embed daemon status -p hermes

# 查看 daemon 日志
hindsight-embed daemon logs -p hermes
hindsight-embed daemon logs -p hermes -f  # 实时跟踪
```

**daemon 启动成功标志：**
```
✓ Daemon Started (hermes @ :9177)
✓ Daemon responding, verifying stability...
✓ Daemon started successfully!
```

**daemon 状态检查输出：**
```
╭─────────────────────────────── Daemon Status ────────────────────────────────╮
│ Daemon is running                                                            │
│   URL: http://127.0.0.1:9177                                                 │
│   Logs: /home/hangskf/.hindsight/profiles/hermes.log                         │
│   Database: /home/hangskf/.pg0/instances/hindsight-embed-hermes              │
╰──────────────────────────────────────────────────────────────────────────────╯
```

## Memory 操作

```bash
# 检索记忆
hindsight-embed memory recall hermes "query string" -p hermes

# 存储记忆
hindsight-embed memory retain hermes "content to store" -p hermes

# 生成反思/上下文答案
hindsight-embed memory reflect hermes "query string" -p hermes

# 列出记忆库
hindsight-embed bank list -p hermes
```

## 常见排查

### Daemon 启动失败

1. 检查 pg0-embedded 是否安装：
   ```bash
   venv/bin/python -c "from hindsight_api.pg0 import EmbeddedPostgres; print('OK')"
   ```

2. 检查 profile env 文件：
   ```bash
   cat ~/.hindsight/profiles/hermes.env
   # 必须包含：LLM_PROVIDER, LLM_API_KEY, LLM_MODEL, LLM_BASE_URL
   ```

3. 检查 daemon 日志：
   ```bash
   tail -50 ~/.hindsight/profiles/hermes.log
   ```

4. 检查 PostgreSQL 实例：
   ```bash
   ls ~/.pg0/instances/
   cat ~/.pg0/instances/hindsight-embed-hermes/data/log/postgresql-*.log | tail -20
   ```

### HuggingFace 网络不可达

VPS 无法访问 huggingface.co 时，daemon 启动会卡在模型下载。解决方案：

```bash
# 方案 A：离线模式（模型已本地缓存）
export HF_HUB_OFFLINE=true
export TRANSFORMERS_OFFLINE=true
hindsight-embed daemon start -p hermes

# 方案 B：使用国内镜像源
export HF_ENDPOINT=https://hf-mirror.com
hindsight-embed daemon start -p hermes
```

## 与 Hermes Gateway 的关系

- `hindsight-embed daemon` 是独立进程，不依赖 Gateway
- Gateway 启动时会自动连接已运行的 hindsight daemon
- 如果 daemon 未运行，Gateway 会尝试自动启动（可能失败）
- 推荐手动管理 daemon：`hindsight-embed daemon start -p hermes`
