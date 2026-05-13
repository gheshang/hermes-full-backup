---
title: Sessions
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/sessions.md]
---

# Sessions

源文档：[Sessions](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/sessions.md)

# Sessions

Hermes Agent automatically saves every conversation as a session. Sessions enable conversation resume, cross-session search, and full conversation history management.

## How Sessions Work

Every conversation — whether from the CLI, Telegram, Discord, Slack, WhatsApp, Signal, Matrix, or any other messaging platform — is stored as a session with full message history. Sessions are tracked in two complementary systems:

1. **SQLite database** (`~/.hermes/state.db`) — structured session metadata with FTS5 full-text search
2. **JSONL transcripts** (`~/.hermes/sessions/`) — raw conversation transcripts including tool calls (gateway)

The SQLite database stores:
- Session ID, source platform, user ID
- **Session title** (unique, human-readable name)
- Model name and configuration
- Syst...

## CLI Session Resume

Resume previous conversations from the CLI using `--continue` or `--resume`:

### Continue Last Session

```bash
# Resume the most recent CLI session
hermes --continue
hermes -c

# Or with the chat subcommand
hermes chat --continue
hermes chat -c
```

This looks up the most recent `cli` session from the SQLite database and loads its full conversation history.

### Resume by Name

If you've given a session a title (see [Session Naming](#session-naming) below), you can resume it by name:

```bash
# Resume a named session
hermes -c "my project"

# If there are lineage variants (my project, my pro...

## Session Naming

Give sessions human-readable titles so you can find and resume them easily.

### Auto-Generated Titles

Hermes automatically generates a short descriptive title (3–7 words) for each session after the first exchange. This runs in a background thread using a fast auxiliary model, so it adds no latency. You'll see auto-generated titles when browsing sessions with `hermes sessions list` or `hermes sessions browse`.

Auto-titling only fires once per session and is skipped if you've already set a title manually.

### Setting a Title Manually

Use the `/title` slash command inside any chat session (C...

## Session Management Commands

Hermes provides a full set of session management commands via `hermes sessions`:

### List Sessions

```bash
# List recent sessions (default: last 20)
hermes sessions list

# Filter by platform
hermes sessions list --source telegram

# Show more sessions
hermes sessions list --limit 50
```

When sessions have titles, the output shows titles, previews, and relative timestamps:

```
Title                  Preview                                  Last Active   ID
────────────────────────────────────────────────────────────────────────────────────────────────
refactoring auth       Help me refacto...

## Session Search Tool

The agent has a built-in `session_search` tool that performs full-text search across all past conversations using SQLite's FTS5 engine.

### How It Works

1. FTS5 searches matching messages ranked by relevance
2. Groups results by session, takes the top N unique sessions (default 3)
3. Loads each session's conversation, truncates to ~100K chars centered on matches
4. Sends to a fast summarization model for focused summaries
5. Returns per-session summaries with metadata and surrounding context

### FTS5 Query Syntax

The search supports standard FTS5 query syntax:

- Simple keywords: `docker d...

## Per-Platform Session Tracking

### Gateway Sessions

On messaging platforms, sessions are keyed by a deterministic session key built from the message source:

| Chat Type | Default Key Format | Behavior |
|-----------|--------------------|----------|
| Telegram DM | `agent:main:telegram:dm:<chat_id>` | One session per DM chat |
| Discord DM | `agent:main:discord:dm:<chat_id>` | One session per DM chat |
| WhatsApp DM | `agent:main:whatsapp:dm:<chat_id>` | One session per DM chat |
| Group chat | `agent:main:<platform>:group:<chat_id>:<user_id>` | Per-user inside the group when the platform exposes a user ID |
| Group thread...

## Storage Locations

| What | Path | Description |
|------|------|-------------|
| SQLite database | `~/.hermes/state.db` | All session metadata + messages with FTS5 |
| Gateway transcripts | `~/.hermes/sessions/` | JSONL transcripts per session + sessions.json index |
| Gateway index | `~/.hermes/sessions/sessions.json` | Maps session keys to active session IDs |

The SQLite database uses WAL mode for concurrent readers and a single writer, which suits the gateway's multi-platform architecture well.

### Database Schema

Key tables in `state.db`:

- **sessions** — session metadata (id, source, user_id, model, tit...

## Session Expiry and Cleanup

### Automatic Cleanup

- Gateway sessions auto-reset based on the configured reset policy
- Before reset, the agent saves memories and skills from the expiring session
- Opt-in auto-pruning: when `sessions.auto_prune` is `true`, ended sessions older than `sessions.retention_days` (default 90) are pruned at CLI/gateway startup
- After a prune that actually removed rows, `state.db` is `VACUUM`ed to reclaim disk space (SQLite does not shrink the file on plain DELETE)
- Pruning runs at most once per `sessions.min_interval_hours` (default 24); the last-run timestamp is tracked inside `state.db` its...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
