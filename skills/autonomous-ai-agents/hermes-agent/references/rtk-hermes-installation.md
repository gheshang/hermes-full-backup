# RTK-Hermes 安装与排错

> 来源：2026-05-19 session — RTK-Hermes 插件安装实战

## 核心陷阱：pip 包名冲突

**`pip install rtk` 装的是 GPS 串口库（Rust Type Kit），不是 rtk-ai 的 shell 输出过滤工具！**

这是最容易被踩的坑。PyPI 上 `rtk` 包和 rtk-ai 的 `rtk` 完全无关。

### 正确安装步骤

#### 1. 安装 Python 插件（进入 Hermes venv）

```bash
/home/hangskf/.hermes/hermes-agent/venv/bin/pip install rtk-hermes
```

> 不要用系统 pip，要用 Hermes 的 venv pip。

#### 2. 下载 rtk 二进制（独立下载，不通过 pip）

```bash
# 从 GitHub releases 下载
curl -fsSL -o /tmp/rtk.tar.gz "https://github.com/rtk-ai/rtk/releases/download/v0.40.0/rtk-x86_64-unknown-linux-musl.tar.gz"
tar -xzf /tmp/rtk.tar.gz -C /tmp
chmod +x /tmp/rtk

# 放到 PATH 中
mkdir -p ~/.local/bin
cp /tmp/rtk ~/.local/bin/
```

> ⚠️ `rtk` 二进制没有 pip/cargo 安装渠道，必须从 GitHub releases 下载。
> 
> Linux x86_64 的二进制包名：`rtk-x86_64-unknown-linux-musl.tar.gz`
> 
> 其他架构：`rtk-aarch64-unknown-linux-gnu.tar.gz`（ARM Linux）、`rtk-aarch64-apple-darwin.tar.gz`（ARM macOS）

#### 3. 启用插件

在 `~/.hermes/config.yaml` 中添加：

```yaml
plugins:
  enabled:
  - rtk-rewrite
```

> ⚠️ `hermes plugins enable rtk-rewrite` CLI 命令可能失败，建议直接编辑 config.yaml。

#### 4. 重启 Hermes 会话

插件通过 `pre_tool_call` 钩子注册，必须重启会话才能加载。

### 验证

```bash
# 检查 rtk 二进制
rtk --version          # 应显示 rtk 0.40.0

# 检查插件状态（重启后）
/rtk status            # 在 Hermes 会话中

# 测试重写
rtk rewrite "git status"  # 应返回 "rtk git status"
```

### 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `RTK_HERMES_MODE` | `rewrite` | `rewrite`/`suggest`/`off` |
| `RTK_HERMES_TIMEOUT_MS` | `2000` | 重写超时（毫秒） |
| `RTK_HERMES_PREVIEW_MARKER` | `true` | 命令前加 `: RTK &&` 标记 |
| `RTK_HERMES_BACKENDS` | `local` | 生效的后端 |

### 工作原理

```
Hermes 想执行:  git status
插件拦截 → 调用 rtk rewrite "git status"
返回:         rtk git status
Hermes 执行:  rtk git status  → 过滤后的精简输出返回给 LLM
```

节省 60-90% 的 LLM token。

### 失败降级

- RTK 二进制不存在 → 钩子不注册，原命令原样执行
- `rtk rewrite` 超时 → 原命令原样执行
- `rtk rewrite` 返回 exit code 1（无等价）→ 原命令原样执行
- `rtk rewrite` 返回 exit code 2（拒绝）→ 原命令原样执行

**不会中断工作，只是不节省 token。**

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `rtk: command not found` | 二进制没放 PATH | 检查 `~/.local/bin` 是否在 PATH |
| 插件不生效 | 没重启会话 | `/reset` 或重启 Hermes |
| `pip install rtk` 装错包 | PyPI 包名冲突 | 卸载，用 GitHub releases 下载二进制 |
| `hermes plugins enable` 失败 | CLI 命令 bug | 直接编辑 config.yaml |

### 资源

- RTK 项目：https://github.com/rtk-ai/rtk
- RTK-Hermes 插件：https://github.com/ogallotti/rtk-hermes
- 安装脚本：`curl -fsSL https://rtk-ai.app/install.sh | bash`（可能超时）
