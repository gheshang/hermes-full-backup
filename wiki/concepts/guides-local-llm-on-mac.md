---
title: Run Local LLMs on Mac
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-local-llm-on-mac.md]
---

# Run Local LLMs on Mac

源文档：[Run Local LLMs on Mac](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/local-llm-on-mac.md)

# Run Local LLMs on Mac

This guide walks you through running a local LLM server on macOS with an OpenAI-compatible API. You get full privacy, zero API costs, and surprisingly good performance on Apple Silicon.

We cover two backends:

| Backend | Install | Best at | Format |
|---------|---------|---------|--------|
| **llama.cpp** | `brew install llama.cpp` | Fastest time-to-first-token, quantized KV cache for low memory | GGUF |
| **omlx** | [omlx.ai](https://omlx.ai) | Fastest token generation, native Metal optimization | MLX (safetensors) |

Both expose an OpenAI-compatible `/v1/chat/completions` endpoint. Hermes works with either one — just point it at `http://localhost:8080` or `http://localhost:8000`.

:::info Apple Silicon only
This guide targets Macs with Apple Silicon (M1 and lat

## Choosing a model

For getting started, we recommend **Qwen3.5-9B** — it's a strong reasoning model that fits comfortably in 8GB+ of unified memory with quantization.

| Variant | Size on disk | RAM needed (128K context) | Backend |
|---------|-------------|---------------------------|---------|
| Qwen3.5-9B-Q4_K_M (GGUF) | 5.3 GB | ~10 GB with quantized KV cache | llama.cpp |
| Qwen3.5-9B-mlx-lm-mxfp4 (MLX) | ~5 GB | ~12 GB | omlx |

**Memory rule of thumb:** model size + KV cache. A 9B Q4 model is ~5 GB. The KV cache at 128K context with Q4 quantization adds ~4-5 GB. With default (f16) KV cache, that balloons ...

## Option A: llama.cpp

llama.cpp is the most portable local LLM runtime. On macOS it uses Metal for GPU acceleration out of the box.

### Install

```bash
brew install llama.cpp
```

This gives you the `llama-server` command globally.

### Download the model

You need a GGUF-format model. The easiest source is Hugging Face via the `huggingface-cli`:

```bash
brew install huggingface-cli
```

Then download:

```bash
huggingface-cli download unsloth/Qwen3.5-9B-GGUF Qwen3.5-9B-Q4_K_M.gguf --local-dir ~/models
```

:::tip Gated models
Some models on Hugging Face require authentication. Run `huggingface-cli login` first ...

## Option B: MLX via omlx

[omlx](https://omlx.ai) is a macOS-native app that manages and serves MLX models. MLX is Apple's own machine learning framework, optimized specifically for Apple Silicon's unified memory architecture.

### Install

Download and install from [omlx.ai](https://omlx.ai). It provides a GUI for model management and a built-in server.

### Download the model

Use the omlx app to browse and download models. Search for `Qwen3.5-9B-mlx-lm-mxfp4` and download it. Models are stored locally (typically in `~/.omlx/models/`).

### Start the server

omlx serves models on `http://127.0.0.1:8000` by default. S...

## Benchmarks: llama.cpp vs MLX

Both backends tested on the same machine (Apple M5 Max, 128 GB unified memory) running the same model (Qwen3.5-9B) at comparable quantization levels (Q4_K_M for GGUF, mxfp4 for MLX). Five diverse prompts, three runs each, backends tested sequentially to avoid resource contention.

### Results

| Metric | llama.cpp (Q4_K_M) | MLX (mxfp4) | Winner |
|--------|-------------------|-------------|--------|
| **TTFT (avg)** | **67 ms** | 289 ms | llama.cpp (4.3x faster) |
| **TTFT (p50)** | **66 ms** | 286 ms | llama.cpp (4.3x faster) |
| **Generation (avg)** | 70 tok/s | **96 tok/s** | MLX (37% fast...

## Connect to Hermes

Once your local server is running:

```bash
hermes model
```

Select **Custom endpoint** and follow the prompts. It will ask for the base URL and model name — use the values from whichever backend you set up above.

---...

## Timeouts

Hermes automatically detects local endpoints (localhost, LAN IPs) and relaxes its streaming timeouts. No configuration needed for most setups.

If you still hit timeout errors (e.g. very large contexts on slow hardware), you can override the streaming read timeout:

```bash
# In your .env — raise from the 120s default to 30 minutes
HERMES_STREAM_READ_TIMEOUT=1800
```

| Timeout | Default | Local auto-adjustment | Env var override |
|---------|---------|----------------------|------------------|
| Stream read (socket-level) | 120s | Raised to 1800s | `HERMES_STREAM_READ_TIMEOUT` |
| Stale strea...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
