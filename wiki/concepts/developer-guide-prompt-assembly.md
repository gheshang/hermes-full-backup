---
title: Prompt Assembly
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-prompt-assembly.md]
---

# Prompt Assembly

源文档：[Prompt Assembly](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/prompt-assembly.md)

# Prompt Assembly

Hermes deliberately separates:

- **cached system prompt state**
- **ephemeral API-call-time additions**

This is one of the most important design choices in the project because it affects:

- token usage
- prompt caching effectiveness
- session continuity
- memory correctness

Primary files:

- `run_agent.py`
- `agent/prompt_builder.py`
- `tools/memory_tool.py`

## Cached system prompt layers

The cached system prompt is assembled in roughly this order:

1. agent identity — `SOUL.md` from `HERMES_HOME` when available, otherwise falls back to `DEFAULT_AGENT_IDENTITY` in `prompt_builder.py`
2. tool-aware behavior guidance
3. Honcho static block (when active)
4. optional system message
5. frozen MEMORY snapshot
6. frozen USER profile snapshot
7. skills index
8. context files (`AGENTS.md`, `.cursorrules`, `.cursor/rules/*.mdc`) — SOUL.md is **not** included here when it was already loaded as the identity in step 1
9. timestamp / optional session ID
10. platform hint

When `skip_context_...

## Persistent Memory

- User prefers Python 3.12, uses pyproject.toml
- Default editor is nvim
- Working on project "atlas" in ~/code/atlas
- Timezone: US/Pacific

# Layer 6: Frozen USER profile snapshot...

## User Profile

- Name: Alice
- GitHub: alice-dev

# Layer 7: Skills index...

## Skills (mandatory)

Before replying, scan the skills below. If one clearly matches
your task, load it with skill_view(name) and follow its instructions.
...
<available_skills>
  software-development:
    - code-review: Structured code review workflow
    - test-driven-development: TDD methodology
  research:
    - arxiv: Search and summarize arXiv papers
</available_skills>

# Layer 8: Context files (from project directory)
# Project Context
The following project context files have been loaded and should be followed:...

## AGENTS.md

This is the atlas project. Use pytest for testing. The main
entry point is src/atlas/main.py. Always run `make lint` before
committing.

# Layer 9: Timestamp + session
Current time: 2026-03-30T14:30:00-07:00
Session: abc123

# Layer 10: Platform hint
You are a CLI AI Agent. Try not to use markdown but simple text
renderable inside a terminal.
```...

## How SOUL.md appears in the prompt

`SOUL.md` lives at `~/.hermes/SOUL.md` and serves as the agent's identity — the very first section of the system prompt. The loading logic in `prompt_builder.py` works as follows:

```python
# From agent/prompt_builder.py (simplified)
def load_soul_md() -> Optional[str]:
    soul_path = get_hermes_home() / "SOUL.md"
    if not soul_path.exists():
        return None
    content = soul_path.read_text(encoding="utf-8").strip()
    content = _scan_context_content(content, "SOUL.md")  # Security scan
    content = _truncate_content(content, "SOUL.md")       # Cap at 20k chars
    return content
``...

## How context files are injected

`build_context_files_prompt()` uses a **priority system** — only one project context type is loaded (first match wins):

```python
# From agent/prompt_builder.py (simplified)
def build_context_files_prompt(cwd=None, skip_soul=False):
    cwd_path = Path(cwd).resolve()

    # Priority: first match wins — only ONE project context loaded
    project_context = (
        _load_hermes_md(cwd_path)       # 1. .hermes.md / HERMES.md (walks to git root)
        or _load_agents_md(cwd_path)    # 2. AGENTS.md (cwd only)
        or _load_claude_md(cwd_path)    # 3. CLAUDE.md (cwd only)
        or _load_cu...

## API-call-time-only layers

These are intentionally *not* persisted as part of the cached system prompt:

- `ephemeral_system_prompt`
- prefill messages
- gateway-derived session context overlays
- later-turn Honcho recall injected into the current-turn user message

This separation keeps the stable prefix stable for caching....

## Memory snapshots

Local memory and user profile data are injected as frozen snapshots at session start. Mid-session writes update disk state but do not mutate the already-built system prompt until a new session or forced rebuild occurs....

## Context files

`agent/prompt_builder.py` scans and sanitizes project context files using a **priority system** — only one type is loaded (first match wins):

1. `.hermes.md` / `HERMES.md` (walks to git root)
2. `AGENTS.md` (CWD at startup; subdirectories discovered progressively during the session via `agent/subdirectory_hints.py`)
3. `CLAUDE.md` (CWD only)
4. `.cursorrules` / `.cursor/rules/*.mdc` (CWD only)

`SOUL.md` is loaded separately via `load_soul_md()` for the identity slot. When it loads successfully, `build_context_files_prompt(skip_soul=True)` prevents it from appearing twice.

Long files are tru...

## Skills index

The skills system contributes a compact skills index to the prompt when skills tooling is available....

## Why prompt assembly is split this way

The architecture is intentionally optimized to:

- preserve provider-side prompt caching
- avoid mutating history unnecessarily
- keep memory semantics understandable
- let gateway/ACP/CLI add context without poisoning persistent prompt state...

## Related docs

- [Context Compression & Prompt Caching](./context-compression-and-caching.md)
- [Session Storage](./session-storage.md)
- [Gateway Internals](./gateway-internals.md)...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
