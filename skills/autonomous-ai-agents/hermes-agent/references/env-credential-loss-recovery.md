# .env Credential Loss Recovery

## Problem
The `~/.hermes/.env` file contains all API keys and platform credentials. If it gets accidentally cleared or overwritten (e.g. by a misconfigured `hermes setup` script, a bad `cp` command, or a failed migration), all gateway platforms fail simultaneously.

## Symptoms
- `hermes gateway status` shows:
  ```
  ⚠ feishu: [Feishu] FEISHU_APP_ID or FEISHU_APP_SECRET not set
  ⚠ weixin: Weixin startup failed: WEIXIN_TOKEN is required
  ```
- `journalctl --user -u hermes-gateway.service` logs repeated credential errors
- `cat ~/.hermes/.env` shows only a few lines (e.g. just `API_SERVER_ENABLED=true` and `API_SERVER_KEY=...`) instead of the full credential block

## Recovery Procedure

### Step 1: Locate Backup
```bash
# Check state snapshots (most reliable)
ls ~/.hermes/state-snapshots/

# Check config backups (config.yaml only, not .env)
ls ~/.hermes/config.yaml.bak
ls ~/.hermes/backups/
```

### Step 2: Restore .env
```bash
# Backup current (damaged) .env first
cp ~/.hermes/.env ~/.hermes/.env.current.bak

# Restore from latest snapshot
cp ~/.hermes/state-snapshots/20260503-012828-pre-update/.env ~/.hermes/.env

# Verify all platform credentials are present
grep "FEISHU\|WEIXIN\|OPENROUTER\|DEEPSEEK" ~/.hermes/.env
```

### Step 3: Clean Up (if needed)
If the restored `.env` has trailing empty lines or problematic entries (e.g. `HINDSIGHT_LLM_API_KEY=***` that conflicts with config):
```bash
sed -i '/# Hindsight Memory Provider - LLM API key (DeepSeek)/d; /HINDSIGHT_LLM_API_KEY=\*\*\*/d' ~/.hermes/.env
```

### Step 4: Restart Gateway
```bash
hermes gateway stop 2>/dev/null
hermes gateway start
```

### Step 5: Verify
```bash
hermes gateway status
# Should show:
# ✓ feishu connected (websocket mode)
# ✓ weixin connected (or appropriate status)

# Check logs
tail -20 ~/.hermes/logs/agent.log | grep -i feishu
# Should show: "[Feishu] Connected in websocket mode"
```

## Prevention

### 1. Backup Before Setup
```bash
cp ~/.hermes/.env ~/.hermes/.env.bak.$(date +%Y%m%d)
```

### 2. Never Overwrite .env Directly
If a script needs to update `.env`, it should:
- Read the current file
- Update only specific keys
- Write back preserving all other keys

### 3. Periodic Snapshot
The `hermes` system already creates snapshots in `~/.hermes/state-snapshots/`. Verify they're being created regularly:
```bash
ls -lt ~/.hermes/state-snapshots/ | head -5
```

### 4. Add to Cron Backup
```bash
# Add to ~/.hermes/cron/ or system cron
0 2 * * * cp ~/.hermes/.env ~/.hermes/backups/.env.$(date +\%Y\%m\%d)
```

## Root Cause Analysis
In the 2026-05-05 incident, `.env` was reduced from 427 lines to 3 lines (only `API_SERVER_ENABLED`, `API_SERVER_PORT`, `API_SERVER_KEY`). The cause was unknown — possibly a misconfigured `hermes setup` or a failed migration script. The file was restored from `~/.hermes/state-snapshots/20260503-012828-pre-update/.env`.
