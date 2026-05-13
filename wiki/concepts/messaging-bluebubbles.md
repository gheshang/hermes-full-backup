---
title: BlueBubbles (iMessage)
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-bluebubbles.md]
---

# BlueBubbles (iMessage)

源文档：[BlueBubbles (iMessage)](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/bluebubbles.md)

# BlueBubbles (iMessage)

Connect Hermes to Apple iMessage via [BlueBubbles](https://bluebubbles.app/) — a free, open-source macOS server that bridges iMessage to any device.

## Prerequisites

- A **Mac** (always on) running [BlueBubbles Server](https://bluebubbles.app/)
- Apple ID signed into Messages.app on that Mac
- BlueBubbles Server v1.0.0+ (webhooks require this version)
- Network connectivity between Hermes and the BlueBubbles server...

## Setup

### 1. Install BlueBubbles Server

Download and install from [bluebubbles.app](https://bluebubbles.app/). Complete the setup wizard — sign in with your Apple ID and configure a connection method (local network, Ngrok, Cloudflare, or Dynamic DNS).

### 2. Get your Server URL and Password

In BlueBubbles Server → **Settings → API**, note:
- **Server URL** (e.g., `http://192.168.1.10:1234`)
- **Server Password**

### 3. Configure Hermes

Run the setup wizard:

```bash
hermes gateway setup
```

Select **BlueBubbles (iMessage)** and enter your server URL and password.

Or set environment variables ...

## How It Works

```
iMessage → Messages.app → BlueBubbles Server → Webhook → Hermes
Hermes → BlueBubbles REST API → Messages.app → iMessage
```

- **Inbound:** BlueBubbles sends webhook events to a local listener when new messages arrive. No polling — instant delivery.
- **Outbound:** Hermes sends messages via the BlueBubbles REST API.
- **Media:** Images, voice messages, videos, and documents are supported in both directions. Inbound attachments are downloaded and cached locally for the agent to process....

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BLUEBUBBLES_SERVER_URL` | Yes | — | BlueBubbles server URL |
| `BLUEBUBBLES_PASSWORD` | Yes | — | Server password |
| `BLUEBUBBLES_WEBHOOK_HOST` | No | `127.0.0.1` | Webhook listener bind address |
| `BLUEBUBBLES_WEBHOOK_PORT` | No | `8645` | Webhook listener port |
| `BLUEBUBBLES_WEBHOOK_PATH` | No | `/bluebubbles-webhook` | Webhook URL path |
| `BLUEBUBBLES_HOME_CHANNEL` | No | — | Phone/email for cron delivery |
| `BLUEBUBBLES_ALLOWED_USERS` | No | — | Comma-separated authorized users |
| `BLU...

## Features

### Text Messaging
Send and receive iMessages. Markdown is automatically stripped for clean plain-text delivery.

### Rich Media
- **Images:** Photos appear natively in the iMessage conversation
- **Voice messages:** Audio files sent as iMessage voice messages
- **Videos:** Video attachments
- **Documents:** Files sent as iMessage attachments

### Tapback Reactions
Love, like, dislike, laugh, emphasize, and question reactions. Requires the BlueBubbles [Private API helper](https://docs.bluebubbles.app/helper-bundle/installation).

### Typing Indicators
Shows "typing..." in the iMessage conversa...

## Private API

Some features require the BlueBubbles [Private API helper](https://docs.bluebubbles.app/helper-bundle/installation):
- Tapback reactions
- Typing indicators
- Read receipts
- Creating new chats by address

Without the Private API, basic text messaging and media still work....

## Troubleshooting

### "Cannot reach server"
- Verify the server URL is correct and the Mac is on
- Check that BlueBubbles Server is running
- Ensure network connectivity (firewall, port forwarding)

### Messages not arriving
- Check that the webhook is registered in BlueBubbles Server → Settings → API → Webhooks
- Verify the webhook URL is reachable from the Mac
- Check `hermes logs gateway` for webhook errors (or `hermes logs -f` to follow in real-time)

### "Private API helper not connected"
- Install the Private API helper: [docs.bluebubbles.app](https://docs.bluebubbles.app/helper-bundle/installation)
- Bas...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
