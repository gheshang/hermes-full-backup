---
title: Extending the CLI
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-extending-the-cli.md]
---

# Extending the CLI

源文档：[Extending the CLI](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/extending-the-cli.md)

# Extending the CLI

Hermes exposes protected extension hooks on `HermesCLI` so wrapper CLIs can add widgets, keybindings, and layout customizations without overriding the 1000+ line `run()` method. This keeps your extension decoupled from internal changes.

## Extension points

There are five extension seams available:

| Hook | Purpose | Override when... |
|------|---------|------------------|
| `_get_extra_tui_widgets()` | Inject widgets into the layout | You need a persistent UI element (panel, status line, mini-player) |
| `_register_extra_tui_keybindings(kb, *, input_area)` | Add keyboard shortcuts | You need hotkeys (toggle panels, transport controls, modal shortcuts) |
| `_build_tui_layout_children(**widgets)` | Full control over widget ordering | You need to reorder or wrap existing widgets (rare) |
| `process_command()` | Add custom slash commands | You need...

## Quick start: a wrapper CLI

```python
#!/usr/bin/env python3
"""my_cli.py — Example wrapper CLI that extends Hermes."""

from cli import HermesCLI
from prompt_toolkit.layout import FormattedTextControl, Window
from prompt_toolkit.filters import Condition


class MyCLI(HermesCLI):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._panel_visible = False

    def _get_extra_tui_widgets(self):
        """Add a toggleable info panel above the status bar."""
        cli_ref = self
        return [
            Window(
                FormattedTextControl(lambda: "📊 My custom panel content"),
   ...

## Hook reference

### `_get_extra_tui_widgets()`

Returns a list of prompt_toolkit widgets to insert into the TUI layout. Widgets appear **between the spacer and the status bar** — above the input area but below the main output.

```python
def _get_extra_tui_widgets(self) -> list:
    return []  # default: no extra widgets
```

Each widget should be a prompt_toolkit container (e.g., `Window`, `ConditionalContainer`, `HSplit`). Use `ConditionalContainer` or `filter=Condition(...)` to make widgets toggleable.

```python
from prompt_toolkit.layout import ConditionalContainer, Window, FormattedTextControl
from prom...

## Layout diagram

The default layout from top to bottom:

1. **Output area** — scrolling conversation history
2. **Spacer**
3. **Extra widgets** — from `_get_extra_tui_widgets()`
4. **Status bar** — model, context %, elapsed time
5. **Image bar** — attached image count
6. **Input area** — user prompt
7. **Voice status** — recording indicator
8. **Completions menu** — autocomplete suggestions...

## Tips

- **Invalidate the display** after state changes: call `self._invalidate()` to trigger a prompt_toolkit redraw.
- **Access agent state**: `self.agent`, `self.model`, `self.conversation_history` are all available.
- **Custom styles**: Override `_build_tui_style_dict()` and add entries for your custom style classes.
- **Slash commands**: Override `process_command()`, handle your commands, and call `super().process_command(cmd)` for everything else.
- **Don't override `run()`** unless absolutely necessary — the extension hooks exist specifically to avoid that coupling....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
