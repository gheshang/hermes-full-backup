---
title: WeCom Callback (Self-Built App)
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-wecom-callback.md]
---

# WeCom Callback (Self-Built App)

源文档：[WeCom Callback (Self-Built App)](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/wecom-callback.md)

# WeCom Callback (Self-Built App)

Connect Hermes to WeCom (Enterprise WeChat) as a self-built enterprise application using the callback/webhook model.

:::info WeCom Bot vs WeCom Callback
Hermes supports two WeCom integration modes:
- **[WeCom Bot](wecom.md)** — bot-style, connects via WebSocket. Simpler setup, works in group chats.
- **WeCom Callback** (this page) — self-built app, receives encrypted XML callbacks. Shows as a first-class app in users' WeCom sidebar. Supports multi-corp routing.
:::

## How It Works

1. You register a self-built application in the WeCom Admin Console
2. WeCom pushes encrypted XML to your HTTP callback endpoint
3. Hermes decrypts the message, queues it for the agent
4. Immediately acknowledges (silent — nothing displayed to the user)
5. The agent processes the request (typically 3–30 minutes)
6. The reply is delivered proactively via the WeCom `message/send` API...

## Prerequisites

- A WeCom enterprise account with admin access
- `aiohttp` and `httpx` Python packages (included in the default install)
- A publicly reachable server for the callback URL (or a tunnel like ngrok)...

## Setup

### 1. Create a Self-Built App in WeCom

1. Go to [WeCom Admin Console](https://work.weixin.qq.com/) → **Applications** → **Create App**
2. Note your **Corp ID** (shown at the top of the admin console)
3. In the app settings, create a **Corp Secret**
4. Note the **Agent ID** from the app's overview page
5. Under **Receive Messages**, configure the callback URL:
   - URL: `http://YOUR_PUBLIC_IP:8645/wecom/callback`
   - Token: Generate a random token (WeCom provides one)
   - EncodingAESKey: Generate a key (WeCom provides one)

### 2. Configure Environment Variables

Add to your `.env` file:

`...

## Configuration Reference

Set these in `config.yaml` under `platforms.wecom_callback.extra`, or use environment variables:

| Setting | Default | Description |
|---------|---------|-------------|
| `corp_id` | — | WeCom enterprise Corp ID (required) |
| `corp_secret` | — | Corp secret for the self-built app (required) |
| `agent_id` | — | Agent ID of the self-built app (required) |
| `token` | — | Callback verification token (required) |
| `encoding_aes_key` | — | 43-character AES key for callback encryption (required) |
| `host` | `0.0.0.0` | Bind address for the HTTP callback server |
| `port` | `8645` | Port for the...

## Multi-App Routing

For enterprises running multiple self-built apps (e.g., across different departments or subsidiaries), configure the `apps` list in `config.yaml`:

```yaml
platforms:
  wecom_callback:
    enabled: true
    extra:
      host: "0.0.0.0"
      port: 8645
      apps:
        - name: "dept-a"
          corp_id: "ww_corp_a"
          corp_secret: "secret-a"
          agent_id: "1000002"
          token: "token-a"
          encoding_aes_key: "key-a-43-chars..."
        - name: "dept-b"
          corp_id: "ww_corp_b"
          corp_secret: "secret-b"
          agent_id: "1000003"
          token: "to...

## Access Control

Restrict which users can interact with the app:

```bash
# Allowlist specific users
WECOM_CALLBACK_ALLOWED_USERS=zhangsan,lisi,wangwu

# Or allow all users
WECOM_CALLBACK_ALLOW_ALL_USERS=true
```...

## Endpoints

The adapter exposes:

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/wecom/callback` | URL verification handshake (WeCom sends this during setup) |
| POST | `/wecom/callback` | Encrypted message callback (WeCom sends user messages here) |
| GET | `/health` | Health check — returns `{"status": "ok"}` |...

## Encryption

All callback payloads are encrypted with AES-CBC using the EncodingAESKey. The adapter handles:

- **Inbound**: Decrypt XML payload, verify SHA1 signature
- **Outbound**: Replies sent via proactive API (not encrypted callback response)

The crypto implementation is compatible with Tencent's official WXBizMsgCrypt SDK....

## Limitations

- **No streaming** — replies arrive as complete messages after the agent finishes
- **No typing indicators** — the callback model doesn't support typing status
- **Text only** — currently supports text messages for input; image/file/voice input not yet implemented. The agent is aware of outbound media capabilities via the WeCom platform hint (images, documents, video, voice).
- **Response latency** — agent sessions take 3–30 minutes; users see the reply when processing completes...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
