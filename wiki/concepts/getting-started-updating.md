---
title: Updating & Uninstalling
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/getting-started-updating.md]
---

# Updating & Uninstalling

源文档：[Updating & Uninstalling](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/updating.md)

# Updating & Uninstalling

## Updating

Update to the latest version with a single command:

```bash
hermes update
```

This pulls the latest code, updates dependencies, and prompts you to configure any new options that were added since your last update.

:::tip
`hermes update` automatically detects new configuration options and prompts you to add them. If you skipped that prompt, you can manually run `hermes config check` to see missing options, then `hermes config migrate` to interactively add them.
:::

### What happens during an update

When you run `hermes update`, the following steps occur:

1. **Git pull** — pulls the latest ...

## Uninstalling

```bash
hermes uninstall
```

The uninstaller gives you the option to keep your configuration files (`~/.hermes/`) for a future reinstall.

### Manual Uninstall

```bash
rm -f ~/.local/bin/hermes
rm -rf /path/to/hermes-agent
rm -rf ~/.hermes            # Optional — keep if you plan to reinstall
```

:::info
If you installed the gateway as a system service, stop and disable it first:
```bash
hermes gateway stop
# Linux: systemctl --user disable hermes-gateway
# macOS: launchctl remove ai.hermes.gateway
```
:::...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
