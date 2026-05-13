---
title: MCP (Model Context Protocol)
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-mcp.md]
---

# MCP (Model Context Protocol)

源文档：[MCP (Model Context Protocol)](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md)

# MCP (Model Context Protocol)

MCP lets Hermes Agent connect to external tool servers so the agent can use tools that live outside Hermes itself — GitHub, databases, file systems, browser stacks, internal APIs, and more.

If you have ever wanted Hermes to use a tool that already exists somewhere else, MCP is usually the cleanest way to do it.

## What MCP gives you

- Access to external tool ecosystems without writing a native Hermes tool first
- Local stdio servers and remote HTTP MCP servers in the same config
- Automatic tool discovery and registration at startup
- Utility wrappers for MCP resources and prompts when supported by the server
- Per-server filtering so you can expose only the MCP tools you actually want Hermes to see...

## Quick start

1. Install MCP support (already included if you used the standard install script):

```bash
cd ~/.hermes/hermes-agent
uv pip install -e ".[mcp]"
```

2. Add an MCP server to `~/.hermes/config.yaml`:

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
```

3. Start Hermes:

```bash
hermes chat
```

4. Ask Hermes to use the MCP-backed capability.

For example:

```text
List the files in /home/user/projects and summarize the repo structure.
```

Hermes will discover the MCP server's tools and use them like any o...

## Two kinds of MCP servers

### Stdio servers

Stdio servers run as local subprocesses and talk over stdin/stdout.

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
```

Use stdio servers when:
- the server is installed locally
- you want low-latency access to local resources
- you are following MCP server docs that show `command`, `args`, and `env`

### HTTP servers

HTTP MCP servers are remote endpoints Hermes connects to directly.

```yaml
mcp_servers:
  remote_api:
    url: "https://mcp.example.com/mcp"
    hea...

## Basic configuration reference

Hermes reads MCP config from `~/.hermes/config.yaml` under `mcp_servers`.

### Common keys

| Key | Type | Meaning |
|---|---|---|
| `command` | string | Executable for a stdio MCP server |
| `args` | list | Arguments for the stdio server |
| `env` | mapping | Environment variables passed to the stdio server |
| `url` | string | HTTP MCP endpoint |
| `headers` | mapping | HTTP headers for remote servers |
| `timeout` | number | Tool call timeout |
| `connect_timeout` | number | Initial connection timeout |
| `enabled` | bool | If `false`, Hermes skips the server entirely |
| `tools` | mapping ...

## How Hermes registers MCP tools

Hermes prefixes MCP tools so they do not collide with built-in names:

```text
mcp_<server_name>_<tool_name>
```

Examples:

| Server | MCP tool | Registered name |
|---|---|---|
| `filesystem` | `read_file` | `mcp_filesystem_read_file` |
| `github` | `create-issue` | `mcp_github_create_issue` |
| `my-api` | `query.data` | `mcp_my_api_query_data` |

In practice, you usually do not need to call the prefixed name manually — Hermes sees the tool and chooses it during normal reasoning....

## MCP utility tools

When supported, Hermes also registers utility tools around MCP resources and prompts:

- `list_resources`
- `read_resource`
- `list_prompts`
- `get_prompt`

These are registered per server with the same prefix pattern, for example:

- `mcp_github_list_resources`
- `mcp_github_get_prompt`

### Important

These utility tools are now capability-aware:
- Hermes only registers resource utilities if the MCP session actually supports resource operations
- Hermes only registers prompt utilities if the MCP session actually supports prompt operations

So a server that exposes callable tools but no resou...

## Per-server filtering

You can control which tools each MCP server contributes to Hermes, allowing fine-grained management of your tool namespace.

### Disable a server entirely

```yaml
mcp_servers:
  legacy:
    url: "https://mcp.legacy.internal"
    enabled: false
```

If `enabled: false`, Hermes skips the server completely and does not even attempt a connection.

### Whitelist server tools

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [create_issue, list_issues]
```

Only thos...

## What happens if everything is filtered out?

If your config filters out all callable tools and disables or omits all supported utilities, Hermes does not create an empty runtime MCP toolset for that server.

That keeps the tool list clean....

## Runtime behavior

### Discovery time

Hermes discovers MCP servers at startup and registers their tools into the normal tool registry.

### Dynamic Tool Discovery

MCP servers can notify Hermes when their available tools change at runtime by sending a `notifications/tools/list_changed` notification. When Hermes receives this notification, it automatically re-fetches the server's tool list and updates the registry — no manual `/reload-mcp` required.

This is useful for MCP servers whose capabilities change dynamically (e.g. a server that adds tools when a new database schema is loaded, or removes tools when a se...

## Security model

### Stdio env filtering

For stdio servers, Hermes does not blindly pass your full shell environment.

Only explicitly configured `env` plus a safe baseline are passed through. This reduces accidental secret leakage.

### Config-level exposure control

The new filtering support is also a security control:
- disable dangerous tools you do not want the model to see
- expose only a minimal whitelist for a sensitive server
- disable resource/prompt wrappers when you do not want that surface exposed...

## Example use cases

### GitHub server with a minimal issue-management surface

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "***"
    tools:
      include: [list_issues, create_issue, update_issue]
      prompts: false
      resources: false
```

Use it like:

```text
Show me open issues labeled bug, then draft a new issue for the flaky MCP reconnection behavior.
```

### Stripe server with dangerous actions removed

```yaml
mcp_servers:
  stripe:
    url: "https://mcp.stripe.com"
    headers:
      Authoriza...

## Troubleshooting

### MCP server not connecting

Check:

```bash
# Verify MCP deps are installed (already included in standard install)
cd ~/.hermes/hermes-agent && uv pip install -e ".[mcp]"

node --version
npx --version
```

Then verify your config and restart Hermes.

### Tools not appearing

Possible causes:
- the server failed to connect
- discovery failed
- your filter config excluded the tools
- the utility capability does not exist on that server
- the server is disabled with `enabled: false`

If you are intentionally filtering, this is expected.

### Why didn't resource or prompt utilities appear?

Bec...

## MCP Sampling Support

MCP servers can request LLM inference from Hermes via the `sampling/createMessage` protocol. This allows an MCP server to ask Hermes to generate text on its behalf — useful for servers that need LLM capabilities but don't have their own model access.

Sampling is **enabled by default** for all MCP servers (when the MCP SDK supports it). Configure it per-server under the `sampling` key:

```yaml
mcp_servers:
  my_server:
    command: "my-mcp-server"
    sampling:
      enabled: true            # Enable sampling (default: true)
      model: "openai/gpt-4o"  # Override model for sampling requests...

## Running Hermes as an MCP server

In addition to connecting **to** MCP servers, Hermes can also **be** an MCP server. This lets other MCP-capable agents (Claude Code, Cursor, Codex, or any MCP client) use Hermes's messaging capabilities — list conversations, read message history, and send messa

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
