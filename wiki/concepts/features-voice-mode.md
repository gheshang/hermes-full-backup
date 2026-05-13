---
title: Voice Mode
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-voice-mode.md]
---

# Voice Mode

源文档：[Voice Mode](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/voice-mode.md)

# Voice Mode

Hermes Agent supports full voice interaction across CLI and messaging platforms. Talk to the agent using your microphone, hear spoken replies, and have live voice conversations in Discord voice channels.

If you want a practical setup walkthrough with recommended configurations and real usage patterns, see [Use Voice Mode with Hermes](/docs/guides/use-voice-mode-with-hermes).

## Prerequisites

Before using voice features, make sure you have:

1. **Hermes Agent installed** — `pip install hermes-agent` (see [Installation](/docs/getting-started/installation))
2. **An LLM provider configured** — run `hermes model` or set your preferred provider credentials in `~/.hermes/.env`
3. **A working base setup** — run `hermes` to verify the agent responds to text before enabling voice

:::tip
The `~/.hermes/` directory and default `config.yaml` are created automatically the first time you run `hermes`. You only need to create `~/.hermes/.env` manually for API keys.
:::...

## Overview

| Feature | Platform | Description |
|---------|----------|-------------|
| **Interactive Voice** | CLI | Press Ctrl+B to record, agent auto-detects silence and responds |
| **Auto Voice Reply** | Telegram, Discord | Agent sends spoken audio alongside text responses |
| **Voice Channel** | Discord | Bot joins VC, listens to users speaking, speaks replies back |...

## Requirements

### Python Packages

```bash
# CLI voice mode (microphone + audio playback)
pip install "hermes-agent[voice]"

# Discord + Telegram messaging (includes discord.py[voice] for VC support)
pip install "hermes-agent[messaging]"

# Premium TTS (ElevenLabs)
pip install "hermes-agent[tts-premium]"

# Local TTS (NeuTTS, optional)
python -m pip install -U neutts[all]

# Everything at once
pip install "hermes-agent[all]"
```

| Extra | Packages | Required For |
|-------|----------|-------------|
| `voice` | `sounddevice`, `numpy` | CLI voice mode |
| `messaging` | `discord.py[voice]`, `python-telegram-b...

## CLI Voice Mode

### Quick Start

Start the CLI and enable voice mode:

```bash
hermes                # Start the interactive CLI
```

Then use these commands inside the CLI:

```
/voice          Toggle voice mode on/off
/voice on       Enable voice mode
/voice off      Disable voice mode
/voice tts      Toggle TTS output
/voice status   Show current state
```

### How It Works

1. Start the CLI with `hermes` and enable voice mode with `/voice on`
2. **Press Ctrl+B** — a beep plays (880Hz), recording starts
3. **Speak** — a live audio level bar shows your input: `● [▁▂▃▅▇▇▅▂] ❯`
4. **Stop speaking** — after 3 ...

## Gateway Voice Reply (Telegram & Discord)

If you haven't set up your messaging bots yet, see the platform-specific guides:
- [Telegram Setup Guide](../messaging/telegram.md)
- [Discord Setup Guide](../messaging/discord.md)

Start the gateway to connect to your messaging platforms:

```bash
hermes gateway        # Start the gateway (connects to configured platforms)
hermes gateway setup  # Interactive setup wizard for first-time configuration
```

### Discord: Channels vs DMs

The bot supports two interaction modes on Discord:

| Mode | How to Talk | Mention Required | Setup |
|------|------------|-----------------|-------|
| **Direct ...

## Discord Voice Channels

The most immersive voice feature: the bot joins a Discord voice channel, listens to users speaking, transcribes their speech, processes through the agent, and speaks the reply back in the voice channel.

### Setup

#### 1. Discord Bot Permissions

If you already have a Discord bot set up for text (see [Discord Setup Guide](../messaging/discord.md)), you need to add voice permissions.

Go to the [Discord Developer Portal](https://discord.com/developers/applications) → your application → **Installation** → **Default Install Settings** → **Guild Install**:

**Add these permissions to the existing...

## Configuration Reference

### config.yaml

```yaml
# Voice recording (CLI)
voice:
  record_key: "ctrl+b"            # Key to start/stop recording
  max_recording_seconds: 120       # Maximum recording length
  auto_tts: false                  # Auto-enable TTS when voice mode starts
  beep_enabled: true               # Play record start/stop beeps
  silence_threshold: 200           # RMS level (0-32767) below which counts as silence
  silence_duration: 3.0            # Seconds of silence before auto-stop

# Speech-to-Text
stt:
  provider: "local"                  # "local" (free) | "groq" | "openai"
  local:
    model:...

## Troubleshooting

### "No audio device found" (CLI)

PortAudio is not installed:

```bash
brew install portaudio    # macOS
sudo apt install portaudio19-dev  # Ubuntu
```

### Bot doesn't respond in Discord server channels

The bot requires an @mention by default in server channels. Make sure you:

1. Type `@` and select the **bot user** (with the #discriminator), not the **role** with the same name
2. Or use DMs instead — no mention needed
3. Or set `DISCORD_REQUIRE_MENTION=false` in `~/.hermes/.env`

### Bot joins VC but doesn't hear me

- Check your Discord user ID is in `DISCORD_ALLOWED_USERS`
- Make sure y...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
