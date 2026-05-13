---
title: API Server
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-api-server.md]
---

# API Server

源文档：[API Server](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/api-server.md)

# API Server

The API server exposes hermes-agent as an OpenAI-compatible HTTP endpoint. Any frontend that speaks the OpenAI format — Open WebUI, LobeChat, LibreChat, NextChat, ChatBox, and hundreds more — can connect to hermes-agent and use it as a backend.

Your agent handles requests with its full toolset (terminal, file operations, web search, memory, skills) and returns the final response. When streaming, tool progress indicators appear inline so frontends can show what the agent is doing.

## Quick Start

### 1. Enable the API server

Add to `~/.hermes/.env`:

```bash
API_SERVER_ENABLED=true
API_SERVER_KEY=change-me-local-dev
# Optional: only if a browser must call Hermes directly
# API_SERVER_CORS_ORIGINS=http://localhost:3000
```

### 2. Start the gateway

```bash
hermes gateway
```

You'll see:

```
[API Server] API server listening on http://127.0.0.1:8642
```

### 3. Connect a frontend

Point any OpenAI-compatible client at `http://localhost:8642/v1`:

```bash
# Test with curl
curl http://localhost:8642/v1/chat/completions \
  -H "Authorization: Bearer change-me-local-dev" \
  -H "Content-...

## Endpoints

### POST /v1/chat/completions

Standard OpenAI Chat Completions format. Stateless — the full conversation is included in each request via the `messages` array.

**Request:**
```json
{
  "model": "hermes-agent",
  "messages": [
    {"role": "system", "content": "You are a Python expert."},
    {"role": "user", "content": "Write a fibonacci function"}
  ],
  "stream": false
}
```

**Response:**
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1710000000,
  "model": "hermes-agent",
  "choices": [{
    "index": 0,
    "message": {"role": "assistant", "content": "Her...

## Runs API (streaming-friendly alternative)

In addition to `/v1/chat/completions` and `/v1/responses`, the server exposes a **runs** API for long-form sessions where the client wants to subscribe to progress events instead of managing streaming themselves.

### POST /v1/runs

Create a new agent run. Returns a `run_id` that can be used to subscribe to progress events.

### GET /v1/runs/\{run_id\}/events

Server-Sent Events stream of the run's tool-call progress, token deltas, and lifecycle events. Designed for dashboards and thick clients that want to attach/detach without losing state....

## Jobs API (background scheduled work)

The server exposes a lightweight jobs CRUD surface for managing scheduled / background agent runs from a remote client. All endpoints are gated behind the same bearer auth.

### GET /api/jobs

List all scheduled jobs.

### POST /api/jobs

Create a new scheduled job. Body accepts the same shape as `hermes cron` — prompt, schedule, skills, provider override, delivery target.

### GET /api/jobs/\{job_id\}

Fetch a single job's definition and last-run state.

### PATCH /api/jobs/\{job_id\}

Update fields on an existing job (prompt, schedule, etc.). Partial updates are merged.

### DELETE /api/jobs...

## System Prompt Handling

When a frontend sends a `system` message (Chat Completions) or `instructions` field (Responses API), hermes-agent **layers it on top** of its core system prompt. Your agent keeps all its tools, memory, and skills — the frontend's system prompt adds extra instructions.

This means you can customize behavior per-frontend without losing capabilities:
- Open WebUI system prompt: "You are a Python expert. Always include type hints."
- The agent still has terminal, file tools, web search, memory, etc....

## Authentication

Bearer token auth via the `Authorization` header:

```
Authorization: Bearer ***
```

Configure the key via `API_SERVER_KEY` env var. If you need a browser to call Hermes directly, also set `API_SERVER_CORS_ORIGINS` to an explicit allowlist.

:::warning Security
The API server gives full access to hermes-agent's toolset, **including terminal commands**. When binding to a non-loopback address like `0.0.0.0`, `API_SERVER_KEY` is **required**. Also keep `API_SERVER_CORS_ORIGINS` narrow to control browser access.

The default bind address (`127.0.0.1`) is for local-only use. Browser access is disa...

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `API_SERVER_ENABLED` | `false` | Enable the API server |
| `API_SERVER_PORT` | `8642` | HTTP server port |
| `API_SERVER_HOST` | `127.0.0.1` | Bind address (localhost only by default) |
| `API_SERVER_KEY` | _(none)_ | Bearer token for auth |
| `API_SERVER_CORS_ORIGINS` | _(none)_ | Comma-separated allowed browser origins |
| `API_SERVER_MODEL_NAME` | _(profile name)_ | Model name on `/v1/models`. Defaults to profile name, or `hermes-agent` for default profile. |

### config.yaml

```yaml
# No...

## Security Headers

All responses include security headers:
- `X-Content-Type-Options: nosniff` — prevents MIME type sniffing
- `Referrer-Policy: no-referrer` — prevents referrer leakage...

## CORS

The API server does **not** enable browser CORS by default.

For direct browser access, set an explicit allowlist:

```bash
API_SERVER_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

When CORS is enabled:
- **Preflight responses** include `Access-Control-Max-Age: 600` (10 minute cache)
- **SSE streaming responses** include CORS headers so browser EventSource clients work correctly
- **`Idempotency-Key`** is an allowed request header — clients can send it for deduplication (responses are cached by key for 5 minutes)

Most documented frontends such as Open WebUI connect server-to-s...

## Compatible Frontends

Any frontend that supports the OpenAI API format works. Tested/documented integrations:

| Frontend | Stars | Connection |
|----------|-------|------------|
| [Open WebUI](/docs/user-guide/messaging/open-webui) | 126k | Full guide available |
| LobeChat | 73k | Custom provider endpoint |
| LibreChat | 34k | Custom endpoint in librechat.yaml |
| AnythingLLM | 56k | Generic OpenAI provider |
| NextChat | 87k | BASE_URL env var |
| ChatBox | 39k | API Host setting |
| Jan | 26k | Remote model config |
| HF Chat-UI | 8k | OPENAI_BASE_URL |
| big-AGI | 7k | Custom endpoint |
| OpenAI Python SDK | —...

## Multi-User Setup with Profiles

To give multiple users their own isolated Hermes instance (separate config, memory, skills), use [profiles](/docs/user-guide/profiles):

```bash
# Create a profile per user
hermes profile create alice
hermes profile create bob

# Configure each profile's API server on a different port
hermes -p alice config set API_SERVER_ENABLED true
hermes -p alice config set API_SERVER_PORT 8643
hermes -p alice config set API_SERVER_KEY alice-secret

hermes -p bob config set API_SERVER_ENABLED true
hermes -p bob config set API_SERVER_PORT 8644
hermes -p bob config set API_SERVER_KEY bob-secret

# Start each...

## Limitations

- **Response storage** — stored responses (for `previous_response_id`) are persisted in SQLite and survive gateway restarts. Max 100 stored responses (LRU eviction).
- **No file upload** — inline images are supported on both `/v1/chat/completions` and `/v1/responses`, but uploaded files (`file`, `input_file`, `file_id`) and non-image document inputs are not supported through the API.
- **Model field is cosmetic** — the `model` field in requests is accepted but the actual LLM model used is configured server-side in config.yaml....

## Proxy Mode

The API server also serves as the backend for **gateway proxy mode**. When another Hermes gateway instance is configured with `GATEWAY_PROXY_URL` pointing at this API server, it forwards all messages here instead of running its own agent. This enables split deployments — for example, a Docker container handling Matrix E2EE that relays to a host-side agent.

See [Matrix Proxy Mode](/docs/user-guide/messaging/matrix#proxy-mode-e2ee-on-macos) for the full setup guide....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
