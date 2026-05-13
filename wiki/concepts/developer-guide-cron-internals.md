---
title: Cron Internals
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-cron-internals.md]
---

# Cron Internals

源文档：[Cron Internals](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/cron-internals.md)

# Cron Internals

The cron subsystem provides scheduled task execution — from simple one-shot delays to recurring cron-expression jobs with skill injection and cross-platform delivery.

## Key Files

| File | Purpose |
|------|---------|
| `cron/jobs.py` | Job model, storage, atomic read/write to `jobs.json` |
| `cron/scheduler.py` | Scheduler loop — due-job detection, execution, repeat tracking |
| `tools/cronjob_tools.py` | Model-facing `cronjob` tool registration and handler |
| `gateway/run.py` | Gateway integration — cron ticking in the long-running loop |
| `hermes_cli/cron.py` | CLI `hermes cron` subcommands |...

## Scheduling Model

Four schedule formats are supported:

| Format | Example | Behavior |
|--------|---------|----------|
| **Relative delay** | `30m`, `2h`, `1d` | One-shot, fires after the specified duration |
| **Interval** | `every 2h`, `every 30m` | Recurring, fires at regular intervals |
| **Cron expression** | `0 9 * * *` | Standard 5-field cron syntax (minute, hour, day, month, weekday) |
| **ISO timestamp** | `2025-01-15T09:00:00` | One-shot, fires at the exact time |

The model-facing surface is a single `cronjob` tool with action-style operations: `create`, `list`, `update`, `pause`, `resume`, `run`, `...

## Job Storage

Jobs are stored in `~/.hermes/cron/jobs.json` with atomic write semantics (write to temp file, then rename). Each job record contains:

```json
{
  "id": "a1b2c3d4e5f6",
  "name": "Daily briefing",
  "prompt": "Summarize today's AI news and funding rounds",
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "display": "0 9 * * *"
  },
  "skills": ["ai-funding-daily-report"],
  "deliver": "telegram:-1001234567890",
  "repeat": {
    "times": null,
    "completed": 42
  },
  "state": "scheduled",
  "enabled": true,
  "next_run_at": "2025-01-16T09:00:00Z",
  "last_run_at": "2025-01-...

## Scheduler Runtime

### Tick Cycle

The scheduler runs on a periodic tick (default: every 60 seconds):

```text
tick()
  1. Acquire scheduler lock (prevents overlapping ticks)
  2. Load all jobs from jobs.json
  3. Filter to due jobs (next_run <= now AND state == "scheduled")
  4. For each due job:
     a. Set state to "running"
     b. Create fresh AIAgent session (no conversation history)
     c. Load attached skills in order (injected as user messages)
     d. Run the job prompt through the agent
     e. Deliver the response to the configured target
     f. Update run_count, compute next_run
     g. If repeat ...

## Skill-Backed Jobs

A cron job can attach one or more skills via the `skills` field. At execution time:

1. Skills are loaded in the specified order
2. Each skill's SKILL.md content is injected as context
3. The job's prompt is appended as the task instruction
4. The agent processes the combined skill context + prompt

This enables reusable, tested workflows without pasting full instructions into cron prompts. For example:

```
Create a daily funding report → attach "ai-funding-daily-report" skill
```

### Script-Backed Jobs

Jobs can also attach a Python script via the `script` field. The script runs *before* ea...

## Delivery Model

Cron job results can be delivered to any supported platform:

| Target | Syntax | Example |
|--------|--------|---------|
| Origin chat | `origin` | Deliver to the chat where the job was created |
| Local file | `local` | Save to `~/.hermes/cron/output/` |
| Telegram | `telegram` or `telegram:<chat_id>` | `telegram:-1001234567890` |
| Discord | `discord` or `discord:#channel` | `discord:#engineering` |
| Slack | `slack` | Deliver to Slack home channel |
| WhatsApp | `whatsapp` | Deliver to WhatsApp home |
| Signal | `signal` | Deliver to Signal |
| Matrix | `matrix` | Deliver to Matrix home ro...

## Recursion Guard

Cron-run sessions have the `cronjob` toolset disabled. This prevents:
- A scheduled job from creating new cron jobs
- Recursive scheduling that could explode token usage
- Accidental mutation of the job schedule from within a job...

## Locking

The scheduler uses file-based locking to prevent overlapping ticks from executing the same due-job batch twice. This is important in gateway mode where multiple maintenance cycles could overlap if a previous tick takes longer than the tick interval....

## CLI Interface

The `hermes cron` CLI provides direct job management:

```bash
hermes cron list                    # Show all jobs
hermes cron create                  # Interactive job creation (alias: add)
hermes cron edit <job_id>           # Edit job configuration
hermes cron pause <job_id>          # Pause a running job
hermes cron resume <job_id>         # Resume a paused job
hermes cron run <job_id>            # Trigger immediate execution
hermes cron remove <job_id>         # Delete a job
```...

## Related Docs

- [Cron Feature Guide](/docs/user-guide/features/cron)
- [Gateway Internals](./gateway-internals.md)
- [Agent Loop Internals](./agent-loop.md)...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
