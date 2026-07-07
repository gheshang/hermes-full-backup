# Plan: Hermes Agent 完整备份 + 清除敏感信息 + 一键部署脚本

## Goal
将当前VPS上的 Hermes Agent（含Hindsight记忆体、CC Switch、Claude Code）完整备份到GitHub，清除飞书/微信连接和所有API Key，使其可安全复制给他人使用。同时提供一键启动配置脚本。

## Current Context

### 目录结构 & 敏感信息分布
| 路径 | 内容 | 敏感项 |
|------|------|--------|
| `~/.hermes/config.yaml` | 主配置 | api_key字段（已被Hermes脱敏，但key值存于.db） |
| `~/.hermes/.env` | 环境变量 | **FEISHU_APP_ID, FEISHU_APP_SECRET, WEIXIN_TOKEN, OPENROUTER_API_KEY, TAVILY_API_KEY, DEEPSEEK_API_KEY, AUX_HEAVY_API_KEY等** |
| `~/.hermes/auth.json` | 认证信息 | 空（已清理） |
| `~/.hermes/pairing/` | 配对记录 | weixin-approved.json（含用户openid） |
| `~/.hermes/weixin/accounts/` | 微信账号数据 | 3个含openid的json文件 |
| `~/.hermes/feishu_seen_message_ids.json` | 飞书已读消息 | 飞书消息ID |
| `~/.hermes/state.db` | SQLite状态库 | 可能含对话历史 |
| `~/.hindsight/profiles/hermes.env` | Hindsight LLM配置 | **API Key（被脱敏显示但文件存完整值）** |
| `~/.cc-switch/cc-switch.db` | CC Switch数据库 | **Provider API Key** |
| `~/.cc-switch/env.sh` | CC Switch环境变量 | ANTHROPIC_AUTH_TOKEN |
| `~/.bashrc` | Shell配置 | WIKI_PATH, source cc-switch/env.sh |
| `~/switch-hindsight-llm.sh` | Hindsight切换脚本 | 含API Key参数 |

### 已有GitHub仓库
- `gheshang/hermes-backup` — 已有旧备份
- `gheshang/hermes-wiki` — Wiki知识库（私有）
- `gheshang/hermes-scripts` — 脚本仓库

### 体积
- `~/.hermes/` = 3.5G（含venv、node_modules、sessions等）
- 需排除：venv、node_modules、sessions、logs、cache、.db大文件

---

## Step-by-step Plan

### Step 1: 准备备份仓库结构
**操作**: 在 `~/hermes-backup/` 创建干净的备份目录结构

```
hermes-backup/
├── .gitignore          # 新写：排除大文件和敏感文件
├── README.md           # 部署说明
├── config/
│   ├── config.yaml.template    # 配置模板（key全部置空）
│   ├── .env.template           # 环境变量模板（key全部置空）
│   └── SOUL.md                 # 人设文件（无敏感信息）
├── hindsight/
│   └── hermes.env.template     # Hindsight配置模板
├── cc-switch/
│   └── env.sh.template         # CC Switch环境变量模板
├── skills/                     # 已安装的skills列表和配置
├── scripts/
│   ├── setup.sh                # 一键部署脚本
│   └── switch-hindsight-llm.sh # Hindsight模型切换
├── wiki/                       # Wiki知识库（子模块或直接拷贝）
├── memories/                   # 记忆文件
├── hooks/                      # 钩子配置
└── cron/                       # 定时任务配置
```

**文件变更**:
- `~/hermes-backup/.gitignore` — 重写，排除 `*.db`, `*.db-shm`, `*.db-wal`, `sessions/`, `logs/`, `cache/`, `venv/`, `node_modules/`, `.env`, `auth.json`, `pairing/`, `weixin/`, `feishu_seen_*`
- `~/hermes-backup/README.md` — 新建

### Step 2: 同步配置文件（脱敏版）
**操作**: 将配置文件复制到备份目录，所有API Key置为空字符串

**文件变更**:
- `config/config.yaml.template` — 从 `~/.hermes/config.yaml` 复制，所有 `api_key: sk-xxx` → `api_key: ''`
- `config/.env.template` — 从 `~/.hermes/.env` 复制，所有KEY值置空，保留注释说明
- `config/SOUL.md` — 直接复制（无敏感信息）
- `hindsight/hermes.env.template` — 复制，KEY置空
- `cc-switch/env.sh.template` — 复制，KEY置空

### Step 3: 同步Skills
**操作**: 复制 `~/.hermes/skills/` 目录到备份仓库

排除 `__pycache__/`、`.cache/`。Skills本身不含敏感信息。

### Step 4: 同步Hindsight本地模型
**操作**: Hindsight的embedding(bge-small)和reranker(MiniLM)模型缓存在 `~/.cache/huggingface/` 下，体积较大。

**决策**: 不备份模型文件（太大），在setup.sh中加一步自动下载。设置 `HF_HUB_OFFLINE=false` 首次运行时下载，后续设为true。

### Step 5: 同步其他组件
- `memories/` — 记忆文件（不含敏感信息，但含用户偏好等，**需确认是否保留**）
- `hooks/` — 钩子配置
- `cron/` — 定时任务配置
- `scripts/` — 已有脚本（wiki_ingest.py, log_generator.py等）

### Step 6: 编写一键部署脚本 `scripts/setup.sh`
**功能**:
1. 检查依赖（Python 3.11+, Node.js, npm, curl）
2. 安装Hermes Agent（`curl -fsSL install.sh | bash`）
3. 提示用户输入API Key（交互式，避免硬编码）
4. 写入 `~/.hermes/.env`（从template复制+填入key）
5. 写入 `~/.hermes/config.yaml`（从template复制）
6. 安装CC Switch CLI（`curl install.sh | bash`）
7. 配置CC Switch provider（交互式输入key）
8. 安装Claude Code（`npm install -g @anthropic-ai/claude-code`）
9. 配置Hindsight（从template复制+写入key）
10. 下载Hindsight本地模型（首次）
11. 配置bashrc环境变量
12. 配置crontab开机自启
13. 启动gateway

**关键**: 所有API Key通过交互式提示输入，不硬编码。

### Step 7: 编写单独的 `set-keys.sh` 脚本
**功能**: 单独设置/更新API Key，无需重跑完整setup
- 接受命令行参数或交互式输入
- 更新 `.env`、`config.yaml`、`cc-switch.db`、`hindsight.env` 中的key
- 重启相关服务

### Step 8: 清除敏感信息
**操作**: 在备份仓库中确认以下文件不含敏感信息：
- 所有 `.env` → 替换为 `.env.template`
- `pairing/` → 不备份
- `weixin/` → 不备份
- `feishu_seen_*` → 不备份
- `auth.json` → 不备份
- `state.db` → 不备份（含对话历史）
- `cc-switch.db` → 不备份（含provider key）

### Step 9: Git提交并推送
```bash
cd ~/hermes-backup
git add -A
git commit -m "full backup: hermes + hindsight + cc-switch + claude code, all keys sanitized"
git push origin main
```

### Step 10: 验证
- 克隆仓库到临时目录，确认无敏感信息泄露
- 运行 `grep -r "sk-" .` 确认无残留API Key
- 确认setup.sh可在干净环境运行

---

## Risks & Tradeoffs

1. **memories/含用户偏好** — 备份则接收者看到你的偏好，不备份则丢失所有记忆配置。建议保留，但加README说明可删除。
2. **sessions/含对话历史** — 绝对不备份，含大量敏感对话内容。
3. **state.db含状态** — 不备份，接收者首次启动会自动创建。
4. **HuggingFace模型** — 缓存约1-2GB，不备份，setup.sh自动下载。但新服务器需能访问huggingface.co。
5. **venv/node_modules** — 3G+，不备份，setup.sh自动安装。
6. **CC Switch SQLite DB** — 含provider key，不能直接备份。改用模板+交互式配置重建。

---

## Open Questions

1. **wiki知识库** — 单独仓库(hermes-wiki)已同步，是否还需要在备份仓库中包含？建议：不包含，setup.sh中加一步 `git clone` 即可。
2. **hermes-scripts仓库** — 已独立同步，同上处理。
3. **接收者是否需要飞书/微信** — 清除后需重新配置，setup.sh中加交互式配置步骤。
4. **备份仓库公开还是私有** — 含skills和配置逻辑，建议**私有**（避免暴露架构细节）。
