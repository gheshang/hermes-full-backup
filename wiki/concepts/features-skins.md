---
title: Skins & Themes
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-skins.md]
---

# Skins & Themes

源文档：[Skins & Themes](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skins.md)

# Skins & Themes

Skins control the **visual presentation** of the Hermes CLI: banner colors, spinner faces and verbs, response-box labels, branding text, and the tool activity prefix.

Conversational style and visual style are separate concepts:

- **Personality** changes the agent's tone and wording.
- **Skin** changes the CLI's appearance.

## Change skins

```bash
/skin                # show the current skin and list available skins
/skin ares           # switch to a built-in skin
/skin mytheme        # switch to a custom skin from ~/.hermes/skins/mytheme.yaml
```

Or set the default skin in `~/.hermes/config.yaml`:

```yaml
display:
  skin: default
```...

## Built-in skins

| Skin | Description | Agent branding | Visual character |
|------|-------------|----------------|------------------|
| `default` | Classic Hermes — gold and kawaii | `Hermes Agent` | Warm gold borders, cornsilk text, kawaii faces in spinners. The familiar caduceus banner. Clean and inviting. |
| `ares` | War-god theme — crimson and bronze | `Ares Agent` | Deep crimson borders with bronze accents. Aggressive spinner verbs ("forging", "marching", "tempering steel"). Custom sword-and-shield ASCII art banner. |
| `mono` | Monochrome — clean grayscale | `Hermes Agent` | All grays — no color. Borde...

## Complete list of configurable keys

### Colors (`colors:`)

Controls all color values throughout the CLI. Values are hex color strings.

| Key | Description | Default (`default` skin) |
|-----|-------------|--------------------------|
| `banner_border` | Panel border around the startup banner | `#CD7F32` (bronze) |
| `banner_title` | Title text color in the banner | `#FFD700` (gold) |
| `banner_accent` | Section headers in the banner (Available Tools, etc.) | `#FFBF00` (amber) |
| `banner_dim` | Muted text in the banner (separators, secondary labels) | `#B8860B` (dark goldenrod) |
| `banner_text` | Body text in the banner (tool ...

## Custom skins

Create YAML files under `~/.hermes/skins/`. User skins inherit missing values from the built-in `default` skin, so you only need to specify the keys you want to change.

### Full custom skin YAML template

```yaml
# ~/.hermes/skins/mytheme.yaml
# Complete skin template — all keys shown. Delete any you don't need;
# missing values automatically inherit from the 'default' skin.

name: mytheme
description: My custom theme

colors:
  banner_border: "#CD7F32"
  banner_title: "#FFD700"
  banner_accent: "#FFBF00"
  banner_dim: "#B8860B"
  banner_text: "#FFF8DC"
  ui_accent: "#FFBF00"
  ui_label: "#4d...

## Hermes Mod — Visual Skin Editor

[Hermes Mod](https://github.com/cocktailpeanut/hermes-mod) is a community-built web UI for creating and managing skins visually. Instead of writing YAML by hand, you get a point-and-click editor with live preview.

![Hermes Mod skin editor](https://raw.githubusercontent.com/cocktailpeanut/hermes-mod/master/nous.png)

**What it does:**

- Lists all built-in and custom skins
- Opens any skin into a visual editor with all Hermes skin fields (colors, spinner, branding, tool prefix, tool emojis)
- Generates `banner_logo` text art from a text prompt
- Converts uploaded images (PNG, JPG, GIF, WEBP) i...

## Operational notes

- Built-in skins load from `hermes_cli/skin_engine.py`.
- Unknown skins automatically fall back to `default`.
- `/skin` updates the active CLI theme immediately for the current session.
- User skins in `~/.hermes/skins/` take precedence over built-in skins with the same name.
- Skin changes via `/skin` are session-only. To make a skin your permanent default, set it in `config.yaml`.
- The `banner_logo` and `banner_hero` fields support Rich console markup (e.g., `[bold #FF0000]text[/]`) for colored ASCII art....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
