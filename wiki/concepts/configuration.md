---
title: Configuration
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/configuration.md]
---

# Configuration

源文档：[Configuration](https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/configuration.md)

# Configuration

All settings are stored in the `~/.hermes/` directory for easy access.

## Directory Structure

```text
~/.hermes/
├── config.yaml     # Settings (model, terminal, TTS, compression, etc.)
├── .env            # API keys and secrets
├── auth.json       # OAuth provider credentials (Nous Portal, etc.)
├── SOUL.md         # Primary agent identity (slot #1 in system prompt)
├── memories/       # Persistent memory (MEMORY.md, USER.md)
├── skills/         # Agent-created skills (managed via skill_manage tool)
├── cron/           # Scheduled jobs
├── sessions/       # Gateway sessions
└── logs/           # Logs (errors.log, gateway.log — secrets auto-redacted)
```...

## Managing Configuration

```bash
hermes config              # View current configuration
hermes config edit         # Open config.yaml in your editor
hermes config set KEY VAL  # Set a specific value
hermes config check        # Check for missing options (after updates)
hermes config migrate      # Interactively add missing options

# Examples:
hermes config set model anthropic/claude-opus-4
hermes config set terminal.backend docker
hermes config set OPENROUTER_API_KEY sk-or-...  # Saves to .env
```

:::tip
The `hermes config set` command automatically routes values to the right file — API keys are saved to `.env`, ev...

## Configuration Precedence

Settings are resolved in this order (highest priority first):

1. **CLI arguments** — e.g., `hermes chat --model anthropic/claude-sonnet-4` (per-invocation override)
2. **`~/.hermes/config.yaml`** — the primary config file for all non-secret settings
3. **`~/.hermes/.env`** — fallback for env vars; **required** for secrets (API keys, tokens, passwords)
4. **Built-in defaults** — hardcoded safe defaults when nothing else is set

:::info Rule of Thumb
Secrets (API keys, bot tokens, passwords) go in `.env`. Everything else (model, terminal backend, compression settings, memory limits, toolsets) g...

## Environment Variable Substitution

You can reference environment variables in `config.yaml` using `${VAR_NAME}` syntax:

```yaml
auxiliary:
  vision:
    api_key: ${GOOGLE_API_KEY}
    base_url: ${CUSTOM_VISION_URL}

delegation:
  api_key: ${DELEGATION_KEY}
```

Multiple references in a single value work: `url: "${HOST}:${PORT}"`. If a referenced variable is not set, the placeholder is kept verbatim (`${UNDEFINED_VAR}` stays as-is). Only the `${VAR}` syntax is supported — bare `$VAR` is not expanded.

For AI provider setup (OpenRouter, Anthropic, Copilot, custom endpoints, self-hosted LLMs, fallback models, etc.), see [AI Provi...

## Terminal Backend Configuration

Hermes supports six terminal backends. Each determines where the agent's shell commands actually execute — your local machine, a Docker container, a remote server via SSH, a Modal cloud sandbox, a Daytona workspace, or a Singularity/Apptainer container.

```yaml
terminal:
  backend: local    # local | docker | ssh | modal | daytona | singularity
  cwd: "."          # Working directory ("." = current dir for local, "/root" for containers)
  timeout: 180      # Per-command timeout in seconds
  env_passthrough: []  # Env var names to forward to sandboxed execution (terminal + execute_code)
  sing...

## Skill Settings

Skills can declare their own configuration settings via their SKILL.md frontmatter. These are non-secret values (paths, preferences, domain settings) stored under the `skills.config` namespace in `config.yaml`.

```yaml
skills:
  config:
    myplugin:
      path: ~/myplugin-data   # Example — each skill defines its own keys
```

**How skill settings work:**

- `hermes config migrate` scans all enabled skills, finds unconfigured settings, and offers to prompt you
- `hermes config show` displays all skill settings under "Skill Settings" with the skill they belong to
- When a skill loads, its res...

## Memory Configuration

```yaml
memory:
  memory_enabled: true
  user_profile_enabled: true
  memory_char_limit: 2200   # ~800 tokens
  user_char_limit: 1375     # ~500 tokens
```...

## File Read Safety

Controls how much content a single `read_file` call can return. Reads that exceed the limit are rejected with an error telling the agent to use `offset` and `limit` for a smaller range. This prevents a single read of a minified JS bundle or large data file from flooding the context window.

```yaml
file_read_max_chars: 100000  # default — ~25-35K tokens
```

Raise it if you're on a model with a large context window and frequently read big files. Lower it for small-context models to keep reads efficient:

```yaml
# Large context model (200K+)
file_read_max_chars: 200000

# Small local model (16...

## Tool Output Truncation Limits

Three related caps control how much raw output a tool can return before Hermes truncates it:

```yaml
tool_output:
  max_bytes: 50000        # terminal output cap (chars)
  max_lines: 2000         # read_file pagination cap
  max_line_length: 2000   # per-line cap in read_file's line-numbered view
```

- **`max_bytes`** — When a `terminal` command produces more than this many characters of combined stdout/stderr, Hermes keeps the first 40% and last 60% and inserts a `[OUTPUT TRUNCATED]` notice between them. Default `50000` (≈12-15K tokens across typical tokenisers).
- **`max_lines`** — Upper b...

## Git Worktree Isolation

Enable isolated git worktrees for running multiple agents in parallel on the same repo:

```yaml
worktree: true    # Always create a worktree (same as hermes -w)
# worktree: false # Default — only when -w flag is passed
```

When enabled, each CLI session creates a fresh worktree under `.worktrees/` with its own branch. Agents can edit files, commit, push, and create PRs without interfering with each other. Clean worktrees are removed on exit; dirty ones are kept for manual recovery.

You can also list gitignored files to copy into worktrees via `.worktreeinclude` in your repo root:

```
# .wo...

## Context Compression

Hermes automatically compresses long conversations to stay within your model's context window. The compression summarizer is a separate LLM call — you can point it at any provider or endpoint.

All compression settings live in `config.yaml` (no environment variables).

### Full reference

```yaml
compression:
  enabled: true                                     # Toggle compression on/off
  threshold: 0.50                                   # Compress at this % of context limit
  target_ratio: 0.20                                # Fraction of threshold to preserve as recent tail
  protect_last_n...

## Context Engine

The context engine controls how conversations are managed when approaching the model's token limit. The built-in `compressor` engine uses lossy summarization (see [Context Compression](/docs/developer-guide/context-compression-and-caching)). Plugin engines can replace it with alternative strategies.

```yaml
context:
  engine: "compressor"    # default — built-in lossy summarization
```

To use a plugin engine (e.g., LCM for lossless context management):

```yaml
context:
  engine: "lcm"          # must match the plugin's name
```

Plugin engines are **never auto-activated** — you must explici...

## Iteration Budget Pressure

When the agent is working on a complex task with many tool calls, it can burn through its iteration budget (default: 90 turns) without realizing it's running low. Budget pressure automatically warns the model as it approaches the limit:

| Threshold | Level | What the model sees |
|-----------|-------|---------------------|
| **70%** | Caution | `[BUDGET: 63/90. 27 iterations left. Start consolidating.]` |
| **90%** | Warning | `[BUDGET WARNING: 81/90. Only 9 left. Respond NOW.]` |

Warnings are injected into the last tool result's JSON (as a `_budget_warning` field) rather than as separate me...

## Context Pressure Warnings

Separate from iteration budget pressure, context pressure tracks how close the conversation is to the **compaction threshold** — the point wh

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
