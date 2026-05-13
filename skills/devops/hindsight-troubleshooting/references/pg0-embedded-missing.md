# pg0-embedded 缺失诊断与修复

**会话日期：** 2026-05-05

## 故障现象

Hindsight daemon 启动失败，日志中出现：

```
ModuleNotFoundError: No module named 'pg0'
ImportError: pg0-embedded is required for embedded PostgreSQL.
Install it with: pip install 'hindsight-api-slim[embedded-db]'
```

daemon 日志路径：`~/.hindsight/profiles/hermes.log`

## 根因

`hindsight-api-slim` 是精简安装包，**不包含** `pg0-embedded` 依赖。

Hindsight 的嵌入式模式需要：
1. `hindsight-api-slim` — API 服务器核心
2. `hindsight-client` — 客户端库
3. `pg0-embedded` — 嵌入式 PostgreSQL（**额外依赖，需显式安装**）

## 修复命令

```bash
# 进入 hermes-agent 虚拟环境
cd ~/.hermes/hermes-agent

# 安装缺失的 pg0-embedded
venv/bin/pip install 'hindsight-api-slim[embedded-db]'

# 验证安装
venv/bin/python -c "from hindsight_api.pg0 import EmbeddedPostgres; print('OK')"

# 启动 daemon
venv/bin/hindsight-embed daemon start -p hermes

# 验证运行
venv/bin/hindsight-embed daemon status -p hermes
```

## 验证 recall 功能

```bash
venv/bin/hindsight-embed memory recall hermes "test" -p hermes
```

预期输出：搜索返回记忆结果，而非连接错误。

## 预防

将 `hindsight-api-slim[embedded-db]` 加入 `requirements.txt` 或 `pyproject.toml` 的依赖列表，防止环境重建时再次缺失。

## 相关错误

| 错误 | 含义 | 修复 |
|------|------|------|
| `No module named 'hindsight'` | `hindsight-all-slim` 不提供顶层命名空间 | 安装 `hindsight-all` 或手动补模块 |
| `No module named 'pg0'` | `pg0-embedded` 未安装 | `pip install 'hindsight-api-slim[embedded-db]'` |
| `use_2to3 is invalid` | `hindsight` 包（0.1.7）已废弃 | 忽略，实际不需要这个包 |

## 关键发现

- `hindsight` 包（PyPI 0.1.7）因 `use_2to3` 废弃无法构建，但 Hermes 实际使用的是 `hindsight-api-slim` + `hindsight_client` 组合
- `hindsight-api-slim[embedded-db]` 额外依赖包含 `pg0-embedded`，这是嵌入式 PostgreSQL 的唯一来源
- 安装后无需重启 hermes-agent，daemon 可独立启动
