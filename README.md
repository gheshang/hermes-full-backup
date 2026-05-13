# Hermes Agent 全量备份

> 备份时间：2026-05-13 | 仓库：`gheshang/hermes-full-backup`（私有）

## 备份内容

| 目录/文件 | 说明 |
|-----------|------|
| `config.yaml` | Hermes 主配置文件 |
| `.env` | 环境变量（已脱敏，需填入API密钥） |
| `SOUL.md` | 人格设定 |
| `memories/` | 记忆文件（MEMORY.md + USER.md） |
| `skills/` | 所有已安装技能 |
| `scripts/` | 自定义脚本（log_generator.py 等） |
| `cron/` | 定时任务定义 |
| `wiki/` | 知识库 |
| `profiles/` | 命名配置档案 |
| `hindsight/` | Hindsight 配置 |
| `cc-switch/` | CC Switch 配置 |
| `claude-settings.json` | Claude 配置 |
| `agency-agents-zh/` | 中文AI角色库 |
| `superpowers/` | Superpowers 技能集 |
| `andrej-karpathy-skills/` | Karpathy 技能集 |

## 恢复流程

### 1. 克隆仓库

```bash
git clone git@github.com:gheshang/hermes-full-backup.git
cd hermes-full-backup
```

### 2. 安装 Hermes Agent

```bash
curl -fsSL https://get.hermes.ai | bash
```

### 3. 恢复配置文件

```bash
# 将备份目录内容复制到 ~/.hermes/
cp -r . ~/.hermes/

# 如果有多个备份目录，选择最新的
```

### 4. 填入 API 密钥

所有敏感字段已脱敏为 `<FILL_IN_SETUP>` 或空值，需要手动填入：

**`.env` 需要填入：**
- `OPENROUTER_API_KEY` — OpenRouter API 密钥（https://openrouter.ai/keys）
- 其他 LLM 提供商密钥（按需启用）

**`config.yaml` 需要填入：**
- `model.api_key` — 主模型 API 密钥
- `model.image.api_key` — 图像模型 API 密钥
- `FEISHU_HOME_CHANNEL` — 飞书 Home Channel ID

**`hindsight/hermes.env` 需要填入：**
- `HINDSIGHT_API_LLM_API_KEY` — Hindsight LLM 密钥

**`cc-switch/env.sh` 需要填入：**
- `ANTHROPIC_AUTH_TOKEN` — Claude Code 代理密钥

### 5. 验证安装

```bash
hermes --version
hermes gateway start
```

### 6. 恢复定时任务

```bash
# 编辑 cron/jobs.json 中的 chat_id 等字段后
hermes cron list
```

## 安全说明

- ⚠️ **所有 API 密钥、Chat ID、Token 均已脱敏**，恢复后必须手动填入
- ⚠️ **不要**将 `.env` 中填入密钥后的版本推送到仓库
- ⚠️ 本地恢复后建议设置文件权限：`chmod 600 ~/.hermes/.env ~/.hermes/config.yaml`
- 本仓库为**私有仓库**，仅限授权访问

## 备份策略

- 每次备份前清除旧备份内容，保留完整 Git 历史
- 采用全量覆盖方式，非增量备份
- 排除项：`hermes-agent/`（可重装源码）、`venv/`、`node_modules/`、`*.lock`、`*.db`、`audio_cache/`、`image_cache/`、`state-snapshots/`

## 排除清单

以下目录/文件**不会**被备份（可重建或非必需）：

- `hermes-agent/` — 源码，通过 `curl -fsSL https://get.hermes.ai | bash` 重装
- `*/venv/`、`*/node_modules/` — 依赖，可 `uv sync` / `npm install` 重建
- `*.lock`、`*.pid`、`*.db` — 运行时状态文件
- `audio_cache/`、`image_cache/` — 缓存
- `state-snapshots/`、`backups/` 旧快照 — 临时状态
- `__pycache__/` — Python 字节码
