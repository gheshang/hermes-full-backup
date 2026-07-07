# lian-zhou-jobs Troubleshooting

## Overview

`lian-zhou-jobs` is a system crontab task (not Hermes Cron) that runs a Python crawler script daily at 08:00 and pushes results to Feishu.

## Common Issues

### 1. Missing Dependencies (bs4)

**Symptom**: Script fails with `ModuleNotFoundError: No module named 'bs4'`

**Fix**:
```bash
pip3 install beautifulsoup4
```

**Verification**:
```bash
python3 -c "from bs4 import BeautifulSoup; print('OK')"
```

### 2. Feishu Push Not Working

**Symptom**: Script runs but no message appears in Feishu

**Root causes**:
- Missing `FEISHU_WEBHOOK_URL` in `.env`
- Webhook URL expired or revoked
- Script path incorrect (cron runs in different working directory)

**Fix**:
```bash
# Verify webhook URL exists
grep FEISHU_WEBHOOK_URL ~/.hermes/.env

# Test manually
python3 ~/.hermes/scripts/lianzhou_jobs_crawler.py
```

### 3. Path Errors in Cron

**Symptom**: Script can't find files it references

**Root cause**: System crontab runs with a different working directory than interactive shell

**Fix**: Always use absolute paths in the script, and `cd` to the correct directory in the crontab entry:
```bash
0 8 * * * cd /home/hangskf && python3 ~/.hermes/scripts/lianzhou_jobs_crawler.py >> ~/.hermes/cron/lian-zhou-jobs/cron.log 2>&1
```

### 4. Log File Growth

**Symptom**: `cron.log` grows unbounded

**Fix**: Add log rotation or use the `monthly_cleanup.sh` script which handles cleanup:
```bash
bash ~/.hermes/cron/archive/monthly_cleanup.sh
```

## Architecture

```
lian-zhou-jobs (system crontab)
    │
    ├── Python script: ~/.hermes/scripts/lianzhou_jobs_crawler.py
    │       ├── Fetches data from web/API
    │       ├── Processes with BeautifulSoup
    │       └── Pushes to Feishu via webhook
    │
    └── Log: ~/.hermes/cron/lian-zhou-jobs/cron.log
```

## Key Difference from Hermes Cron

| Aspect | lian-zhou-jobs (system crontab) | Hermes Cron |
|--------|--------------------------------|-------------|
| Scheduler | System crontab | Hermes daemon |
| Execution | Direct Python script | LLM + Skills (unless `no_agent=True`) |
| Context | None (fresh shell) | Has session context |
| Delivery | Script-embedded Feishu webhook | Native `deliver` parameter |
| Retry | None (one-shot) | Built-in retry logic |
