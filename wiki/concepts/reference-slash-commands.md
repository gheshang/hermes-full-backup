---
title: Slash Commands Reference
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/reference-slash-commands.md]
---

# Slash Commands Reference

源文档：[Slash Commands Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/slash-commands.md)

# Slash Commands Reference

Hermes has two slash-command surfaces, both driven by a central `COMMAND_REGISTRY` in `hermes_cli/commands.py`:

- **Interactive CLI slash commands** — dispatched by `cli.py`, with autocomplete from the registry
- **Messaging slash commands** — dispatched by `gateway/run.py`, with help text and platform menus generated from the registry

Installed skills are also exposed as dynamic slash commands on both surfaces. That includes bundled skills like `/plan`, which opens plan mode and saves markdown plans under `.hermes/plans/` relative to the active workspace/backend working directory.

## Interactive CLI slash commands

Type `/` in the CLI to open the autocomplete menu. Built-in commands are case-insensitive.

### Session

| Command | Description |
|---------|-------------|
| `/new` (alias: `/reset`) | Start a new session (fresh session ID + history) |
| `/clear` | Clear screen and start a new session |
| `/history` | Show conversation history |
| `/save` | Save the current conversation |
| `/retry` | Retry the last message (resend to agent) |
| `/undo` | Remove the last user/assistant exchange |
| `/title` | Set a title for the current session (usage: /title My Session Name) |
| `/compress [focus topic]` | M...

## Messaging slash commands

The messaging gateway supports the following built-in commands inside Telegram, Discord, Slack, WhatsApp, Signal, Email, and Home Assistant chats:

| Command | Description |
|---------|-------------|
| `/new` | Start a new conversation. |
| `/reset` | Reset conversation history. |
| `/status` | Show session info. |
| `/stop` | Kill all running background processes and interrupt the running agent. |
| `/model [provider:model]` | Show or change the model. Supports provider switches (`/model zai:glm-5`), custom endpoints (`/model custom:model`), named custom providers (`/model custom:local:qwen`)...

## Notes

- `/skin`, `/snapshot`, `/gquota`, `/reload`, `/tools`, `/toolsets`, `/browser`, `/config`, `/cron`, `/skills`, `/platforms`, `/paste`, `/image`, `/terminal-setup`, `/statusbar`, and `/plugins` are **CLI-only** commands.
- `/verbose` is **CLI-only by default**, but can be enabled for messaging platforms by setting `display.tool_progress_command: true` in `config.yaml`. When enabled, it cycles the `display.tool_progress` mode and saves to config.
- `/sethome`, `/update`, `/restart`, `/approve`, `/deny`, and `/commands` are **messaging-only** commands.
- `/status`, `/background`, `/voice`, `/rel...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
