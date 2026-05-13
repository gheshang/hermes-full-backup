---
name: cc-switch-setup
description: 在headless Linux VPS上部署CC Switch CLI + Claude Code的完整流程。包括安装、provider配置（非交互式）、proxy启动、环境变量、开机自启、验证。适用于无法使用GUI的场景。
version: 2.0.0
---

# CC Switch CLI + Claude Code 部署指南

## 适用场景
- headless Linux VPS（无GUI）
- Claude Code通过本地代理转发到非Anthropic API（如z-ai/MiniMax等OpenAI兼容提供商）
- 需要Anthropic→OpenAI协议转换

## 安装步骤

### 1. 安装 Claude Code
```bash
npm install -g @anthropic-ai/claude-code
claude --version # 验证
```

### 2. 安装 CC Switch CLI
```bash
curl -fsSL https://github.com/SaladDay/cc-switch-cli/raw/main/install.sh | bash
cc-switch --version # 验证
```

### 3. 添加Provider
**交互式（需TTY）**：
```bash
cc-switch provider add -a claude
```

**非交互式（无TTY时）**：直接写SQLite数据库
```python
import sqlite3, json, time, os
conn = sqlite3.connect(os.path.expanduser('~/.cc-switch/cc-switch.db'))
c = conn.cursor()
provider_id = "your-provider-name"
config = json.dumps({
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-full-api-key",
    "ANTHROPIC_BASE_URL": "https://your-api-url/v1",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "your-model",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "your-model",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "your-model",
    "ANTHROPIC_MODEL": "your-model"
  }
})
c.execute("INSERT OR REPLACE INTO providers (id, app_type, name, settings_config, is_current, created_at) VALUES (?,?,?,json(?),1,?)",
  (provider_id, 'claude', provider_id, config, int(time.time())))
conn.commit()
conn.close()
```

### 4. 启用Proxy + Takeover
```bash
cc-switch proxy enable -a claude
cc-switch proxy serve --takeover claude &
```

### 5. 设置环境变量
```bash
cat > ~/.cc-switch/env.sh << 'EOF'
export ANTHROPIC_BASE_URL=http://127.0.0.1:15721
export ANTHROPIC_AUTH_TOKEN=your-real-api-key-here
EOF

echo 'source ~/.cc-switch/env.sh' >> ~/.bashrc
source ~/.cc-switch/env.sh
```

### 6. 开机自启（systemd user service）
crontab @reboot 不可靠，必须用 systemd：
```bash
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/cc-switch-proxy.service << 'EOF'
[Unit]
Description=CC Switch Proxy for Claude Code
After=network.target

[Service]
Type=simple
ExecStart=/home/$(whoami)/.local/bin/cc-switch proxy serve --takeover claude
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF
systemctl --user daemon-reload
systemctl --user enable cc-switch-proxy.service
systemctl --user start cc-switch-proxy.service
loginctl enable-linger $(whoami) # 开机不登录也能跑user service
```
然后**删掉crontab里的@reboot cc-switch条目**，避免跟systemd冲突。

### 7. 终端PATH配置
Claude Code 装在 `~/.hermes/node/bin/`，Hermes 内部 PATH 包含该目录，但用户终端默认没有：
```bash
echo 'export PATH="$HOME/.hermes/node/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
claude --version # 验证
```

### 8. 端到端验证
```bash
source ~/.cc-switch/env.sh
claude --print "say hello" 2>&1
```

验证 env.sh 中 AUTH_TOKEN 是真实值（不是 `***`）：
```bash
source ~/.cc-switch/env.sh && echo ${#ANTHROPIC_AUTH_TOKEN}
# 如果长度≤11就是脱敏值，真实key通常40+字符
```

## 踩坑记录

1. **env.sh AUTH_TOKEN脱敏陷阱**：Hermes备份/还原流程会把 `~/.cc-switch/env.sh` 中的真实API key脱敏为字面量 `***`（3个星号，不是占位符）。还原后必须手动填回真实key，否则 Claude Code 拿到 `***` 作为token导致空输出。修复：用 `patch`/`sed` 精准替换，不要用序列化工具重写整个文件。验证：`echo ${#ANTHROPIC_AUTH_TOKEN}` 看长度。

2. **开机自启必须用systemd user service**：crontab @reboot 在VPS环境下不可靠（cron守护进程可能晚于网络就绪，或根本不触发）。systemd user service + `loginctl enable-linger` 才是正确方案，开机自动拉起、挂了自动重试（Restart=on-failure）。配完systemd后删掉crontab @reboot条目避免冲突。

3. **终端PATH缺失**：Claude Code 通过npm装在 `~/.hermes/node/bin/claude`，Hermes内部PATH包含该目录但用户终端 `.bashrc` 没有。用户在终端跑 `claude` 会 command not found。必须在 `.bashrc` 加 `export PATH="$HOME/.hermes/node/bin:$PATH"`。

4. **config.yaml API Key脱敏**：Hermes框架会在config.yaml中脱敏API Key（显示为sk-XDO...HI2b），文件里存的就是脱敏后的值。CC Switch的`provider add`是交互式的，必须TTY环境输入key，或者用Python直接写SQLite。

5. **Anthropic≠OpenAI格式**：不能简单设`ANTHROPIC_BASE_URL`指向OpenAI兼容API。Claude Code发的是`/v1/messages`（Anthropic格式），CC Switch的proxy做协议转换后转发到`/v1/chat/completions`（OpenAI格式）。这是CC Switch的核心价值。

6. **模型名映射**：CC Switch将Claude的Opus/Sonnet/Haiku映射到你配置的`ANTHROPIC_DEFAULT_*_MODEL`。直接在请求中传的model字段可能被忽略或fallback到免费模型。确保三个DEFAULT字段都配成你想要的模型。

7. **proxy日志**：`cc-switch proxy serve --verbose`在background模式下日志为空。调试时用前台模式。systemd环境下用 `journalctl --user -u cc-switch-proxy` 查日志。

8. **Hindsight LLM切换**：`~/.hindsight/profiles/hermes.env`中的API Key也会被脱敏。用Python写文件绕过，或用脚本`~/switch-hindsight-llm.sh`。Hindsight也需要`HF_HUB_OFFLINE=true`和`TRANSFORMERS_OFFLINE=true`防止VPS连不上huggingface卡死启动。

9. **cc-switch provider delete**：非交互模式下会报TTY错误，用Python直接DELETE from providers表。

## 切换Provider
```bash
cc-switch provider switch -a claude <provider-id>
# 重启proxy生效（systemd方式）
systemctl --user restart cc-switch-proxy.service
```
