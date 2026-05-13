---
title: Web Dashboard
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-web-dashboard.md]
---

# Web Dashboard

源文档：[Web Dashboard](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/web-dashboard.md)

# Web Dashboard

The web dashboard is a browser-based UI for managing your Hermes Agent installation. Instead of editing YAML files or running CLI commands, you can configure settings, manage API keys, and monitor sessions from a clean web interface.

## Quick Start

```bash
hermes dashboard
```

This starts a local web server and opens `http://127.0.0.1:9119` in your browser. The dashboard runs entirely on your machine — no data leaves localhost.

### Options

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | `9119` | Port to run the web server on |
| `--host` | `127.0.0.1` | Bind address |
| `--no-open` | — | Don't auto-open the browser |

```bash
# Custom port
hermes dashboard --port 8080

# Bind to all interfaces (use with caution on shared networks)
hermes dashboard --host 0.0.0.0

# Start without opening browser
hermes da...

## Prerequisites

The web dashboard requires FastAPI and Uvicorn. Install them with:

```bash
pip install hermes-agent[web]
```

If you installed with `pip install hermes-agent[all]`, the web dependencies are already included.

When you run `hermes dashboard` without the dependencies, it will tell you what to install. If the frontend hasn't been built yet and `npm` is available, it builds automatically on first launch....

## Pages

### Status

The landing page shows a live overview of your installation:

- **Agent version** and release date
- **Gateway status** — running/stopped, PID, connected platforms and their state
- **Active sessions** — count of sessions active in the last 5 minutes
- **Recent sessions** — list of the 20 most recent sessions with model, message count, token usage, and a preview of the conversation

The status page auto-refreshes every 5 seconds.

### Config

A form-based editor for `config.yaml`. All 150+ configuration fields are auto-discovered from `DEFAULT_CONFIG` and organized into tabbed cate...

## `/reload` Slash Command

The dashboard PR also adds a `/reload` slash command to the interactive CLI. After changing API keys via the web dashboard (or by editing `.env` directly), use `/reload` in an active CLI session to pick up the changes without restarting:

```
You → /reload
  Reloaded .env (3 var(s) updated)
```

This re-reads `~/.hermes/.env` into the running process's environment. Useful when you've added a new provider key via the dashboard and want to use it immediately....

## REST API

The web dashboard exposes a REST API that the frontend consumes. You can also call these endpoints directly for automation:

### GET /api/status

Returns agent version, gateway status, platform states, and active session count.

### GET /api/sessions

Returns the 20 most recent sessions with metadata (model, token counts, timestamps, preview).

### GET /api/config

Returns the current `config.yaml` contents as JSON.

### GET /api/config/defaults

Returns the default configuration values.

### GET /api/config/schema

Returns a schema describing every config field — type, description, category, ...

## CORS

The web server restricts CORS to localhost origins only:

- `http://localhost:9119` / `http://127.0.0.1:9119` (production)
- `http://localhost:3000` / `http://127.0.0.1:3000`
- `http://localhost:5173` / `http://127.0.0.1:5173` (Vite dev server)

If you run the server on a custom port, that origin is added automatically....

## Development

If you're contributing to the web dashboard frontend:

```bash
# Terminal 1: start the backend API
hermes dashboard --no-open

# Terminal 2: start the Vite dev server with HMR
cd web/
npm install
npm run dev
```

The Vite dev server at `http://localhost:5173` proxies `/api` requests to the FastAPI backend at `http://127.0.0.1:9119`.

The frontend is built with React 19, TypeScript, Tailwind CSS v4, and shadcn/ui-style components. Production builds output to `hermes_cli/web_dist/` which the FastAPI server serves as a static SPA....

## Automatic Build on Update

When you run `hermes update`, the web frontend is automatically rebuilt if `npm` is available. This keeps the dashboard in sync with code updates. If `npm` isn't installed, the update skips the frontend build and `hermes dashboard` will build it on first launch....

## Themes

Themes control the dashboard's visual presentation across three layers:

- **Palette** — colors (background, text, accents, warm glow, noise)
- **Typography** — font families, base size, line height, letter spacing
- **Layout** — corner radius and density (spacing multiplier)

Switch themes live from the header bar — click the palette icon next to the language switcher. Selection persists to `config.yaml` under `dashboard.theme` and is restored on page load.

### Built-in themes

Each built-in ships its own palette, typography, and layout — switching produces visible changes beyond color alone...

## Dashboard plugins

Plugins live in `~/.hermes/plugins/<name>/dashboard/` (user) or repo `plugins/<name>/dashboard/` (bundled). Each ships a `manifest.json` plus a plain JS bundle that uses the plugin SDK exposed on `window.__HERMES_PLUGIN_SDK__`.

### Manifest

```json
{
  "name": "my-plugin",
  "label": "My Plugin",
  "icon": "Sparkles",
  "version": "1.0.0",
  "tab": {
    "path": "/my-plugin",
    "position": "after:skills",
    "override": "/",
    "hidden": false
  },
  "slots": ["sidebar", "header-left"],
  "entry": "dist/index.js",
  "css": "dist/index.css",
  "api": "api.py"
}
```

| Field | Description ...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
