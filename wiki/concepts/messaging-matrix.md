---
title: Matrix Setup
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-matrix.md]
---

# Matrix Setup

源文档：[Matrix Setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/matrix.md)

# Matrix Setup

Hermes Agent integrates with Matrix, the open, federated messaging protocol. Matrix lets you run your own homeserver or use a public one like matrix.org — either way, you keep control of your communications. The bot connects via the `mautrix` Python SDK, processes messages through the Hermes Agent pipeline (including tool use, memory, and reasoning), and responds in real time. It supports text, file attachments, images, audio, video, and optional end-to-end encryption (E2EE).

Hermes works with any Matrix homeserver — Synapse, Conduit, Dendrite, or matrix.org.

Before setup, here's the part most people want to know: how Hermes behaves once it's connected.

## How Hermes Behaves

| Context | Behavior |
|---------|----------|
| **DMs** | Hermes responds to every message. No `@mention` needed. Each DM has its own session. Set `MATRIX_DM_MENTION_THREADS=true` to start a thread when the bot is `@mentioned` in a DM. |
| **Rooms** | By default, Hermes requires an `@mention` to respond. Set `MATRIX_REQUIRE_MENTION=false` or add room IDs to `MATRIX_FREE_RESPONSE_ROOMS` for free-response rooms. Room invites are auto-accepted. |
| **Threads** | Hermes supports Matrix threads (MSC3440). If you reply in a thread, Hermes keeps the thread context isolated from the main room timeline...

## Step 1: Create a Bot Account

You need a Matrix user account for the bot. There are several ways to do this:

### Option A: Register on Your Homeserver (Recommended)

If you run your own homeserver (Synapse, Conduit, Dendrite):

1. Use the admin API or registration tool to create a new user:

```bash
# Synapse example
register_new_matrix_user -c /etc/synapse/homeserver.yaml http://localhost:8008
```

2. Choose a username like `hermes` — the full user ID will be `@hermes:your-server.org`.

### Option B: Use matrix.org or Another Public Homeserver

1. Go to [Element Web](https://app.element.io) and create a new account.
2. P...

## Step 2: Get an Access Token

Hermes needs an access token to authenticate with the homeserver. You have two options:

### Option A: Access Token (Recommended)

The most reliable way to get a token:

**Via Element:**
1. Log in to [Element](https://app.element.io) with the bot account.
2. Go to **Settings** → **Help & About**.
3. Scroll down and expand **Advanced** — the access token is displayed there.
4. **Copy it immediately.**

**Via the API:**

```bash
curl -X POST https://your-server/_matrix/client/v3/login \
  -H "Content-Type: application/json" \
  -d '{
    "type": "m.login.password",
    "user": "@hermes:your-serv...

## Step 3: Find Your Matrix User ID

Hermes Agent uses your Matrix User ID to control who can interact with the bot. Matrix User IDs follow the format `@username:server`.

To find yours:

1. Open [Element](https://app.element.io) (or your preferred Matrix client).
2. Click your avatar → **Settings**.
3. Your User ID is displayed at the top of the profile (e.g., `@alice:matrix.org`).

:::tip
Matrix User IDs always start with `@` and contain a `:` followed by the server name. For example: `@alice:matrix.org`, `@bob:your-server.com`.
:::...

## Step 4: Configure Hermes Agent

### Option A: Interactive Setup (Recommended)

Run the guided setup command:

```bash
hermes gateway setup
```

Select **Matrix** when prompted, then provide your homeserver URL, access token (or user ID + password), and allowed user IDs when asked.

### Option B: Manual Configuration

Add the following to your `~/.hermes/.env` file:

**Using an access token:**

```bash
# Required
MATRIX_HOMESERVER=https://matrix.example.org
MATRIX_ACCESS_TOKEN=***

# Optional: user ID (auto-detected from token if omitted)
# MATRIX_USER_ID=@hermes:matrix.example.org

# Security: restrict who can interact with ...

## End-to-End Encryption (E2EE)

Hermes supports Matrix end-to-end encryption, so you can chat with your bot in encrypted rooms.

### Requirements

E2EE requires the `mautrix` library with encryption extras and the `libolm` C library:

```bash
# Install mautrix with E2EE support
pip install 'mautrix[encryption]'

# Or install with hermes extras
pip install 'hermes-agent[matrix]'
```

You also need `libolm` installed on your system:

```bash
# Debian/Ubuntu
sudo apt install libolm-dev

# macOS
brew install libolm

# Fedora
sudo dnf install libolm-devel
```

### Enable E2EE

Add to your `~/.hermes/.env`:

```bash
MATRIX_ENCRYPT...

## Home Room

You can designate a "home room" where the bot sends proactive messages (such as cron job output, reminders, and notifications). There are two ways to set it:

### Using the Slash Command

Type `/sethome` in any Matrix room where the bot is present. That room becomes the home room.

### Manual Configuration

Add this to your `~/.hermes/.env`:

```bash
MATRIX_HOME_ROOM=!abc123def456:matrix.example.org
```

:::tip
To find a Room ID: in Element, go to the room → **Settings** → **Advanced** → the **Internal room ID** is shown there (starts with `!`).
:::...

## Troubleshooting

### Bot is not responding to messages

**Cause**: The bot hasn't joined the room, or `MATRIX_ALLOWED_USERS` doesn't include your User ID.

**Fix**: Invite the bot to the room — it auto-joins on invite. Verify your User ID is in `MATRIX_ALLOWED_USERS` (use the full `@user:server` format). Restart the gateway.

### "Failed to authenticate" / "whoami failed" on startup

**Cause**: The access token or homeserver URL is incorrect.

**Fix**: Verify `MATRIX_HOMESERVER` points to your homeserver (include `https://`, no trailing slash). Check that `MATRIX_ACCESS_TOKEN` is valid — try it with curl:

```...

## Proxy Mode (E2EE on macOS)

Matrix E2EE requires `libolm`, which doesn't compile on macOS ARM64 (Apple Silicon). The `hermes-agent[matrix]` extra is gated to Linux only. If you're on macOS, proxy mode lets you run E2EE in a Docker container on a Linux VM while the actual agent runs natively on macOS with full access to your local files, memory, and skills.

### How It Works

```
macOS (Host):
  └─ hermes gateway
       ├─ api_server adapter ← listens on 0.0.0.0:8642
       ├─ AIAgent ← single source of truth
       ├─ Sessions, memory, skills
       └─ Local file access (Obsidian, projects, etc.)

Linux VM (Docker):
  └─...

## Security

:::warning
Always set `MATRIX_ALLOWED_USERS` to restrict who can interact with the bot. Without it, the gateway denies all users by default as a safety measure. Only add User IDs of people you trust — authorized users have full access to the agent's capabilities, including tool use and system access.
:::

For more information on securing your Hermes Agent deployment, see the [Security Guide](../security.md)....

## Notes

- **Any homeserver**: Works with Synapse, Conduit, Dendrite, matrix.org, or any spec-compliant Matrix homeserver. No specific homeserver software required.
- **Federation**: If you're on a federated homeserver, the bot can communicate with users from other servers — just add their full `@user:server` IDs to `MATRIX_ALLOWED_USERS`.
- **Auto-join**: The bot automatically accepts room invites and joins. It starts responding immediately after joining.
- **Media support**: Hermes can send and receive images, audio, video, and file attachments. Media is uploaded to your homeserver using the Matrix c...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
