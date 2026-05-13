---
title: Tools & Toolsets
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-tools.md]
---

# Tools & Toolsets

源文档：[Tools & Toolsets](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/tools.md)

# Tools & Toolsets

Tools are functions that extend the agent's capabilities. They're organized into logical **toolsets** that can be enabled or disabled per platform.

## Available Tools

Hermes ships with a broad built-in tool registry covering web search, browser automation, terminal execution, file editing, memory, delegation, RL training, messaging delivery, Home Assistant, and more.

:::note
**Honcho cross-session memory** is available as a memory provider plugin (`plugins/memory/honcho/`), not as a built-in toolset. See [Plugins](./plugins.md) for installation.
:::

High-level categories:

| Category | Examples | Description |
|----------|----------|-------------|
| **Web** | `web_search`, `web_extract` | Search the web and extract page content. |
| **Terminal & Files** |...

## Using Toolsets

```bash
# Use specific toolsets
hermes chat --toolsets "web,terminal"

# See all available tools
hermes tools

# Configure tools per platform (interactive)
hermes tools
```

Common toolsets include `web`, `terminal`, `file`, `browser`, `vision`, `image_gen`, `moa`, `skills`, `tts`, `todo`, `memory`, `session_search`, `cronjob`, `code_execution`, `delegation`, `clarify`, `homeassistant`, and `rl`.

See [Toolsets Reference](/docs/reference/toolsets-reference) for the full set, including platform presets such as `hermes-cli`, `hermes-telegram`, and dynamic MCP toolsets like `mcp-<server>`....

## Terminal Backends

The terminal tool can execute commands in different environments:

| Backend | Description | Use Case |
|---------|-------------|----------|
| `local` | Run on your machine (default) | Development, trusted tasks |
| `docker` | Isolated containers | Security, reproducibility |
| `ssh` | Remote server | Sandboxing, keep agent away from its own code |
| `singularity` | HPC containers | Cluster computing, rootless |
| `modal` | Cloud execution | Serverless, scale |
| `daytona` | Cloud sandbox workspace | Persistent remote dev environments |

### Configuration

```yaml
# In ~/.hermes/config.yaml
te...

## Background Process Management

Start background processes and manage them:

```python
terminal(command="pytest -v tests/", background=true)
# Returns: {"session_id": "proc_abc123", "pid": 12345}

# Then manage with the process tool:
process(action="list")       # Show all running processes
process(action="poll", session_id="proc_abc123")   # Check status
process(action="wait", session_id="proc_abc123")   # Block until done
process(action="log", session_id="proc_abc123")    # Full output
process(action="kill", session_id="proc_abc123")   # Terminate
process(action="write", session_id="proc_abc123", data="y")  # Send input
``...

## Sudo Support

If a command needs sudo, you'll be prompted for your password (cached for the session). Or set `SUDO_PASSWORD` in `~/.hermes/.env`.

:::warning
On messaging platforms, if sudo fails, the output includes a tip to add `SUDO_PASSWORD` to `~/.hermes/.env`.
:::...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
