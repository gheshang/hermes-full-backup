---
title: Webhooks
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/messaging-webhooks.md]
---

# Webhooks

源文档：[Webhooks](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/webhooks.md)

# Webhooks

Receive events from external services (GitHub, GitLab, JIRA, Stripe, etc.) and trigger Hermes agent runs automatically. The webhook adapter runs an HTTP server that accepts POST requests, validates HMAC signatures, transforms payloads into agent prompts, and routes responses back to the source or to another configured platform.

The agent processes the event and can respond by posting comments on PRs, sending messages to Telegram/Discord, or logging the result.

---

## Quick Start

1. Enable via `hermes gateway setup` or environment variables
2. Define routes in `config.yaml` **or** create them dynamically with `hermes webhook subscribe`
3. Point your service at `http://your-server:8644/webhooks/<route-name>`

---...

## Setup

There are two ways to enable the webhook adapter.

### Via setup wizard

```bash
hermes gateway setup
```

Follow the prompts to enable webhooks, set the port, and set a global HMAC secret.

### Via environment variables

Add to `~/.hermes/.env`:

```bash
WEBHOOK_ENABLED=true
WEBHOOK_PORT=8644        # default
WEBHOOK_SECRET=your-global-secret
```

### Verify the server

Once the gateway is running:

```bash
curl http://localhost:8644/health
```

Expected response:

```json
{"status": "ok", "platform": "webhook"}
```

---...

## Configuring Routes {#configuring-routes}

Routes define how different webhook sources are handled. Each route is a named entry under `platforms.webhook.extra.routes` in your `config.yaml`.

### Route properties

| Property | Required | Description |
|----------|----------|-------------|
| `events` | No | List of event types to accept (e.g. `["pull_request"]`). If empty, all events are accepted. Event type is read from `X-GitHub-Event`, `X-GitLab-Event`, or `event_type` in the payload. |
| `secret` | **Yes** | HMAC secret for signature validation. Falls back to the global `secret` if not set on the route. Set to `"INSECURE_NO_AUTH"` fo...

## GitHub PR Review (Step by Step) {#github-pr-review}

This walkthrough sets up automatic code review on every pull request.

### 1. Create the webhook in GitHub

1. Go to your repository → **Settings** → **Webhooks** → **Add webhook**
2. Set **Payload URL** to `http://your-server:8644/webhooks/github-pr`
3. Set **Content type** to `application/json`
4. Set **Secret** to match your route config (e.g. `github-webhook-secret`)
5. Under **Which events?**, select **Let me select individual events** and check **Pull requests**
6. Click **Add webhook**

### 2. Add the route config

Add the `github-pr` route to your `~/.hermes/config.yaml` as shown in th...

## GitLab Webhook Setup {#gitlab-webhook-setup}

GitLab webhooks work similarly but use a different authentication mechanism. GitLab sends the secret as a plain `X-Gitlab-Token` header (exact string match, not HMAC).

### 1. Create the webhook in GitLab

1. Go to your project → **Settings** → **Webhooks**
2. Set the **URL** to `http://your-server:8644/webhooks/gitlab-mr`
3. Enter your **Secret token**
4. Select **Merge request events** (and any other events you want)
5. Click **Add webhook**

### 2. Add the route config

```yaml
platforms:
  webhook:
    enabled: true
    extra:
      routes:
        gitlab-mr:
          events: ["merge_requ...

## Delivery Options {#delivery-options}

The `deliver` field controls where the agent's response goes after processing the webhook event.

| Deliver Type | Description |
|-------------|-------------|
| `log` | Logs the response to the gateway log output. This is the default and is useful for testing. |
| `github_comment` | Posts the response as a PR/issue comment via the `gh` CLI. Requires `deliver_extra.repo` and `deliver_extra.pr_number`. The `gh` CLI must be installed and authenticated on the gateway host (`gh auth login`). |
| `telegram` | Routes the response to Telegram. Uses the home channel, or specify `chat_id` in `deliver_ex...

## Direct Delivery Mode {#direct-delivery-mode}

By default, every webhook POST triggers an agent run — the payload becomes a prompt, the agent processes it, and the agent's response is delivered. This costs LLM tokens on every event.

For use cases where you just want to **push a plain notification** — no reasoning, no agent loop, just deliver the message — set `deliver_only: true` on the route. The rendered `prompt` template becomes the literal message body, and the adapter dispatches it directly to the configured delivery target.

### When to use direct delivery

- **External service push** — Supabase/Firebase webhook fires on a database ...

## Dynamic Subscriptions (CLI) {#dynamic-subscriptions}

In addition to static routes in `config.yaml`, you can create webhook subscriptions dynamically using the `hermes webhook` CLI command. This is especially useful when the agent itself needs to set up event-driven triggers.

### Create a subscription

```bash
hermes webhook subscribe github-issues \
  --events "issues" \
  --prompt "New issue #{issue.number}: {issue.title}\nBy: {issue.user.login}\n\n{issue.body}" \
  --deliver telegram \
  --deliver-chat-id "-100123456789" \
  --description "Triage new GitHub issues"
```

This returns the webhook URL and an auto-generated HMAC secret. Configure...

## Security {#security}

The webhook adapter includes multiple layers of security:

### HMAC signature validation

The adapter validates incoming webhook signatures using the appropriate method for each source:

- **GitHub**: `X-Hub-Signature-256` header — HMAC-SHA256 hex digest prefixed with `sha256=`
- **GitLab**: `X-Gitlab-Token` header — plain secret string match
- **Generic**: `X-Webhook-Signature` header — raw HMAC-SHA256 hex digest

If a secret is configured but no recognized signature header is present, the request is rejected.

### Secret is required

Every route must have a secret — either set directly on th...

## Troubleshooting {#troubleshooting}

### Webhook not arriving

- Verify the port is exposed and accessible from the webhook source
- Check firewall rules — port `8644` (or your configured port) must be open
- Verify the URL path matches: `http://your-server:8644/webhooks/<route-name>`
- Use the `/health` endpoint to confirm the server is running

### Signature validation failing

- Ensure the secret in your route config exactly matches the secret configured in the webhook source
- For GitHub, the secret is HMAC-based — check `X-Hub-Signature-256`
- For GitLab, the secret is a plain token match — check `X-Gitlab-Token`
- Check gat...

## Environment Variables {#environment-variables}

| Variable | Description | Default |
|----------|-------------|---------|
| `WEBHOOK_ENABLED` | Enable the webhook platform adapter | `false` |
| `WEBHOOK_PORT` | HTTP server port for receiving webhooks | `8644` |
| `WEBHOOK_SECRET` | Global HMAC secret (used as fallback when routes don't specify their own) | _(none)_ |...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
