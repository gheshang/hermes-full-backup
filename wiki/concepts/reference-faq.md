---
title: FAQ & Troubleshooting
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/reference-faq.md]
---

# FAQ & Troubleshooting

源文档：[FAQ & Troubleshooting](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/faq.md)

# FAQ & Troubleshooting

Quick answers and fixes for the most common questions and issues.

---

## Frequently Asked Questions

### What LLM providers work with Hermes?

Hermes Agent works with any OpenAI-compatible API. Supported providers include:

- **[OpenRouter](https://openrouter.ai/)** — access hundreds of models through one API key (recommended for flexibility)
- **Nous Portal** — Nous Research's own inference endpoint
- **OpenAI** — GPT-4o, o1, o3, etc.
- **Anthropic** — Claude models (via OpenRouter or compatible proxy)
- **Google** — Gemini models (via OpenRouter or compatible proxy)
- **z.ai / ZhipuAI** — GLM models
- **Kimi / Moonshot AI** — Kimi models
- **MiniMax** — global and China endpoints
- **Local ...

## Troubleshooting

### Installation Issues

#### `hermes: command not found` after installation

**Cause:** Your shell hasn't reloaded the updated PATH.

**Solution:**
```bash
# Reload your shell profile
source ~/.bashrc    # bash
source ~/.zshrc     # zsh

# Or start a new terminal session
```

If it still doesn't work, verify the install location:
```bash
which hermes
ls ~/.local/bin/hermes
```

:::tip
The installer adds `~/.local/bin` to your PATH. If you use a non-standard shell config, add `export PATH="$HOME/.local/bin:$PATH"` manually.
:::

#### Python version too old

**Cause:** Hermes requires Python 3....

## Profiles

### How do profiles differ from just setting HERMES_HOME?

Profiles are a managed layer on top of `HERMES_HOME`. You *could* manually set `HERMES_HOME=/some/path` before every command, but profiles handle all the plumbing for you: creating the directory structure, generating shell aliases (`hermes-work`), tracking the active profile in `~/.hermes/active_profile`, and syncing skill updates across all profiles automatically. They also integrate with tab completion so you don't have to remember paths.

### Can two profiles share the same bot token?

No. Each messaging platform (Telegram, Discord,...

## Workflows & Patterns

### Using different models for different tasks (multi-model workflows)

**Scenario:** You use GPT-5.4 as your daily driver, but Gemini or Grok writes better social media content. Manually switching models every time is tedious.

**Solution: Delegation config.** Hermes can route subagents to a different model automatically. Set this in `~/.hermes/config.yaml`:

```yaml
delegation:
  model: "google/gemini-3-flash-preview"   # subagents use this model
  provider: "openrouter"                    # provider for subagents
```

Now when you tell Hermes "write me a Twitter thread about X" and it spawn...

## Still Stuck?

If your issue isn't covered here:

1. **Search existing issues:** [GitHub Issues](https://github.com/NousResearch/hermes-agent/issues)
2. **Ask the community:** [Nous Research Discord](https://discord.gg/nousresearch)
3. **File a bug report:** Include your OS, Python version (`python3 --version`), Hermes version (`hermes --version`), and the full error message...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
