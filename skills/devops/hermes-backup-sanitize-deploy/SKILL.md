---
name: hermes-backup-sanitize-deploy
description: Full backup of Hermes Agent + Hindsight + CC Switch + Claude Code to GitHub, sanitize all secrets, and create setup/set-keys scripts for redeployment.
version: 1.0.0
author: Hermes Agent
tags: [backup, sanitize, deploy, migration, github]
---

# Hermes Full Backup, Sanitize & Deploy

## When to Use
- Migrating Hermes to a new server
- Sharing Hermes setup with someone else (removing your credentials)
- Periodic backup before major config changes

## Overview
3-phase workflow: BACKUP → SANITIZE → DEPLOY SCRIPTS

## Phase 1: Backup to GitHub (Private Repo)

1. Create/use private repo `gheshang/hermes-backup`
2. Copy these directories/files (excluding sensitive runtime data):

**Include:**
- `~/.hermes/config.yaml` — main config
- `~/.hermes/config-backups/` — config version history
- `~/.hermes/SOUL.md` — personality
- `~/.hermes/memories/` — MEMORY.md + USER.md
- `~/.hermes/skills/` — all installed skills
- `~/.hermes/scripts/` — wiki_ingest.py, wiki-sync.sh, log_generator.py
- `~/.hermes/cron/jobs.json` — cron definitions
- `~/.hermes/wiki/` — knowledge base (exclude .git)
- `~/.hermes/profiles/` — named profiles
- `~/.hermes/skills-inventory.md` — skills inventory
- `~/.hermes/hermes_setup_all.py` — full install script
- `~/.hermes/.env` — AFTER sanitization (see Phase 2)
- `~/.hermes/config.yaml.bak.homechannel` — homechannel backup
- `~/.hindsight/profiles/hermes.env` — AFTER sanitization
- `~/.hindsight/profiles/metadata.json`
- `~/.cc-switch/settings.json`
- `~/.cc-switch/env.sh` — AFTER sanitization
- `~/.claude/settings.json`
- `~/agency-agents-zh/` — exclude .git
- `~/superpowers/` — exclude .git
- `~/andrej-karpathy-skills/` — exclude .git
- `~/tencentyun-snake-up/` — exclude .git

**Exclude (in .gitignore + skip):**
- `hermes-agent/` (source code, re-installable)
- `state.db`, `state-snapshots/` (session history)
- `auth.json`, `auth.lock` (credential pool)
- `pairing/` (platform pairing records)
- `weixin/` (WeChat account data)
- `feishu_seen_message_ids.json`
- `channel_directory.json`
- `gateway.lock`, `gateway.pid`, `gateway_state.json`
- `logs/`, `cache/`, `backups/`, `checkpoints/`
- `audio_cache/`, `image_cache/`
- `processes.json`, `models_dev_cache.json`
- `*.db` (CC Switch DB, state DB)
- `*.lock` files
- `__pycache__/`, `node_modules/`, `venv/`

## Phase 2: Sanitize Secrets

### .env sanitization
- All `FEISHU_*` lines → comment out, clear values
- All `WEIXIN_*` lines → comment out, clear values
- All `*_API_KEY=*` → set to empty, add `# <-- fill in setup`
- All `*_TOKEN=*` → set to empty
- All `*_SECRET=*` → set to empty
- Keep non-sensitive config (HERMES_MAX_ITERATIONS, BROWSER_* etc.)
- Keep template comments (the `# Get your key at: ...` lines)

### config.yaml sanitization
- Replace all `api_key: <real-value>` → `api_key: ''  # <-- fill in setup`
- Clear `FEISHU_HOME_CHANNEL` oc_ IDs
- Keep base_urls (not secrets)

### cron/jobs.json sanitization
- Replace all `oc_<hex>` Feishu chat IDs with empty

### Other files
- `cc-switch/env.sh`: clear ANTHROPIC_AUTH_TOKEN value
- `hindsight/hermes.env`: clear HINDSIGHT_API_LLM_API_KEY value

### Verification (MANDATORY after sanitization)
```bash
cd /tmp/hermes-backup
# Check for leaked secrets (exclude template examples in skills/wiki docs)
grep -rn 'sk-[a-zA-Z0-9]\{8,\}' --include='*.yaml' --include='*.env' --include='*.json' . | grep -v '# <-- fill in' | grep -v "''" | grep -v 'skills/' | grep -v 'wiki/'
grep -rn 'tvly-' --include='*.yaml' --include='*.env' --include='*.json' .
grep -rn 'cli_a[0-9]' --include='*.yaml' --include='*.env' --include='*.json' .
grep -rn 'oc_[a-f0-9]\{20,\}' --include='*.yaml' --include='*.env' --include='*.json' .
# Also check Python/Shell scripts
grep -rn 'sk-[a-zA-Z0-9]\{8,\}' --include='*.py' --include='*.sh' . | grep -v '# <-- fill in'
```
All must return CLEAN (no matches) before pushing.

### Common Pitfalls
- `FEISHU_APP_ID=cli_a960bb2a60f89cd2` — looks like an ID but IS a real secret. Must clear value.
- `WEIXIN_HOME_CHANNEL=o9cq80z...` — user-specific ID, must clear value.
- Skills/wiki docs may contain `sk-xxx` as **template examples** (e.g. `Authorization: "Bearer sk-xxx...xxxx"`) — these are fine, NOT real secrets.
- `cron/jobs.json` contains `oc_<hex>` Feishu chat IDs in `chat_id`/`chat_name` fields — must clear.
- **Regex-based sanitization can miss values** — always run verification grep AFTER writing sanitized files.
- **Multiple passes may be needed** — write_file may not take effect if the file was read in the same code block; use separate terminal calls to verify.

## Phase 3: Deploy Scripts

### setup.sh — Full one-click deployment
- Installs Hermes Agent (pip)
- Restores all configs/skills/scripts to `~/.hermes/`
- Installs Hindsight + restores config
- Installs CC Switch + Claude Code
- **Interactive key prompt**: walks user through ALL API keys with clear labels
- Sets file permissions (600 on .env, config.yaml, etc.)
- Flags: `--skip-hermes`, `--skip-hindsight`, `--skip-cc-switch`

### set-keys.sh — Quick key update only
- No reinstall, just updates key values in .env/config.yaml/hindsight/cc-switch/bashrc
- Flags: `--all` (default), `--llm-only`, `--messaging-only`
- Uses `set_key()` helper that handles both commented and uncommented key lines

## Phase 4: Local Sanitization (AFTER backup confirmed)

Items to clear on source machine before handover:
1. `~/.hermes/.env` — all API keys / Feishu / WeChat credentials
2. `~/.hermes/config.yaml` — all api_key values
3. `~/.hermes/auth.json` — credential pool
4. `~/.hermes/pairing/` — WeChat pairing records
5. `~/.hermes/weixin/` — WeChat account data
6. `~/.hermes/feishu_seen_message_ids.json`
7. `~/.hermes/channel_directory.json`
8. `~/.hermes/state.db` — session/conversation history
9. `~/.cc-switch/cc-switch.db`
10. `~/.cc-switch/env.sh` — ANTHROPIC_AUTH_TOKEN
11. `~/.hindsight/profiles/hermes.env` — HINDSIGHT_API_LLM_API_KEY
12. `~/.bashrc` — GITHUB_TOKEN

**⚠️ CONFIRM WITH USER BEFORE EXECUTING — this is irreversible.**

**User may choose to skip local sanitization** (e.g. if the backup is for someone else and the source machine stays in use). Don't assume — ask explicitly.

## Quick Local tar Backup (Server Migration / 日常备份)

上次全目录打包3.6G报错，根因：venv/node_modules/lock文件被打进tar，二进制冲突+文件被修改导致中断。

**核心思路**：只备不可重建的数据，排除可重装的重物。最终34M（原始3.6G）。

```bash
cd /home/hangskf && tar czf /tmp/hermes-backup-$(date +%Y%m%d).tar.gz \
  --exclude='hermes-agent' \
  --exclude='*/venv' --exclude='*/node_modules' --exclude='*/__pycache__' \
  --exclude='*.lock' --exclude='*.pid' --exclude='*.db-wal' --exclude='*.db-shm' \
  --exclude='*/web' --exclude='*/ui-tui' --exclude='*/node' \
  --exclude='*/audio_cache' --exclude='*/image_cache' --exclude='*/state-snapshots' \
  --exclude='.hermes/backups/2026-04-2[3-7]' \
  .hermes
```

| 分层 | 内容 | 大小 | 可重建 |
|------|------|------|--------|
| 核心 | config.yaml .env SOUL.md memories/ skills/ scripts/ cron/jobs.json auth.json wiki/ | ~30M | 否 |
| 状态 | state.db sessions/ plans/ hindsight/ checkpoints/ backups/最新/ | ~120M | 部分 |

恢复：`tar xzf *.tar.gz -C /home/newuser/` → 改.env/config.yaml凭证 → `cd hermes-agent && uv sync && npm install` → `hermes gateway start`

GitHub仓库：gheshang/hermes-full-backup（私有，SSH push，2026-04-28首次提交）

```bash
# 打包（约34M，干净无报错）
tar czf hermes-backup-$(date +%Y%m%d).tar.gz \
 --exclude='hermes-agent' \
 --exclude='*/venv' \
 --exclude='*/node_modules' \
 --exclude='*/__pycache__' \
 --exclude='*.lock' \
 --exclude='*.pid' \
 --exclude='*.db-wal' \
 --exclude='*.db-shm' \
 --exclude='*/web' \
 --exclude='*/ui-tui' \
 --exclude='*/node' \
 --exclude='*/audio_cache' \
 --exclude='*/image_cache' \
 --exclude='*/state-snapshots' \
 --exclude='.hermes/backups/2026-04-2[0-7]' \
 -C /home/hangskf .hermes
```

**排除项补充说明**：
- `hermes-agent/` 整个目录排除（源码+venv+node_modules+web+ui-tui），pip/uv可重装，打进去多200M+无意义
- `state-snapshots/` 旧迁移快照，17M无恢复价值
- `backups/` 只保留最新一天（排除 `2026-04-2[0-7]`，保留28号），5105→更少文件
- 实测34M（含state.db 18M + sessions 52M + skills 12M + wiki 11M + 其他）

**备份内容分层**：

| 层级 | 内容 | 大小 | 能否重建 |
|------|------|------|----------|
| 核心（必备） | config.yaml, .env, SOUL.md, memories/, skills/, scripts/, cron/jobs.json, auth.json, channel_directory.json, wiki/ | ~30M | 不能 |
| 状态（重要） | state.db, sessions/, plans/, hindsight/, cron/output/, checkpoints/, backups/ | ~140M | 部分可重建，但丢会话历史 |
| 重物（排除） | hermes-agent/(含venv 2.1G+node 475M+源码+web+ui-tui), state-snapshots/(17M), backups/旧快照 | ~3.5G | 全部可重装 |

**恢复到新服务器**：
```bash
# 1. 新服务器装Hermes
curl -fsSL https://get.hermes.ai | bash
# 2. 解压覆盖
tar xzf hermes-backup-XXXXXXXX.tar.gz -C /home/newuser/
# 3. 修改 .env 和 config.yaml 里的API key
# 4. 重装venv（hermes首次启动自动执行，或手动 cd ~/.hermes/hermes-agent && uv sync）
# 5. 重装node依赖（cd ~/.hermes/hermes-agent && npm install）
# 6. 启动gateway
hermes gateway start
```

**推送到GitHub私有仓库**：
- SSH key只能push，**不能创建仓库**。创建仓库需要 `gh` CLI 或 PAT token。
- 如果VPS无gh CLI且无PAT：让用户在GitHub网页手动创建空仓库，然后本地 `git init && git remote add origin git@github.com:USER/REPO.git && git push -u origin main`
- 已有仓库（如 `gheshang/hermes-backup`）可直接clone+替换内容+force push

## Quick Commands

```bash
# Full workflow: clone existing repo → rebuild backup → sanitize → force push
cd /tmp && rm -rf hermes-backup && git clone git@github.com:gheshang/hermes-backup.git
# (copy current files, run sanitization steps, verify)
cd hermes-backup && rm -rf .git && git init && git branch -m main
git add -A && git commit -m "backup update $(date +%Y%m%d)" && git push --force origin main

# Deploy on new machine
git clone git@github.com:gheshang/hermes-backup.git
cd hermes-backup && bash setup.sh

# Update keys later
bash set-keys.sh --llm-only
```

- **PEP 668 handling**: Debian/Ubuntu Bookworm+ blocks `pip install` system-wide. setup.sh uses `pip install --break-system-packages` as fallback for Hindsight install.
- **hermes-agent NOT on PyPI**: `pip install hermes-agent` will always fail with `ERROR: No matching distribution found for requirement hermes-agent`. Must install from GitHub source: `git clone https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent` → `python3 -m venv ~/.hermes/hermes-agent/venv` → `venv/bin/pip install -e ~/.hermes/hermes-agent` → `ln -sf ~/.hermes/hermes-agent/venv/bin/hermes ~/.local/bin/hermes`. setup.sh handles this automatically.
- **Custom repo/branch**: setup.sh supports `--hermes-repo=URL` and `--hermes-branch=NAME` flags for forks.
- **Force push with SSH**: GitHub repo push via HTTPS will fail auth on headless VPS. Must `git remote set-url origin git@github.com:gheshang/hermes-backup.git` before pushing.
- **setup.sh 结尾自动验证**: 脚本结尾不再让用户手动 `source ~/.bashrc && hermes --version`。自动确保 symlink 存在、在脚本内验证 hermes 版本；只有验证失败时才提示一条 `source ~/.bashrc` 命令。
- **setup.sh / set-keys.sh 维护方式**: 这些脚本在 skill 模板目录 (`~/.hermes/skills/devops/hermes-backup-sanitize-deploy/templates/`) 维护。备份流程 Phase 3 应从模板拷贝，而非手动维护仓库中的副本。改 skill 模板即自动生效。
- **config.yaml 可能被飞书相关操作意外覆盖/精简**：Hermes 与飞书交互时，可能触发 config.yaml 重写，导致 `platforms: {}` 等关键字段被清空。表现为 gateway 启动报 "No messaging platforms enabled"。恢复方法：`cp ~/.hermes/config.yaml.bak ~/.hermes/config.yaml`。**禁止用 yaml.dump/json.dumps 重写整个 config.yaml** — 格式/注释/顺序全丢。必须用 patch/sed 精准替换。
- **env.sh 脱敏问题**：`~/.cc-switch/env.sh` 中的 ANTHROPIC_AUTH_TOKEN 会被 Hermes 脱敏为字面量 `***`。备份还原后必须手动恢复真实 key。
- **单独同步模板到仓库**: 改完模板后如果只想推 setup.sh，手动 `cp templates/setup.sh ~/hermes-backup/setup.sh && cd ~/hermes-backup && git add setup.sh && git commit -m "msg" && git push --force`。远程 reject 时 force push 是安全的（快照仓库非协作历史）。
- **Repo made public**: `gheshang/hermes-backup` was changed from private to public. Clone URL for new users: `https://github.com/gheshang/hermes-backup.git`
- **User may skip local sanitization**: backup is for giving to someone else, source machine stays untouched. Don't assume local cleanup is wanted.
- **Rebuild from scratch each time**: delete old `.git` in backup dir, `git init` fresh. Avoids stale history mixing with new sanitized content.
- **Force push** (`--force`) is safe here — the repo is a backup snapshot, not a collaborative history.
- **rsync for large dirs**: use `rsync -a --exclude='.git'` for skills/, wiki/, project repos. Faster than cp -r and handles excludes.
- **Project repos** (agency-agents-zh, superpowers, etc.) are copied WITHOUT .git — they're data, not git history.
- **CRITICAL: 禁止用 yaml.dump/json.dumps 重写整个配置文件**: 序列化工具会丢失注释、打乱键值顺序、破坏YAML格式。必须用 `patch`/`sed` 精准替换。修改任何配置文件前必先 `cp` 备份为 `.bak`。
- **gateway "No messaging platforms enabled" 排查**: 如果 setup.sh 还原后 gateway 启动报此错误，检查 `config.yaml` 的 `platforms` 字段是否为空 `{}`。正确值应包含 `feishu:`/`weixin:` 等平台配置。还原流程可能因 yaml.dump 或手动编辑导致 platforms 段丢失。修复：用 sed/patch 精准插入 platforms 配置，不要重写整个文件。
- **`gh` CLI 不可用时的 SSH 直推**：VPS 可能未安装 `gh` CLI。SSH key 认证通过 (`ssh -T git@github.com`) 即可直接 `git push`，无需 `gh`。仓库创建需网页手动完成或 PAT。
- **增量备份 vs 全量重建**：已有仓库可直接 `git clone` → 替换内容 → `git add -A` → `git commit` → `git push`，无需 `rm -rf .git && git init`。全量重建仅用于首次创建或彻底清洗历史。
- **已跟踪的敏感文件需 `git rm --cached`**：若 `.env` 等敏感文件已被 git 跟踪，删除本地文件后必须 `git rm --cached <file>` 才能从跟踪中移除，否则仍会随 commit 上传。批量处理：`git ls-files | grep -E '^(.env|cron/output|auth\.json|hindsight/)' | xargs git rm --cached`。
- **必须更新 `.gitignore`**：每次备份前检查 `.gitignore` 是否覆盖所有排除项。新增排除项后需 `git add .gitignore` 一并提交。
- **额外建议备份项**：`config-backups/`（config 历史快照）、`skills-inventory.md`（技能清单）、`hermes_setup_all.py`（全量安装脚本）、`config.yaml.bak.homechannel`（homechannel 专用配置）。
- **Python `shutil.copytree` 替代 `cp -r`**：在脚本中批量复制目录时，`shutil.copytree(src, dst, dirs_exist_ok=True)` 比 shell `cp` 更可靠，自动处理权限和符号链接。
