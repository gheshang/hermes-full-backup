---
title: Weixin (WeChat)
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-weixin.md]
---

# Weixin (WeChat)

源文档：[Weixin (WeChat)](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/weixin.md)

# Weixin (WeChat)

Connect Hermes to [WeChat](https://weixin.qq.com/) (微信), Tencent's personal messaging platform. The adapter uses Tencent's **iLink Bot API** for personal WeChat accounts — this is distinct from WeCom (Enterprise WeChat). Messages are delivered via long-polling, so no public endpoint or webhook is required.

:::info
This adapter is for **personal WeChat accounts** (微信). If you need enterprise/corporate WeChat, see the [WeCom adapter](./wecom.md) instead.
:::

## Prerequisites

- A personal WeChat account
- Python packages: `aiohttp` and `cryptography`
- Terminal QR rendering is included when Hermes is installed with the `messaging` extra

Install the required dependencies:

```bash
pip install aiohttp cryptography
# Optional: for terminal QR code display
pip install hermes-agent[messaging]
```...

## Setup

### 1. Run the Setup Wizard

The easiest way to connect your WeChat account is through the interactive setup:

```bash
hermes gateway setup
```

Select **Weixin** when prompted. The wizard will:

1. Request a QR code from the iLink Bot API
2. Display the QR code in your terminal (or provide a URL)
3. Wait for you to scan the QR code with the WeChat mobile app
4. Prompt you to confirm the login on your phone
5. Save the account credentials automatically to `~/.hermes/weixin/accounts/`

Once confirmed, you'll see a message like:

```
微信连接成功，account_id=your-account-id
```

The wizard stores the `...

## Features

- **Long-poll transport** — no public endpoint, webhook, or WebSocket needed
- **QR code login** — scan-to-connect setup via `hermes gateway setup`
- **DM and group messaging** — configurable access policies
- **Media support** — images, video, files, and voice messages
- **AES-128-ECB encrypted CDN** — automatic encryption/decryption for all media transfers
- **Context token persistence** — disk-backed reply continuity across restarts
- **Markdown formatting** — preserves Markdown, including headers, tables, and code blocks, so WeChat clients that support Markdown can render it natively
- **S...

## Configuration Options

Set these in `config.yaml` under `platforms.weixin.extra`:

| Key | Default | Description |
|-----|---------|-------------|
| `account_id` | — | iLink Bot account ID (required) |
| `token` | — | iLink Bot token (required, auto-saved from QR login) |
| `base_url` | `https://ilinkai.weixin.qq.com` | iLink API base URL |
| `cdn_base_url` | `https://novac2c.cdn.weixin.qq.com/c2c` | CDN base URL for media transfer |
| `dm_policy` | `open` | DM access: `open`, `allowlist`, `disabled`, `pairing` |
| `group_policy` | `disabled` | Group access: `open`, `allowlist`, `disabled` |
| `allow_from` | `[]` | ...

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
WEIXIN_DM_POLICY=allowlist
WEIXIN_ALLOWED_USERS=user_id_1,user_id_2
```

### Group Policy

Controls which groups the bot responds in:

| Value | Behavior |
|-------|----------|
| `open` | Bot responds in all groups |
| `allowlist` | Bot only responds in group IDs listed in `group_allow_from` |
| ...

## Media Support

### Inbound (receiving)

The adapter receives media attachments from users, downloads them from the WeChat CDN, decrypts them, and caches them locally for agent processing:

| Type | How it's handled |
|------|-----------------| 
| **Images** | Downloaded, AES-decrypted, and cached as JPEG. |
| **Video** | Downloaded, AES-decrypted, and cached as MP4. |
| **Files** | Downloaded, AES-decrypted, and cached. Original filename is preserved. |
| **Voice** | If a text transcription is available, it's extracted as text. Otherwise the audio (SILK format) is downloaded and cached. |

**Quoted messages:...

## Context Token Persistence

The iLink Bot API requires a `context_token` to be echoed back with each outbound message for a given peer. The adapter maintains a disk-backed context token store:

- Tokens are saved per account+peer to `~/.hermes/weixin/accounts/<account_id>.context-tokens.json`
- On startup, previously saved tokens are restored
- Every inbound message updates the stored token for that sender
- Outbound messages automatically include the latest context token

This ensures reply continuity even after gateway restarts....

## Markdown Formatting

WeChat clients connected through the iLink Bot API can render Markdown directly, so the adapter preserves Markdown instead of rewriting it:

- **Headers** stay as Markdown headings (`#`, `##`, ...)
- **Tables** stay as Markdown tables
- **Code fences** stay as fenced code blocks
- **Excessive blank lines** are collapsed to double newlines outside fenced code blocks...

## Message Chunking

Messages are delivered as a single chat message whenever they fit within the platform limit. Only oversized payloads are split for delivery:

- Maximum message length: **4000 characters**
- Messages under the limit stay intact even when they contain multiple paragraphs or line breaks
- Oversized messages split at logical boundaries (paragraphs, blank lines, code fences)
- Code fences are kept intact whenever possible (never split mid-block unless the fence itself exceeds the limit)
- Oversized individual blocks fall back to the base adapter's truncation logic
- A 0.3 s inter-chunk delay preven...

## Typing Indicators

The adapter shows typing status in the WeChat client:

1. When a message arrives, the adapter fetches a `typing_ticket` via the `getconfig` API
2. Typing tickets are cached for 10 minutes per user
3. `send_typing` sends a typing-start signal; `stop_typing` sends a typing-stop signal
4. The gateway automatically triggers typing indicators while the agent processes a message...

## Long-Poll Connection

The adapter uses HTTP long-polling (not WebSocket) to receive messages:

### How It Works

1. **Connect:** Validates credentials and starts the poll loop
2. **Poll:** Calls `getupdates` with a 35-second timeout; the server holds the request until messages arrive or the timeout expires
3. **Dispatch:** Inbound messages are dispatched concurrently via `asyncio.create_task`
4. **Sync buffer:** A persistent sync cursor (`get_updates_buf`) is saved to disk so the adapter resumes from the correct position after restarts

### Retry Behavior

On API errors, the adapter uses a simple retry strategy:

|...

## All Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `WEIXIN_ACCOUNT_ID` | ✅ | — | iLink Bot account ID (from QR login) |
| `WEIXIN_TOKEN` | ✅ | — | iLink Bot token (auto-saved from QR login) |
| `WEIXIN_BASE_URL` | — | `https://ilinkai.weixin.qq.com` | iLink API base URL |
| `WEIXIN_CDN_BASE_URL` | — | `https://novac2c.cdn.weixin.qq.com/c2c` | CDN base URL for media transfer |
| `WEIXIN_DM_POLICY` | — | `open` | DM access policy: `open`, `allowlist`, `disabled`, `pairing` |
| `WEIXIN_GROUP_POLICY` | — | `disabled` | Group access policy: `open`, `al...

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Weixin startup failed: aiohttp and cryptography are required` | Install both: `pip install aiohttp cryptography` |
| `Weixin startup failed: WEIXIN_TOKEN is required` | Run `hermes gateway setup` to complete QR login, or set `WEIXIN_TOKEN` manually |
| `Weixin startup failed: WEIXIN_ACCOUNT_ID is required` | Set `WEIXIN_ACCOUNT_ID` in your `.env` or run `hermes gateway setup` |
| `Another local Hermes gateway is already using this Weixin token` | Stop the other gateway instance first — only one poller per token is allowed |
| Session expired (`errcode=-14...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
