---
title: Vision & Image Paste
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-vision.md]
---

# Vision & Image Paste

源文档：[Vision & Image Paste](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/vision.md)

# Vision & Image Paste

Hermes Agent supports **multimodal vision** — you can paste images from your clipboard directly into the CLI and ask the agent to analyze, describe, or work with them. Images are sent to the model as base64-encoded content blocks, so any vision-capable model can process them.

## How It Works

1. Copy an image to your clipboard (screenshot, browser image, etc.)
2. Attach it using one of the methods below
3. Type your question and press Enter
4. The image appears as a `[📎 Image #1]` badge above the input
5. On submit, the image is sent to the model as a vision content block

You can attach multiple images before sending — each gets its own badge. Press `Ctrl+C` to clear all attached images.

Images are saved to `~/.hermes/images/` as PNG files with timestamped filenames....

## Paste Methods

How you attach an image depends on your terminal environment. Not all methods work everywhere — here's the full breakdown:

### `/paste` Command

**The most reliable explicit image-attach fallback.**

```
/paste
```

Type `/paste` and press Enter. Hermes checks your clipboard for an image and attaches it. This is the safest option when your terminal rewrites `Cmd+V`/`Ctrl+V`, or when you copied only an image and there is no bracketed-paste text payload to inspect.

### Ctrl+V / Cmd+V

Hermes now treats paste as a layered flow:
- normal text paste first
- native clipboard / OSC52 text fallback ...

## Platform Compatibility

| Environment | `/paste` | Cmd/Ctrl+V | `/terminal-setup` | Notes |
|---|:---:|:---:|:---:|---|
| **macOS Terminal / iTerm2** | ✅ | ✅ | n/a | Best experience — native clipboard + screenshot-path recovery |
| **Apple Terminal** | ✅ | ✅ | n/a | If Cmd+←/→/⌫ gets rewritten, use Ctrl+A / Ctrl+E / Ctrl+U fallbacks |
| **Linux X11 desktop** | ✅ | ✅ | n/a | Requires `xclip` (`apt install xclip`) |
| **Linux Wayland desktop** | ✅ | ✅ | n/a | Requires `wl-paste` (`apt install wl-clipboard`) |
| **WSL2 (Windows Terminal)** | ✅ | ✅ | n/a | Uses `powershell.exe` — no extra install needed |
| **VS Code / C...

## Platform-Specific Setup

### macOS

**No setup required.** Hermes uses `osascript` (built into macOS) to read the clipboard. For faster performance, optionally install `pngpaste`:

```bash
brew install pngpaste
```

### Linux (X11)

Install `xclip`:

```bash
# Ubuntu/Debian
sudo apt install xclip

# Fedora
sudo dnf install xclip

# Arch
sudo pacman -S xclip
```

### Linux (Wayland)

Modern Linux desktops (Ubuntu 22.04+, Fedora 34+) often use Wayland by default. Install `wl-clipboard`:

```bash
# Ubuntu/Debian
sudo apt install wl-clipboard

# Fedora
sudo dnf install wl-clipboard

# Arch
sudo pacman -S wl-clipboard
```
...

## SSH & Remote Sessions

**Clipboard image paste does not fully work over SSH.** When you SSH into a remote machine, the Hermes CLI runs on the remote host. Clipboard tools (`xclip`, `wl-paste`, `powershell.exe`, `osascript`) read the clipboard of the machine they run on — which is the remote server, not your local machine. Your local clipboard image is therefore inaccessible from the remote side.

Text can sometimes still bridge through terminal paste or OSC52, but image clipboard access and local screenshot temp paths remain tied to the machine running Hermes.

### Workarounds for SSH

1. **Upload the image file** —...

## Why Terminals Can't Paste Images

This is a common source of confusion, so here's the technical explanation:

Terminals are **text-based** interfaces. When you press Ctrl+V (or Cmd+V), the terminal emulator:

1. Reads the clipboard for **text content**
2. Wraps it in [bracketed paste](https://en.wikipedia.org/wiki/Bracketed-paste) escape sequences
3. Sends it to the application through the terminal's text stream

If the clipboard contains only an image (no text), the terminal has nothing to send. There is no standard terminal escape sequence for binary image data. The terminal simply does nothing.

This is why Hermes uses a se...

## Supported Models

Image paste works with any vision-capable model. The image is sent as a base64-encoded data URL in the OpenAI vision content format:

```json
{
  "type": "image_url",
  "image_url": {
    "url": "data:image/png;base64,..."
  }
}
```

Most modern models support this format, including GPT-4 Vision, Claude (with vision), Gemini, and open-source multimodal models served through OpenRouter....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
