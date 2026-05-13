---
title: Memory Providers
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-memory-providers.md]
---

# Memory Providers

源文档：[Memory Providers](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/memory-providers.md)

# Memory Providers

Hermes Agent ships with 8 external memory provider plugins that give the agent persistent, cross-session knowledge beyond the built-in MEMORY.md and USER.md. Only **one** external provider can be active at a time — the built-in memory is always active alongside it.

## Quick Start

```bash
hermes memory setup      # interactive picker + configuration
hermes memory status     # check what's active
hermes memory off        # disable external provider
```

You can also select the active memory provider via `hermes plugins` → Provider Plugins → Memory Provider.

Or set manually in `~/.hermes/config.yaml`:

```yaml
memory:
  provider: openviking   # or honcho, mem0, hindsight, holographic, retaindb, byterover, supermemory
```...

## How It Works

When a memory provider is active, Hermes automatically:

1. **Injects provider context** into the system prompt (what the provider knows)
2. **Prefetches relevant memories** before each turn (background, non-blocking)
3. **Syncs conversation turns** to the provider after each response
4. **Extracts memories on session end** (for providers that support it)
5. **Mirrors built-in memory writes** to the external provider
6. **Adds provider-specific tools** so the agent can search, store, and manage memories

The built-in memory (MEMORY.md / USER.md) continues to work exactly as before. The externa...

## Available Providers

### Honcho

AI-native cross-session user modeling with dialectic reasoning, session-scoped context injection, semantic search, and persistent conclusions. Base context now includes the session summary alongside user representation and peer cards, giving the agent awareness of what has already been discussed.

| | |
|---|---|
| **Best for** | Multi-agent systems with cross-session context, user-agent alignment |
| **Requires** | `pip install honcho-ai` + [API key](https://app.honcho.dev) or self-hosted instance |
| **Data storage** | Honcho Cloud or self-hosted |
| **Cost** | Honcho pricing (cl...

## Provider Comparison

| Provider | Storage | Cost | Tools | Dependencies | Unique Feature |
|----------|---------|------|-------|-------------|----------------|
| **Honcho** | Cloud | Paid | 5 | `honcho-ai` | Dialectic user modeling + session-scoped context |
| **OpenViking** | Self-hosted | Free | 5 | `openviking` + server | Filesystem hierarchy + tiered loading |
| **Mem0** | Cloud | Paid | 3 | `mem0ai` | Server-side LLM extraction |
| **Hindsight** | Cloud/Local | Free/Paid | 3 | `hindsight-client` | Knowledge graph + reflect synthesis |
| **Holographic** | Local | Free | 2 | None | HRR algebra + trust scoring |...

## Profile Isolation

Each provider's data is isolated per [profile](/docs/user-guide/profiles):

- **Local storage providers** (Holographic, ByteRover) use `$HERMES_HOME/` paths which differ per profile
- **Config file providers** (Honcho, Mem0, Hindsight, Supermemory) store config in `$HERMES_HOME/` so each profile has its own credentials
- **Cloud providers** (RetainDB) auto-derive profile-scoped project names
- **Env var providers** (OpenViking) are configured via each profile's `.env` file...

## Building a Memory Provider

See the [Developer Guide: Memory Provider Plugins](/docs/developer-guide/memory-provider-plugin) for how to create your own....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
