---
title: WhatsApp Setup
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-whatsapp.md]
---

# WhatsApp Setup

源文档：[WhatsApp Setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/whatsapp.md)

# WhatsApp Setup

Hermes connects to WhatsApp through a built-in bridge based on **Baileys**. This works by emulating a WhatsApp Web session — **not** through the official WhatsApp Business API. No Meta developer account or Business verification is required.

:::warning Unofficial API — Ban Risk
WhatsApp does **not** officially support third-party bots outside the Business API. Using a third-party bridge carries a small risk of account restrictions. To minimize risk:
- **Use a dedicated phone number** for the bot (not your personal number)
- **Don't send bulk/spam messages** — keep usage conversational
- **Don't automate outbound messaging** to people who haven't messaged first
:::

:::warning WhatsApp Web Protocol Updates
WhatsApp periodically updates their Web protocol, which can tempora

## Two Modes

| Mode | How it works | Best for |
|------|-------------|----------|
| **Separate bot number** (recommended) | Dedicate a phone number to the bot. People message that number directly. | Clean UX, multiple users, lower ban risk |
| **Personal self-chat** | Use your own WhatsApp. You message yourself to talk to the agent. | Quick setup, single user, testing |

---...

## Prerequisites

- **Node.js v18+** and **npm** — the WhatsApp bridge runs as a Node.js process
- **A phone with WhatsApp** installed (for scanning the QR code)

Unlike older browser-driven bridges, the current Baileys-based bridge does **not** require a local Chromium or Puppeteer dependency stack.

---...

## Step 1: Run the Setup Wizard

```bash
hermes whatsapp
```

The wizard will:

1. Ask which mode you want (**bot** or **self-chat**)
2. Install bridge dependencies if needed
3. Display a **QR code** in your terminal
4. Wait for you to scan it

**To scan the QR code:**

1. Open WhatsApp on your phone
2. Go to **Settings → Linked Devices**
3. Tap **Link a Device**
4. Point your camera at the terminal QR code

Once paired, the wizard confirms the connection and exits. Your session is saved automatically.

:::tip
If the QR code looks garbled, make sure your terminal is at least 60 columns wide and supports
Unicode. You can also ...

## Step 2: Getting a Second Phone Number (Bot Mode)

For bot mode, you need a phone number that isn't already registered with WhatsApp. Three options:

| Option | Cost | Notes |
|--------|------|-------|
| **Google Voice** | Free | US only. Get a number at [voice.google.com](https://voice.google.com). Verify WhatsApp via SMS through the Google Voice app. |
| **Prepaid SIM** | $5–15 one-time | Any carrier. Activate, verify WhatsApp, then the SIM can sit in a drawer. Number must stay active (make a call every 90 days). |
| **VoIP services** | Free–$5/month | TextNow, TextFree, or similar. Some VoIP numbers are blocked by WhatsApp — try a few if th...

## Step 3: Configure Hermes

Add the following to your `~/.hermes/.env` file:

```bash
# Required
WHATSAPP_ENABLED=true
WHATSAPP_MODE=bot                          # "bot" or "self-chat"

# Access control — pick ONE of these options:
WHATSAPP_ALLOWED_USERS=15551234567         # Comma-separated phone numbers (with country code, no +)
# WHATSAPP_ALLOWED_USERS=*                 # OR use * to allow everyone
# WHATSAPP_ALLOW_ALL_USERS=true            # OR set this flag instead (same effect as *)
```

:::tip Allow-all shorthand
Setting `WHATSAPP_ALLOWED_USERS=*` allows **all** senders (equivalent to `WHATSAPP_ALLOW_ALL_USERS=tru...

## Session Persistence

The Baileys bridge saves its session under `~/.hermes/platforms/whatsapp/session`. This means:

- **Sessions survive restarts** — you don't need to re-scan the QR code every time
- The session data includes encryption keys and device credentials
- **Do not share or commit this session directory** — it grants full access to the WhatsApp account

---...

## Re-pairing

If the session breaks (phone reset, WhatsApp update, manually unlinked), you'll see connection
errors in the gateway logs. To fix it:

```bash
hermes whatsapp
```

This generates a fresh QR code. Scan it again and the session is re-established. The gateway
handles **temporary** disconnections (network blips, phone going offline briefly) automatically
with reconnection logic.

---...

## Voice Messages

Hermes supports voice on WhatsApp:

- **Incoming:** Voice messages (`.ogg` opus) are automatically transcribed using the configured STT provider: local `faster-whisper`, Groq Whisper (`GROQ_API_KEY`), or OpenAI Whisper (`VOICE_TOOLS_OPENAI_KEY`)
- **Outgoing:** TTS responses are sent as MP3 audio file attachments
- Agent responses are prefixed with "⚕ **Hermes Agent**" by default. You can customize or disable this in `config.yaml`:

```yaml
# ~/.hermes/config.yaml
whatsapp:
  reply_prefix: ""                          # Empty string disables the header
  # reply_prefix: "🤖 *My Bot*\n──────\n"  ...

## Message Formatting & Delivery

WhatsApp supports **streaming (progressive) responses** — the bot edits its message in real-time as the AI generates text, just like Discord and Telegram. Internally, WhatsApp is classified as a TIER_MEDIUM platform for delivery capabilities.

### Chunking

Long responses are automatically split into multiple messages at **4,096 characters** per chunk (WhatsApp's practical display limit). You don't need to configure anything — the gateway handles splitting and sends chunks sequentially.

### WhatsApp-Compatible Markdown

Standard Markdown in AI responses is automatically converted to WhatsApp'...

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **QR code not scanning** | Ensure terminal is wide enough (60+ columns). Try a different terminal. Make sure you're scanning from the correct WhatsApp account (bot number, not personal). |
| **QR code expires** | QR codes refresh every ~20 seconds. If it times out, restart `hermes whatsapp`. |
| **Session not persisting** | Check that `~/.hermes/platforms/whatsapp/session` exists and is writable. If containerized, mount it as a persistent volume. |
| **Logged out unexpectedly** | WhatsApp unlinks devices after long inactivity. Keep the phone on a...

## Security

:::warning
**Configure access control** before going live. Set `WHATSAPP_ALLOWED_USERS` with specific
phone numbers (including country code, without the `+`), use `*` to allow everyone, or set
`WHATSAPP_ALLOW_ALL_USERS=true`. Without any of these, the gateway **denies all incoming
messages** as a safety measure.
:::

By default, unauthorized DMs still receive a pairing code reply. If you want a private WhatsApp number to stay completely silent to strangers, set:

```yaml
whatsapp:
  unauthorized_dm_behavior: ignore
```

- The `~/.hermes/platforms/whatsapp/session` directory contains full sessi...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
