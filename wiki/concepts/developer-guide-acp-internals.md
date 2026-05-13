---
title: ACP Internals
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-acp-internals.md]
---

# ACP Internals

源文档：[ACP Internals](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/acp-internals.md)

# ACP Internals

The ACP adapter wraps Hermes' synchronous `AIAgent` in an async JSON-RPC stdio server.

Key implementation files:

- `acp_adapter/entry.py`
- `acp_adapter/server.py`
- `acp_adapter/session.py`
- `acp_adapter/events.py`
- `acp_adapter/permissions.py`
- `acp_adapter/tools.py`
- `acp_adapter/auth.py`
- `acp_registry/agent.json`

## Boot flow

```text
hermes acp / hermes-acp / python -m acp_adapter
  -> acp_adapter.entry.main()
  -> load ~/.hermes/.env
  -> configure stderr logging
  -> construct HermesACPAgent
  -> acp.run_agent(agent)
```

Stdout is reserved for ACP JSON-RPC transport. Human-readable logs go to stderr....

## Major components

### `HermesACPAgent`

`acp_adapter/server.py` implements the ACP agent protocol.

Responsibilities:

- initialize / authenticate
- new/load/resume/fork/list/cancel session methods
- prompt execution
- session model switching
- wiring sync AIAgent callbacks into ACP async notifications

### `SessionManager`

`acp_adapter/session.py` tracks live ACP sessions.

Each session stores:

- `session_id`
- `agent`
- `cwd`
- `model`
- `history`
- `cancel_event`

The manager is thread-safe and supports:

- create
- get
- remove
- fork
- list
- cleanup
- cwd updates

### Event bridge

`acp_adapter/events.p...

## Session lifecycle

```text
new_session(cwd)
  -> create SessionState
  -> create AIAgent(platform="acp", enabled_toolsets=["hermes-acp"])
  -> bind task_id/session_id to cwd override

prompt(..., session_id)
  -> extract text from ACP content blocks
  -> reset cancel event
  -> install callbacks + approval bridge
  -> run AIAgent in ThreadPoolExecutor
  -> update session history
  -> emit final agent message chunk
```

### Cancelation

`cancel(session_id)`:

- sets the session cancel event
- calls `agent.interrupt()` when available
- causes the prompt response to return `stop_reason="cancelled"`

### Forking

`f...

## Provider/auth behavior

ACP does not implement its own auth store.

Instead it reuses Hermes' runtime resolver:

- `acp_adapter/auth.py`
- `hermes_cli/runtime_provider.py`

So ACP advertises and uses the currently configured Hermes provider/credentials....

## Working directory binding

ACP sessions carry an editor cwd.

The session manager binds that cwd to the ACP session ID via task-scoped terminal/file overrides, so file and terminal tools operate relative to the editor workspace....

## Duplicate same-name tool calls

The event bridge tracks tool IDs FIFO per tool name, not just one ID per name. This is important for:

- parallel same-name calls
- repeated same-name calls in one step

Without FIFO queues, completion events would attach to the wrong tool invocation....

## Approval callback restoration

ACP temporarily installs an approval callback on the terminal tool during prompt execution, then restores the previous callback afterward. This avoids leaving ACP session-specific approval handlers installed globally forever....

## Current limitations

- ACP sessions are process-local from the ACP server's point of view
- non-text prompt blocks are currently ignored for request text extraction
- editor-specific UX varies by ACP client implementation...

## Related files

- `tests/acp/` — ACP test suite
- `toolsets.py` — `hermes-acp` toolset definition
- `hermes_cli/main.py` — `hermes acp` CLI subcommand
- `pyproject.toml` — `[acp]` optional dependency + `hermes-acp` script...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
