---
title: Email Setup
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-email.md]
---

# Email Setup

源文档：[Email Setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/email.md)

# Email Setup

Hermes can receive and reply to emails using standard IMAP and SMTP protocols. Send an email to the agent's address and it replies in-thread — no special client or bot API needed. Works with Gmail, Outlook, Yahoo, Fastmail, or any provider that supports IMAP/SMTP.

:::info No External Dependencies
The Email adapter uses Python's built-in `imaplib`, `smtplib`, and `email` modules. No additional packages or external services are required.
:::

---

## Prerequisites

- **A dedicated email account** for your Hermes agent (don't use your personal email)
- **IMAP enabled** on the email account
- **An app password** if using Gmail or another provider with 2FA

### Gmail Setup

1. Enable 2-Factor Authentication on your Google Account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Create a new App Password (select "Mail" or "Other")
4. Copy the 16-character password — you'll use this instead of your regular password

### Outlook / Microsoft 365

1. Go to [Security Settings](https://account.microsoft.com/security)
2. Enable 2FA if not alre...

## Step 1: Configure Hermes

The easiest way:

```bash
hermes gateway setup
```

Select **Email** from the platform menu. The wizard prompts for your email address, password, IMAP/SMTP hosts, and allowed senders.

### Manual Configuration

Add to `~/.hermes/.env`:

```bash
# Required
EMAIL_ADDRESS=hermes@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop    # App password (not your regular password)
EMAIL_IMAP_HOST=imap.gmail.com
EMAIL_SMTP_HOST=smtp.gmail.com

# Security (recommended)
EMAIL_ALLOWED_USERS=your@email.com,colleague@work.com

# Optional
EMAIL_IMAP_PORT=993                    # Default: 993 (IMAP SSL)
EMAIL_SMTP_PO...

## Step 2: Start the Gateway

```bash
hermes gateway              # Run in foreground
hermes gateway install      # Install as a user service
sudo hermes gateway install --system   # Linux only: boot-time system service
```

On startup, the adapter:
1. Tests IMAP and SMTP connections
2. Marks all existing inbox messages as "seen" (only processes new emails)
3. Starts polling for new messages

---...

## How It Works

### Receiving Messages

The adapter polls the IMAP inbox for UNSEEN messages at a configurable interval (default: 15 seconds). For each new email:

- **Subject line** is included as context (e.g., `[Subject: Deploy to production]`)
- **Reply emails** (subject starting with `Re:`) skip the subject prefix — the thread context is already established
- **Attachments** are cached locally:
  - Images (JPEG, PNG, GIF, WebP) → available to the vision tool
  - Documents (PDF, ZIP, etc.) → available for file access
- **HTML-only emails** have tags stripped for plain text extraction
- **Self-messages** a...

## Access Control

Email access follows the same pattern as all other Hermes platforms:

1. **`EMAIL_ALLOWED_USERS` set** → only emails from those addresses are processed
2. **No allowlist set** → unknown senders get a pairing code
3. **`EMAIL_ALLOW_ALL_USERS=true`** → any sender is accepted (use with caution)

:::warning
**Always configure `EMAIL_ALLOWED_USERS`.** Without it, anyone who knows the agent's email address could send commands. The agent has terminal access by default.
:::

---...

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **"IMAP connection failed"** at startup | Verify `EMAIL_IMAP_HOST` and `EMAIL_IMAP_PORT`. Ensure IMAP is enabled on the account. For Gmail, enable it in Settings → Forwarding and POP/IMAP. |
| **"SMTP connection failed"** at startup | Verify `EMAIL_SMTP_HOST` and `EMAIL_SMTP_PORT`. Check that your password is correct (use App Password for Gmail). |
| **Messages not received** | Check `EMAIL_ALLOWED_USERS` includes the sender's email. Check spam folder — some providers flag automated replies. |
| **"Authentication failed"** | For Gmail, you must u...

## Security

:::warning
**Use a dedicated email account.** Don't use your personal email — the agent stores the password in `.env` and has full inbox access via IMAP.
:::

- Use **App Passwords** instead of your main password (required for Gmail with 2FA)
- Set `EMAIL_ALLOWED_USERS` to restrict who can interact with the agent
- The password is stored in `~/.hermes/.env` — protect this file (`chmod 600`)
- IMAP uses SSL (port 993) and SMTP uses STARTTLS (port 587) by default — connections are encrypted

---...

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EMAIL_ADDRESS` | Yes | — | Agent's email address |
| `EMAIL_PASSWORD` | Yes | — | Email password or app password |
| `EMAIL_IMAP_HOST` | Yes | — | IMAP server host (e.g., `imap.gmail.com`) |
| `EMAIL_SMTP_HOST` | Yes | — | SMTP server host (e.g., `smtp.gmail.com`) |
| `EMAIL_IMAP_PORT` | No | `993` | IMAP server port |
| `EMAIL_SMTP_PORT` | No | `587` | SMTP server port |
| `EMAIL_POLL_INTERVAL` | No | `15` | Seconds between inbox checks |
| `EMAIL_ALLOWED_USERS` | No | — | Comma-separated allowe...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
