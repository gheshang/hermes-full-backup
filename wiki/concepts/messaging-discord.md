---
title: Discord Setup
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-discord.md]
---

# Discord Setup

源文档：[Discord Setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/discord.md)

# Discord Setup

Hermes Agent integrates with Discord as a bot, letting you chat with your AI assistant through direct messages or server channels. The bot receives your messages, processes them through the Hermes Agent pipeline (including tool use, memory, and reasoning), and responds in real time. It supports text, voice messages, file attachments, and slash commands.

Before setup, here's the part most people want to know: how Hermes behaves once it's in your server.

## How Hermes Behaves

| Context | Behavior |
|---------|----------|
| **DMs** | Hermes responds to every message. No `@mention` needed. Each DM has its own session. |
| **Server channels** | By default, Hermes only responds when you `@mention` it. If you post in a channel without mentioning it, Hermes ignores the message. |
| **Free-response channels** | You can make specific channels mention-free with `DISCORD_FREE_RESPONSE_CHANNELS`, or disable mentions globally with `DISCORD_REQUIRE_MENTION=false`. Messages in these channels are answered inline — auto-threading is skipped so the channel stays a lightweight chat....

## Step 1: Create a Discord Application

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and sign in with your Discord account.
2. Click **New Application** in the top-right corner.
3. Enter a name for your application (e.g., "Hermes Agent") and accept the Developer Terms of Service.
4. Click **Create**.

You'll land on the **General Information** page. Note the **Application ID** — you'll need it later to build the invite URL....

## Step 2: Create the Bot

1. In the left sidebar, click **Bot**.
2. Discord automatically creates a bot user for your application. You'll see the bot's username, which you can customize.
3. Under **Authorization Flow**:
   - Set **Public Bot** to **ON** — required to use the Discord-provided invite link (recommended). This allows the Installation tab to generate a default authorization URL.
   - Leave **Require OAuth2 Code Grant** set to **OFF**.

:::tip
You can set a custom avatar and banner for your bot on this page. This is what users will see in Discord.
:::

:::info[Private Bot Alternative]
If you prefer to keep y...

## Step 3: Enable Privileged Gateway Intents

This is the most critical step in the entire setup. Without the correct intents enabled, your bot will connect to Discord but **will not be able to read message content**.

On the **Bot** page, scroll down to **Privileged Gateway Intents**. You'll see three toggles:

| Intent | Purpose | Required? |
|--------|---------|-----------| 
| **Presence Intent** | See user online/offline status | Optional |
| **Server Members Intent** | Access the member list, resolve usernames | **Required** |
| **Message Content Intent** | Read the text content of messages | **Required** |

**Enable both Server Memb...

## Step 4: Get the Bot Token

The bot token is the credential Hermes Agent uses to log in as your bot. Still on the **Bot** page:

1. Under the **Token** section, click **Reset Token**.
2. If you have two-factor authentication enabled on your Discord account, enter your 2FA code.
3. Discord will display your new token. **Copy it immediately.**

:::warning[Token shown only once]
The token is only displayed once. If you lose it, you'll need to reset it and generate a new one. Never share your token publicly or commit it to Git — anyone with this token has full control of your bot.
:::

Store the token somewhere safe (a passw...

## Step 5: Generate the Invite URL

You need an OAuth2 URL to invite the bot to your server. There are two ways to do this:

### Option A: Using the Installation Tab (Recommended)

:::note[Requires Public Bot]
This method requires **Public Bot** to be set to **ON** in Step 2. If you set Public Bot to OFF, use the Manual URL method below instead.
:::

1. In the left sidebar, click **Installation**.
2. Under **Installation Contexts**, enable **Guild Install**.
3. For **Install Link**, select **Discord Provided Link**.
4. Under **Default Install Settings** for Guild Install:
   - **Scopes**: select `bot` and `applications.commands`...

## Step 6: Invite to Your Server

1. Open the invite URL in your browser (from the Installation tab or the manual URL you constructed).
2. In the **Add to Server** dropdown, select your server.
3. Click **Continue**, then **Authorize**.
4. Complete the CAPTCHA if prompted.

:::info
You need the **Manage Server** permission on the Discord server to invite a bot. If you don't see your server in the dropdown, ask a server admin to use the invite link instead.
:::

After authorizing, the bot will appear in your server's member list (it will show as offline until you start the Hermes gateway)....

## Step 7: Find Your Discord User ID

Hermes Agent uses your Discord User ID to control who can interact with the bot. To find it:

1. Open Discord (desktop or web app).
2. Go to **Settings** → **Advanced** → toggle **Developer Mode** to **ON**.
3. Close settings.
4. Right-click your own username (in a message, the member list, or your profile) → **Copy User ID**.

Your User ID is a long number like `284102345871466496`.

:::tip
Developer Mode also lets you copy **Channel IDs** and **Server IDs** the same way — right-click the channel or server name and select Copy ID. You'll need a Channel ID if you want to set a home channel man...

## Step 8: Configure Hermes Agent

### Option A: Interactive Setup (Recommended)

Run the guided setup command:

```bash
hermes gateway setup
```

Select **Discord** when prompted, then paste your bot token and user ID when asked.

### Option B: Manual Configuration

Add the following to your `~/.hermes/.env` file:

```bash
# Required
DISCORD_BOT_TOKEN=your-bot-token
DISCORD_ALLOWED_USERS=284102345871466496

# Multiple allowed users (comma-separated)
# DISCORD_ALLOWED_USERS=284102345871466496,198765432109876543
```

Then start the gateway:

```bash
hermes gateway
```

The bot should come online in Discord within a few seconds. ...

## Configuration Reference

Discord behavior is controlled through two files: **`~/.hermes/.env`** for credentials and env-level toggles, and **`~/.hermes/config.yaml`** for structured settings. Environment variables always take precedence over config.yaml values when both are set.

### Environment Variables (`.env`)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_BOT_TOKEN` | **Yes** | — | Bot token from the [Discord Developer Portal](https://discord.com/developers/applications). |
| `DISCORD_ALLOWED_USERS` | **Yes** | — | Comma-separated Discord user IDs allow...

## Interactive Model Picker

Send `/model` with no arguments in a Discord channel to open a dropdown-based model picker:

1. **Provider selection** — a Select dropdown showing available providers (up to 25).
2. **Model selection** — a second dropdown with models for the chosen provider (up to 25).

The picker times out after 120 seconds. Only authorized users (those in `DISCORD_ALLOWED_USERS`) can interact with it. If you know the model name, type `/model <name>` directly....

## Native Slash Commands for Skills

Hermes automatically registers installed skills as **native Discord Application Commands**. This means skills appear in Discord's autocomplete `/` menu alongside built-in commands.

- Each skill becomes a Discord slash command (e.g., `/code-review`, `/ascii-art`)
- Skills accept an optional `args` string parameter
- Discord has a limit of 100 application commands per bot — if you have more skills than available slots, extra skills are skipped with a warning in the logs
- Skills are registered during bot startup alongside built-in commands like `/model`, `/reset`, and `/background`

No extra co...

## Home Channel

You can designate a "home channel" where the bot sends proactive messages (such as cron job output, reminders, and notifications). There are two ways to set it:

### Using the Slash Command

Type `/sethome` 

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
