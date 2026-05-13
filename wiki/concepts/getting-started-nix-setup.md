---
title: Nix & NixOS Setup
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/getting-started-nix-setup.md]
---

# Nix & NixOS Setup

源文档：[Nix & NixOS Setup](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/nix-setup.md)

# Nix & NixOS Setup

Hermes Agent ships a Nix flake with three levels of integration:

| Level | Who it's for | What you get |
|-------|-------------|--------------|
| **`nix run` / `nix profile install`** | Any Nix user (macOS, Linux) | Pre-built binary with all deps — then use the standard CLI workflow |
| **NixOS module (native)** | NixOS server deployments | Declarative config, hardened systemd service, managed secrets |
| **NixOS module (container)** | Agents that need self-modification | Everything above, plus a persistent Ubuntu container where the agent can `apt`/`pip`/`npm install` |

:::info What's different from the standard install
The `curl | bash` installer manages Python, Node, and dependencies itself. The Nix flake replaces all of that — every Python dependency is a Nix der

## Prerequisites

- **Nix with flakes enabled** — [Determinate Nix](https://install.determinate.systems) recommended (enables flakes by default)
- **API keys** for the services you want to use (at minimum: an OpenRouter or Anthropic key)

---...

## Quick Start (Any Nix User)

No clone needed. Nix fetches, builds, and runs everything:

```bash
# Run directly (builds on first use, cached after)
nix run github:NousResearch/hermes-agent -- setup
nix run github:NousResearch/hermes-agent -- chat

# Or install persistently
nix profile install github:NousResearch/hermes-agent
hermes setup
hermes chat
```

After `nix profile install`, `hermes`, `hermes-agent`, and `hermes-acp` are on your PATH. From here, the workflow is identical to the [standard installation](./installation.md) — `hermes setup` walks you through provider selection, `hermes gateway install` sets up a launc...

## NixOS Module

The flake exports `nixosModules.default` — a full NixOS service module that declaratively manages user creation, directories, config generation, secrets, documents, and service lifecycle.

:::note
This module requires NixOS. For non-NixOS systems (macOS, other Linux distros), use `nix profile install` and the standard CLI workflow above.
:::

### Add the Flake Input

```nix
# /etc/nixos/flake.nix (or your system flake)
{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    hermes-agent.url = "github:NousResearch/hermes-agent";
  };

  outputs = { nixpkgs, hermes-agent, ......

## Configuration

### Declarative Settings

The `settings` option accepts an arbitrary attrset that is rendered as `config.yaml`. It supports deep merging across multiple module definitions (via `lib.recursiveUpdate`), so you can split config across files:

```nix
# base.nix
services.hermes-agent.settings = {
  model.default = "anthropic/claude-sonnet-4";
  toolsets = [ "all" ];
  terminal = { backend = "local"; timeout = 180; };
};

# personality.nix
services.hermes-agent.settings = {
  display = { compact = false; personality = "kawaii"; };
  memory = { memory_enabled = true; user_profile_enabled = true; };
}...

## Secrets Management

:::danger Never put API keys in `settings` or `environment`
Values in Nix expressions end up in `/nix/store`, which is world-readable. Always use `environmentFiles` with a secrets manager.
:::

Both `environment` (non-secret vars) and `environmentFiles` (secret files) are merged into `$HERMES_HOME/.env` at activation time (`nixos-rebuild switch`). Hermes reads this file on every startup, so changes take effect with a `systemctl restart hermes-agent` — no container recreation needed.

### sops-nix

```nix
{
  sops = {
    defaultSopsFile = ./secrets/hermes.yaml;
    age.keyFile = "/home/user/.c...

## Documents

The `documents` option installs files into the agent's working directory (the `workingDirectory`, which the agent reads as its workspace). Hermes looks for specific filenames by convention:

- **`USER.md`** — context about the user the agent is interacting with.
- Any other files you place here are visible to the agent as workspace files.

The agent identity file is separate: Hermes loads its primary `SOUL.md` from `$HERMES_HOME/SOUL.md`, which in the NixOS module is `${services.hermes-agent.stateDir}/.hermes/SOUL.md`. Putting `SOUL.md` in `documents` only creates a workspace file and will not...

## MCP Servers

The `mcpServers` option declaratively configures [MCP (Model Context Protocol)](https://modelcontextprotocol.io) servers. Each server uses either **stdio** (local command) or **HTTP** (remote URL) transport.

### Stdio Transport (Local Servers)

```nix
{
  services.hermes-agent.mcpServers = {
    filesystem = {
      command = "npx";
      args = [ "-y" "@modelcontextprotocol/server-filesystem" "/data/workspace" ];
    };
    github = {
      command = "npx";
      args = [ "-y" "@modelcontextprotocol/server-github" ];
      env.GITHUB_PERSONAL_ACCESS_TOKEN = "\${GITHUB_TOKEN}"; # resolved fro...

## Managed Mode

When hermes runs via the NixOS module, the following CLI commands are **blocked** with a descriptive error pointing you to `configuration.nix`:

| Blocked command | Why |
|---|---|
| `hermes setup` | Config is declarative — edit `settings` in your Nix config |
| `hermes config edit` | Config is generated from `settings` |
| `hermes config set <key> <value>` | Config is generated from `settings` |
| `hermes gateway install` | The systemd service is managed by NixOS |
| `hermes gateway uninstall` | The systemd service is managed by NixOS |

This prevents drift between what Nix declares and what'...

## Container Architecture

:::info
This section is only relevant if you're using `container.enable = true`. Skip it for native mode deployments.
:::

When container mode is enabled, hermes runs inside a persistent Ubuntu container with the Nix-built binary bind-mounted read-only from the host:

```
Host                                    Container
────                                    ─────────
/nix/store/...-hermes-agent-0.1.0  ──►  /nix/store/... (ro)
~/.hermes -> /var/lib/hermes/.hermes       (symlink bridge, per hostUsers)
/var/lib/hermes/                    ──►  /data/          (rw)
  ├── current-package -> /nix/...

## Development

### Dev Shell

The flake provides a development shell with Python 3.11, uv, Node.js, and all runtime tools:

```bash
cd hermes-agent
nix develop

# Shell provides:
#   - Python 3.11 + uv (deps installed into .venv on first entry)
#   - Node.js 20, ripgrep, git, openssh, ffmpeg on PATH
#   - Stamp-file optimization: re-entry is near-instant if deps haven't changed

hermes setup
hermes chat
```

### direnv (Recommended)

The included `.envrc` activates the dev shell automatically:

```bash
cd hermes-agent
direnv allow    # one-time
# Subsequent entries are near-instant (stamp file skips dep inst...

## Options Reference

### Core

| Option | Type | Default | Description |
|---|---|---|---|
| `enable` | `bool` | `false` | Enable the hermes-agent service |
| `package` | `package` | `hermes-agent` | The hermes-agent package to use |
| `user` | `str` | `"hermes"` | System user |
| `group` | `str` | `"hermes"` | System group |
| `createUser` | `bool` | `true` | Auto-create user/group |
| `stateDir` | `str` | `"/var/lib/hermes"` | State directory (`HERMES_HOME` parent) |
| `workingDirectory` | `str` | `"${stateDir}/workspace"` | Agent working directory (`MESSAGING_CWD`) |
| `addToSystemPackages` | `bool` | `false` |...

## Directory Layout

### Native Mode

```
/var/lib/hermes/                     # stateDir (owned by hermes:hermes, 0750)
├── .hermes/                         # HERMES_HOME
│   ├── config.yaml                  # Nix-generated (deep-merged each rebuild)
│   ├── .managed                     # Marker: CLI config mutation blocked
│   ├── .env                         # Merged from environment + environmentFiles
│   ├── auth.json                    # OAuth credentials (seeded, then self-managed)
│   ├── gateway.pid
│   ├── state.db
│   ├── mcp-tokens/                  # OAuth tokens for MCP servers
│   ├── sessions/
│   ...

## Updating

```bash
# Update the flake input
nix flake update hermes-agen

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
