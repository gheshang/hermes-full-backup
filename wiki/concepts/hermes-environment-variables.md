---
title: Hermes Environment Variables
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: [hermes, env, reference, config]
sources: [raw/articles/hermes-environment-variables.md]
---

# Hermes Environment Variables

源文档：[Hermes Environment Variables](https://hermes-agent.nousresearch.com/docs/reference/environment-variables)

# Environment Variables Reference

All variables go in `~/.hermes/.env`. You can also set them with `hermes config set VAR value`.

## LLM Providers

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | OpenRouter API key (recommended for flexibility) |
| `OPENROUTER_BASE_URL` | Override the OpenRouter-compatible base URL |
| `NOUS_BASE_URL` | Override Nous Portal base URL (rarely needed; development/testing only) |
| `NOUS_INFERENCE_BASE_URL` | Override Nous inference endpoint directly |
| `AI_GATEWAY_API_KEY` | Vercel AI Gateway API key ([ai-gateway.vercel.sh](https://ai-gateway.vercel.sh)) |
| `AI_GATEWAY_BASE_URL` | Override AI Gateway base URL (default: `https://ai-gateway.vercel.sh/v1`) |
| `OPENAI_API_KEY` |...

## Provider Auth (OAuth)

For native Anthropic auth, Hermes prefers Claude Code's own credential files when they exist because those credentials can refresh automatically. Environment variables such as `ANTHROPIC_TOKEN` remain useful as manual overrides, but they are no longer the preferred path for Claude Pro/Max login.

| Variable | Description |
|----------|-------------|
| `HERMES_INFERENCE_PROVIDER` | Override provider selection: `auto`, `openrouter`, `nous`, `openai-codex`, `copilot`, `copilot-acp`, `anthropic`, `huggingface`, `zai`, `kimi-coding`, `kimi-coding-cn`, `minimax`, `minimax-cn`, `kilocode`, `xiaomi`, ...

## Tool APIs

| Variable | Description |
|----------|-------------|
| `PARALLEL_API_KEY` | AI-native web search ([parallel.ai](https://parallel.ai/)) |
| `FIRECRAWL_API_KEY` | Web scraping and cloud browser ([firecrawl.dev](https://firecrawl.dev/)) |
| `FIRECRAWL_API_URL` | Custom Firecrawl API endpoint for self-hosted instances (optional) |
| `TAVILY_API_KEY` | Tavily API key for AI-native web search, extract, and crawl ([app.tavily.com](https://app.tavily.com/home)) |
| `EXA_API_KEY` | Exa API key for AI-native web search and contents ([exa.ai](https://exa.ai/)) |
| `BROWSERBASE_API_KEY` | Browser automat...

## Terminal Backend

| Variable | Description |
|----------|-------------|
| `TERMINAL_ENV` | Backend: `local`, `docker`, `ssh`, `singularity`, `modal`, `daytona` |
| `TERMINAL_DOCKER_IMAGE` | Docker image (default: `nikolaik/python-nodejs:python3.11-nodejs20`) |
| `TERMINAL_DOCKER_FORWARD_ENV` | JSON array of env var names to explicitly forward into Docker terminal sessions. Note: skill-declared `required_environment_variables` are forwarded automatically — you only need this for vars not declared by any skill. |
| `TERMINAL_DOCKER_VOLUMES` | Additional Docker volume mounts (comma-separated `host:container` pairs...

## SSH Backend

| Variable | Description |
|----------|-------------|
| `TERMINAL_SSH_HOST` | Remote server hostname |
| `TERMINAL_SSH_USER` | SSH username |
| `TERMINAL_SSH_PORT` | SSH port (default: 22) |
| `TERMINAL_SSH_KEY` | Path to private key |
| `TERMINAL_SSH_PERSISTENT` | Override persistent shell for SSH (default: follows `TERMINAL_PERSISTENT_SHELL`) |...

## Container Resources (Docker, Singularity, Modal, Daytona)

| Variable | Description |
|----------|-------------|
| `TERMINAL_CONTAINER_CPU` | CPU cores (default: 1) |
| `TERMINAL_CONTAINER_MEMORY` | Memory in MB (default: 5120) |
| `TERMINAL_CONTAINER_DISK` | Disk in MB (default: 51200) |
| `TERMINAL_CONTAINER_PERSISTENT` | Persist container filesystem across sessions (default: `true`) |
| `TERMINAL_SANDBOX_DIR` | Host directory for workspaces and overlays (default: `~/.hermes/sandboxes/`) |...

## Persistent Shell

| Variable | Description |
|----------|-------------|
| `TERMINAL_PERSISTENT_SHELL` | Enable persistent shell for non-local backends (default: `true`). Also settable via `terminal.persistent_shell` in config.yaml |
| `TERMINAL_LOCAL_PERSISTENT` | Enable persistent shell for local backend (default: `false`) |
| `TERMINAL_SSH_PERSISTENT` | Override persistent shell for SSH backend (default: follows `TERMINAL_PERSISTENT_SHELL`) |...

## Messaging

| Variable | Description |
|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token (from @BotFather) |
| `TELEGRAM_ALLOWED_USERS` | Comma-separated user IDs allowed to use the bot |
| `TELEGRAM_HOME_CHANNEL` | Default Telegram chat/channel for cron delivery |
| `TELEGRAM_HOME_CHANNEL_NAME` | Display name for the Telegram home channel |
| `TELEGRAM_WEBHOOK_URL` | Public HTTPS URL for webhook mode (enables webhook instead of polling) |
| `TELEGRAM_WEBHOOK_PORT` | Local listen port for webhook server (default: `8443`) |
| `TELEGRAM_WEBHOOK_SECRET` | Secret token for verifying updat...

## Agent Behavior

| Variable | Description |
|----------|-------------|
| `HERMES_MAX_ITERATIONS` | Max tool-calling iterations per conversation (default: 90) |
| `HERMES_TOOL_PROGRESS` | Deprecated compatibility variable for tool progress display. Prefer `display.tool_progress` in `config.yaml`. |
| `HERMES_TOOL_PROGRESS_MODE` | Deprecated compatibility variable for tool progress mode. Prefer `display.tool_progress` in `config.yaml`. |
| `HERMES_HUMAN_DELAY_MODE` | Response pacing: `off`/`natural`/`custom` |
| `HERMES_HUMAN_DELAY_MIN_MS` | Custom delay range minimum (ms) |
| `HERMES_HUMAN_DELAY_MAX_MS` | Custo...

## Interface

| Variable | Description |
|----------|-------------|
| `HERMES_TUI` | Launch the [TUI](../user-guide/tui.md) instead of the classic CLI when set to `1`. Equivalent to passing `--tui`. |
| `HERMES_TUI_DIR` | Path to a prebuilt `ui-tui/` directory (must contain `dist/entry.js` and populated `node_modules`). Used by distros and Nix to skip the first-launch `npm install`. |...

## Cron Scheduler

| Variable | Description |
|----------|-------------|
| `HERMES_CRON_TIMEOUT` | Inactivity timeout for cron job agent runs in seconds (default: `600`). The agent can run indefinitely while actively calling tools or receiving stream tokens — this only triggers when idle. Set to `0` for unlimited. |
| `HERMES_CRON_SCRIPT_TIMEOUT` | Timeout for pre-run scripts attached to cron jobs in seconds (default: `120`). Override for scripts that need longer execution (e.g., randomized delays for anti-bot timing). Also configurable via `cron.script_timeout_seconds` in `config.yaml`. |...

## Session Settings

| Variable | Description |
|----------|-------------|
| `SESSION_IDLE_MINUTES` | Reset sessions after N minutes of inactivity (default: 1440) |
| `SESSION_RESET_HOUR` | Daily reset hour in 24h format (default: 4 = 4am) |...

## Context Compression (config.yaml only)

Context compression is configured exclusively through `config.yaml` — there are no environment variables for it. Threshold settings live in the `compression:` block, while the summarization model/provider lives under `auxiliary.compression:`.

```yaml
compression:
  enabled: true
  threshold: 0.50
  target_ratio: 0.20         # fraction of threshold to preserve as recent tail
  protect_last_n: 20         # minimum recent messages to keep uncompressed
```

:::info Legacy migration
Older configs with `compression.summary_model`, `compression.summary_provider`, and `compression.summary_base_url` ...

## Auxiliary Task Overrides

| Variable | Description |
|----------|-------------|
| `AUXILIARY_VISION_PROVIDER` | Override provider for vision tasks |
| `AUXILIARY_VISION_MODEL` | Override model for vision tasks |
| `AUXILIARY_VISION_BASE_URL` | Direct OpenAI-compatible endpoint for vision tasks |
| `AUXILIARY_VISION_API_KEY` | API key paired with `AUXILIARY_VISION_BASE_URL` |
| `AUXILIARY_WEB_EXTRACT_PROVIDER` | Override provider for web extraction/summarization |
| `AUXILIARY_WEB_EXTRACT_MODEL` | Override model for web extraction/summarization |
| `AUXILIARY_WEB_EXTRACT_BASE_URL` | Direct OpenAI-compatible endpoint for...

## Fallback Model (config.yaml only)

The primary model fallback is configured exclusively through `config.yaml` — there are no environment variables for it. Add a `fallback_model` section with `provider` and `model` keys to enable automatic failover when your main model enco

> 完整内容见 raw 源文件

## 关联

- [[hermes-agent]] — 框架本体
- [[hermes-bundled-skills-catalog]] — 内置skill目录
- [[hermes-optional-skills-catalog]] — 可选skill目录
