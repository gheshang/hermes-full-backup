---
title: Browser CDP Supervisor — Design
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-browser-supervisor.md]
---

# Browser CDP Supervisor — Design

源文档：[Browser CDP Supervisor — Design](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/browser-supervisor.md)

# Browser CDP Supervisor — Design

**Status:** Shipped (PR 14540)
**Last updated:** 2026-04-23
**Author:** @teknium1

## Problem

Native JS dialogs (`alert`/`confirm`/`prompt`/`beforeunload`) and iframes are
the two biggest gaps in our browser tooling:

1. **Dialogs block the JS thread.** Any operation on the page stalls until the
   dialog is handled. Before this work, the agent had no way to know a dialog
   was open — subsequent tool calls would hang or throw opaque errors.
2. **Iframes are invisible.** The agent could see iframe nodes in the DOM
   snapshot but could not click, type, or eval inside them — especially
   cross-origin (OOPIF) iframes that live in separate Chromium processes.

[PR #12550](https://github....

## Backend capability matrix (verified live 2026-04-23)

Using throwaway probe scripts against a data-URL page that fires alerts in the
main frame and in a same-origin srcdoc iframe, plus a cross-origin
`https://example.com` iframe:

| Backend | Dialog detect | Dialog respond | Frame tree | OOPIF `Runtime.evaluate` via `browser_cdp(frame_id=...)` |
|---|---|---|---|---|
| Local Chrome (`--remote-debugging-port`) / `/browser connect` | ✓ | ✓ full workflow | ✓ | ✓ |
| Browserbase | ✓ (via bridge) | ✓ full workflow (via bridge) | ✓ | ✓ (`document.title = "Example Domain"` verified on real cross-origin iframe) |
| Camofox | ✗ no CDP (REST-only) | ✗ | pa...

## Architecture

### CDPSupervisor

One `asyncio.Task` running in a background daemon thread per Hermes `task_id`.
Holds a persistent WebSocket to the backend's CDP endpoint. Maintains:

- **Dialog queue** — `List[PendingDialog]` with `{id, type, message, default_prompt, session_id, opened_at}`
- **Frame tree** — `Dict[frame_id, FrameInfo]` with parent relationships, URL, origin, whether cross-origin child session
- **Session map** — `Dict[session_id, SessionInfo]` so interaction tools can route to the right attached session for OOPIF operations
- **Recent console errors** — ring buffer of the last 50 (for PR ...

## Agent surface (PR 1)

### One new tool

```
browser_dialog(action, prompt_text=None, dialog_id=None)
```

- `action="accept"` / `"dismiss"` → responds to the specified or sole pending dialog (required)
- `prompt_text=...` → text to supply to a `prompt()` dialog
- `dialog_id=...` → disambiguate when multiple dialogs queued (rare)

Tool is response-only. Agent reads pending dialogs from `browser_snapshot`
output before calling.

### `browser_snapshot` extension

Adds three optional fields to the existing snapshot output when a supervisor
is attached:

```json
{
  "pending_dialogs": [
    {"id": "d-1", "type": "alert"...

## Cross-origin iframe interaction

Extending the dialog-detect work, `browser_cdp(frame_id=...)` routes CDP
calls (notably `Runtime.evaluate`) through the supervisor's already-connected
WebSocket using the OOPIF's child `sessionId`. Agents pick frame_ids out of
`browser_snapshot.frame_tree.children[]` where `is_oopif=true` and pass them
to `browser_cdp`. For same-origin iframes (no dedicated CDP session), the
agent uses `contentWindow`/`contentDocument` from a top-level
`Runtime.evaluate` instead — supervisor surfaces an error pointing at that
fallback when `frame_id` belongs to a non-OOPIF.

On Browserbase, this is the ONLY re...

## Camofox (follow-up)

Issue planned against `jo-inc/camofox-browser` adding:
- Playwright `page.on('dialog', handler)` per session
- `GET /tabs/:tabId/dialogs` polling endpoint
- `POST /tabs/:tabId/dialogs/:id` to accept/dismiss
- Frame-tree introspection endpoint...

## Files touched (PR 1)

### New

- `tools/browser_supervisor.py` — `CDPSupervisor`, `SupervisorRegistry`, `PendingDialog`, `FrameInfo`
- `tools/browser_dialog_tool.py` — `browser_dialog` tool handler
- `tests/tools/test_browser_supervisor.py` — mock CDP WebSocket server + lifecycle/state tests
- `website/docs/developer-guide/browser-supervisor.md` — this file

### Modified

- `toolsets.py` — register `browser_dialog` in `browser`, `hermes-acp`, `hermes-api-server`, core toolsets (gated on CDP reachability)
- `tools/browser_tool.py`
  - `browser_navigate` start-hook: if CDP URL resolvable, `SupervisorRegistry.get_or_s...

## Non-goals

- Detection/interaction for Camofox (upstream gap; tracked separately)
- Streaming dialog/frame events live to the user (would require gateway hooks)
- Persisting dialog history across sessions (in-memory only)
- Per-iframe dialog policies (agent can express this via `dialog_id`)
- Replacing `browser_cdp` — it stays as the escape hatch for the long tail (cookies, viewport, network throttling)...

## Testing

Unit tests use an asyncio mock CDP server that speaks enough of the protocol
to exercise all state transitions: attach, enable, navigate, dialog fire,
dialog dismiss, frame attach/detach, child target attach, session teardown.
Real-backend E2E (Browserbase + local Chrome) is manual; probe scripts from
the 2026-04-23 investigation kept in-repo under
`scripts/browser_supervisor_e2e.py` so anyone can re-verify on new backend
versions....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
