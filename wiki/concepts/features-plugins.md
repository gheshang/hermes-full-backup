---
title: Plugins
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-plugins.md]
---

# Plugins

源文档：[Plugins](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/plugins.md)

# Plugins

Hermes has a plugin system for adding custom tools, hooks, and integrations without modifying core code.

**→ [Build a Hermes Plugin](/docs/guides/build-a-hermes-plugin)** — step-by-step guide with a complete working example.

## Quick overview

Drop a directory into `~/.hermes/plugins/` with a `plugin.yaml` and Python code:

```
~/.hermes/plugins/my-plugin/
├── plugin.yaml      # manifest
├── __init__.py      # register() — wires schemas to handlers
├── schemas.py       # tool schemas (what the LLM sees)
└── tools.py         # tool handlers (what runs when called)
```

Start Hermes — your tools appear alongside built-in tools. The model can call them immediately.

### Minimal working example

Here is a complete plugin that adds a `hello_world` tool and logs every tool call via a hook.

**`~/.hermes/plugins/hello-world/plugin.yaml`**
...

## What plugins can do

| Capability | How |
|-----------|-----|
| Add tools | `ctx.register_tool(name, schema, handler)` |
| Add hooks | `ctx.register_hook("post_tool_call", callback)` |
| Add slash commands | `ctx.register_command(name, handler, description)` — adds `/name` in CLI and gateway sessions |
| Add CLI commands | `ctx.register_cli_command(name, help, setup_fn, handler_fn)` — adds `hermes <plugin> <subcommand>` |
| Inject messages | `ctx.inject_message(content, role="user")` — see [Injecting Messages](#injecting-messages) |
| Ship data files | `Path(__file__).parent / "data" / "file.yaml"` |
| Bundle skil...

## Plugin discovery

| Source | Path | Use case |
|--------|------|----------|
| Bundled | `<repo>/plugins/` | Ships with Hermes — see [Built-in Plugins](/docs/user-guide/features/built-in-plugins) |
| User | `~/.hermes/plugins/` | Personal plugins |
| Project | `.hermes/plugins/` | Project-specific plugins (requires `HERMES_ENABLE_PROJECT_PLUGINS=true`) |
| pip | `hermes_agent.plugins` entry_points | Distributed packages |

Later sources override earlier ones on name collision, so a user plugin with the same name as a bundled plugin replaces it....

## Plugins are opt-in

**Every plugin — user-installed, bundled, or pip — is disabled by default.** Discovery finds them (so they show up in `hermes plugins` and `/plugins`), but nothing loads until you add the plugin's name to `plugins.enabled` in `~/.hermes/config.yaml`. This stops anything with hooks or tools from running without your explicit consent.

```yaml
plugins:
  enabled:
    - my-tool-plugin
    - disk-cleanup
  disabled:       # optional deny-list — always wins if a name appears in both
    - noisy-plugin
```

Three ways to flip state:

```bash
hermes plugins                    # interactive toggle (sp...

## Available hooks

Plugins can register callbacks for these lifecycle events. See the **[Event Hooks page](/docs/user-guide/features/hooks#plugin-hooks)** for full details, callback signatures, and examples.

| Hook | Fires when |
|------|-----------|
| [`pre_tool_call`](/docs/user-guide/features/hooks#pre_tool_call) | Before any tool executes |
| [`post_tool_call`](/docs/user-guide/features/hooks#post_tool_call) | After any tool returns |
| [`pre_llm_call`](/docs/user-guide/features/hooks#pre_llm_call) | Once per turn, before the LLM loop — can return `{"context": "..."}` to [inject context into the user messag...

## Plugin types

Hermes has three kinds of plugins:

| Type | What it does | Selection | Location |
|------|-------------|-----------|----------|
| **General plugins** | Add tools, hooks, slash commands, CLI commands | Multi-select (enable/disable) | `~/.hermes/plugins/` |
| **Memory providers** | Replace or augment built-in memory | Single-select (one active) | `plugins/memory/` |
| **Context engines** | Replace the built-in context compressor | Single-select (one active) | `plugins/context_engine/` |

Memory providers and context engines are **provider plugins** — only one of each type can be active at a tim...

## Managing plugins

```bash
hermes plugins                               # unified interactive UI
hermes plugins list                          # table: enabled / disabled / not enabled
hermes plugins install user/repo             # install from Git, then prompt Enable? [y/N]
hermes plugins install user/repo --enable    # install AND enable (no prompt)
hermes plugins install user/repo --no-enable # install but leave disabled (no prompt)
hermes plugins update my-plugin              # pull latest
hermes plugins remove my-plugin              # uninstall
hermes plugins enable my-plugin              # add to allow-list...

## Injecting Messages

Plugins can inject messages into the active conversation using `ctx.inject_message()`:

```python
ctx.inject_message("New data arrived from the webhook", role="user")
```

**Signature:** `ctx.inject_message(content: str, role: str = "user") -> bool`

How it works:

- If the agent is **idle** (waiting for user input), the message is queued as the next input and starts a new turn.
- If the agent is **mid-turn** (actively running), the message interrupts the current operation — the same as a user typing a new message and pressing Enter.
- For non-`"user"` roles, the content is prefixed with `[rol...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
