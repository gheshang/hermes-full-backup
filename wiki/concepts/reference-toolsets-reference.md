---
title: Toolsets Reference
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/reference-toolsets-reference.md]
---

# Toolsets Reference

源文档：[Toolsets Reference](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/toolsets-reference.md)

# Toolsets Reference

Toolsets are named bundles of tools that control what the agent can do. They're the primary mechanism for configuring tool availability per platform, per session, or per task.

## How Toolsets Work

Every tool belongs to exactly one toolset. When you enable a toolset, all tools in that bundle become available to the agent. Toolsets come in three kinds:

- **Core** — A single logical group of related tools (e.g., `file` bundles `read_file`, `write_file`, `patch`, `search_files`)
- **Composite** — Combines multiple core toolsets for a common scenario (e.g., `debugging` bundles file, terminal, and web tools)
- **Platform** — A complete tool configuration for a specific deployment context (e.g., `hermes-cli` is the default for interactive CLI sessions)...

## Configuring Toolsets

### Per-session (CLI)

```bash
hermes chat --toolsets web,file,terminal
hermes chat --toolsets debugging        # composite — expands to file + terminal + web
hermes chat --toolsets all              # everything
```

### Per-platform (config.yaml)

```yaml
toolsets:
  - hermes-cli          # default for CLI
  # - hermes-telegram   # override for Telegram gateway
```

### Interactive management

```bash
hermes tools                            # curses UI to enable/disable per platform
```

Or in-session:

```
/tools list
/tools disable browser
/tools enable rl
```...

## Core Toolsets

| Toolset | Tools | Purpose |
|---------|-------|---------|
| `browser` | `browser_back`, `browser_cdp`, `browser_click`, `browser_console`, `browser_dialog`, `browser_get_images`, `browser_navigate`, `browser_press`, `browser_scroll`, `browser_snapshot`, `browser_type`, `browser_vision`, `web_search` | Full browser automation. Includes `web_search` as a fallback for quick lookups. `browser_cdp` and `browser_dialog` are gated on a reachable CDP endpoint — they only appear when `/browser connect` is active, `browser.cdp_url` is set, or a Browserbase session is active. `browser_dialog` works tog...

## Composite Toolsets

These expand to multiple core toolsets, providing a convenient shorthand for common scenarios:

| Toolset | Expands to | Use case |
|---------|-----------|----------|
| `debugging` | `web` + `file` + `process`, `terminal` (via `includes`) — effectively `patch`, `process`, `read_file`, `search_files`, `terminal`, `web_extract`, `web_search`, `write_file` | Debug sessions — file access, terminal, and web research without browser or delegation overhead. |
| `safe` | `image_generate`, `vision_analyze`, `web_extract`, `web_search` | Read-only research and media generation. No file writes, no termin...

## Platform Toolsets

Platform toolsets define the complete tool configuration for a deployment target. Most messaging platforms use the same set as `hermes-cli`:

| Toolset | Differences from `hermes-cli` |
|---------|-------------------------------|
| `hermes-cli` | Full toolset — all 36 core tools including `clarify`. The default for interactive CLI sessions. |
| `hermes-acp` | Drops `clarify`, `cronjob`, `image_generate`, `send_message`, `text_to_speech`, homeassistant tools. Focused on coding tasks in IDE context. |
| `hermes-api-server` | Drops `clarify`, `send_message`, and `text_to_speech`. Adds everything ...

## Dynamic Toolsets

### MCP server toolsets

Each configured MCP server generates a `mcp-<server>` toolset at runtime. For example, if you configure a `github` MCP server, a `mcp-github` toolset is created containing all tools that server exposes.

```yaml
# config.yaml
mcp_servers:
  github:
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
```

This creates a `mcp-github` toolset you can reference in `--toolsets` or platform configs.

### Plugin toolsets

Plugins can register their own toolsets via `ctx.register_tool()` during plugin initialization. These appear alongside built-in toolset...

## Relationship to `hermes tools`

The `hermes tools` command provides a curses-based UI for toggling individual tools on or off per platform. This operates at the tool level (finer than toolsets) and persists to `config.yaml`. Disabled tools are filtered out even if their toolset is enabled.

See also: [Tools Reference](./tools-reference.md) for the complete list of individual tools and their parameters....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
