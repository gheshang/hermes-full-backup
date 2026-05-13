---
title: Image Generation
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-image-generation.md]
---

# Image Generation

源文档：[Image Generation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/image-generation.md)

# Image Generation

Hermes Agent generates images from text prompts via FAL.ai. Nine models are supported out of the box, each with different speed, quality, and cost tradeoffs. The active model is user-configurable via `hermes tools` and persists in `config.yaml`.

## Supported Models

| Model | Speed | Strengths | Price |
|---|---|---|---|
| `fal-ai/flux-2/klein/9b` *(default)* | `<1s` | Fast, crisp text | $0.006/MP |
| `fal-ai/flux-2-pro` | ~6s | Studio photorealism | $0.03/MP |
| `fal-ai/z-image/turbo` | ~2s | Bilingual EN/CN, 6B params | $0.005/MP |
| `fal-ai/nano-banana-pro` | ~8s | Gemini 3 Pro, reasoning depth, text rendering | $0.15/image (1K) |
| `fal-ai/gpt-image-1.5` | ~15s | Prompt adherence | $0.034/image |
| `fal-ai/gpt-image-2` | ~20s | SOTA text rendering + CJK, world-aware photorealism | $0.04–0.06/image |
| `fal-ai/ideogram/v3` | ~5s | Best typography | $0....

## Setup

:::tip Nous Subscribers
If you have a paid [Nous Portal](https://portal.nousresearch.com) subscription, you can use image generation through the **[Tool Gateway](tool-gateway.md)** without a FAL API key. Your model selection persists across both paths.

If the managed gateway returns `HTTP 4xx` for a specific model, that model isn't yet proxied on the portal side — the agent will tell you so, with remediation steps (set `FAL_KEY` for direct access, or pick a different model).
:::

### Get a FAL API Key

1. Sign up at [fal.ai](https://fal.ai/)
2. Generate an API key from your dashboard

### Con...

## Usage

The agent-facing schema is intentionally minimal — the model picks up whatever you've configured:

```
Generate an image of a serene mountain landscape with cherry blossoms
```

```
Create a square portrait of a wise old owl — use the typography model
```

```
Make me a futuristic cityscape, landscape orientation
```...

## Aspect Ratios

Every model accepts the same three aspect ratios from the agent's perspective. Internally, each model's native size spec is filled in automatically:

| Agent input | image_size (flux/z-image/qwen/recraft/ideogram) | aspect_ratio (nano-banana-pro) | image_size (gpt-image-1.5) | image_size (gpt-image-2) |
|---|---|---|---|---|
| `landscape` | `landscape_16_9` | `16:9` | `1536x1024` | `landscape_4_3` (1024×768) |
| `square` | `square_hd` | `1:1` | `1024x1024` | `square_hd` (1024×1024) |
| `portrait` | `portrait_16_9` | `9:16` | `1024x1536` | `portrait_4_3` (768×1024) |

GPT Image 2 maps to 4:3 pr...

## Automatic Upscaling

Upscaling via FAL's **Clarity Upscaler** is gated per-model:

| Model | Upscale? | Why |
|---|---|---|
| `fal-ai/flux-2-pro` | ✓ | Backward-compat (was the pre-picker default) |
| All others | ✗ | Fast models would lose their sub-second value prop; hi-res models don't need it |

When upscaling runs, it uses these settings:

| Setting | Value |
|---|---|
| Upscale factor | 2× |
| Creativity | 0.35 |
| Resemblance | 0.6 |
| Guidance scale | 4 |
| Inference steps | 18 |

If upscaling fails (network issue, rate limit), the original image is returned automatically....

## How It Works Internally

1. **Model resolution** — `_resolve_fal_model()` reads `image_gen.model` from `config.yaml`, falls back to the `FAL_IMAGE_MODEL` env var, then to `fal-ai/flux-2/klein/9b`.
2. **Payload building** — `_build_fal_payload()` translates your `aspect_ratio` into the model's native format (preset enum, aspect-ratio enum, or GPT literal), merges the model's default params, applies any caller overrides, then filters to the model's `supports` whitelist so unsupported keys are never sent.
3. **Submission** — `_submit_fal_request()` routes via direct FAL credentials or the managed Nous gateway.
4. **Upsca...

## Debugging

Enable debug logging:

```bash
export IMAGE_TOOLS_DEBUG=true
```

Debug logs go to `./logs/image_tools_debug_<session_id>.json` with per-call details (model, parameters, timing, errors)....

## Platform Delivery

| Platform | Delivery |
|---|---|
| **CLI** | Image URL printed as markdown `![](url)` — click to open |
| **Telegram** | Photo message with the prompt as caption |
| **Discord** | Embedded in a message |
| **Slack** | URL unfurled by Slack |
| **WhatsApp** | Media message |
| **Others** | URL in plain text |...

## Limitations

- **Requires FAL credentials** (direct `FAL_KEY` or Nous Subscription)
- **Text-to-image only** — no inpainting, img2img, or editing via this tool
- **Temporary URLs** — FAL returns hosted URLs that expire after hours/days; save locally if needed
- **Per-model constraints** — some models don't support `seed`, `num_inference_steps`, etc. The `supports` filter silently drops unsupported params; this is expected behavior...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
