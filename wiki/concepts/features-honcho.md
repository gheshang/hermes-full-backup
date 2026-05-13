---
title: Honcho Memory
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-honcho.md]
---

# Honcho Memory

源文档：[Honcho Memory](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/honcho.md)

# Honcho Memory

[Honcho](https://github.com/plastic-labs/honcho) is an AI-native memory backend that adds dialectic reasoning and deep user modeling on top of Hermes's built-in memory system. Instead of simple key-value storage, Honcho maintains a running model of who the user is — their preferences, communication style, goals, and patterns — by reasoning about conversations after they happen.

:::info Honcho is a Memory Provider Plugin
Honcho is integrated into the [Memory Providers](./memory-providers.md) system. All features below are available through the unified memory provider interface.
:::

## What Honcho Adds

| Capability | Built-in Memory | Honcho |
|-----------|----------------|--------|
| Cross-session persistence | ✔ File-based MEMORY.md/USER.md | ✔ Server-side with API |
| User profile | ✔ Manual agent curation | ✔ Automatic dialectic reasoning |
| Session summary | — | ✔ Session-scoped context injection |
| Multi-agent isolation | — | ✔ Per-peer profile separation |
| Observation modes | — | ✔ Unified or directional observation |
| Conclusions (derived insights) | — | ✔ Server-side reasoning about patterns |
| Search across history | ✔ FTS5 session search | ✔ Semantic search over conclusions ...

## Setup

```bash
hermes memory setup    # select "honcho" from the provider list
```

Or configure manually:

```yaml
# ~/.hermes/config.yaml
memory:
  provider: honcho
```

```bash
echo "HONCHO_API_KEY=*** >> ~/.hermes/.env
```

Get an API key at [honcho.dev](https://honcho.dev)....

## Architecture

### Two-Layer Context Injection

Every turn (in `hybrid` or `context` mode), Honcho assembles two layers of context injected into the system prompt:

1. **Base context** — session summary, user representation, user peer card, AI self-representation, and AI identity card. Refreshed on `contextCadence`. This is the "who is this user" layer.
2. **Dialectic supplement** — LLM-synthesized reasoning about the user's current state and needs. Refreshed on `dialecticCadence`. This is the "what matters right now" layer.

Both layers are concatenated and truncated to the `contextTokens` budget (if set).
...

## Configuration Options

Honcho is configured in `~/.honcho/config.json` (global) or `$HERMES_HOME/honcho.json` (profile-local). The setup wizard handles this for you.

### Full Config Reference

| Key | Default | Description |
|-----|---------|-------------|
| `contextTokens` | `null` (uncapped) | Token budget for auto-injected context per turn. Set to an integer (e.g. 1200) to cap. Truncates at word boundaries |
| `contextCadence` | `1` | Minimum turns between `context()` API calls (base layer refresh) |
| `dialecticCadence` | `2` | Minimum turns between `peer.chat()` LLM calls (dialectic layer). Recommended 1–5. In...

## Observation (Directional vs. Unified)

Honcho models a conversation as peers exchanging messages. Each peer has two observation toggles that map 1:1 to Honcho's `SessionPeerConfig`:

| Toggle | Effect |
|--------|--------|
| `observeMe` | Honcho builds a representation of this peer from its own messages |
| `observeOthers` | This peer observes the other peer's messages (feeds cross-peer reasoning) |

Two peers × two toggles = four flags. `observationMode` is a shorthand preset:

| Preset | User flags | AI flags | Semantics |
|--------|-----------|----------|-----------|
| `"directional"` (default) | me: on, others: on | me: on, oth...

## Tools

When Honcho is active as the memory provider, five tools become available:

| Tool | Purpose |
|------|---------|
| `honcho_profile` | Read or update peer card — pass `card` (list of facts) to update, omit to read |
| `honcho_search` | Semantic search over context — raw excerpts, no LLM synthesis |
| `honcho_context` | Full session context — summary, representation, card, recent messages |
| `honcho_reasoning` | Synthesized answer from Honcho's LLM — pass `reasoning_level` (minimal/low/medium/high/max) to control depth |
| `honcho_conclude` | Create or delete conclusions — pass `conclusion` to...

## CLI Commands

```bash
hermes honcho status          # Connection status, config, and key settings
hermes honcho setup           # Interactive setup wizard
hermes honcho strategy        # Show or set session strategy
hermes honcho peer            # Update peer names for multi-agent setups
hermes honcho mode            # Show or set recall mode
hermes honcho tokens          # Show or set context token budget
hermes honcho identity        # Show Honcho peer identity
hermes honcho sync            # Sync host blocks for all profiles
hermes honcho enable          # Enable Honcho
hermes honcho disable         # Di...

## Migrating from `hermes honcho`

If you previously used the standalone `hermes honcho setup`:

1. Your existing configuration (`honcho.json` or `~/.honcho/config.json`) is preserved
2. Your server-side data (memories, conclusions, user profiles) is intact
3. Set `memory.provider: honcho` in config.yaml to reactivate

No re-login or re-setup needed. Run `hermes memory setup` and select "honcho" — the wizard detects your existing config....

## Full Documentation

See [Memory Providers — Honcho](./memory-providers.md#honcho) for the complete reference....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
