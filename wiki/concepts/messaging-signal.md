---
title: Signal Setup
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-signal.md]
---

# Signal Setup

源文档：[Signal Setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/signal.md)

# Signal Setup

Hermes connects to Signal through the [signal-cli](https://github.com/AsamK/signal-cli) daemon running in HTTP mode. The adapter streams messages in real-time via SSE (Server-Sent Events) and sends responses via JSON-RPC.

Signal is the most privacy-focused mainstream messenger — end-to-end encrypted by default, open-source protocol, minimal metadata collection. This makes it ideal for security-sensitive agent workflows.

:::info No New Python Dependencies
The Signal adapter uses `httpx` (already a core Hermes dependency) for all communication. No additional Python packages are required. You just need signal-cli installed externally.
:::

---

## Prerequisites

- **signal-cli** — Java-based Signal client ([GitHub](https://github.com/AsamK/signal-cli))
- **Java 17+** runtime — required by signal-cli
- **A phone number** with Signal installed (for linking as a secondary device)

### Installing signal-cli

```bash
# macOS
brew install signal-cli

# Linux (download latest release)
VERSION=$(curl -Ls -o /dev/null -w %{url_effective} \
  https://github.com/AsamK/signal-cli/releases/latest | sed 's/^.*\/v//')
curl -L -O "https://github.com/AsamK/signal-cli/releases/download/v${VERSION}/signal-cli-${VERSION}.tar.gz"
sudo tar xf "signal-cli-${VERSION}.tar.gz"...

## Step 1: Link Your Signal Account

Signal-cli works as a **linked device** — like WhatsApp Web, but for Signal. Your phone stays the primary device.

```bash
# Generate a linking URI (displays a QR code or link)
signal-cli link -n "HermesAgent"
```

1. Open **Signal** on your phone
2. Go to **Settings → Linked Devices**
3. Tap **Link New Device**
4. Scan the QR code or enter the URI

---...

## Step 2: Start the signal-cli Daemon

```bash
# Replace +1234567890 with your Signal phone number (E.164 format)
signal-cli --account +1234567890 daemon --http 127.0.0.1:8080
```

:::tip
Keep this running in the background. You can use `systemd`, `tmux`, `screen`, or run it as a service.
:::

Verify it's running:

```bash
curl http://127.0.0.1:8080/api/v1/check
# Should return: {"versions":{"signal-cli":...}}
```

---...

## Step 3: Configure Hermes

The easiest way:

```bash
hermes gateway setup
```

Select **Signal** from the platform menu. The wizard will:

1. Check if signal-cli is installed
2. Prompt for the HTTP URL (default: `http://127.0.0.1:8080`)
3. Test connectivity to the daemon
4. Ask for your account phone number
5. Configure allowed users and access policies

### Manual Configuration

Add to `~/.hermes/.env`:

```bash
# Required
SIGNAL_HTTP_URL=http://127.0.0.1:8080
SIGNAL_ACCOUNT=+1234567890

# Security (recommended)
SIGNAL_ALLOWED_USERS=+1234567890,+0987654321    # Comma-separated E.164 numbers or UUIDs

# Optional
SIGNAL_...

## Access Control

### DM Access

DM access follows the same pattern as all other Hermes platforms:

1. **`SIGNAL_ALLOWED_USERS` set** → only those users can message
2. **No allowlist set** → unknown users get a DM pairing code (approve via `hermes pairing approve signal CODE`)
3. **`SIGNAL_ALLOW_ALL_USERS=true`** → anyone can message (use with caution)

### Group Access

Group access is controlled by the `SIGNAL_GROUP_ALLOWED_USERS` env var:

| Configuration | Behavior |
|---------------|----------|
| Not set (default) | All group messages are ignored. The bot only responds to DMs. |
| Set with group IDs | Only...

## Features

### Attachments

The adapter supports sending and receiving media in both directions.

**Incoming** (user → agent):

- **Images** — PNG, JPEG, GIF, WebP (auto-detected via magic bytes)
- **Audio** — MP3, OGG, WAV, M4A (voice messages transcribed if Whisper is configured)
- **Documents** — PDF, ZIP, and other file types

**Outgoing** (agent → user):

The agent can send media files via `MEDIA:` tags in responses. The following delivery methods are supported:

- **Images** — `send_image_file` sends PNG, JPEG, GIF, WebP as native Signal attachments
- **Voice** — `send_voice` sends audio files (OGG...

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **"Cannot reach signal-cli"** during setup | Ensure signal-cli daemon is running: `signal-cli --account +YOUR_NUMBER daemon --http 127.0.0.1:8080` |
| **Messages not received** | Check that `SIGNAL_ALLOWED_USERS` includes the sender's number in E.164 format (with `+` prefix) |
| **"signal-cli not found on PATH"** | Install signal-cli and ensure it's in your PATH, or use Docker |
| **Connection keeps dropping** | Check signal-cli logs for errors. Ensure Java 17+ is installed. |
| **Group messages ignored** | Configure `SIGNAL_GROUP_ALLOWED_USERS` ...

## Security

:::warning
**Always configure access controls.** The bot has terminal access by default. Without `SIGNAL_ALLOWED_USERS` or DM pairing, the gateway denies all incoming messages as a safety measure.
:::

- Phone numbers are redacted in all log output
- Use DM pairing or explicit allowlists for safe onboarding of new users
- Keep groups disabled unless you specifically need group support, or allowlist only the groups you trust
- Signal's end-to-end encryption protects message content in transit
- The signal-cli session data in `~/.local/share/signal-cli/` contains account credentials — protect it...

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SIGNAL_HTTP_URL` | Yes | — | signal-cli HTTP endpoint |
| `SIGNAL_ACCOUNT` | Yes | — | Bot phone number (E.164) |
| `SIGNAL_ALLOWED_USERS` | No | — | Comma-separated phone numbers/UUIDs |
| `SIGNAL_GROUP_ALLOWED_USERS` | No | — | Group IDs to monitor, or `*` for all (omit to disable groups) |
| `SIGNAL_ALLOW_ALL_USERS` | No | `false` | Allow any user to interact (skip allowlist) |
| `SIGNAL_HOME_CHANNEL` | No | — | Default delivery target for cron jobs |...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
