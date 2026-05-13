---
title: Quickstart
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/getting-started-quickstart.md]
---

# Quickstart

源文档：[Quickstart](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/quickstart.md)

# Quickstart

This guide gets you from zero to a working Hermes setup that survives real use. Install, choose a provider, verify a working chat, and know exactly what to do when something breaks.

## Who this is for

- Brand new and want the shortest path to a working setup
- Switching providers and don't want to lose time to config mistakes
- Setting up Hermes for a team, bot, or always-on workflow
- Tired of "it installed, but it still does nothing"...

## The fastest path

Pick the row that matches your goal:

| Goal | Do this first | Then do this |
|---|---|---|
| I just want Hermes working on my machine | `hermes setup` | Run a real chat and verify it responds |
| I already know my provider | `hermes model` | Save the config, then start chatting |
| I want a bot or always-on setup | `hermes gateway setup` after CLI works | Connect Telegram, Discord, Slack, or another platform |
| I want a local or self-hosted model | `hermes model` → custom endpoint | Verify the endpoint, model name, and context length |
| I want multi-provider fallback | `hermes model` first ...

## 1. Install Hermes Agent

Run the one-line installer:

```bash
# Linux / macOS / WSL2 / Android (Termux)
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

:::tip Android / Termux
If you're installing on a phone, see the dedicated [Termux guide](./termux.md) for the tested manual path, supported extras, and current Android-specific limitations.
:::

:::tip Windows Users
Install [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) first, then run the command above inside your WSL2 terminal.
:::

After it finishes, reload your shell:

```bash
source ~/.bash...

## 2. Choose a Provider

The single most important setup step. Use `hermes model` to walk through the choice interactively:

```bash
hermes model
```

Good defaults:

| Situation | Recommended path |
|---|---|
| Least friction | Nous Portal or OpenRouter |
| You already have Claude or Codex auth | Anthropic or OpenAI Codex |
| You want local/private inference | Ollama or any custom OpenAI-compatible endpoint |
| You want multi-provider routing | OpenRouter |
| You have a custom GPU server | vLLM, SGLang, LiteLLM, or any OpenAI-compatible endpoint |

For most first-time users: choose a provider, accept the defaults unl...

## 3. Run Your First Chat

```bash
hermes            # classic CLI
hermes --tui      # modern TUI (recommended)
```

You'll see a welcome banner with your model, available tools, and skills. Use a prompt that's specific and easy to verify:

:::tip Pick your interface
Hermes ships with two terminal interfaces: the classic `prompt_toolkit` CLI and a newer [TUI](../user-guide/tui.md) with modal overlays, mouse selection, and non-blocking input. Both share the same sessions, slash commands, and config — try each with `hermes` vs `hermes --tui`.
:::

```
Summarize this repo in 5 bullets and tell me what the main entrypoint i...

## 4. Verify Sessions Work

Before moving on, make sure resume works:

```bash
hermes --continue    # Resume the most recent session
hermes -c            # Short form
```

That should bring you back to the session you just had. If it doesn't, check whether you're in the same profile and whether the session actually saved. This matters later when you're juggling multiple setups or machines....

## 5. Try Key Features

### Use the terminal

```
❯ What's my disk usage? Show the top 5 largest directories.
```

The agent runs terminal commands on your behalf and shows results.

### Slash commands

Type `/` to see an autocomplete dropdown of all commands:

| Command | What it does |
|---------|-------------|
| `/help` | Show all available commands |
| `/tools` | List available tools |
| `/model` | Switch models interactively |
| `/personality pirate` | Try a fun personality |
| `/save` | Save the conversation |

### Multi-line input

Press `Alt+Enter` or `Ctrl+J` to add a new line. Great for pasting code or writ...

## 6. Add the Next Layer

Only after the base chat works. Pick what you need:

### Bot or shared assistant

```bash
hermes gateway setup    # Interactive platform configuration
```

Connect [Telegram](/docs/user-guide/messaging/telegram), [Discord](/docs/user-guide/messaging/discord), [Slack](/docs/user-guide/messaging/slack), [WhatsApp](/docs/user-guide/messaging/whatsapp), [Signal](/docs/user-guide/messaging/signal), [Email](/docs/user-guide/messaging/email), or [Home Assistant](/docs/user-guide/messaging/homeassistant).

### Automation and tools

- `hermes tools` — tune tool access per platform
- `hermes skills` — b...

## Common Failure Modes

These are the problems that waste the most time:

| Symptom | Likely cause | Fix |
|---|---|---|
| Hermes opens but gives empty or broken replies | Provider auth or model selection is wrong | Run `hermes model` again and confirm provider, model, and auth |
| Custom endpoint "works" but returns garbage | Wrong base URL, model name, or not actually OpenAI-compatible | Verify the endpoint in a separate client first |
| Gateway starts but nobody can message it | Bot token, allowlist, or platform setup is incomplete | Re-run `hermes gateway setup` and check `hermes gateway status` |
| `hermes --con...

## Recovery Toolkit

When something feels off, use this order:

1. `hermes doctor`
2. `hermes model`
3. `hermes setup`
4. `hermes sessions list`
5. `hermes --continue`
6. `hermes gateway status`

That sequence gets you from "broken vibes" back to a known state fast.

---...

## Quick Reference

| Command | Description |
|---------|-------------|
| `hermes` | Start chatting |
| `hermes model` | Choose your LLM provider and model |
| `hermes tools` | Configure which tools are enabled per platform |
| `hermes setup` | Full setup wizard (configures everything at once) |
| `hermes doctor` | Diagnose issues |
| `hermes update` | Update to latest version |
| `hermes gateway` | Start the messaging gateway |
| `hermes --continue` | Resume last session |...

## Next Steps

- **[CLI Guide](../user-guide/cli.md)** — Master the terminal interface
- **[Configuration](../user-guide/configuration.md)** — Customize your setup
- **[Messaging Gateway](../user-guide/messaging/index.md)** — Connect Telegram, Discord, Slack, WhatsApp, Signal, Email, or Home Assistant
- **[Tools & Toolsets](../user-guide/features/tools.md)** — Explore available capabilities
- **[AI Providers](../integrations/providers.md)** — Full provider list and setup details
- **[Skills System](../user-guide/features/skills.md)** — Reusable workflows and knowledge
- **[Tips & Best Practices](../guides/ti...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
