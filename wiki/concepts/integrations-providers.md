---
title: AI Providers
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/integrations-providers.md]
---

# AI Providers

源文档：[AI Providers](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md)

# AI Providers

This page covers setting up inference providers for Hermes Agent — from cloud APIs like OpenRouter and Anthropic, to self-hosted endpoints like Ollama and vLLM, to advanced routing and fallback configurations. You need at least one provider configured to use Hermes.

## Inference Providers

You need at least one way to connect to an LLM. Use `hermes model` to switch providers and models interactively, or configure directly:

| Provider | Setup |
|----------|-------|
| **Nous Portal** | `hermes model` (OAuth, subscription-based) |
| **OpenAI Codex** | `hermes model` (ChatGPT OAuth, uses Codex models) |
| **GitHub Copilot** | `hermes model` (OAuth device code flow, `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, or `gh auth token`) |
| **GitHub Copilot ACP** | `hermes model` (spawns local `copilot --acp --stdio`) |
| **Anthropic** | `hermes model` (Claude Pro/Max via Claude Code auth, Anthropi...

## Custom & Self-Hosted LLM Providers

Hermes Agent works with **any OpenAI-compatible API endpoint**. If a server implements `/v1/chat/completions`, you can point Hermes at it. This means you can use local models, GPU inference servers, multi-provider routers, or any third-party API.

### General Setup

Three ways to configure a custom endpoint:

**Interactive setup (recommended):**
```bash
hermes model
# Select "Custom endpoint (self-hosted / VLLM / etc.)"
# Enter: API base URL, API key, Model name
```

**Manual config (`config.yaml`):**
```yaml
# In ~/.hermes/config.yaml
model:
  default: your-model-name
  provider: custom
  bas...

## Optional API Keys

| Feature | Provider | Env Variable |
|---------|----------|--------------|
| Web scraping | [Firecrawl](https://firecrawl.dev/) | `FIRECRAWL_API_KEY`, `FIRECRAWL_API_URL` |
| Browser automation | [Browserbase](https://browserbase.com/) | `BROWSERBASE_API_KEY`, `BROWSERBASE_PROJECT_ID` |
| Image generation | [FAL](https://fal.ai/) | `FAL_KEY` |
| Premium TTS voices | [ElevenLabs](https://elevenlabs.io/) | `ELEVENLABS_API_KEY` |
| OpenAI TTS + voice transcription | [OpenAI](https://platform.openai.com/api-keys) | `VOICE_TOOLS_OPENAI_KEY` |
| Mistral TTS + voice transcription | [Mistral](https:/...

## OpenRouter Provider Routing

When using OpenRouter, you can control how requests are routed across providers. Add a `provider_routing` section to `~/.hermes/config.yaml`:

```yaml
provider_routing:
  sort: "throughput"          # "price" (default), "throughput", or "latency"
  # only: ["anthropic"]      # Only use these providers
  # ignore: ["deepinfra"]    # Skip these providers
  # order: ["anthropic", "google"]  # Try providers in this order
  # require_parameters: true  # Only use providers that support all request params
  # data_collection: "deny"   # Exclude providers that may store/train on data
```

**Shortcuts:...

## Fallback Model

Configure a backup provider:model that Hermes switches to automatically when your primary model fails (rate limits, server errors, auth failures):

```yaml
fallback_model:
  provider: openrouter                    # required
  model: anthropic/claude-sonnet-4        # required
  # base_url: http://localhost:8000/v1    # optional, for custom endpoints
  # key_env: MY_CUSTOM_KEY               # optional, env var name for custom endpoint API key
```

When activated, the fallback swaps the model and provider mid-session without losing your conversation. It fires **at most once** per session.

Supp...

## See Also

- [Configuration](/docs/user-guide/configuration) — General configuration (directory structure, config precedence, terminal backends, memory, compression, and more)
- [Environment Variables](/docs/reference/environment-variables) — Complete reference of all environment variables...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
