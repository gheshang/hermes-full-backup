---
title: Tutorial: Build a Daily Briefing Bot
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-daily-briefing-bot.md]
---

# Tutorial: Build a Daily Briefing Bot

源文档：[Tutorial: Build a Daily Briefing Bot](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/daily-briefing-bot.md)

# Tutorial: Build a Daily Briefing Bot

In this tutorial, you'll build a personal briefing bot that wakes up every morning, researches topics you care about, summarizes the findings, and delivers a concise briefing straight to your Telegram or Discord.

By the end, you'll have a fully automated workflow combining **web search**, **cron scheduling**, **delegation**, and **messaging delivery** — no code required.

## What We're Building

Here's the flow:

1. **8:00 AM** — The cron scheduler triggers your job
2. **Hermes spins up** a fresh agent session with your prompt
3. **Web search** pulls the latest news on your topics
4. **Summarization** distills it into a clean briefing format
5. **Delivery** sends the briefing to your Telegram or Discord

The whole thing runs hands-free. You just read your briefing with your morning coffee....

## Prerequisites

Before starting, make sure you have:

- **Hermes Agent installed** — see the [Installation guide](/docs/getting-started/installation)
- **Gateway running** — the gateway daemon handles cron execution:
  ```bash
  hermes gateway install   # Install as a user service
  sudo hermes gateway install --system   # Linux servers: boot-time system service
  # or
  hermes gateway           # Run in foreground
  ```
- **Firecrawl API key** — set `FIRECRAWL_API_KEY` in your environment for web search
- **Messaging configured** (optional but recommended) — [Telegram](/docs/user-guide/messaging/telegram) or...

## Step 1: Test the Workflow Manually

Before automating anything, let's make sure the briefing works. Start a chat session:

```bash
hermes
```

Then enter this prompt:

```
Search for the latest news about AI agents and open source LLMs.
Summarize the top 3 stories in a concise briefing format with links.
```

Hermes will search the web, read through results, and produce something like:

```
☀️ Your AI Briefing — March 8, 2026

1. Qwen 3 Released with 235B Parameters
   Alibaba's latest open-weight model matches GPT-4.5 on several
   benchmarks while remaining fully open source.
   → https://qwenlm.github.io/blog/qwen3/

2. LangC...

## Step 2: Create the Cron Job

Now let's schedule this to run automatically every morning. You can do this in two ways.

Before creating cron jobs, ensure Hermes has a default model and provider configured globally. If you want a specific job to use different values, set explicit per-job model/provider overrides when creating it.

### Option A: Natural Language (in chat)

Just tell Hermes what you want:

```
Every morning at 8am, search the web for the latest news about AI agents
and open source LLMs. Summarize the top 3 stories in a concise briefing
with links. Use a friendly, professional tone. Deliver to telegram.
```

H...

## Step 3: Customize the Briefing

Once the basic briefing works, you can get creative.

### Multi-Topic Briefings

Cover several areas in one briefing:

```
/cron add "0 8 * * *" "Create a morning briefing covering three topics. For each topic, search the web for recent news from the past 24 hours and summarize the top 2 stories with links.

Topics:
1. AI and machine learning — focus on open source models and agent frameworks
2. Cryptocurrency — focus on Bitcoin, Ethereum, and regulatory news
3. Space exploration — focus on SpaceX, NASA, and commercial space

Format as a clean briefing with section headers and emoji. End with ...

## Step 4: Manage Your Jobs

### List All Scheduled Jobs

In chat:
```
/cron list
```

Or from the terminal:
```bash
hermes cron list
```

You'll see output like:

```
ID          | Name              | Schedule    | Next Run           | Deliver
------------|-------------------|-------------|--------------------|--------
a1b2c3d4    | Morning Briefing  | 0 8 * * *   | 2026-03-09 08:00   | telegram
e5f6g7h8    | Evening Recap     | 0 18 * * *  | 2026-03-08 18:00   | telegram
```

### Remove a Job

In chat:
```
/cron remove a1b2c3d4
```

Or ask conversationally:
```
Remove my morning briefing cron job.
```

Hermes will use `...

## Going Further

You've built a working daily briefing bot. Here are some directions to explore next:

- **[Scheduled Tasks (Cron)](/docs/user-guide/features/cron)** — Full reference for schedule formats, repeat limits, and delivery options
- **[Delegation](/docs/user-guide/features/delegation)** — Deep dive into parallel sub-agent workflows
- **[Messaging Platforms](/docs/user-guide/messaging)** — Set up Telegram, Discord, or other delivery targets
- **[Memory](/docs/user-guide/features/memory)** — Persistent context across sessions
- **[Tips & Best Practices](/docs/guides/tips)** — More prompt engineering ad...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
