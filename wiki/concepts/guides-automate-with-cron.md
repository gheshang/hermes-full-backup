---
title: Automate Anything with Cron
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-automate-with-cron.md]
---

# Automate Anything with Cron

源文档：[Automate Anything with Cron](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/automate-with-cron.md)

# Automate Anything with Cron

The [daily briefing bot tutorial](/docs/guides/daily-briefing-bot) covers the basics. This guide goes further — five real-world automation patterns you can adapt for your own workflows.

For the full feature reference, see [Scheduled Tasks (Cron)](/docs/user-guide/features/cron).

:::info Key Concept
Cron jobs run in fresh agent sessions with no memory of your current chat. Prompts must be **completely self-contained** — include everything the agent needs to know.
:::

---

## Pattern 1: Website Change Monitor

Watch a URL for changes and get notified only when something is different.

The `script` parameter is the secret weapon here. A Python script runs before each execution, and its stdout becomes context for the agent. The script handles the mechanical work (fetching, diffing); the agent handles the reasoning (is this change interesting?).

Create the monitoring script:

```bash
mkdir -p ~/.hermes/scripts
```

```python title="~/.hermes/scripts/watch-site.py"
import hashlib, json, os, urllib.request

URL = "https://example.com/pricing"
STATE_FILE = os.path.expanduser("~/.hermes/scripts/.watch-sit...

## Pattern 2: Weekly Report

Compile information from multiple sources into a formatted summary. This runs once a week and delivers to your home channel.

```bash
/cron add "0 9 * * 1" "Generate a weekly report covering:

1. Search the web for the top 5 AI news stories from the past week
2. Search GitHub for trending repositories in the 'machine-learning' topic
3. Check Hacker News for the most discussed AI/ML posts

Format as a clean summary with sections for each source. Include links.
Keep it under 500 words — highlight only what matters." --name "Weekly AI digest" --deliver telegram
```

From the CLI:

```bash
hermes ...

## Pattern 3: GitHub Repository Watcher

Monitor a repository for new issues, PRs, or releases.

```bash
/cron add "every 6h" "Check the GitHub repository NousResearch/hermes-agent for:
- New issues opened in the last 6 hours
- New PRs opened or merged in the last 6 hours
- Any new releases

Use the terminal to run gh commands:
  gh issue list --repo NousResearch/hermes-agent --state open --json number,title,author,createdAt --limit 10
  gh pr list --repo NousResearch/hermes-agent --state all --json number,title,author,createdAt,mergedAt --limit 10

Filter to only items from the last 6 hours. If nothing new, respond with [SILENT].
Ot...

## Pattern 4: Data Collection Pipeline

Scrape data at regular intervals, save to files, and detect trends over time. This pattern combines a script (for collection) with the agent (for analysis).

```python title="~/.hermes/scripts/collect-prices.py"
import json, os, urllib.request
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.hermes/data/prices")
os.makedirs(DATA_DIR, exist_ok=True)

# Fetch current data (example: crypto prices)
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
data = json.loads(urllib.request.urlopen(url, timeout=30).read())

# Append to history file
e...

## Pattern 5: Multi-Skill Workflow

Chain skills together for complex scheduled tasks. Skills are loaded in order before the prompt executes.

```bash
# Use the arxiv skill to find papers, then the obsidian skill to save notes
/cron add "0 8 * * *" "Search arXiv for the 3 most interesting papers on 'language model reasoning' from the past day. For each paper, create an Obsidian note with the title, authors, abstract summary, and key contribution." \
  --skill arxiv \
  --skill obsidian \
  --name "Paper digest"
```

From the tool directly:

```python
cronjob(
    action="create",
    skills=["arxiv", "obsidian"],
    prompt="Sea...

## Managing Your Jobs

```bash
# List all active jobs
/cron list

# Trigger a job immediately (for testing)
/cron run <job_id>

# Pause a job without deleting it
/cron pause <job_id>

# Edit a running job's schedule or prompt
/cron edit <job_id> --schedule "every 4h"
/cron edit <job_id> --prompt "Updated task description"

# Add or remove skills from an existing job
/cron edit <job_id> --skill arxiv --skill obsidian
/cron edit <job_id> --clear-skills

# Remove a job permanently
/cron remove <job_id>
```

---...

## Delivery Targets

The `--deliver` flag controls where results go:

| Target | Example | Use case |
|--------|---------|----------|
| `origin` | `--deliver origin` | Same chat that created the job (default) |
| `local` | `--deliver local` | Save to local file only |
| `telegram` | `--deliver telegram` | Your Telegram home channel |
| `discord` | `--deliver discord` | Your Discord home channel |
| `slack` | `--deliver slack` | Your Slack home channel |
| Specific chat | `--deliver telegram:-1001234567890` | A specific Telegram group |
| Threaded | `--deliver telegram:-1001234567890:17585` | A specific Telegram to...

## Tips

**Make prompts self-contained.** The agent in a cron job has no memory of your conversations. Include URLs, repo names, format preferences, and delivery instructions directly in the prompt.

**Use `[SILENT]` liberally.** For monitoring jobs, always include instructions like "if nothing changed, respond with `[SILENT]`." This prevents notification noise.

**Use scripts for data collection.** The `script` parameter lets a Python script handle the boring parts (HTTP requests, file I/O, state tracking). The agent only sees the script's stdout and applies reasoning to it. This is cheaper and more r...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
