---
title: Fallback Providers
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-fallback-providers.md]
---

# Fallback Providers

源文档：[Fallback Providers](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/fallback-providers.md)

# Fallback Providers

Hermes Agent has three layers of resilience that keep your sessions running when providers hit issues:

1. **[Credential pools](./credential-pools.md)** — rotate across multiple API keys for the *same* provider (tried first)
2. **Primary model fallback** — automatically switches to a *different* provider:model when your main model fails
3. **Auxiliary task fallback** — independent provider resolution for side tasks like vision, compression, and web extraction

Credential pools handle same-provider rotation (e.g., multiple OpenRouter keys). This page covers cross-provider fallback. Both are optional and work independently.

## Primary Model Fallback

When your main LLM provider encounters errors — rate limits, server overload, auth failures, connection drops — Hermes can automatically switch to a backup provider:model pair mid-session without losing your conversation.

### Configuration

Add a `fallback_model` section to `~/.hermes/config.yaml`:

```yaml
fallback_model:
  provider: openrouter
  model: anthropic/claude-sonnet-4
```

Both `provider` and `model` are **required**. If either is missing, the fallback is disabled.

### Supported Providers

| Provider | Value | Requirements |
|----------|-------|-------------|
| AI Gateway | `ai-g...

## Auxiliary Task Fallback

Hermes uses separate lightweight models for side tasks. Each task has its own provider resolution chain that acts as a built-in fallback system.

### Tasks with Independent Provider Resolution

| Task | What It Does | Config Key |
|------|-------------|-----------|
| Vision | Image analysis, browser screenshots | `auxiliary.vision` |
| Web Extract | Web page summarization | `auxiliary.web_extract` |
| Compression | Context compression summaries | `auxiliary.compression` |
| Session Search | Past session summarization | `auxiliary.session_search` |
| Skills Hub | Skill search and discovery | `a...

## Context Compression Fallback

Context compression uses the `auxiliary.compression` config block to control which model and provider handles summarization:

```yaml
auxiliary:
  compression:
    provider: "auto"                              # auto | openrouter | nous | main
    model: "google/gemini-3-flash-preview"
```

:::info Legacy migration
Older configs with `compression.summary_model` / `compression.summary_provider` / `compression.summary_base_url` are automatically migrated to `auxiliary.compression.*` on first load (config version 17).
:::

If no provider is available for compression, Hermes drops middle conversat...

## Delegation Provider Override

Subagents spawned by `delegate_task` do **not** use the primary fallback model. However, they can be routed to a different provider:model pair for cost optimization:

```yaml
delegation:
  provider: "openrouter"                      # override provider for all subagents
  model: "google/gemini-3-flash-preview"      # override model
  # base_url: "http://localhost:1234/v1"      # or use a direct endpoint
  # api_key: "local-key"
```

See [Subagent Delegation](/docs/user-guide/features/delegation) for full configuration details.

---...

## Cron Job Providers

Cron jobs run with whatever provider is configured at execution time. They do not support a fallback model. To use a different provider for cron jobs, configure `provider` and `model` overrides on the cron job itself:

```python
cronjob(
    action="create",
    schedule="every 2h",
    prompt="Check server status",
    provider="openrouter",
    model="google/gemini-3-flash-preview"
)
```

See [Scheduled Tasks (Cron)](/docs/user-guide/features/cron) for full configuration details.

---...

## Summary

| Feature | Fallback Mechanism | Config Location |
|---------|-------------------|----------------|
| Main agent model | `fallback_model` in config.yaml — per-turn failover on errors (primary restored each turn) | `fallback_model:` (top-level) |
| Vision | Auto-detection chain + internal OpenRouter retry | `auxiliary.vision` |
| Web extraction | Auto-detection chain + internal OpenRouter retry | `auxiliary.web_extract` |
| Context compression | Auto-detection chain, degrades to no-summary if unavailable | `auxiliary.compression` |
| Session search | Auto-detection chain | `auxiliary.session_se...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
