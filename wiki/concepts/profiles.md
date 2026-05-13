---
title: Profiles: Running Multiple Agents
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/profiles.md]
---

# Profiles: Running Multiple Agents

源文档：[Profiles: Running Multiple Agents](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/profiles.md)

# Profiles: Running Multiple Agents

Run multiple independent Hermes agents on the same machine — each with its own config, API keys, memory, sessions, skills, and gateway state.

## What are profiles?

A profile is a separate Hermes home directory. Each profile gets its own directory containing its own `config.yaml`, `.env`, `SOUL.md`, memories, sessions, skills, cron jobs, and state database. Profiles let you run separate agents for different purposes — a coding assistant, a personal bot, a research agent — without mixing up Hermes state.

When you create a profile, it automatically becomes its own command. Create a profile called `coder` and you immediately have `coder chat`, `coder setup`, `coder gateway start`, etc....

## Quick start

```bash
hermes profile create coder       # creates profile + "coder" command alias
coder setup                       # configure API keys and model
coder chat                        # start chatting
```

That's it. `coder` is now its own Hermes profile with its own config, memory, and state....

## Creating a profile

### Blank profile

```bash
hermes profile create mybot
```

Creates a fresh profile with bundled skills seeded. Run `mybot setup` to configure API keys, model, and gateway tokens.

### Clone config only (`--clone`)

```bash
hermes profile create work --clone
```

Copies your current profile's `config.yaml`, `.env`, and `SOUL.md` into the new profile. Same API keys and model, but fresh sessions and memory. Edit `~/.hermes/profiles/work/.env` for different API keys, or `~/.hermes/profiles/work/SOUL.md` for a different personality.

### Clone everything (`--clone-all`)

```bash
hermes profile cre...

## Using profiles

### Command aliases

Every profile automatically gets a command alias at `~/.local/bin/<name>`:

```bash
coder chat                    # chat with the coder agent
coder setup                   # configure coder's settings
coder gateway start           # start coder's gateway
coder doctor                  # check coder's health
coder skills list             # list coder's skills
coder config set model.model anthropic/claude-sonnet-4
```

The alias works with every hermes subcommand — it's just `hermes -p <name>` under the hood.

### The `-p` flag

You can also target a profile explicitly with a...

## Profiles vs workspaces vs sandboxing

Profiles are often confused with workspaces or sandboxes, but they are different things:

- A **profile** gives Hermes its own state directory: `config.yaml`, `.env`, `SOUL.md`, sessions, memory, logs, cron jobs, and gateway state.
- A **workspace** or **working directory** is where terminal commands start. That is controlled separately by `terminal.cwd`.
- A **sandbox** is what limits filesystem access. Profiles do **not** sandbox the agent.

On the default `local` terminal backend, the agent still has the same filesystem access as your user account. A profile does not stop it from accessing ...

## Running gateways

Each profile runs its own gateway as a separate process with its own bot token:

```bash
coder gateway start           # starts coder's gateway
assistant gateway start       # starts assistant's gateway (separate process)
```

### Different bot tokens

Each profile has its own `.env` file. Configure a different Telegram/Discord/Slack bot token in each:

```bash
# Edit coder's tokens
nano ~/.hermes/profiles/coder/.env

# Edit assistant's tokens
nano ~/.hermes/profiles/assistant/.env
```

### Safety: token locks

If two profiles accidentally use the same bot token, the second gateway will be blo...

## Configuring profiles

Each profile has its own:

- **`config.yaml`** — model, provider, toolsets, all settings
- **`.env`** — API keys, bot tokens
- **`SOUL.md`** — personality and instructions

```bash
coder config set model.model anthropic/claude-sonnet-4
echo "You are a focused coding assistant." > ~/.hermes/profiles/coder/SOUL.md
```

If you want this profile to work in a specific project by default, also set its own `terminal.cwd`:

```bash
coder config set terminal.cwd /absolute/path/to/project
```...

## Updating

`hermes update` pulls code once (shared) and syncs new bundled skills to **all** profiles automatically:

```bash
hermes update
# → Code updated (12 commits)
# → Skills synced: default (up to date), coder (+2 new), assistant (+2 new)
```

User-modified skills are never overwritten....

## Managing profiles

```bash
hermes profile list           # show all profiles with status
hermes profile show coder     # detailed info for one profile
hermes profile rename coder dev-bot   # rename (updates alias + service)
hermes profile export coder   # export to coder.tar.gz
hermes profile import coder.tar.gz   # import from archive
```...

## Deleting a profile

```bash
hermes profile delete coder
```

This stops the gateway, removes the systemd/launchd service, removes the command alias, and deletes all profile data. You'll be asked to type the profile name to confirm.

Use `--yes` to skip confirmation: `hermes profile delete coder --yes`

:::note
You cannot delete the default profile (`~/.hermes`). To remove everything, use `hermes uninstall`.
:::...

## Tab completion

```bash
# Bash
eval "$(hermes completion bash)"

# Zsh
eval "$(hermes completion zsh)"
```

Add the line to your `~/.bashrc` or `~/.zshrc` for persistent completion. Completes profile names after `-p`, profile subcommands, and top-level commands....

## How it works

Profiles use the `HERMES_HOME` environment variable. When you run `coder chat`, the wrapper script sets `HERMES_HOME=~/.hermes/profiles/coder` before launching hermes. Since 119+ files in the codebase resolve paths via `get_hermes_home()`, Hermes state automatically scopes to the profile's directory — config, sessions, memory, skills, state database, gateway PID, logs, and cron jobs.

This is separate from terminal working directory. Tool execution starts from `terminal.cwd` (or the launch directory when `cwd: "."` on the local backend), not automatically from `HERMES_HOME`.

The default profi...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
