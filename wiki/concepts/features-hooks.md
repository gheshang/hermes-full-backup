---
title: Event Hooks
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-hooks.md]
---

# Event Hooks

源文档：[Event Hooks](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/hooks.md)

# Event Hooks

Hermes has three hook systems that run custom code at key lifecycle points:

| System | Registered via | Runs in | Use case |
|--------|---------------|---------|----------|
| **[Gateway hooks](#gateway-event-hooks)** | `HOOK.yaml` + `handler.py` in `~/.hermes/hooks/` | Gateway only | Logging, alerts, webhooks |
| **[Plugin hooks](#plugin-hooks)** | `ctx.register_hook()` in a [plugin](/docs/user-guide/features/plugins) | CLI + Gateway | Tool interception, metrics, guardrails |
| **[Shell hooks](#shell-hooks)** | `hooks:` block in `~/.hermes/config.yaml` pointing at shell scripts | CLI + Gateway | Drop-in scripts for blocking, auto-formatting, context injection |

All three systems are non-blocking — errors in any hook are caught and logged, never crashing the agent.

## Gateway Event Hooks

Gateway hooks fire automatically during gateway operation (Telegram, Discord, Slack, WhatsApp) without blocking the main agent pipeline.

### Creating a Hook

Each hook is a directory under `~/.hermes/hooks/` containing two files:

```text
~/.hermes/hooks/
└── my-hook/
    ├── HOOK.yaml      # Declares which events to listen for
    └── handler.py     # Python handler function
```

#### HOOK.yaml

```yaml
name: my-hook
description: Log all agent activity to a file
events:
  - agent:start
  - agent:end
  - agent:step
```

The `events` list determines which events trigger your handler. You can s...

## Plugin Hooks

[Plugins](/docs/user-guide/features/plugins) can register hooks that fire in **both CLI and gateway** sessions. These are registered programmatically via `ctx.register_hook()` in your plugin's `register()` function.

```python
def register(ctx):
    ctx.register_hook("pre_tool_call", my_tool_observer)
    ctx.register_hook("post_tool_call", my_tool_logger)
    ctx.register_hook("pre_llm_call", my_memory_callback)
    ctx.register_hook("post_llm_call", my_sync_callback)
    ctx.register_hook("on_session_start", my_init_callback)
    ctx.register_hook("on_session_end", my_cleanup_callback)
```

...

## Shell Hooks

Declare shell-script hooks in your `cli-config.yaml` and Hermes will run them as subprocesses whenever the corresponding plugin-hook event fires — in both CLI and gateway sessions. No Python plugin authoring required.

Use shell hooks when you want a drop-in, single-file script (Bash, Python, anything with a shebang) to:

- **Block a tool call** — reject dangerous `terminal` commands, enforce per-directory policies, require approval for destructive `write_file` / `patch` operations.
- **Run after a tool call** — auto-format Python or TypeScript files that the agent just wrote, log API calls, t...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
