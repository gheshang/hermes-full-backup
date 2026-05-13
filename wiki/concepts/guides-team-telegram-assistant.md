---
title: Set Up a Team Telegram Assistant
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-team-telegram-assistant.md]
---

# Set Up a Team Telegram Assistant

源文档：[Set Up a Team Telegram Assistant](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/team-telegram-assistant.md)

# Set Up a Team Telegram Assistant

This tutorial walks you through setting up a Telegram bot powered by Hermes Agent that multiple team members can use. By the end, your team will have a shared AI assistant they can message for help with code, research, system administration, and anything else — secured with per-user authorization.

## What We're Building

A Telegram bot that:

- **Any authorized team member** can DM for help — code reviews, research, shell commands, debugging
- **Runs on your server** with full tool access — terminal, file editing, web search, code execution
- **Per-user sessions** — each person gets their own conversation context
- **Secure by default** — only approved users can interact, with two authorization methods
- **Scheduled tasks** — daily standups, health checks, and reminders delivered to a team channel

---...

## Prerequisites

Before starting, make sure you have:

- **Hermes Agent installed** on a server or VPS (not your laptop — the bot needs to stay running). Follow the [installation guide](/docs/getting-started/installation) if you haven't yet.
- **A Telegram account** for yourself (the bot owner)
- **An LLM provider configured** — at minimum, an API key for OpenAI, Anthropic, or another supported provider in `~/.hermes/.env`

:::tip
A $5/month VPS is plenty for running the gateway. Hermes itself is lightweight — the LLM API calls are what cost money, and those happen remotely.
:::

---...

## Step 1: Create a Telegram Bot

Every Telegram bot starts with **@BotFather** — Telegram's official bot for creating bots.

1. **Open Telegram** and search for `@BotFather`, or go to [t.me/BotFather](https://t.me/BotFather)

2. **Send `/newbot`** — BotFather will ask you two things:
   - **Display name** — what users see (e.g., `Team Hermes Assistant`)
   - **Username** — must end in `bot` (e.g., `myteam_hermes_bot`)

3. **Copy the bot token** — BotFather replies with something like:
   ```
   Use this token to access the HTTP API:
   7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...
   ```
   Save this token — you'll need it in...

## Step 2: Configure the Gateway

You have two options: the interactive setup wizard (recommended) or manual configuration.

### Option A: Interactive Setup (Recommended)

```bash
hermes gateway setup
```

This walks you through everything with arrow-key selection. Pick **Telegram**, paste your bot token, and enter your user ID when prompted.

### Option B: Manual Configuration

Add these lines to `~/.hermes/.env`:

```bash
# Telegram bot token from BotFather
TELEGRAM_BOT_TOKEN=7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...

# Your Telegram user ID (numeric)
TELEGRAM_ALLOWED_USERS=123456789
```

### Finding Your User ID

Your T...

## Step 3: Start the Gateway

### Quick Test

Run the gateway in the foreground first to make sure everything works:

```bash
hermes gateway
```

You should see output like:

```
[Gateway] Starting Hermes Gateway...
[Gateway] Telegram adapter connected
[Gateway] Cron scheduler started (tick every 60s)
```

Open Telegram, find your bot, and send it a message. If it replies, you're in business. Press `Ctrl+C` to stop.

### Production: Install as a Service

For a persistent deployment that survives reboots:

```bash
hermes gateway install
sudo hermes gateway install --system   # Linux only: boot-time system service
```

This ...

## Step 4: Set Up Team Access

Now let's give your teammates access. There are two approaches.

### Approach A: Static Allowlist

Collect each team member's Telegram user ID (have them message [@userinfobot](https://t.me/userinfobot)) and add them as a comma-separated list:

```bash
# In ~/.hermes/.env
TELEGRAM_ALLOWED_USERS=123456789,987654321,555555555
```

Restart the gateway after changes:

```bash
hermes gateway stop && hermes gateway start
```

### Approach B: DM Pairing (Recommended for Teams)

DM pairing is more flexible — you don't need to collect user IDs upfront. Here's how it works:

1. **Teammate DMs the bot** ...

## Step 5: Configure the Bot

### Set a Home Channel

A **home channel** is where the bot delivers cron job results and proactive messages. Without one, scheduled tasks have nowhere to send output.

**Option 1:** Use the `/sethome` command in any Telegram group or chat where the bot is a member.

**Option 2:** Set it manually in `~/.hermes/.env`:

```bash
TELEGRAM_HOME_CHANNEL=-1001234567890
TELEGRAM_HOME_CHANNEL_NAME="Team Updates"
```

To find a channel ID, add [@userinfobot](https://t.me/userinfobot) to the group — it will report the group's chat ID.

### Configure Tool Progress Display

Control how much detail the bot ...

## Step 6: Set Up Scheduled Tasks

With the gateway running, you can schedule recurring tasks that deliver results to your team channel.

### Daily Standup Summary

Message the bot on Telegram:

```
Every weekday at 9am, check the GitHub repository at
github.com/myorg/myproject for:
1. Pull requests opened/merged in the last 24 hours
2. Issues created or closed
3. Any CI/CD failures on the main branch
Format as a brief standup-style summary.
```

The agent creates a cron job automatically and delivers results to the chat where you asked (or the home channel).

### Server Health Check

```
Every 6 hours, check disk usage with 'd...

## Production Tips

### Use Docker for Safety

On a shared team bot, use Docker as the terminal backend so agent commands run in a container instead of on your host:

```bash
# In ~/.hermes/.env
TERMINAL_BACKEND=docker
TERMINAL_DOCKER_IMAGE=nikolaik/python-nodejs:python3.11-nodejs20
```

Or in `~/.hermes/config.yaml`:

```yaml
terminal:
  backend: docker
  container_cpu: 1
  container_memory: 5120
  container_persistent: true
```

This way, even if someone asks the bot to run something destructive, your host system is protected.

### Monitor the Gateway

```bash
# Check if the gateway is running
hermes gateway st...

## Going Further

You've got a working team Telegram assistant. Here are some next steps:

- **[Security Guide](/docs/user-guide/security)** — deep dive into authorization, container isolation, and command approval
- **[Messaging Gateway](/docs/user-guide/messaging)** — full reference for gateway architecture, session management, and chat commands
- **[Telegram Setup](/docs/user-guide/messaging/telegram)** — platform-specific details including voice messages and TTS
- **[Scheduled Tasks](/docs/user-guide/features/cron)** — advanced cron scheduling with delivery options and cron expressions
- **[Context Files](/...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
