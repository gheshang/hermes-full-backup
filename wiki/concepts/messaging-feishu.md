---
title: Feishu / Lark Setup
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-feishu.md]
---

# Feishu / Lark Setup

源文档：[Feishu / Lark Setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/feishu.md)

# Feishu / Lark Setup

Hermes Agent integrates with Feishu and Lark as a full-featured bot. Once connected, you can chat with the agent in direct messages or group chats, receive cron job results in a home chat, and send text, images, audio, and file attachments through the normal gateway flow.

The integration supports both connection modes:

- `websocket` — recommended; Hermes opens the outbound connection and you do not need a public webhook endpoint
- `webhook` — useful when you want Feishu/Lark to push events into your gateway over HTTP

## How Hermes Behaves

| Context | Behavior |
|---------|----------|
| Direct messages | Hermes responds to every message. |
| Group chats | Hermes responds only when the bot is @mentioned in the chat. |
| Shared group chats | By default, session history is isolated per user inside a shared chat. |

This shared-chat behavior is controlled by `config.yaml`:

```yaml
group_sessions_per_user: true
```

Set it to `false` only if you explicitly want one shared conversation per chat....

## Step 1: Create a Feishu / Lark App

### Recommended: Scan-to-Create (one command)

```bash
hermes gateway setup
```

Select **Feishu / Lark** and scan the QR code with your Feishu or Lark mobile app. Hermes will automatically create a bot application with the correct permissions and save the credentials.

### Alternative: Manual Setup

If scan-to-create is not available, the wizard falls back to manual input:

1. Open the Feishu or Lark developer console:
   - Feishu: [https://open.feishu.cn/](https://open.feishu.cn/)
   - Lark: [https://open.larksuite.com/](https://open.larksuite.com/)
2. Create a new app.
3. In **Credentials &...

## Step 2: Choose a Connection Mode

### Recommended: WebSocket mode

Use WebSocket mode when Hermes runs on your laptop, workstation, or a private server. No public URL is required. The official Lark SDK opens and maintains a persistent outbound WebSocket connection with automatic reconnection.

```bash
FEISHU_CONNECTION_MODE=websocket
```

**Requirements:** The `websockets` Python package must be installed. The SDK handles connection lifecycle, heartbeats, and auto-reconnection internally.

**How it works:** The adapter runs the Lark SDK's WebSocket client in a background executor thread. Inbound events (messages, reactions, ca...

## Step 3: Configure Hermes

### Option A: Interactive Setup

```bash
hermes gateway setup
```

Select **Feishu / Lark** and fill in the prompts.

### Option B: Manual Configuration

Add the following to `~/.hermes/.env`:

```bash
FEISHU_APP_ID=cli_xxx
FEISHU_APP_SECRET=secret_xxx
FEISHU_DOMAIN=feishu
FEISHU_CONNECTION_MODE=websocket

# Optional but strongly recommended
FEISHU_ALLOWED_USERS=ou_xxx,ou_yyy
FEISHU_HOME_CHANNEL=oc_xxx
```

`FEISHU_DOMAIN` accepts:

- `feishu` for Feishu China
- `lark` for Lark international...

## Step 4: Start the Gateway

```bash
hermes gateway
```

Then message the bot from Feishu/Lark to confirm that the connection is live....

## Home Chat

Use `/set-home` in a Feishu/Lark chat to mark it as the home channel for cron job results and cross-platform notifications.

You can also preconfigure it:

```bash
FEISHU_HOME_CHANNEL=oc_xxx
```...

## Security

### User Allowlist

For production use, set an allowlist of Feishu Open IDs:

```bash
FEISHU_ALLOWED_USERS=ou_xxx,ou_yyy
```

If you leave the allowlist empty, anyone who can reach the bot may be able to use it. In group chats, the allowlist is checked against the sender's open_id before the message is processed.

### Webhook Encryption Key

When running in webhook mode, set an encryption key to enable signature verification of inbound webhook payloads:

```bash
FEISHU_ENCRYPT_KEY=your-encrypt-key
```

This key is found in the **Event Subscriptions** section of your Feishu app configuration. W...

## Group Message Policy

The `FEISHU_GROUP_POLICY` environment variable controls whether and how Hermes responds in group chats:

```bash
FEISHU_GROUP_POLICY=allowlist   # default
```

| Value | Behavior |
|-------|----------|
| `open` | Hermes responds to @mentions from any user in any group. |
| `allowlist` | Hermes only responds to @mentions from users listed in `FEISHU_ALLOWED_USERS`. |
| `disabled` | Hermes ignores all group messages entirely. |

In all modes, the bot must be explicitly @mentioned (or @all) in the group before the message is processed. Direct messages bypass this gate.

### Bot Identity for @Ment...

## Interactive Card Actions

When users click buttons or interact with interactive cards sent by the bot, the adapter routes these as synthetic `/card` command events:

- Button clicks become: `/card button {"key": "value", ...}`
- The action's `value` payload from the card definition is included as JSON.
- Card actions are deduplicated with a 15-minute window to prevent double processing.

Card action events are dispatched with `MessageType.COMMAND`, so they flow through the normal command processing pipeline.

This is also how **command approval** works — when the agent needs to run a dangerous command, it sends an inte...

## Document Comment Intelligent Reply

Beyond chat, the adapter can also answer `@`-mentions left on **Feishu/Lark documents**. When a user comments on a document (local text selection or whole-doc comment) and @-mentions the bot, Hermes reads the document plus the surrounding comment thread and posts an LLM reply inline on the thread.

Powered by the `drive.notice.comment_add_v1` event, the handler:

- Fetches the document content and comment timeline in parallel (20 messages for whole-doc threads, 12 for local-selection threads).
- Runs the agent with the `feishu_doc` + `feishu_drive` toolsets scoped to that single comment sessio...

## Media Support

### Inbound (receiving)

The adapter receives and caches the following media types from users:

| Type | Extensions | How it's processed |
|------|-----------|-------------------|
| **Images** | .jpg, .jpeg, .png, .gif, .webp, .bmp | Downloaded via Feishu API and cached locally |
| **Audio** | .ogg, .mp3, .wav, .m4a, .aac, .flac, .opus, .webm | Downloaded and cached; small text files are auto-extracted |
| **Video** | .mp4, .mov, .avi, .mkv, .webm, .m4v, .3gp | Downloaded and cached as documents |
| **Files** | .pdf, .doc, .docx, .xls, .xlsx, .ppt, .pptx, and more | Downloaded and cached as do...

## Markdown Rendering and Post Fallback

When outbound text contains markdown formatting (headings, bold, lists, code blocks, links, etc.), the adapter automatically sends it as a Feishu **post** message with an embedded `md` tag rather than as plain text. This enables rich rendering in the Feishu client.

If the Feishu API rejects the post payload (e.g., due to unsupported markdown constructs), the adapter automatically falls back to sending as plain text with markdown stripped. This two-stage fallback ensures messages are always delivered.

Plain text messages (no markdown detected) are sent as the simple `text` message type....

## Processing Status Reactions

While the agent is working, the bot shows a `Typing` reaction on your message. It's cleared when the reply arrives, or replaced with `CrossMark` if processing failed.

Set `FEISHU_REACTIONS=false` to turn it off....

## Burst Protection and Batching

The adapter includes debouncing for rapid message bursts to avoid overwhelming the agent:

### Text Batching

When a user sends multiple text messages in quick succession, they are merged into a single event before being dispatched:

| Setting | Env Var | Default |
|---------|---------|---------|
| Quiet period | `HERMES_FEISHU_TEXT_BATCH_DELAY_SECONDS` | 0.6s |
| Max messages per batch | `HERMES_FEISHU_TEXT_BATCH_MAX_MESSAGES` | 8 |
| Max characters per batch | `HERMES_FEISHU_TEXT_BATCH_MAX_CHARS` | 4000 |

### Media Batching

Multiple media attachments sent in quick succession (e.g., draggin...

## Rate Limiting (Webhook Mode)

In webhook mode, the adapter enforces per-IP rate limiting to protect against abuse:


> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
