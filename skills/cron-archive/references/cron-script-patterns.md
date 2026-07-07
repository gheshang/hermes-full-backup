# Cron Script Execution Pattern (no_agent + script)

## Overview

Hermes Cron supports a **pure script execution mode** that bypasses the LLM entirely. This is ideal for deterministic tasks like monitoring, data collection, and scheduled scripts.

## Configuration

```python
cronjob(action='create',
    script='/path/to/script.sh',      # or .py, .bash
    no_agent=True,                     # KEY: skip LLM, run script directly
    schedule='0 8 * * *',
    deliver='feishu'                   # stdout delivered to Feishu
)
```

## Behavior

| Condition | Result |
|-----------|--------|
| Script stdout non-empty | Sent verbatim to `deliver` target |
| Script stdout empty | Silent — nothing delivered |
| Script exits non-zero / timeout | Error alert sent |

## Use Cases

- **Monitoring**: Disk space, CPU, memory thresholds
- **Data collection**: Scheduled scraping, API polling
- **Change detection**: File/directory change watchers
- **CI notifications**: Build/test status alerts

## Script Requirements

1. **Must be self-contained** — no reliance on parent session context
2. **Must produce output** — empty stdout = silent (watchdog pattern)
3. **Must handle errors** — non-zero exit triggers alert
4. **Path resolution**: Relative paths resolve under `~/.hermes/scripts/`
5. **Extensions**: `.sh`/`.bash` → bash, everything else → Python

## Example: lian-zhou-jobs Pattern

```python
# System crontab (not Hermes Cron):
0 8 * * * cd /home/hangskf && python3 ~/.hermes/scripts/lianzhou_jobs_crawler.py >> ~/.hermes/cron/lian-zhou-jobs/cron.log 2>&1

# Equivalent Hermes Cron:
cronjob(action='create',
    script='/home/hangskf/.hermes/scripts/lianzhou_jobs_crawler.py',
    no_agent=True,
    schedule='0 8 * * *',
    deliver='feishu'
)
```

## Pitfalls

- **Don't use `no_agent=True` for reasoning tasks** — it skips the LLM entirely
- **Empty stdout = silent** — design scripts to always produce output (even "OK")
- **Errors are silent without non-zero exit** — always `exit 1` on failure
- **Context is NOT injected** — the script runs in a fresh session with no chat context

---

# Guarded Execution Pattern (script + prompt hybrid)

## Overview

A hybrid mode where a script collects data / checks conditions, its output is injected as context, and the LLM prompt decides whether or how to act.

## Configuration

```python
cronjob(action='create',
    script='check-condition.py',    # runs first, output → context
    prompt='''检查上下文中的 [Script Output]，
如果包含 INACTIVE 则输出 [SILENT] 跳过，
否则执行审计流程...''',
    schedule='30 2 * * *'
)
```

## How It Works

1. Cron fires → runs the script (bash/Python) first
2. Script stdout → injected into agent prompt as `[Script Output]` context
3. LLM receives prompt + script output → decides whether to proceed
4. If conditions not met → outputs `[SILENT]` → nothing delivered

## ⚠️ Script Path Convention

The `script` parameter accepts a **filename only** (relative to `~/.hermes/scripts/`). Absolute paths (`/home/user/...`) and home-relative paths (`~/...`) are rejected.

```python
# ✅ Correct:
script='check-yesterday-activity.py'

# ❌ Wrong (will error):
script='/home/hangskf/.hermes/scripts/check-yesterday-activity.py'
script='~/check-yesterday-activity.py'
```

## Key Behaviours

| Condition | Result |
|-----------|--------|
| Script says skip → LLM outputs [SILENT] | Nothing delivered (silent) |
| Script says proceed → LLM runs main logic | Report delivered normally |
| Script errors → LLM still fires (no context) | Prompt runs without guard — design prompts to handle missing context |

## Use Cases

- **Activity guard**: Skip audit if no user activity yesterday
- **Threshold guard**: Only alert when disk > 80%
- **Window guard**: Only run on weekdays, skip weekends
- **State guard**: Only run if previous job completed successfully

## Example: Daily Activity Guard

```python
# ~/.hermes/scripts/check-yesterday-activity.py
import sqlite3, sys
from datetime import datetime, timedelta, timezone

db = '/home/hangskf/.hermes/state.db'
tz = timezone(timedelta(hours=8))
yesterday = (datetime.now(tz) - timedelta(days=1)).strftime('%Y-%m-%d')

conn = sqlite3.connect(db)
rows = conn.execute('''
    SELECT source, COUNT(*) FROM sessions
    WHERE source IN ('feishu','weixin','cli')
    AND date(datetime(started_at,'unixepoch','+8 hours')) = ?
    GROUP BY source
''', (yesterday,)).fetchall()
conn.close()

total = sum(r[1] for r in rows)
if total > 0:
    print(f'ACTIVE|昨日({yesterday})有{total}次用户会话')
else:
    print(f'INACTIVE|昨日({yesterday})无用户活动')
```
