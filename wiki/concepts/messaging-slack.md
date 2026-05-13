---
title: Slack Setup
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-slack.md]
---

# Slack Setup

源文档：[Slack Setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/slack.md)

# Slack Setup

Connect Hermes Agent to Slack as a bot using Socket Mode. Socket Mode uses WebSockets instead of
public HTTP endpoints, so your Hermes instance doesn't need to be publicly accessible — it works
behind firewalls, on your laptop, or on a private server.

:::warning Classic Slack Apps Deprecated
Classic Slack apps (using RTM API) were **fully deprecated in March 2025**. Hermes uses the modern
Bolt SDK with Socket Mode. If you have an old classic app, you must create a new one following
the steps below.
:::

## Overview

| Component | Value |
|-----------|-------|
| **Library** | `slack-bolt` / `slack_sdk` for Python (Socket Mode) |
| **Connection** | WebSocket — no public URL required |
| **Auth tokens needed** | Bot Token (`xoxb-`) + App-Level Token (`xapp-`) |
| **User identification** | Slack Member IDs (e.g., `U01ABC2DEF3`) |

---...

## Step 1: Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create New App**
3. Choose **From scratch**
4. Enter an app name (e.g., "Hermes Agent") and select your workspace
5. Click **Create App**

You'll land on the app's **Basic Information** page.

---...

## Step 2: Configure Bot Token Scopes

Navigate to **Features → OAuth & Permissions** in the sidebar. Scroll to **Scopes → Bot Token Scopes** and add the following:

| Scope | Purpose |
|-------|---------|
| `chat:write` | Send messages as the bot |
| `app_mentions:read` | Detect when @mentioned in channels |
| `channels:history` | Read messages in public channels the bot is in |
| `channels:read` | List and get info about public channels |
| `groups:history` | Read messages in private channels the bot is invited to |
| `im:history` | Read direct message history |
| `im:read` | View basic DM info |
| `im:write` | Open and manage DM...

## Step 3: Enable Socket Mode

Socket Mode lets the bot connect via WebSocket instead of requiring a public URL.

1. In the sidebar, go to **Settings → Socket Mode**
2. Toggle **Enable Socket Mode** to ON
3. You'll be prompted to create an **App-Level Token**:
   - Name it something like `hermes-socket` (the name doesn't matter)
   - Add the **`connections:write`** scope
   - Click **Generate**
4. **Copy the token** — it starts with `xapp-`. This is your `SLACK_APP_TOKEN`

:::tip
You can always find or regenerate app-level tokens under **Settings → Basic Information → App-Level Tokens**.
:::

---...

## Step 4: Subscribe to Events

This step is critical — it controls what messages the bot can see.


1. In the sidebar, go to **Features → Event Subscriptions**
2. Toggle **Enable Events** to ON
3. Expand **Subscribe to bot events** and add:

| Event | Required? | Purpose |
|-------|-----------|---------|
| `message.im` | **Yes** | Bot receives direct messages |
| `message.channels` | **Yes** | Bot receives messages in **public** channels it's added to |
| `message.groups` | **Recommended** | Bot receives messages in **private** channels it's invited to |
| `app_mention` | **Yes** | Prevents Bolt SDK errors when bot is @ment...

## Step 5: Enable the Messages Tab

This step enables direct messages to the bot. Without it, users see **"Sending messages to this app has been turned off"** when trying to DM the bot.

1. In the sidebar, go to **Features → App Home**
2. Scroll to **Show Tabs**
3. Toggle **Messages Tab** to ON
4. Check **"Allow users to send Slash commands and messages from the messages tab"**

:::danger Without this step, DMs are completely blocked
Even with all the correct scopes and event subscriptions, Slack will not allow users to send direct messages to the bot unless the Messages Tab is enabled. This is a Slack platform requirement, not ...

## Step 6: Install App to Workspace

1. In the sidebar, go to **Settings → Install App**
2. Click **Install to Workspace**
3. Review the permissions and click **Allow**
4. After authorization, you'll see a **Bot User OAuth Token** starting with `xoxb-`
5. **Copy this token** — this is your `SLACK_BOT_TOKEN`

:::tip
If you change scopes or event subscriptions later, you **must reinstall the app** for the changes
to take effect. The Install App page will show a banner prompting you to do so.
:::

---...

## Step 7: Find User IDs for the Allowlist

Hermes uses Slack **Member IDs** (not usernames or display names) for the allowlist.

To find a Member ID:

1. In Slack, click on the user's name or avatar
2. Click **View full profile**
3. Click the **⋮** (more) button
4. Select **Copy member ID**

Member IDs look like `U01ABC2DEF3`. You need your own Member ID at minimum.

---...

## Step 8: Configure Hermes

Add the following to your `~/.hermes/.env` file:

```bash
# Required
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
SLACK_ALLOWED_USERS=U01ABC2DEF3              # Comma-separated Member IDs

# Optional
SLACK_HOME_CHANNEL=C01234567890              # Default channel for cron/scheduled messages
SLACK_HOME_CHANNEL_NAME=general              # Human-readable name for the home channel (optional)
```

Or run the interactive setup:

```bash
hermes gateway setup    # Select Slack when prompted
```

Then start the gateway:

```bash
hermes gateway              # Foregrou...

## Step 9: Invite the Bot to Channels

After starting the gateway, you need to **invite the bot** to any channel where you want it to respond:

```
/invite @Hermes Agent
```

The bot will **not** automatically join channels. You must invite it to each channel individually.

---...

## How the Bot Responds

Understanding how Hermes behaves in different contexts:

| Context | Behavior |
|---------|----------|
| **DMs** | Bot responds to every message — no @mention needed |
| **Channels** | Bot **only responds when @mentioned** (e.g., `@Hermes Agent what time is it?`). In channels, Hermes replies in a thread attached to that message. |
| **Threads** | If you @mention Hermes inside an existing thread, it replies in that same thread. Once the bot has an active session in a thread, **subsequent replies in that thread do not require @mention** — the bot follows the conversation naturally. |

:::tip
In ...

## Configuration Options

Beyond the required environment variables from Step 8, you can customize Slack bot behavior through `~/.hermes/config.yaml`.

### Thread & Reply Behavior

```yaml
platforms:
  slack:
    # Controls how multi-part responses are threaded
    # "off"   — never thread replies to the original message
    # "first" — first chunk threads to user's message (default)
    # "all"   — all chunks thread to user's message
    reply_to_mode: "first"

    extra:
      # Whether to reply in a thread (default: true).
      # When false, channel messages get direct channel replies instead
      # of threads. Me...

## Home Channel

Set `SLACK_HOME_CHANNEL` to a channel ID where Hermes will deliver scheduled messages,
cron job results, and other proactive notifications. To find a channel ID:

1. Right-click the channel name in Slack
2. Click **View channel details**
3. Scroll to the bottom — the Channel ID is shown there

```bash
SLACK_HOME_CHANNEL=C01234567890
```

Make sure the bot has been **invited to the channel** (`/invite @Hermes Agent`).

---...

## Multi-Workspace Support

Hermes can connect to **multiple Slack workspaces** simultaneously using a single gateway instance. Each workspace is authenticated independently with its own bot user ID.

### Configuration

Provide multiple bot tokens as a **comma-separated list** in `SLACK_BOT_TOKEN`:

```bash
# Multiple bot tokens — one per workspace
SLACK_BOT_TOKEN=xoxb-workspace1-token,xoxb-workspace2-token,xoxb-workspace3-token

# A single app-level token is still used for Socket Mode
SLACK_APP_TOKEN=xapp-your-app-token
```

Or in `~/.hermes/config.yaml`:

```yaml
platforms:
  slack:
    token: "xoxb-workspace1-token,xo...

## Voice Messages

Hermes supports voice on Slack:

- **Incoming:** Voice/audio messages are automatically transcribed using the configured STT provider:

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
