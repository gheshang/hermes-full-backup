---
title: Automated GitHub PR Comments with Webhooks
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-webhook-github-pr-review.md]
---

# Automated GitHub PR Comments with Webhooks

源文档：[Automated GitHub PR Comments with Webhooks](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/webhook-github-pr-review.md)

# Automated GitHub PR Comments with Webhooks

This guide walks you through connecting Hermes Agent to GitHub so it automatically fetches a pull request's diff, analyzes the code changes, and posts a comment — triggered by a webhook event with no manual prompting.

When a PR is opened or updated, GitHub sends a webhook POST to your Hermes instance. Hermes runs the agent with a prompt that instructs it to retrieve the diff via the `gh` CLI, and the response is posted back to the PR thread.

:::tip Want a simpler setup without a public endpoint?
If you don't have a public URL or just want to get started quickly, check out [Build a GitHub PR Review Agent](./github-pr-review-agent.md) — uses cron jobs to poll for PRs on a schedule, works behind NAT and firewalls.
:::

:::info Reference docs
For

## Prerequisites

- Hermes Agent installed and running (`hermes gateway`)
- [`gh` CLI](https://cli.github.com/) installed and authenticated on the gateway host (`gh auth login`)
- A publicly reachable URL for your Hermes instance (see [Local testing with ngrok](#local-testing-with-ngrok) if running locally)
- Admin access to the GitHub repository (required to manage webhooks)

---...

## Step 1 — Enable the webhook platform

Add the following to your `~/.hermes/config.yaml`:

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      port: 8644          # default; change if another service occupies this port
      rate_limit: 30      # max requests per minute per route (not a global cap)

      routes:
        github-pr-review:
          secret: "your-webhook-secret-here"   # must match the GitHub webhook secret exactly
          events:
            - pull_request

          # The agent is instructed to fetch the actual diff before reviewing.
          # {number} and {repository.full_name} are resolved from ...

## Step 2 — Start the gateway

```bash
hermes gateway
```

You should see:

```
[webhook] Listening on 0.0.0.0:8644 — routes: github-pr-review
```

Verify it's running:

```bash
curl http://localhost:8644/health
# {"status": "ok", "platform": "webhook"}
```

---...

## Step 3 — Register the webhook on GitHub

1. Go to your repository → **Settings** → **Webhooks** → **Add webhook**
2. Fill in:
   - **Payload URL:** `https://your-public-url.example.com/webhooks/github-pr-review`
   - **Content type:** `application/json`
   - **Secret:** the same value you set for `secret` in the route config
   - **Which events?** → Select individual events → check **Pull requests**
3. Click **Add webhook**

GitHub will immediately send a `ping` event to confirm the connection. It is safely ignored — `ping` is not in your `events` list — and returns `{"status": "ignored", "event": "ping"}`. It is only logged at DEBUG...

## Step 4 — Open a test PR

Create a branch, push a change, and open a PR. Within 30–90 seconds (depending on PR size and model), Hermes should post a review comment.

To follow the agent's progress in real time:

```bash
tail -f "${HERMES_HOME:-$HOME/.hermes}/logs/gateway.log"
```

---...

## Local testing with ngrok

If Hermes is running on your laptop, use [ngrok](https://ngrok.com/) to expose it:

```bash
ngrok http 8644
```

Copy the `https://...ngrok-free.app` URL and use it as your GitHub Payload URL. On the free ngrok tier the URL changes each time ngrok restarts — update your GitHub webhook each session. Paid ngrok accounts get a static domain.

You can smoke-test a static route directly with `curl` — no GitHub account or real PR needed.

:::tip Use `deliver: log` when testing locally
Change `deliver: github_comment` to `deliver: log` in your config while testing. Otherwise the agent will attempt to...

## Filtering to specific actions

GitHub sends `pull_request` events for many actions: `opened`, `synchronize`, `reopened`, `closed`, `labeled`, etc. The `events` list filters only by the `X-GitHub-Event` header value — it cannot filter by action sub-type at the routing level.

The prompt in Step 1 already handles this by instructing the agent to stop early for `closed` and `labeled` events.

:::warning The agent still runs and consumes tokens
The "stop here" instruction prevents a meaningful review, but the agent still runs to completion for every `pull_request` event regardless of action. GitHub webhooks can only filter by e...

## Using a skill for consistent review style

Load a [Hermes skill](/docs/user-guide/features/skills) to give the agent a consistent review persona. Add `skills` to your route inside `platforms.webhook.extra.routes` in `config.yaml`:

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      routes:
        github-pr-review:
          secret: "your-webhook-secret-here"
          events: [pull_request]
          prompt: |
            A pull request event was received (action: {action}).
            PR #{number}: {pull_request.title} by {pull_request.user.login}
            URL: {pull_request.html_url}

            If the action is "...

## Sending responses to Slack or Discord instead

Replace the `deliver` and `deliver_extra` fields inside your route with your target platform:

```yaml
# Inside platforms.webhook.extra.routes.<route-name>:

# Slack
deliver: slack
deliver_extra:
  chat_id: "C0123456789"   # Slack channel ID (omit to use the configured home channel)

# Discord
deliver: discord
deliver_extra:
  chat_id: "987654321012345678"  # Discord channel ID (omit to use home channel)
```

The target platform must also be enabled and connected in the gateway. If `chat_id` is omitted, the response is sent to that platform's configured home channel.

Valid `deliver` values: `...

## GitLab support

The same adapter works with GitLab. GitLab uses `X-Gitlab-Token` for authentication (plain string match, not HMAC) — Hermes handles both automatically.

For event filtering, GitLab sets `X-GitLab-Event` to values like `Merge Request Hook`, `Push Hook`, `Pipeline Hook`. Use the exact header value in `events`:

```yaml
events:
  - Merge Request Hook
```

GitLab payload fields differ from GitHub's — e.g. `{object_attributes.title}` for the MR title and `{object_attributes.iid}` for the MR number. The easiest way to discover the full payload structure is GitLab's **Test** button in your webhook se...

## Security notes

- **Never use `INSECURE_NO_AUTH`** in production — it disables signature validation entirely. It is only for local development.
- **Rotate your webhook secret** periodically and update it in both GitHub (webhook settings) and your `config.yaml`.
- **Rate limiting** is 30 req/min per route by default (configurable via `extra.rate_limit`). Exceeding it returns `429`.
- **Duplicate deliveries** (webhook retries) are deduplicated via a 1-hour idempotency cache. The cache key is `X-GitHub-Delivery` if present, then `X-Request-ID`, then a millisecond timestamp. When neither delivery ID header is set...

## Troubleshooting

| Symptom | Check |
|---|---|
| `401 Invalid signature` | Secret in config.yaml doesn't match GitHub webhook secret |
| `404 Unknown route` | Route name in the URL doesn't match the key in `routes:` |
| `429 Rate limit exceeded` | 30 req/min per route exceeded — common when re-delivering test events from GitHub's UI; wait a minute or raise `extra.rate_limit` |
| No comment posted | `gh` not installed, not on PATH, or not authenticated (`gh auth login`) |
| Agent runs but no comment | Check the gateway log — if the agent output was empty or just "SKIP", delivery is still attempted |
| Port alre...

## Full config reference

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      host: "0.0.0.0"         # bind address (default: 0.0.0.0)
      port: 8644               # listen port (default: 8644)
      secret: ""               # optional global fallback secret
      rate_limit: 30           # requests per minute per route
      max_body_bytes: 1048576  # payload size limit in bytes (default: 1 MB)

      routes:
        <route-name>:
          secret: "required-per-route"
          eve

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
