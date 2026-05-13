---
title: Automation Templates
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-automation-templates.md]
---

# Automation Templates

源文档：[Automation Templates](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/automation-templates.md)

# Automation Templates

Copy-paste recipes for common automation patterns. Each template uses Hermes's built-in [cron scheduler](/docs/user-guide/features/cron) for time-based triggers and [webhook platform](/docs/user-guide/messaging/webhooks) for event-driven triggers.

Every template works with **any model** — not locked to a single provider.

:::tip Three Trigger Types
| Trigger | How | Tool |
|---------|-----|------|
| **Schedule** | Runs on a cadence (hourly, nightly, weekly) | `cronjob` tool or `/cron` slash command |
| **GitHub Event** | Fires on PR opens, pushes, issues, CI results | Webhook platform (`hermes webhook subscribe`) |
| **API Call** | External service POSTs JSON to your endpoint | Webhook platform (config.yaml routes or `hermes webhook subscribe`) |

All three support

## Development Workflow

### Nightly Backlog Triage

Label, prioritize, and summarize new issues every night. Delivers a digest to your team channel.

**Trigger:** Schedule (nightly)

```bash
hermes cron create "0 2 * * *" \
  "You are a project manager triaging the NousResearch/hermes-agent GitHub repo.

1. Run: gh issue list --repo NousResearch/hermes-agent --state open --json number,title,labels,author,createdAt --limit 30
2. Identify issues opened in the last 24 hours
3. For each new issue:
   - Suggest a priority label (P0-critical, P1-high, P2-medium, P3-low)
   - Suggest a category label (bug, feature, docs, se...

## DevOps & Monitoring

### Deploy Verification

Trigger smoke tests after every deployment. Your CI/CD pipeline POSTs to the webhook when a deploy completes.

**Trigger:** API call (webhook)

```bash
hermes webhook subscribe deploy-verify \
  --events "deployment" \
  --prompt "A deployment just completed:
Service: {service}
Environment: {environment}
Version: {version}
Deployed by: {deployer}

Run these verification steps:
1. Check if the service is responding: curl -s -o /dev/null -w '%{http_code}' {health_url}
2. Search recent logs for errors: check the deployment payload for any error indicators
3. Verify the ve...

## Research & Intelligence

### Competitive Repository Scout

Monitor competitor repos for interesting PRs, features, and architectural decisions.

**Trigger:** Schedule (daily)

```bash
hermes cron create "0 8 * * *" \
  "Scout these AI agent repositories for notable activity in the last 24 hours:

Repos to check:
- anthropics/claude-code
- openai/codex
- All-Hands-AI/OpenHands
- Aider-AI/aider

For each repo:
1. gh pr list --repo <repo> --state all --json number,title,author,createdAt,mergedAt --limit 15
2. gh issue list --repo <repo> --state open --json number,title,labels,createdAt --limit 10

Focus on:
- New feature...

## Industry Moves (funding, acquisitions, launches)

Keep each item to 1-2 sentences. Include links. Total under 600 words." \
  --name "Weekly AI digest" \
  --deliver telegram
```

### Paper Digest with Notes

Daily arXiv scan that saves summaries to your note-taking system.

**Trigger:** Schedule (daily)

```bash
hermes cron create "0 8 * * *" \
  "Search arXiv for the 3 most interesting papers on 'language model reasoning' OR 'tool-use agents' from the past day. For each paper, create an Obsidian note with the title, authors, abstract summary, key contribution, and potential relevance to Hermes Agent development." \
  --skills "arxiv,obsidia...

## GitHub Event Automations

### Issue Auto-Labeling

Automatically label and respond to new issues.

**Trigger:** GitHub webhook

```bash
hermes webhook subscribe github-issues \
  --events "issues" \
  --prompt "New GitHub issue received:
Repository: {repository.full_name}
Issue #{issue.number}: {issue.title}
Author: {issue.user.login}
Action: {action}
Body: {issue.body}
Labels: {issue.labels}

If this is a new issue (action=opened):
1. Read the issue title and body carefully
2. Suggest appropriate labels (bug, feature, docs, security, question)
3. If it's a bug report, check if you can identify the affected component f...

## Business Operations

### Stripe Payment Monitoring

Track payment events and get summaries of failures.

**Trigger:** API call (webhook)

```bash
hermes webhook subscribe stripe-payments \
  --events "payment_intent.succeeded,payment_intent.payment_failed,charge.dispute.created" \
  --prompt "Stripe event received:
Event type: {type}
Amount: {data.object.amount} cents ({data.object.currency})
Customer: {data.object.customer}
Status: {data.object.status}

For payment_intent.payment_failed:
- Identify the failure reason from {data.object.last_payment_error}
- Suggest whether this is a transient issue (retry) or perm...

## Multi-Skill Workflows

### Security Audit Pipeline

Combine multiple skills for a comprehensive weekly security review.

**Trigger:** Schedule (weekly)

```bash
hermes cron create "0 3 * * 0" \
  "Run a comprehensive security audit of the hermes-agent codebase.

1. Check for dependency vulnerabilities (pip audit, npm audit)
2. Search the codebase for common security anti-patterns:
   - Hardcoded secrets or API keys
   - SQL injection vectors (string formatting in queries)
   - Path traversal risks (user input in file paths without validation)
   - Unsafe deserialization (pickle.loads, yaml.load without SafeLoader)
3...

## Quick Reference

### Cron Schedule Syntax

| Expression | Meaning |
|-----------|---------|
| `every 30m` | Every 30 minutes |
| `every 2h` | Every 2 hours |
| `0 2 * * *` | Daily at 2:00 AM |
| `0 9 * * 1` | Every Monday at 9:00 AM |
| `0 9 * * 1-5` | Weekdays at 9:00 AM |
| `0 3 * * 0` | Every Sunday at 3:00 AM |
| `0 */6 * * *` | Every 6 hours |

### Delivery Targets

| Target | Flag | Notes |
|--------|------|-------|
| Same chat | `--deliver origin` | Default — delivers to where the job was created |
| Local file | `--deliver local` | Saves output, no notification |
| Telegram | `--deliver telegram` | Hom...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
