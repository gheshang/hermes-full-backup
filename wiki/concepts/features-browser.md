---
title: Browser Automation
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-browser.md]
---

# Browser Automation

源文档：[Browser Automation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/browser.md)

# Browser Automation

Hermes Agent includes a full browser automation toolset with multiple backend options:

- **Browserbase cloud mode** via [Browserbase](https://browserbase.com) for managed cloud browsers and anti-bot tooling
- **Browser Use cloud mode** via [Browser Use](https://browser-use.com) as an alternative cloud browser provider
- **Firecrawl cloud mode** via [Firecrawl](https://firecrawl.dev) for cloud browsers with built-in scraping
- **Camofox local mode** via [Camofox](https://github.com/jo-inc/camofox-browser) for local anti-detection browsing (Firefox-based fingerprint spoofing)
- **Local Chrome via CDP** — connect browser tools to your own Chrome instance using `/browser connect`
- **Local browser mode** via the `agent-browser` CLI and a local Chromium installation

In a

## Overview

Pages are represented as **accessibility trees** (text-based snapshots), making them ideal for LLM agents. Interactive elements get ref IDs (like `@e1`, `@e2`) that the agent uses for clicking and typing.

Key capabilities:

- **Multi-provider cloud execution** — Browserbase, Browser Use, or Firecrawl — no local browser needed
- **Local Chrome integration** — attach to your running Chrome via CDP for hands-on browsing
- **Built-in stealth** — random fingerprints, CAPTCHA solving, residential proxies (Browserbase)
- **Session isolation** — each task gets its own browser session
- **Automatic cl...

## Setup

:::tip Nous Subscribers
If you have a paid [Nous Portal](https://portal.nousresearch.com) subscription, you can use browser automation through the **[Tool Gateway](tool-gateway.md)** without any separate API keys. Run `hermes model` or `hermes tools` to enable it.
:::

### Browserbase cloud mode

To use Browserbase-managed cloud browsers, add:

```bash
# Add to ~/.hermes/.env
BROWSERBASE_API_KEY=***
BROWSERBASE_PROJECT_ID=your-project-id-here
```

Get your credentials at [browserbase.com](https://browserbase.com).

### Browser Use cloud mode

To use Browser Use as your cloud browser provider, ...

## Available Tools

### `browser_navigate`

Navigate to a URL. Must be called before any other browser tool. Initializes the Browserbase session.

```
Navigate to https://github.com/NousResearch
```

:::tip
For simple information retrieval, prefer `web_search` or `web_extract` — they are faster and cheaper. Use browser tools when you need to **interact** with a page (click buttons, fill forms, handle dynamic content).
:::

### `browser_snapshot`

Get a text-based snapshot of the current page's accessibility tree. Returns interactive elements with ref IDs like `@e1`, `@e2` for use with `browser_click` and `browser...

## Practical Examples

### Filling Out a Web Form

```
User: Sign up for an account on example.com with my email john@example.com

Agent workflow:
1. browser_navigate("https://example.com/signup")
2. browser_snapshot()  → sees form fields with refs
3. browser_type(ref="@e3", text="john@example.com")
4. browser_type(ref="@e5", text="SecurePass123")
5. browser_click(ref="@e8")  → clicks "Create Account"
6. browser_snapshot()  → confirms success
```

### Researching Dynamic Content

```
User: What are the top trending repos on GitHub right now?

Agent workflow:
1. browser_navigate("https://github.com/trending")
2. brow...

## Session Recording

Automatically record browser sessions as WebM video files:

```yaml
browser:
  record_sessions: true  # default: false
```

When enabled, recording starts automatically on the first `browser_navigate` and saves to `~/.hermes/browser_recordings/` when the session closes. Works in both local and cloud (Browserbase) modes. Recordings older than 72 hours are automatically cleaned up....

## Stealth Features

Browserbase provides automatic stealth capabilities:

| Feature | Default | Notes |
|---------|---------|-------|
| Basic Stealth | Always on | Random fingerprints, viewport randomization, CAPTCHA solving |
| Residential Proxies | On | Routes through residential IPs for better access |
| Advanced Stealth | Off | Custom Chromium build, requires Scale Plan |
| Keep Alive | On | Session reconnection after network hiccups |

:::note
If paid features aren't available on your plan, Hermes automatically falls back — first disabling `keepAlive`, then proxies — so browsing still works on free plans.
::...

## Session Management

- Each task gets an isolated browser session via Browserbase
- Sessions are automatically cleaned up after inactivity (default: 2 minutes)
- A background thread checks every 30 seconds for stale sessions
- Emergency cleanup runs on process exit to prevent orphaned sessions
- Sessions are released via the Browserbase API (`REQUEST_RELEASE` status)...

## Limitations

- **Text-based interaction** — relies on accessibility tree, not pixel coordinates
- **Snapshot size** — large pages may be truncated or LLM-summarized at 8000 characters
- **Session timeout** — cloud sessions expire based on your provider's plan settings
- **Cost** — cloud sessions consume provider credits; sessions are automatically cleaned up when the conversation ends or after inactivity. Use `/browser connect` for free local browsing.
- **No file downloads** — cannot download files from the browser...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
