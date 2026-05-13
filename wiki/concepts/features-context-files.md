---
title: Context Files
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-context-files.md]
---

# Context Files

源文档：[Context Files](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/context-files.md)

# Context Files

Hermes Agent automatically discovers and loads context files that shape how it behaves. Some are project-local and discovered from your working directory. `SOUL.md` is now global to the Hermes instance and is loaded from `HERMES_HOME` only.

## Supported Context Files

| File | Purpose | Discovery |
|------|---------|-----------| 
| **.hermes.md** / **HERMES.md** | Project instructions (highest priority) | Walks to git root |
| **AGENTS.md** | Project instructions, conventions, architecture | CWD at startup + subdirectories progressively |
| **CLAUDE.md** | Claude Code context files (also detected) | CWD at startup + subdirectories progressively |
| **SOUL.md** | Global personality and tone customization for this Hermes instance | `HERMES_HOME/SOUL.md` only |
| **.cursorrules** | Cursor IDE coding conventions | CWD only |
| **.cursor/rules/*.mdc** | Cursor I...

## AGENTS.md

`AGENTS.md` is the primary project context file. It tells the agent how your project is structured, what conventions to follow, and any special instructions.

### Progressive Subdirectory Discovery

At session start, Hermes loads the `AGENTS.md` from your working directory into the system prompt. As the agent navigates into subdirectories during the session (via `read_file`, `terminal`, `search_files`, etc.), it **progressively discovers** context files in those directories and injects them into the conversation at the moment they become relevant.

```
my-project/
├── AGENTS.md              ← ...

## Architecture

- Frontend: Next.js 14 with App Router in `/frontend`
- Backend: FastAPI in `/backend`, uses SQLAlchemy ORM
- Database: PostgreSQL 16
- Deployment: Docker Compose on a Hetzner VPS...

## Conventions

- Use TypeScript strict mode for all frontend code
- Python code follows PEP 8, use type hints everywhere
- All API endpoints return JSON with `{data, error, meta}` shape
- Tests go in `__tests__/` directories (frontend) or `tests/` (backend)...

## Important Notes

- Never modify migration files directly — use Alembic commands
- The `.env.local` file has real API keys, don't commit it
- Frontend port is 3000, backend is 8000, DB is 5432
```...

## SOUL.md

`SOUL.md` controls the agent's personality, tone, and communication style. See the [Personality](/docs/user-guide/features/personality) page for full details.

**Location:**

- `~/.hermes/SOUL.md`
- or `$HERMES_HOME/SOUL.md` if you run Hermes with a custom home directory

Important details:

- Hermes seeds a default `SOUL.md` automatically if one does not exist yet
- Hermes loads `SOUL.md` only from `HERMES_HOME`
- Hermes does not probe the working directory for `SOUL.md`
- If the file is empty, nothing from `SOUL.md` is added to the prompt
- If the file has content, the content is injected ve...

## .cursorrules

Hermes is compatible with Cursor IDE's `.cursorrules` file and `.cursor/rules/*.mdc` rule modules. If these files exist in your project root and no higher-priority context file (`.hermes.md`, `AGENTS.md`, or `CLAUDE.md`) is found, they're loaded as the project context.

This means your existing Cursor conventions automatically apply when using Hermes....

## How Context Files Are Loaded

### At startup (system prompt)

Context files are loaded by `build_context_files_prompt()` in `agent/prompt_builder.py`:

1. **Scan working directory** — checks for `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules` (first match wins)
2. **Content is read** — each file is read as UTF-8 text
3. **Security scan** — content is checked for prompt injection patterns
4. **Truncation** — files exceeding 20,000 characters are head/tail truncated (70% head, 20% tail, with a marker in the middle)
5. **Assembly** — all sections are combined under a `# Project Context` header
6. **Injection** — the...

## AGENTS.md

[Your AGENTS.md content here]...

## .cursorrules

[Your .cursorrules content here]

[Your SOUL.md content here]
```

Notice that SOUL content is inserted directly, without extra wrapper text....

## Security: Prompt Injection Protection

All context files are scanned for potential prompt injection before being included. The scanner checks for:

- **Instruction override attempts**: "ignore previous instructions", "disregard your rules"
- **Deception patterns**: "do not tell the user"
- **System prompt overrides**: "system prompt override"
- **Hidden HTML comments**: `<!-- ignore instructions -->`
- **Hidden div elements**: `<div style="display:none">`
- **Credential exfiltration**: `curl ... $API_KEY`
- **Secret file access**: `cat .env`, `cat credentials`
- **Invisible characters**: zero-width spaces, bidirectional overrides, ...

## Size Limits

| Limit | Value |
|-------|-------|
| Max chars per file | 20,000 (~7,000 tokens) |
| Head truncation ratio | 70% |
| Tail truncation ratio | 20% |
| Truncation marker | 10% (shows char counts and suggests using file tools) |

When a file exceeds 20,000 characters, the truncation message reads:

```
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]
```...

## Tips for Effective Context Files

:::tip Best practices for AGENTS.md
1. **Keep it concise** — stay well under 20K chars; the agent reads it every turn
2. **Structure with headers** — use `##` sections for architecture, conventions, important notes
3. **Include concrete examples** — show preferred code patterns, API shapes, naming conventions
4. **Mention what NOT to do** — "never modify migration files directly"
5. **List key paths and ports** — the agent uses these for terminal commands
6. **Update as the project evolves** — stale context is worse than no context
:::

### Per-Subdirectory Context

For monorepos, put subdirec...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
