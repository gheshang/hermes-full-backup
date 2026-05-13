---
title: WeCom (Enterprise WeChat)
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-wecom.md]
---

# WeCom (Enterprise WeChat)

源文档：[WeCom (Enterprise WeChat)](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/wecom.md)

# WeCom (Enterprise WeChat)

Connect Hermes to [WeCom](https://work.weixin.qq.com/) (企业微信), Tencent's enterprise messaging platform. The adapter uses WeCom's AI Bot WebSocket gateway for real-time bidirectional communication — no public endpoint or webhook needed.

## Prerequisites

- A WeCom organization account
- An AI Bot created in the WeCom Admin Console
- The Bot ID and Secret from the bot's credentials page
- Python packages: `aiohttp` and `httpx`...

## Setup

### Step 1: Create an AI Bot

#### Recommended: Scan-to-Create (one command)

```bash
hermes gateway setup
```

Select **WeCom** and scan the QR code with your WeCom mobile app. Hermes will automatically create a bot application with the correct permissions and save the credentials.

The setup wizard will:
1. Display a QR code in your terminal
2. Wait for you to scan it with the WeCom mobile app
3. Automatically retrieve the Bot ID and Secret
4. Guide you through access control configuration

#### Alternative: Manual Setup

If scan-to-create is not available, the wizard falls back to manual in...

## Features

- **WebSocket transport** — persistent connection, no public endpoint needed
- **DM and group messaging** — configurable access policies
- **Per-group sender allowlists** — fine-grained control over who can interact in each group
- **Media support** — images, files, voice, video upload and download
- **AES-encrypted media** — automatic decryption for inbound attachments
- **Quote context** — preserves reply threading
- **Markdown rendering** — rich text responses
- **Reply-mode streaming** — correlates responses to inbound message context
- **Auto-reconnect** — exponential backoff on connectio...

## Configuration Options

Set these in `config.yaml` under `platforms.wecom.extra`:

| Key | Default | Description |
|-----|---------|-------------|
| `bot_id` | — | WeCom AI Bot ID (required) |
| `secret` | — | WeCom AI Bot Secret (required) |
| `websocket_url` | `wss://openws.work.weixin.qq.com` | WebSocket gateway URL |
| `dm_policy` | `open` | DM access: `open`, `allowlist`, `disabled`, `pairing` |
| `group_policy` | `open` | Group access: `open`, `allowlist`, `disabled` |
| `allow_from` | `[]` | User IDs allowed for DMs (when dm_policy=allowlist) |
| `group_allow_from` | `[]` | Group IDs allowed (when group_policy...

## Access Policies

### DM Policy

Controls who can send direct messages to the bot:

| Value | Behavior |
|-------|----------|
| `open` | Anyone can DM the bot (default) |
| `allowlist` | Only user IDs in `allow_from` can DM |
| `disabled` | All DMs are ignored |
| `pairing` | Pairing mode (for initial setup) |

```bash
WECOM_DM_POLICY=allowlist
```

### Group Policy

Controls which groups the bot responds in:

| Value | Behavior |
|-------|----------|
| `open` | Bot responds in all groups (default) |
| `allowlist` | Bot only responds in group IDs listed in `group_allow_from` |
| `disabled` | All group messages ...

## Media Support

### Inbound (receiving)

The adapter receives media attachments from users and caches them locally for agent processing:

| Type | How it's handled |
|------|-----------------|
| **Images** | Downloaded and cached locally. Supports both URL-based and base64-encoded images. |
| **Files** | Downloaded and cached. Filename is preserved from the original message. |
| **Voice** | Voice message text transcription is extracted if available. |
| **Mixed messages** | WeCom mixed-type messages (text + images) are parsed and all components extracted. |

**Quoted messages:** Media from quoted (replied-to)...

## Reply-Mode Stream Responses

When the bot receives a message via the WeCom callback, the adapter remembers the inbound request ID. If a response is sent while the request context is still active, the adapter uses WeCom's reply-mode (`aibot_respond_msg`) with streaming to correlate the response directly to the inbound message. This provides a more natural conversation experience in the WeCom client.

If the inbound request context has expired or is unavailable, the adapter falls back to proactive message sending via `aibot_send_msg`.

Reply-mode also works for media: uploaded media can be sent as a reply to the originating...

## Connection and Reconnection

The adapter maintains a persistent WebSocket connection to WeCom's gateway at `wss://openws.work.weixin.qq.com`.

### Connection Lifecycle

1. **Connect:** Opens a WebSocket connection and sends an `aibot_subscribe` authentication frame with the bot_id and secret.
2. **Heartbeat:** Sends application-level ping frames every 30 seconds to keep the connection alive.
3. **Listen:** Continuously reads inbound frames and dispatches message callbacks.

### Reconnection Behavior

On connection loss, the adapter uses exponential backoff to reconnect:

| Attempt | Delay |
|---------|-------|
| 1st retry...

## All Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WECOM_BOT_ID` | ✅ | — | WeCom AI Bot ID |
| `WECOM_SECRET` | ✅ | — | WeCom AI Bot Secret |
| `WECOM_ALLOWED_USERS` | — | _(empty)_ | Comma-separated user IDs for the gateway-level allowlist |
| `WECOM_HOME_CHANNEL` | — | — | Chat ID for cron/notification output |
| `WECOM_WEBSOCKET_URL` | — | `wss://openws.work.weixin.qq.com` | WebSocket gateway URL |
| `WECOM_DM_POLICY` | — | `open` | DM access policy |
| `WECOM_GROUP_POLICY` | — | `open` | Group access policy |...

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `WECOM_BOT_ID and WECOM_SECRET are required` | Set both env vars or configure in setup wizard |
| `WeCom startup failed: aiohttp not installed` | Install aiohttp: `pip install aiohttp` |
| `WeCom startup failed: httpx not installed` | Install httpx: `pip install httpx` |
| `invalid secret (errcode=40013)` | Verify the secret matches your bot's credentials |
| `Timed out waiting for subscribe acknowledgement` | Check network connectivity to `openws.work.weixin.qq.com` |
| Bot doesn't respond in groups | Check `group_policy` setting and ensure the group ID i...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
