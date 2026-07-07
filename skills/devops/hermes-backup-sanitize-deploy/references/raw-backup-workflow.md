# Raw (Unsanitized) Backup Workflow

## When to Use

User explicitly requests "不脱敏" / "raw backup" / "保留密钥" — push all secrets as-is to a private GitHub repo.

## Session 2026-05-13 Execution Log

### Context
- User first requested sanitized backup to `gheshang/hermes-full-backup` ✓ completed
- User then requested **raw (unsanitized)** backup to **new** repo `gheshang/hermes-full-backup-raw`

### Key Decisions

1. **Confirmed intent**: "不需要脱敏，重新推送" → confirmed raw mode
2. **New repo**: User created `gheshang/hermes-full-backup-raw` manually on GitHub web UI (SSH key cannot create repos)
3. **No sanitization**: Skipped all Phase 2 steps — all API keys, Chat IDs, Tokens preserved
4. **Force push**: Used `git push -f` to overwrite the default repo content (GitHub auto-created README)

### Files Backed Up (2048 files, ~34MB)

| File/Dir | Status |
|----------|--------|
| `config.yaml` | ✓ Original (含 API key) |
| `.env` | ✓ Original (含所有密钥) |
| `auth.json` | ✓ Original (含 access_token) |
| `channel_directory.json` | ✓ Original (含 Feishu Chat ID) |
| `hindsight/hermes.env` | ✓ Original (含 HINDSIGHT_API_LLM_API_KEY) |
| `cc-switch/env.sh` | ✓ Original (含 ANTHROPIC_AUTH_TOKEN) |
| `cron/jobs.json` | ✓ Original (含 chat_id) |
| `config-backups/` | ✓ Original |
| `skills/`, `wiki/`, `memories/`, `scripts/`, `profiles/` | ✓ Original |
| `agency-agents-zh/`, `superpowers/`, `andrej-karpathy-skills/` | ✓ Without .git |
| `SOUL.md`, `skills-inventory.md`, `hermes_setup_all.py` | ✓ Original |

### Verification

After copy, verified secrets are **present** (inverted check from sanitized mode):
```bash
grep -c 'sk-' .env config.yaml  # should return > 0
grep -c 'oc_' channel_directory.json  # should return > 0
```

### Git Commands Used

```bash
cd /tmp && rm -rf hermes-full-backup-raw && mkdir hermes-full-backup-raw && cd hermes-full-backup-raw
git init
git branch -m main  # ← critical: GitHub default is 'main', local git init creates 'master'
git config user.name "gheshang"
git config user.email "gheshang@users.noreply.github.com"
git remote add origin git@github.com:gheshang/hermes-full-backup-raw.git
# ... copy files ...
git add -A
git commit -m "feat: Hermes Agent 全量备份 (2026-05-13) - 不脱敏"
git push -f -u origin main  # ← force push to overwrite GitHub's auto-created content
```

### Pitfalls Encountered

1. **SSH key can't create repos**: `ssh -T git@github.com` authenticates but cannot call GitHub API. User must create repo manually on web UI.
2. **Branch name mismatch**: Local `git init` creates `master`, GitHub creates `main`. Must `git branch -m main` before first push.
3. **Force push needed**: New repo may have auto-created README/.gitignore from web UI. `git push -f` overwrites safely (backup repo, not collaborative history).
4. **Never default to raw**: Always ask explicit confirmation. Default is sanitized.

### README Template for Raw Backup

```markdown
# Hermes Agent 全量备份（不脱敏）

> ⚠️ **安全警告**：此仓库包含完整的 API 密钥、Chat ID、Token 等敏感信息，未做任何脱敏处理。

- 仅限私有仓库，严禁公开
- 恢复后请确保文件权限：`chmod 600 ~/.hermes/.env ~/.hermes/config.yaml`

## 恢复流程

```bash
git clone git@github.com:USER/REPO.git
cd REPO
cp -r . ~/.hermes/
hermes --version
hermes gateway start
```
```

### .gitignore for Raw Backup

Same as sanitized mode — exclude runtime state files:
- `*.lock`, `*.pid`, `*.db`, `*.db-wal`, `*.db-shm`
- `state-snapshots/`, `backups/`, `checkpoints/`, `logs/`, `cache/`
- `audio_cache/`, `image_cache/`
- `__pycache__/`, `*.pyc`, `node_modules/`, `venv/`
- Project repo `.git` directories
