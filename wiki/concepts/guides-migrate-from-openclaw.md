---
title: Migrate from OpenClaw
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-migrate-from-openclaw.md]
---

# Migrate from OpenClaw

源文档：[Migrate from OpenClaw](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/migrate-from-openclaw.md)

# Migrate from OpenClaw

`hermes claw migrate` imports your OpenClaw (or legacy Clawdbot/Moldbot) setup into Hermes. This guide covers exactly what gets migrated, the config key mappings, and what to verify after migration.

## Quick start

```bash
# Preview then migrate (always shows a preview first, then asks to confirm)
hermes claw migrate

# Preview only, no changes
hermes claw migrate --dry-run

# Full migration including API keys, skip confirmation
hermes claw migrate --preset full --yes
```

The migration always shows a full preview of what will be imported before making any changes. Review the list, then confirm to proceed.

Reads from `~/.openclaw/` by default. Legacy `~/.clawdbot/` or `~/.moltbot/` directories are detected automatically. Same for legacy config filenames (`clawdbot.json`, `moltbot.json`)....

## Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview only — stop after showing what would be migrated. |
| `--preset <name>` | `full` (default, includes secrets) or `user-data` (excludes API keys). |
| `--overwrite` | Overwrite existing Hermes files on conflicts (default: skip). |
| `--migrate-secrets` | Include API keys (on by default with `--preset full`). |
| `--source <path>` | Custom OpenClaw directory. |
| `--workspace-target <path>` | Where to place `AGENTS.md`. |
| `--skill-conflict <mode>` | `skip` (default), `overwrite`, or `rename`. |
| `--yes` | Skip the confir...

## What gets migrated

### Persona, memory, and instructions

| What | OpenClaw source | Hermes destination | Notes |
|------|----------------|-------------------|-------|
| Persona | `workspace/SOUL.md` | `~/.hermes/SOUL.md` | Direct copy |
| Workspace instructions | `workspace/AGENTS.md` | `AGENTS.md` in `--workspace-target` | Requires `--workspace-target` flag |
| Long-term memory | `workspace/MEMORY.md` | `~/.hermes/memories/MEMORY.md` | Parsed into entries, merged with existing, deduped. Uses `§` delimiter. |
| User profile | `workspace/USER.md` | `~/.hermes/memories/USER.md` | Same entry-merge logic as memory....

## API key resolution

When `--migrate-secrets` is enabled, API keys are collected from **four sources** in priority order:

1. **Config values** — `models.providers.*.apiKey` and TTS provider keys in `openclaw.json`
2. **Environment file** — `~/.openclaw/.env` (keys like `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, etc.)
3. **Config env sub-object** — `openclaw.json` → `"env"` or `"env"."vars"` (some setups store keys here instead of a separate `.env` file)
4. **Auth profiles** — `~/.openclaw/agents/main/agent/auth-profiles.json` (per-agent credentials)

Config values take priority. Each subsequent source fills any r...

## SecretRef handling

OpenClaw config values for tokens and API keys can be in three formats:

```json
// Plain string
"channels": { "telegram": { "botToken": "123456:ABC-DEF..." } }

// Environment template
"channels": { "telegram": { "botToken": "${TELEGRAM_BOT_TOKEN}" } }

// SecretRef object
"channels": { "telegram": { "botToken": { "source": "env", "id": "TELEGRAM_BOT_TOKEN" } } }
```

The migration resolves all three formats. For env templates and SecretRef objects with `source: "env"`, it looks up the value in `~/.openclaw/.env` and the `openclaw.json` env sub-object. SecretRef objects with `source: "file"` ...

## After migration

1. **Check the migration report** — printed on completion with counts of migrated, skipped, and conflicting items.

2. **Review archived files** — anything in `~/.hermes/migration/openclaw/<timestamp>/archive/` needs manual attention.

3. **Start a new session** — imported skills and memory entries take effect in new sessions, not the current one.

4. **Verify API keys** — run `hermes status` to check provider authentication.

5. **Test messaging** — if you migrated platform tokens, restart the gateway: `systemctl --user restart hermes-gateway`

6. **Check session policies** — verify `hermes c...

## Troubleshooting

### "OpenClaw directory not found"

The migration checks `~/.openclaw/`, then `~/.clawdbot/`, then `~/.moltbot/`. If your installation is elsewhere, use `--source /path/to/your/openclaw`.

### "No provider API keys found"

Keys might be stored in several places depending on your OpenClaw version: inline in `openclaw.json` under `models.providers.*.apiKey`, in `~/.openclaw/.env`, in the `openclaw.json` `"env"` sub-object, or in `agents/main/agent/auth-profiles.json`. The migration checks all four. If keys use `source: "file"` or `source: "exec"` SecretRefs, they can't be resolved automatically ...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
