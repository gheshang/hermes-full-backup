---
title: Session Storage
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-session-storage.md]
---

# Session Storage

源文档：[Session Storage](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/session-storage.md)

# Session Storage

Hermes Agent uses a SQLite database (`~/.hermes/state.db`) to persist session
metadata, full message history, and model configuration across CLI and gateway
sessions. This replaces the earlier per-session JSONL file approach.

Source file: `hermes_state.py`

## Architecture Overview

```
~/.hermes/state.db (SQLite, WAL mode)
├── sessions          — Session metadata, token counts, billing
├── messages          — Full message history per session
├── messages_fts      — FTS5 virtual table for full-text search
└── schema_version    — Single-row table tracking migration state
```

Key design decisions:
- **WAL mode** for concurrent readers + one writer (gateway multi-platform)
- **FTS5 virtual table** for fast text search across all session messages
- **Session lineage** via `parent_session_id` chains (compression-triggered splits)
- **Source tagging** (`cli`, `telegram`, `disc...

## SQLite Schema

### Sessions Table

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    user_id TEXT,
    model TEXT,
    model_config TEXT,
    system_prompt TEXT,
    parent_session_id TEXT,
    started_at REAL NOT NULL,
    ended_at REAL,
    end_reason TEXT,
    message_count INTEGER DEFAULT 0,
    tool_call_count INTEGER DEFAULT 0,
    input_tokens INTEGER DEFAULT 0,
    output_tokens INTEGER DEFAULT 0,
    cache_read_tokens INTEGER DEFAULT 0,
    cache_write_tokens INTEGER DEFAULT 0,
    reasoning_tokens INTEGER DEFAULT 0,
    billing_provider TEXT,
    bi...

## Schema Version and Migrations

Current schema version: **6**

The `schema_version` table stores a single integer. On initialization,
`_init_schema()` checks the current version and applies migrations sequentially:

| Version | Change |
|---------|--------|
| 1 | Initial schema (sessions, messages, FTS5) |
| 2 | Add `finish_reason` column to messages |
| 3 | Add `title` column to sessions |
| 4 | Add unique index on `title` (NULLs allowed, non-NULL must be unique) |
| 5 | Add billing columns: `cache_read_tokens`, `cache_write_tokens`, `reasoning_tokens`, `billing_provider`, `billing_base_url`, `billing_mode`, `estimated_cost...

## Write Contention Handling

Multiple hermes processes (gateway + CLI sessions + worktree agents) share one
`state.db`. The `SessionDB` class handles write contention with:

- **Short SQLite timeout** (1 second) instead of the default 30s
- **Application-level retry** with random jitter (20-150ms, up to 15 retries)
- **BEGIN IMMEDIATE** transactions to surface lock contention at transaction start
- **Periodic WAL checkpoints** every 50 successful writes (PASSIVE mode)

This avoids the "convoy effect" where SQLite's deterministic internal backoff
causes all competing writers to retry at the same intervals.

```
_WRITE_MAX_...

## Common Operations

### Initialize

```python
from hermes_state import SessionDB

db = SessionDB()                           # Default: ~/.hermes/state.db
db = SessionDB(db_path=Path("/tmp/test.db"))  # Custom path
```

### Create and Manage Sessions

```python
# Create a new session
db.create_session(
    session_id="sess_abc123",
    source="cli",
    model="anthropic/claude-sonnet-4.6",
    user_id="user_1",
    parent_session_id=None,  # or previous session ID for lineage
)

# End a session
db.end_session("sess_abc123", end_reason="user_exit")

# Reopen a session (clear ended_at/end_reason)
db.reopen_session(...

## Full-Text Search

The `search_messages()` method supports FTS5 query syntax with automatic
sanitization of user input.

### Basic Search

```python
results = db.search_messages("docker deployment")
```

### FTS5 Query Syntax

| Syntax | Example | Meaning |
|--------|---------|---------|
| Keywords | `docker deployment` | Both terms (implicit AND) |
| Quoted phrase | `"exact phrase"` | Exact phrase match |
| Boolean OR | `docker OR kubernetes` | Either term |
| Boolean NOT | `python NOT java` | Exclude term |
| Prefix | `deploy*` | Prefix match |

### Filtered Search

```python
# Search only CLI sessions
results...

## Session Lineage

Sessions can form chains via `parent_session_id`. This happens when context
compression triggers a session split in the gateway.

### Query: Find Session Lineage

```sql
-- Find all ancestors of a session
WITH RECURSIVE lineage AS (
    SELECT * FROM sessions WHERE id = ?
    UNION ALL
    SELECT s.* FROM sessions s
    JOIN lineage l ON s.id = l.parent_session_id
)
SELECT id, title, started_at, parent_session_id FROM lineage;

-- Find all descendants of a session
WITH RECURSIVE descendants AS (
    SELECT * FROM sessions WHERE id = ?
    UNION ALL
    SELECT s.* FROM sessions s
    JOIN desce...

## Export and Cleanup

```python
# Export a single session with messages
data = db.export_session("sess_abc123")

# Export all sessions (with messages) as list of dicts
all_data = db.export_all(source="cli")

# Delete old sessions (only ended sessions)
deleted_count = db.prune_sessions(older_than_days=90)
deleted_count = db.prune_sessions(older_than_days=30, source="telegram")

# Clear messages but keep the session record
db.clear_messages("sess_abc123")

# Delete session and all messages
db.delete_session("sess_abc123")
```...

## Database Location

Default path: `~/.hermes/state.db`

This is derived from `hermes_constants.get_hermes_home()` which resolves to
`~/.hermes/` by default, or the value of `HERMES_HOME` environment variable.

The database file, WAL file (`state.db-wal`), and shared-memory file
(`state.db-shm`) are all created in the same directory....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
