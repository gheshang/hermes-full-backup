---
title: Dashboard Plugins
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-dashboard-plugins.md]
---

# Dashboard Plugins

源文档：[Dashboard Plugins](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/dashboard-plugins.md)

# Dashboard Plugins

Dashboard plugins let you add custom tabs to the web dashboard. A plugin can display its own UI, call the Hermes API, and optionally register backend endpoints — all without touching the dashboard source code.

## Quick Start

Create a plugin directory with a manifest and a JS file:

```bash
mkdir -p ~/.hermes/plugins/my-plugin/dashboard/dist
```

**manifest.json:**

```json
{
  "name": "my-plugin",
  "label": "My Plugin",
  "icon": "Sparkles",
  "version": "1.0.0",
  "tab": {
    "path": "/my-plugin",
    "position": "after:skills"
  },
  "entry": "dist/index.js"
}
```

**dist/index.js:**

```javascript
(function () {
  var SDK = window.__HERMES_PLUGIN_SDK__;
  var React = SDK.React;
  var Card = SDK.components.Card;
  var CardHeader = SDK.components.CardHeader;
  var CardTitle = SDK.components.CardTitle;
  var Car...

## Plugin Structure

Plugins live inside the standard `~/.hermes/plugins/` directory. The dashboard extension is a `dashboard/` subfolder:

```
~/.hermes/plugins/my-plugin/
  plugin.yaml              # optional — existing CLI/gateway plugin manifest
  __init__.py              # optional — existing CLI/gateway hooks
  dashboard/               # dashboard extension
    manifest.json          # required — tab config, icon, entry point
    dist/
      index.js             # required — pre-built JS bundle
      style.css            # optional — custom CSS
    plugin_api.py          # optional — backend API routes
```

...

## Manifest Reference

The `manifest.json` file describes your plugin to the dashboard:

```json
{
  "name": "my-plugin",
  "label": "My Plugin",
  "description": "What this plugin does",
  "icon": "Sparkles",
  "version": "1.0.0",
  "tab": {
    "path": "/my-plugin",
    "position": "after:skills"
  },
  "entry": "dist/index.js",
  "css": "dist/style.css",
  "api": "plugin_api.py"
}
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique plugin identifier (lowercase, hyphens ok) |
| `label` | Yes | Display name shown in the nav tab |
| `description` | No | Short descriptio...

## Plugin SDK

Plugins don't bundle React or UI components — they use the SDK exposed on `window.__HERMES_PLUGIN_SDK__`. This avoids version conflicts and keeps plugin bundles tiny.

### SDK Contents

```javascript
var SDK = window.__HERMES_PLUGIN_SDK__;

// React
SDK.React              // React instance
SDK.hooks.useState     // React hooks
SDK.hooks.useEffect
SDK.hooks.useCallback
SDK.hooks.useMemo
SDK.hooks.useRef
SDK.hooks.useContext
SDK.hooks.createContext

// API
SDK.api                // Hermes API client (getStatus, getSessions, etc.)
SDK.fetchJSON          // Raw fetch for custom endpoints — handles...

## Backend API Routes

Plugins can register FastAPI routes by setting the `api` field in the manifest. Create a Python file that exports a `router`:

```python
# plugin_api.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
async def get_data():
    return {"items": ["one", "two", "three"]}

@router.post("/action")
async def do_action(body: dict):
    return {"ok": True, "received": body}
```

Routes are mounted at `/api/plugins/<name>/`, so the above becomes:
- `GET /api/plugins/my-plugin/data`
- `POST /api/plugins/my-plugin/action`

Plugin API routes bypass session token authentication si...

## Custom CSS

If your plugin needs custom styles, add a CSS file and reference it in the manifest:

```json
{
  "css": "dist/style.css"
}
```

The CSS file is injected as a `<link>` tag when the plugin loads. Use specific class names to avoid conflicts with the dashboard's existing styles.

```css
/* dist/style.css */
.my-plugin-chart {
  border: 1px solid var(--color-border);
  background: var(--color-card);
  padding: 1rem;
}
```

You can use the dashboard's CSS custom properties (e.g. `--color-border`, `--color-foreground`) to match the active theme....

## Plugin Loading Flow

1. Dashboard loads — `main.tsx` exposes the SDK on `window.__HERMES_PLUGIN_SDK__`
2. `App.tsx` calls `usePlugins()` which fetches `GET /api/dashboard/plugins`
3. For each plugin: CSS `<link>` injected (if declared), JS `<script>` loaded
4. Plugin JS calls `window.__HERMES_PLUGINS__.register(name, Component)`
5. Dashboard adds the tab to navigation and mounts the component as a route

Plugins have up to 2 seconds to register after their script loads. If a plugin fails to load, the dashboard continues without it....

## Plugin Discovery

The dashboard scans these directories for `dashboard/manifest.json`:

1. **User plugins:** `~/.hermes/plugins/<name>/dashboard/manifest.json`
2. **Bundled plugins:** `<repo>/plugins/<name>/dashboard/manifest.json`
3. **Project plugins:** `./.hermes/plugins/<name>/dashboard/manifest.json` (only when `HERMES_ENABLE_PROJECT_PLUGINS` is set)

User plugins take precedence — if the same plugin name exists in multiple sources, the user version wins.

To force re-scanning after adding a new plugin without restarting the server:

```bash
curl http://127.0.0.1:9119/api/dashboard/plugins/rescan
```...

## Plugin API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/dashboard/plugins` | GET | List discovered plugins |
| `/api/dashboard/plugins/rescan` | GET | Force re-scan for new plugins |
| `/dashboard-plugins/<name>/<path>` | GET | Serve plugin static assets |
| `/api/plugins/<name>/*` | * | Plugin-registered API routes |...

## Example Plugin

The repository includes an example plugin at `plugins/example-dashboard/` that demonstrates:

- Using SDK components (Card, Badge, Button)
- Calling a backend API route
- Registering via `window.__HERMES_PLUGINS__.register()`

To try it, run `hermes dashboard` — the "Example" tab appears after Skills....

## Tips

- **No build step required** — write plain JavaScript IIFEs. If you prefer JSX, use any bundler (esbuild, Vite, webpack) targeting IIFE output with React as an external.
- **Keep bundles small** — React and all UI components are provided by the SDK. Your bundle should only contain your plugin logic.
- **Use theme variables** — reference `var(--color-*)` in CSS to automatically match whatever theme the user has selected.
- **Test locally** — run `hermes dashboard --no-open` and use browser dev tools to verify your plugin loads and registers correctly....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
