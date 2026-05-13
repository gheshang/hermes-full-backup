---
title: CLI Interface
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/cli.md]
---

# CLI Interface

源文档：[CLI Interface](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/cli.md)

# CLI Interface

Hermes Agent's CLI is a full terminal user interface (TUI) — not a web UI. It features multiline editing, slash-command autocomplete, conversation history, interrupt-and-redirect, and streaming tool output. Built for people who live in the terminal.

:::tip
Hermes also ships a modern TUI with modal overlays, mouse selection, and non-blocking input. Launch it with `hermes --tui` — see the [TUI](tui.md) guide.
:::

## Running the CLI

```bash
# Start an interactive session (default)
hermes

# Single query mode (non-interactive)
hermes chat -q "Hello"

# With a specific model
hermes chat --model "anthropic/claude-sonnet-4"

# With a specific provider
hermes chat --provider nous        # Use Nous Portal
hermes chat --provider openrouter  # Force OpenRouter

# With specific toolsets
hermes chat --toolsets "web,terminal,skills"

# Start with one or more skills preloaded
hermes -s hermes-agent-dev,github-auth
hermes chat -s github-pr-workflow -q "open a draft PR"

# Resume previous sessions
hermes --continue             # Resume...

## Interface Layout

<img className="docs-terminal-figure" src="/img/docs/cli-layout.svg" alt="Stylized preview of the Hermes CLI layout showing the banner, conversation area, and fixed input prompt." />
<p className="docs-figure-caption">The Hermes CLI banner, conversation stream, and fixed input prompt rendered as a stable docs figure instead of fragile text art.</p>

The welcome banner shows your model, terminal backend, working directory, available tools, and installed skills at a glance.

### Status Bar

A persistent status bar sits above the input area, updating in real time:

```
 ⚕ claude-sonnet-4-20250514...

## Keybindings

| Key | Action |
|-----|--------|
| `Enter` | Send message |
| `Alt+Enter` or `Ctrl+J` | New line (multi-line input) |
| `Alt+V` | Paste an image from the clipboard when supported by the terminal |
| `Ctrl+V` | Paste text and opportunistically attach clipboard images |
| `Ctrl+B` | Start/stop voice recording when voice mode is enabled (`voice.record_key`, default: `ctrl+b`) |
| `Ctrl+C` | Interrupt agent (double-press within 2s to force exit) |
| `Ctrl+D` | Exit |
| `Ctrl+Z` | Suspend Hermes to background (Unix only). Run `fg` in the shell to resume. |
| `Tab` | Accept auto-suggestion (ghost t...

## Slash Commands

Type `/` to see the autocomplete dropdown. Hermes supports a large set of CLI slash commands, dynamic skill commands, and user-defined quick commands.

Common examples:

| Command | Description |
|---------|-------------|
| `/help` | Show command help |
| `/model` | Show or change the current model |
| `/tools` | List currently available tools |
| `/skills browse` | Browse the skills hub and official optional skills |
| `/background <prompt>` | Run a prompt in a separate background session |
| `/skin` | Show or switch the active CLI skin |
| `/voice on` | Enable CLI voice mode (press `Ctrl+B` ...

## Quick Commands

You can define custom commands that run shell commands instantly without invoking the LLM. These work in both the CLI and messaging platforms (Telegram, Discord, etc.).

```yaml
# ~/.hermes/config.yaml
quick_commands:
  status:
    type: exec
    command: systemctl status hermes-agent
  gpu:
    type: exec
    command: nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader
```

Then type `/status` or `/gpu` in any chat. See the [Configuration guide](/docs/user-guide/configuration#quick-commands) for more examples....

## Preloading Skills at Launch

If you already know which skills you want active for the session, pass them at launch time:

```bash
hermes -s hermes-agent-dev,github-auth
hermes chat -s github-pr-workflow -s github-auth
```

Hermes loads each named skill into the session prompt before the first turn. The same flag works in interactive mode and single-query mode....

## Skill Slash Commands

Every installed skill in `~/.hermes/skills/` is automatically registered as a slash command. The skill name becomes the command:

```
/gif-search funny cats
/axolotl help me fine-tune Llama 3 on my dataset
/github-pr-workflow create a PR for the auth refactor

# Just the skill name loads it and lets the agent ask what you need:
/excalidraw
```...

## Personalities

Set a predefined personality to change the agent's tone:

```
/personality pirate
/personality kawaii
/personality concise
```

Built-in personalities include: `helpful`, `concise`, `technical`, `creative`, `teacher`, `kawaii`, `catgirl`, `pirate`, `shakespeare`, `surfer`, `noir`, `uwu`, `philosopher`, `hype`.

You can also define custom personalities in `~/.hermes/config.yaml`:

```yaml
personalities:
  helpful: "You are a helpful, friendly AI assistant."
  kawaii: "You are a kawaii assistant! Use cute expressions..."
  pirate: "Arrr! Ye be talkin' to Captain Hermes..."
  # Add your own!
```...

## Multi-line Input

There are two ways to enter multi-line messages:

1. **`Alt+Enter` or `Ctrl+J`** — inserts a new line
2. **Backslash continuation** — end a line with `\` to continue:

```
❯ Write a function that:\
  1. Takes a list of numbers\
  2. Returns the sum
```

:::info
Pasting multi-line text is supported — use `Alt+Enter` or `Ctrl+J` to insert newlines, or simply paste content directly.
:::...

## Interrupting the Agent

You can interrupt the agent at any point:

- **Type a new message + Enter** while the agent is working — it interrupts and processes your new instructions
- **`Ctrl+C`** — interrupt the current operation (press twice within 2s to force exit)
- In-progress terminal commands are killed immediately (SIGTERM, then SIGKILL after 1s)
- Multiple messages typed during interrupt are combined into one prompt

### Busy Input Mode

The `display.busy_input_mode` config key controls what happens when you press Enter while the agent is working:

| Mode | Behavior |
|------|----------|
| `"interrupt"` (defaul...

## Tool Progress Display

The CLI shows animated feedback as the agent works:

**Thinking animation** (during API calls):
```
  ◜ (｡•́︿•̀｡) pondering... (1.2s)
  ◠ (⊙_⊙) contemplating... (2.4s)
  ✧٩(ˊᗜˋ*)و✧ got it! (3.1s)
```

**Tool execution feed:**
```
  ┊ 💻 terminal `ls -la` (0.3s)
  ┊ 🔍 web_search (1.2s)
  ┊ 📄 web_extract (2.1s)
```

Cycle through display modes with `/verbose`: `off → new → all → verbose`. This command can also be enabled for messaging platforms — see [configuration](/docs/user-guide/configuration#display-settings).

### Tool Preview Length

The `display.tool_preview_length` config key controls th...

## Session Management

### Resuming Sessions

When you exit a CLI session, a resume command is printed:

```
Resume this session with:
  hermes --resume 20260225_143052_a1b2c3

Session:        20260225_143052_a1b2c3
Duration:       12m 34s
Messages:       28 (5 user, 18 tool calls)
```

Resume options:

```bash
hermes --continue                          # Resume the most recent CLI session
hermes -c                                  # Short form
hermes -c "my project"                     # Resume a named session (latest in lineage)
hermes --resume 20260225_143052_a1b2c3     # Resume a specific session by ID
hermes --...

## Background Sessions

Run a prompt in a separate background session while continuing to use the CLI for other work:

```
/background Analyze the logs in /var/log and summarize any errors from today
```

Hermes immediately confirms the task and gives you back the prompt:

```
🔄 Background task #1 started: "Analyze the logs in /var/log and summarize..."
   Task ID: bg_143022_a1b2c3
```

### How It Works

Each `/background` prompt spawns a **completely separate agent session** in a daemon thread:

- **Isolated conversation** — the background agent has no knowledge of your current session's history. It receives only th...

## Quiet Mode

By default, the CLI runs in quiet mode which:
- Suppresses verbose logging from tools
- Enables kawaii-style animated feedback
- Keeps output clean and user-friendly

For debug output:
```bash
he

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
