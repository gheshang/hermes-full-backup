---
name: coding-agents
description: Delegate coding tasks to autonomous AI coding agents (Claude Code, Codex, OpenCode). Covers installation, orchestration modes, PTY handling, session management, and parallel execution patterns.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Claude, Codex, OpenCode, Anthropic, OpenAI, Code-Review, Refactoring, Automation, PTY]
    related_skills: []
---

# Coding Agents — Unified Guide

This umbrella skill consolidates all autonomous AI coding agent integrations. Each agent has its own orchestration patterns, but they share common concepts: print mode vs interactive mode, PTY handling, session management, and parallel execution.

**Choose your agent:**

- [Claude Code](#1-claude-code) — Anthropic's CLI agent (v2.x+)
- [Codex](#2-codex) — OpenAI's CLI agent
- [OpenCode](#3-opencode) — Provider-agnostic open-source agent

---

## 1. Claude Code

### Prerequisites

```bash
# Install
npm install -g @anthropic-ai/claude-code

# Auth
claude auth login  # browser OAuth
claude auth login --console  # API key billing
claude auth status  # verify

# Health check
claude doctor
claude --version  # requires v2.x+
```

### Two Orchestration Modes

#### Mode 1: Print Mode (`-p`) — Non-Interactive (PREFERRED)

```bash
terminal(command="claude -p 'Add error handling to all API calls' --allowedTools 'Read,Edit' --max-turns 10", workdir="/path/to/project", timeout=120)
```

**When to use:**
- One-shot coding tasks (fix bug, add feature, refactor)
- CI/CD automation
- Structured data extraction with `--json-schema`
- Piped input processing

**Print mode skips ALL interactive dialogs** — no workspace trust prompt, no permission confirmations.

#### Mode 2: Interactive PTY via tmux — Multi-Turn Sessions

```bash
# Start tmux session
terminal(command="tmux new-session -d -s claude-work -x 140 -y 40")

# Launch Claude
terminal(command="tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter")

# Wait for startup, send task
terminal(command="sleep 5 && tmux send-keys -t claude-work 'Refactor auth module to use JWT' Enter")

# Monitor progress
terminal(command="sleep 15 && tmux capture-pane -t claude-work -p -S -50")

# Send follow-ups
terminal(command="tmux send-keys -t claude-work 'Now add unit tests' Enter")

# Exit
terminal(command="tmux send-keys -t claude-work '/exit' Enter")
```

**When to use:**
- Multi-turn iterative work
- Tasks requiring human-in-the-loop
- Exploratory coding sessions
- When you need slash commands (`/compact`, `/review`, `/model`)

### PTY Dialog Handling (CRITICAL)

**Dialog 1: Workspace Trust (first visit)**
```
❯ 1. Yes, I trust this folder    ← DEFAULT (just press Enter)
  2. No, exit
```
**Handling:** `tmux send-keys -t <session> Enter`

**Dialog 2: Bypass Permissions Warning**
```
❯ 1. No, exit                    ← DEFAULT (WRONG!)
  2. Yes, I accept
```
**Handling:** `tmux send-keys -t <session> Down && sleep 0.3 && tmux send-keys -t <session> Enter`

### Print Mode Deep Dive

**Structured JSON output:**
```bash
claude -p 'Analyze auth.py for security issues' --output-format json --max-turns 5
```

Returns:
```json
{
  "type": "result",
  "subtype": "success",
  "result": "Analysis text...",
  "session_id": "75e2167f-...",
  "num_turns": 3,
  "total_cost_usd": 0.0787,
  "usage": { "input_tokens": 5, "output_tokens": 603 }
}
```

**Streaming JSON:**
```bash
claude -p 'Write summary' --output-format stream-json --verbose | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

**Piped input:**
```bash
cat src/auth.py | claude -p 'Review for bugs' --max-turns 1
cat src/*.py | claude -p 'Find TODOs' --max-turns 1
git diff HEAD~3 | claude -p 'Summarize changes' --max-turns 1
```

**JSON Schema for structured extraction:**
```bash
claude -p 'List all functions' --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}}}' \
  --max-turns 5
```

**Session continuation:**
```bash
# Start
claude -p 'Start refactoring' --output-format json --max-turns 10 > /tmp/session.json

# Resume with session ID
claude -p 'Continue with connection pooling' \
  --resume $(cat /tmp/session.json | python3 -c 'import json,sys; print(json.load(sys.stdin)["session_id"])') \
  --max-turns 5

# Or resume most recent in directory
claude -p 'What did you do last time?' --continue --max-turns 1
```

**Bare mode for CI:**
```bash
claude --bare -p 'Run all tests and report' --allowedTools 'Read,Bash' --max-turns 10
```

`--bare` skips hooks, plugins, MCP discovery, CLAUDE.md loading.

### Key CLI Flags

| Flag | Effect |
|------|--------|
| `-p, --print` | Non-interactive one-shot mode |
| `-c, --continue` | Resume most recent conversation |
| `-r, --resume <id>` | Resume specific session |
| `--fork-session` | New session ID when resuming |
| `--max-turns <n>` | Limit agentic loops (print mode) |
| `--max-budget-usd <n>` | Cap API spend |
| `--fallback-model haiku` | Auto-fallback on overload |
| `--dangerously-skip-permissions` | Auto-approve ALL tool use |
| `--allowedTools <tools>` | Whitelist tools |
| `--output-format json` | Single JSON result |
| `--output-format stream-json` | Streaming JSON events |
| `--json-schema <schema>` | Force structured output |
| `--bare` | Skip plugins/hooks (fastest) |
| `--model <alias>` | Model selection |
| `--effort <level>` | Reasoning depth: low/medium/high/max |

### Interactive Session Slash Commands

| Command | Purpose |
|---------|---------|
| `/help` | Show all commands |
| `/compact [focus]` | Compress context |
| `/clear` | Wipe history |
| `/context` | Visualize context usage |
| `/cost` | View token usage |
| `/review` | Request code review |
| `/plan [desc]` | Enter plan mode |
| `/model [name]` | Switch model |
| `/effort [level]` | Set reasoning effort |
| `/init` | Create CLAUDE.md |
| `/memory` | Open CLAUDE.md |
| `/config` | Open settings |
| `/permissions` | View/update tool perms |
| `/agents` | Manage subagents |
| `/mcp` | Manage MCP servers |
| `/exit` or `Ctrl+D` | End session |

### CLAUDE.md — Project Context

```markdown
# Project: My API

## Architecture
- FastAPI backend, PostgreSQL database
- pytest for testing with 90% coverage

## Key Commands
- `make test` — run full test suite
- `make lint` — ruff + mypy

## Code Standards
- Type hints on all public functions
- 2-space indentation for YAML
```

Claude auto-loads `CLAUDE.md` from project root.

### MCP Integration

```bash
# Add GitHub MCP
claude mcp add -s user github -- npx @modelcontextprotocol/server-github

# Add PostgreSQL
claude mcp add -s local postgres -- npx @anthropic-ai/server-postgres

# List
claude mcp list

# Remove
claude mcp remove postgres
```

### Cost & Performance Tips

1. Use `--max-turns` in print mode (start with 5-10)
2. Use `--max-budget-usd` for cost caps (~$0.05 minimum)
3. Use `--effort low` for simple tasks, `high/max` for complex
4. Use `--bare` for CI/scripting
5. Use `--allowedTools` to restrict capabilities
6. Use `/compact` in interactive sessions when context gets large
7. Use `--model haiku` for simple tasks, `opus` for complex
8. Start new sessions for distinct tasks (sessions last 5 hours)

### CC Switch — 国内网络代理方案

| 版本 | 仓库 | 适用 |
|------|------|------|
| CC Switch Desktop | farion1231/cc-switch | macOS/Windows/Linux桌面 |
| **CC Switch CLI** | SaladDay/cc-switch-cli | **headless Linux ✅** |
| CC Switch Web | Laliet/cc-switch-web | headless + 浏览器 |

**安装（Linux headless）:**
```bash
curl -fsSL https://github.com/SaladDay/cc-switch-cli/raw/main/install.sh | bash
cc-switch --version  # v5.3.4+
```

**配置:**
```bash
# 添加Provider
cc-switch provider add -a claude
# 启动本地Proxy
cc-switch proxy enable -a claude
cc-switch proxy serve --takeover claude
# 设置环境变量
export ANTHROPIC_BASE_URL=http://127.0.0.1:15721
```

### Pitfalls & Gotchas

1. **Claude Code 模型不可用** — 模型别名报错 "model may not exist"。解决：运行 `claude doctor` 或用 `claude -p '...'` 不带 `--model` 参数。
2. **Interactive mode REQUIRES tmux** — `pty=true` alone works but tmux gives `capture-pane` for monitoring.
3. **`--dangerously-skip-permissions` dialog defaults to "No, exit"** — must send Down then Enter.
4. **`--max-budget-usd` minimum is ~$0.05** — system prompt cache creation costs this.
5. **`--max-turns` is print-mode only** — ignored in interactive sessions.
6. **Session resumption requires same directory** — `--continue` finds most recent for current CWD.
7. **`--json-schema` needs enough `--max-turns`** — Claude must read files first.
8. **Trust dialog only appears once per directory** — first-time only.
9. **Background tmux sessions persist** — clean up with `tmux kill-session -t <name>`.
10. **Slash commands only work in interactive mode** — use natural language in `-p` mode.
11. **`--bare` skips OAuth** — requires `ANTHROPIC_API_KEY` env var.
12. **Context degradation above 70%** — monitor with `/context` and proactively `/compact`.

---

## 2. Codex

### Prerequisites

```bash
# Install
npm install -g @openai/codex

# Must be inside a git repository
cd /path/to/repo
```

### One-Shot Tasks

```bash
terminal(command="codex exec 'Add dark mode toggle'", workdir="~/project", pty=true)
```

For scratch work:
```bash
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build snake game'", pty=true)
```

### Background Mode (Long Tasks)

```bash
# Start with PTY
terminal(command="codex exec --full-auto 'Refactor auth module'", workdir="~/project", background=true, pty=true)
# Returns session_id

# Monitor
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send input if Codex asks
process(action="submit", session_id="<id>", data="yes")

# Kill if needed
process(action="kill", session_id="<id>")
```

### Key Flags

| Flag | Effect |
|------|--------|
| `exec "prompt"` | One-shot execution, exits when done |
| `--full-auto` | Sandboxed, auto-approves file changes |
| `--yolo` | No sandbox, no approvals (fastest, dangerous) |

### PR Reviews

```bash
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

### Parallel Issue Fixing with Worktrees

```bash
# Create worktrees
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# Launch Codex in each
terminal(command="codex --yolo exec 'Fix issue #78: <desc>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <desc>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# Monitor
process(action="list")

# After completion, push and create PRs
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# Cleanup
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

### Batch PR Reviews

```bash
# Fetch all PR refs
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# Review in parallel
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)
```

### Rules

1. **Always use `pty=true`** — Codex is interactive terminal app, hangs without PTY
2. **Git repo required** — Codex won't run outside git directory
3. **Use `exec` for one-shots** — `codex exec "prompt"` runs and exits
4. **`--full-auto` for building** — auto-approves changes within sandbox
5. **Background for long tasks** — use `background=true` and monitor with `process`
6. **Don't interfere** — monitor with `poll`/`log`, be patient
7. **Parallel is fine** — run multiple Codex processes at once

---

## 3. OpenCode

### Prerequisites

```bash
# Install
npm i -g opencode-ai@latest
# or: brew install anomalyco/tap/opencode

# Auth
opencode auth login
opencode auth list  # verify

# Verify
opencode --version
```

### Binary Resolution (Important)

```bash
which -a opencode
opencode --version
```

If needed, pin explicit path:
```bash
terminal(command="$HOME/.opencode/bin/opencode run '...'", workdir="~/project", pty=true)
```

### One-Shot Tasks

```bash
terminal(command="opencode run 'Add retry logic to API calls'", workdir="~/project")
```

Attach context files:
```bash
opencode run 'Review config' -f config.yaml -f .env.example
```

Show thinking:
```bash
opencode run 'Debug tests' --thinking
```

Force model:
```bash
opencode run 'Refactor auth' --model openrouter/anthropic/claude-sonnet-4
```

### Interactive Sessions (Background)

```bash
# Start TUI
terminal(command="opencode", workdir="~/project", background=true, pty=true)
# Returns session_id

# Send prompt
process(action="submit", session_id="<id>", data="Implement OAuth refresh flow")

# Monitor
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# Send follow-up
process(action="submit", session_id="<id>", data="Add error handling for expiry")

# Exit — Ctrl+C
process(action="write", session_id="<id>", data="\x03")
# Or kill
process(action="kill", session_id="<id>")
```

**Important:** Do NOT use `/exit` — opens agent selector. Use Ctrl+C or `process(action="kill")`.

### TUI Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Submit message (press twice if needed) |
| `Tab` | Switch between agents (build/plan) |
| `Ctrl+P` | Open command palette |
| `Ctrl+X L` | Switch session |
| `Ctrl+X M` | Switch model |
| `Ctrl+X N` | New session |
| `Ctrl+X E` | Open editor |
| `Ctrl+C` | Exit OpenCode |

### Resuming Sessions

```bash
# Continue last session
terminal(command="opencode -c", workdir="~/project", background=true, pty=true)

# Specific session
terminal(command="opencode -s ses_abc123", workdir="~/project", background=true, pty=true)
```

### Common Flags

| Flag | Use |
|------|-----|
| `run 'prompt'` | One-shot execution |
| `--continue / -c` | Continue last session |
| `--session <id> / -s` | Continue specific session |
| `--agent <name>` | Choose agent (build/plan) |
| `--model provider/model` | Force specific model |
| `--format json` | Machine-readable output |
| `--file <path> / -f` | Attach file(s) |
| `--thinking` | Show thinking blocks |
| `--variant <level>` | Reasoning effort (high/max/minimal) |
| `--title <name>` | Name session |

### PR Review Workflow

```bash
# Built-in PR command
terminal(command="opencode pr 42", workdir="~/project", pty=true)

# Or review in temp clone
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && opencode run 'Review PR vs main. Report bugs, security risks, test gaps.'", pty=true)
```

### Parallel Work Pattern

```bash
terminal(command="opencode run 'Fix issue #101 and commit'", workdir="/tmp/issue-101", background=true, pty=true)
terminal(command="opencode run 'Add parser tests and commit'", workdir="/tmp/issue-102", background=true, pty=true)
process(action="list")
```

### Session & Cost Management

```bash
# List past sessions
opencode session list

# Check token usage and costs
opencode stats
opencode stats --days 7 --models anthropic/claude-sonnet-4
```

### Pitfalls

- Interactive `opencode` (TUI) requires `pty=true`. `opencode run` does NOT need pty.
- `/exit` is NOT valid command — opens agent selector. Use Ctrl+C.
- PATH mismatch can select wrong binary/model config.
- If OpenCode appears stuck, inspect logs before killing: `process(action="log", session_id="<id>")`
- Avoid sharing one working directory across parallel sessions.
- Enter may need to be pressed twice in TUI.

### Knowledge Base

**Reference:** `opencode-manual` skill — comprehensive Chinese operation manual (21 chapters + appendix).

**Wiki:** `~/wiki/opencode/` contains 77 documents (Entities, Concepts, Raw Articles).

### Oh My Opencode (Multi-Agent Orchestration)

Community plugin transforming OpenCode into multi-agent system with 11 specialized agents:

- **Sisyphus**: Main orchestrator (Claude/Kimi/GLM)
- **Hephaestus**: GPT-native deep worker (GPT-5.3-Codex only)
- **Prometheus**: Strategic planning
- **Atlas**: Todo orchestration
- **Oracle, Librarian, Explore**: Read-only subagents

Key commands:
- `ultrawork` — Fully automatic task execution
- `/start-work` — Prometheus planning mode
- `/init-deep` — Generate hierarchical AGENTS.md files

---

## Agent Comparison

| Feature | Claude Code | Codex | OpenCode |
|---------|-------------|-------|----------|
| **Provider** | Anthropic | OpenAI | Provider-agnostic |
| **Install** | `npm i -g @anthropic-ai/claude-code` | `npm i -g @openai/codex` | `npm i -g opencode-ai` |
| **Print Mode** | `claude -p` | `codex exec` | `opencode run` |
| **Interactive** | tmux + claude | pty + codex | pty + opencode |
| **Session Resume** | `--resume <id>` | No | `-c`, `-s <id>` |
| **Structured Output** | `--json-schema` | No | `--format json` |
| **MCP Support** | Yes | No | Yes |
| **Worktrees** | `--worktree` | Manual | Manual |
| **Cost Tracking** | `--max-budget-usd` | No | `opencode stats` |
| **Thinking Mode** | `/effort` | No | `--thinking` |
| **Multi-Agent** | `--agents` | No | Oh My Opencode |

---

## General Rules for All Agents

1. **Prefer print mode for single tasks** — cleaner, no dialog handling
2. **Use tmux/PTY for interactive work** — reliable orchestration
3. **Always set `workdir`** — keep agent focused on correct project
4. **Set `--max-turns` in print mode** — prevents infinite loops
5. **Monitor tmux sessions** — `tmux capture-pane -t <session> -p -S -50`
6. **Look for `❯` prompt** — indicates agent waiting for input
7. **Clean up tmux sessions** — `tmux kill-session -t <name>`
8. **Report results to user** — summarize what agent did and changed
9. **Don't kill slow sessions** — agent may be doing multi-step work
10. **Use `--allowedTools`** — restrict to what task needs