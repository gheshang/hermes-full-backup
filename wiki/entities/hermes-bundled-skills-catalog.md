---
title: Hermes Bundled Skills Catalog
created: 2026-04-24
updated: 2026-04-24
type: entity
tags: [hermes, skills, catalog, reference]
sources: [raw/articles/hermes-bundled-skills-catalog.md]
---

# Hermes Bundled Skills Catalog

官方打包的内置skill库，安装时复制到 `~/.hermes/skills/`。共 **87 个skill**，覆盖 **28 个分类**。

源文档：[Bundled Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/skills-catalog)


## apple (4)

| Skill | 描述 | 路径 |
|-------|------|------|
| `apple-notes` | Manage Apple Notes via the memo CLI on macOS (create, view, search, edit). | `apple/apple-notes` |
| `apple-reminders` | Manage Apple Reminders via remindctl CLI (list, add, complete, delete). | `apple/apple-reminders` |
| `findmy` | Track Apple devices and AirTags via FindMy.app on macOS using AppleScript and screen capture. | `apple/findmy` |
| `imessage` | Send and receive iMessages/SMS via the imsg CLI on macOS. | `apple/imessage` |

## autonomous-ai-agents (5)

| Skill | 描述 | 路径 |
|-------|------|------|
| `claude-code` | Delegate coding tasks to Claude Code (Anthropic's CLI agent). Use for building features, refactoring, PR reviews, and iterative coding. Requires the claude CLI installed. | `autonomous-ai-agents/claude-code` |
| `codex` | Delegate coding tasks to OpenAI Codex CLI agent. Use for building features, refactoring, PR reviews, and batch issue fixing. Requires the codex CLI and a git repository. | `autonomous-ai-agents/codex` |
| `hermes-agent` | Complete guide to using and extending Hermes Agent — CLI usage, setup, configuration, spawning additional agents, gateway platforms, skills, voice, tools, profiles, and a concise contributor reference. | `autonomous-ai-agents/hermes-agent` |
| `opencode` | Delegate coding tasks to OpenCode CLI agent for feature implementation, refactoring, PR review, and long-running autonomous sessions. | `autonomous-ai-agents/opencode` |
| `blackbox` | Delegate coding tasks to Blackbox AI CLI agent. Multi-model agent with built-in judge that runs tasks through multiple LLMs and picks the best result. | `autonomous-ai-agents/blackbox` |

## blockchain (2)

| Skill | 描述 | 路径 |
|-------|------|------|
| `base` | Query Base (Ethereum L2) blockchain data with USD pricing — wallet balances, token info, transaction details, gas analysis, contract inspection, whale detection, and live network stats. | `blockchain/base` |
| `solana` | Query Solana blockchain data with USD pricing — wallet balances, token portfolios with values, transaction details, NFTs, whale detection, and live network stats. | `blockchain/solana` |

## creative (12)

| Skill | 描述 | 路径 |
|-------|------|------|
| `architecture-diagram` | Generate dark-themed SVG diagrams of software systems and cloud infrastructure as standalone HTML files with inline SVG graphics. | `creative/architecture-diagram` |
| `ascii-art` | Generate ASCII art using pyfiglet (571 fonts), cowsay, boxes, toilet, image-to-ascii, remote APIs, and LLM fallback. No API keys required. | `creative/ascii-art` |
| `ascii-video` | Production pipeline for ASCII art video — any format. Converts video/audio/images/generative input into colored ASCII character video output. | `creative/ascii-video` |
| `blender-mcp` | Control Blender directly from Hermes via socket connection to the blender-mcp addon. Create 3D objects, materials, animations, and run arbitrary Blender Python (bpy) code. | `creative/blender-mcp` |
| `excalidraw` | Create hand-drawn style diagrams using Excalidraw JSON format. | `creative/excalidraw` |
| `ideation` | Generate project ideas through creative constraints. | `creative/creative-ideation` |
| `manim-video` | Production pipeline for mathematical and technical animations using Manim Community Edition. Creates 3Blue1Brown-style explainer videos. | `creative/manim-video` |
| `meme-generation` | Generate real meme images by picking a template and overlaying text with Pillow. Produces actual .png meme files. | `creative/meme-generation` |
| `p5js` | Production pipeline for interactive and generative visual art using p5.js. | `creative/p5js` |
| `popular-web-designs` | 54 production-quality design systems extracted from real websites. Load a template to generate HTML/CSS that matches the visual identity of sites like Stripe, Linear, Vercel, Notion, Airbnb, and more. | `creative/popular-web-designs` |
| `songwriting-and-ai-music` | Songwriting craft, AI music generation prompts (Suno focus), parody/adaptation techniques, phonetic tricks, and lessons learned. | `creative/songwriting-and-ai-music` |
| `touchdesigner-mcp` | Control a running TouchDesigner instance via the twozero MCP plugin — create operators, set parameters, wire connections, execute Python, build real-time audio-reactive visuals and GLSL networks. 36 native tools. | `creative/touchdesigner-mcp` |

## data-science (1)

| Skill | 描述 | 路径 |
|-------|------|------|
| `jupyter-live-kernel` | Use a live Jupyter kernel for stateful, iterative Python execution via hamelnb. Load this skill when the task involves exploration, iteration, or inspecting intermediate results. | `data-science/jupyter-live-kernel` |

## devops (2)

| Skill | 描述 | 路径 |
|-------|------|------|
| `webhook-subscriptions` | Create and manage webhook subscriptions for event-driven agent activation. | `devops/webhook-subscriptions` |
| `docker-management` | Manage Docker containers, images, volumes, networks, and Compose stacks — lifecycle ops, debugging, cleanup, and Dockerfile optimization. | `devops/docker-management` |

## dogfood (2)

| Skill | 描述 | 路径 |
|-------|------|------|
| `dogfood` | Systematic exploratory QA testing of web applications — find bugs, capture evidence, and generate structured reports. | `dogfood` |
| `adversarial-ux-test` | Roleplay the most difficult, tech-resistant user for a product — browse in-persona, rant, then filter through a RED/YELLOW/WHITE/GREEN pragmatism layer so only real UX friction becomes tickets. | `dogfood/adversarial-ux-test` |

## email (2)

| Skill | 描述 | 路径 |
|-------|------|------|
| `himalaya` | CLI to manage emails via IMAP/SMTP. Use himalaya to list, read, write, reply, forward, search, and organize emails from the terminal. | `email/himalaya` |
| `agentmail` | Give the agent its own dedicated email inbox via AgentMail. Send, receive, and manage email autonomously using agent-owned email addresses. | `email/agentmail` |

## gaming (2)

| Skill | 描述 | 路径 |
|-------|------|------|
| `minecraft-modpack-server` | Set up a modded Minecraft server from a CurseForge/Modrinck server pack zip. | `gaming/minecraft-modpack-server` |
| `pokemon-player` | Play Pokemon games autonomously via headless emulation. | `gaming/pokemon-player` |

## github (6)

| Skill | 描述 | 路径 |
|-------|------|------|
| `codebase-inspection` | Inspect and analyze codebases using pygount for LOC counting, language breakdown, and code-vs-comment ratios. | `github/codebase-inspection` |
| `github-auth` | Set up GitHub authentication for the agent using git or the gh CLI. Covers HTTPS tokens, SSH keys, credential helpers, and gh auth. | `github/github-auth` |
| `github-code-review` | Review code changes by analyzing git diffs, leaving inline comments on PRs, and performing thorough pre-push review. | `github/github-code-review` |
| `github-issues` | Create, manage, triage, and close GitHub issues. Search existing issues, add labels, assign people, and link to PRs. | `github/github-issues` |
| `github-pr-workflow` | Full pull request lifecycle — create branches, commit changes, open PRs, monitor CI status, auto-fix failures, and merge. | `github/github-pr-workflow` |
| `github-repo-management` | Clone, create, fork, configure, and manage GitHub repositories. | `github/github-repo-management` |

## health (1)

| Skill | 描述 | 路径 |
|-------|------|------|
| `neuroskill-bci` | Connect to a running NeuroSkill instance and incorporate the user's real-time cognitive and emotional state into responses. Requires a BCI wearable. | `health/neuroskill-bci` |

## mcp (2)

| Skill | 描述 | 路径 |
|-------|------|------|
| `native-mcp` | Built-in MCP (Model Context Protocol) client that connects to external MCP servers, discovers their tools, and registers them as native Hermes Agent tools. | `mcp/native-mcp` |
| `fastmcp` | Build, test, inspect, install, and deploy MCP servers with FastMCP in Python. | `mcp/fastmcp` |

## media (4)

| Skill | 描述 | 路径 |
|-------|------|------|
| `gif-search` | Search and download GIFs from Tenor using curl. No dependencies beyond curl and jq. | `media/gif-search` |
| `heartmula` | Set up and run HeartMuLa, the open-source music generation model family (Suno-like). Generates full songs from lyrics + tags with multilingual support. | `media/heartmula` |
| `songsee` | Generate spectrograms and audio feature visualizations from audio files via CLI. | `media/songsee` |
| `youtube-content` | Fetch YouTube video transcripts and transform them into structured content (chapters, summaries, threads, blog posts). | `media/youtube-content` |

## migration (1)

| Skill | 描述 | 路径 |
|-------|------|------|
| `openclaw-migration` | Migrate a user's OpenClaw customization footprint into Hermes Agent. Imports memories, SOUL.md, command allowlists, user skills, and selected workspace assets. | `migration/openclaw-migration` |

## mlops (1)

| Skill | 描述 | 路径 |
|-------|------|------|
| `huggingface-hub` | Hugging Face Hub CLI (hf) — search, download, and upload models and datasets, manage repos, query datasets with SQL, deploy inference endpoints. | `mlops/huggingface-hub` |

## mlops/evaluation (2)

| Skill | 描述 | 路径 |
|-------|------|------|
| `evaluating-llms-harness` | Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Industry standard used by EleutherAI, HuggingFace, and major labs. | `mlops/evaluation/lm-evaluation-harness` |
| `weights-and-biases` | Track ML experiments with automatic logging, visualize training in real-time, optimize hyperparameters with sweeps, and manage model registry with W&B. | `mlops/evaluation/weights-and-biases` |

## mlops/inference (4)

| Skill | 描述 | 路径 |
|-------|------|------|
| `llama-cpp` | Run LLM inference with llama.cpp on CPU, Apple Silicon, AMD/Intel GPUs, or NVIDIA — plus GGUF model conversion and quantization. | `mlops/inference/llama-cpp` |
| `obliteratus` | Remove refusal behaviors from open-weight LLMs using OBLITERATUS — mechanistic interpretability techniques to excise guardrails while preserving reasoning. | `mlops/inference/obliteratus` |
| `outlines` | Guarantee valid JSON/XML/code structure during generation with Pydantic models for type-safe outputs. | `mlops/inference/outlines` |
| `serving-llms-vllm` | Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching. | `mlops/inference/vllm` |

## mlops/models (2)

| Skill | 描述 | 路径 |
|-------|------|------|
| `audiocraft-audio-generation` | PyTorch library for audio generation including text-to-music (MusicGen) and text-to-sound (AudioGen). | `mlops/models/audiocraft` |
| `segment-anything-model` | Foundation model for image segmentation with zero-shot transfer. | `mlops/models/segment-anything` |

## mlops/research (1)

| Skill | 描述 | 路径 |
|-------|------|------|
| `dspy` | Build complex AI systems with declarative programming, optimize prompts automatically, create modular RAG systems and agents with DSPy. | `mlops/research/dspy` |

## mlops/training (3)

| Skill | 描述 | 路径 |
|-------|------|------|
| `axolotl` | Expert guidance for fine-tuning LLMs with Axolotl - YAML configs, 100+ models, LoRA/QLoRA, DPO/KTO/ORPO/GRPO, multimodal support. | `mlops/training/axolotl` |
| `fine-tuning-with-trl` | Fine-tune LLMs using reinforcement learning with TRL - SFT, DPO, PPO/GRPO, and reward model training. | `mlops/training/trl-fine-tuning` |
| `unsloth` | Expert guidance for fast fine-tuning with Unsloth - 2-5x faster training, 50-80% less memory, LoRA/QLoRA optimization. | `mlops/training/unsloth` |

## note-taking (1)

| Skill | 描述 | 路径 |
|-------|------|------|
| `obsidian` | Read, search, and create notes in the Obsidian vault. | `note-taking/obsidian` |

## productivity (8)

| Skill | 描述 | 路径 |
|-------|------|------|
| `google-workspace` | Gmail, Calendar, Drive, Contacts, Sheets, and Docs integration for Hermes. Uses Hermes-managed OAuth2 setup. | `productivity/google-workspace` |
| `linear` | Manage Linear issues, projects, and teams via the GraphQL API. All operations via curl — no dependencies. | `productivity/linear` |
| `maps` | Location intelligence — geocode, reverse-geocode, nearby POI search, driving/walking/cycling distance + time, turn-by-turn directions. Uses OpenStreetMap + Overpass + OSRM. No API key needed. | `productivity/maps` |
| `nano-pdf` | Edit PDFs with natural-language instructions using the nano-pdf CLI. | `productivity/nano-pdf` |
| `notion` | Notion API for creating and managing pages, databases, and blocks via curl. | `productivity/notion` |
| `ocr-and-documents` | Extract text from PDFs and scanned documents. Use web_extract for remote URLs, pymupdf for local text-based PDFs, marker-pdf for OCR/scanned docs. | `productivity/ocr-and-documents` |
| `powerpoint` | Use this skill any time a .pptx file is involved in any way — as input, output, or both. | `productivity/powerpoint` |
| `telephony` | Give Hermes phone capabilities — provision and persist a Twilio number, send and receive SMS/MMS, make direct calls, and place AI-driven outbound calls through Bland.ai or Vapi. | `productivity/telephony` |

## red-teaming (1)

| Skill | 描述 | 路径 |
|-------|------|------|
| `godmode` | Jailbreak API-served LLMs using G0DM0D3 techniques — Parseltongue input obfuscation (33 techniques), GODMODE CLASSIC system prompt templates, ULTRAPLINIAN multi-model racing, encoding escalation. | `red-teaming/godmode` |

## research (7)

| Skill | 描述 | 路径 |
|-------|------|------|
| `arxiv` | Search and retrieve academic papers from arXiv using their free REST API. No API key needed. | `research/arxiv` |
| `bioinformatics` | Gateway to 400+ bioinformatics skills from bioSkills and ClawBio. Covers genomics, transcriptomics, single-cell, variant calling, pharmacogenomics, metagenomics, structural biology, and more. | `research/bioinformatics` |
| `blogwatcher` | Monitor blogs and RSS/Atom feeds for updates using the blogwatcher-cli tool. | `research/blogwatcher` |
| `llm-wiki` | Karpathy's LLM Wiki — build and maintain a persistent, interlinked markdown knowledge base. | `research/llm-wiki` |
| `polymarket` | Query Polymarket prediction market data — search markets, get prices, orderbooks, and price history. No API key needed. | `research/polymarket` |
| `research-paper-writing` | End-to-end pipeline for writing ML/AI research papers — from experiment design through analysis, drafting, revision, and submission. | `research/research-paper-writing` |
| `qmd` | Search personal knowledge bases, notes, docs, and meeting transcripts locally using qmd — a hybrid retrieval engine with BM25, vector search, and LLM reranking. | `research/qmd` |

## security (3)

| Skill | 描述 | 路径 |
|-------|------|------|
| `1password` | Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in, and reading/injecting secrets for commands. | `security/1password` |
| `oss-forensics` | Supply chain investigation, evidence recovery, and forensic analysis for GitHub repositories. Covers deleted commit recovery, force-push detection, IOC extraction. | `security/oss-forensics` |
| `sherlock` | OSINT username search across 400+ social networks. Hunt down social media accounts by username. | `security/sherlock` |

## smart-home (1)

| Skill | 描述 | 路径 |
|-------|------|------|
| `openhue` | Control Philips Hue lights, rooms, and scenes via the OpenHue CLI. | `smart-home/openhue` |

## social-media (1)

| Skill | 描述 | 路径 |
|-------|------|------|
| `xurl` | Interact with X/Twitter via xurl, the official X API CLI. Use for posting, replying, quoting, searching, timelines, mentions, likes, reposts, bookmarks, follows, DMs, media upload. | `social-media/xurl` |

## software-development (6)

| Skill | 描述 | 路径 |
|-------|------|------|
| `plan` | Plan mode for Hermes — inspect context, write a markdown plan into the active workspace's .hermes/plans/ directory, and do not execute the work. | `software-development/plan` |
| `requesting-code-review` | Pre-commit verification pipeline — static security scan, baseline-aware quality gates, independent reviewer subagent, and auto-fix loop. | `software-development/requesting-code-review` |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks. Dispatches fresh delegate_task per task with two-stage review. | `software-development/subagent-driven-development` |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior. 4-phase root cause investigation. | `software-development/systematic-debugging` |
| `test-driven-development` | Use when implementing any feature or bugfix, before writing implementation code. Enforces RED-GREEN-REFACTOR cycle. | `software-development/test-driven-development` |
| `writing-plans` | Use when you have a spec or requirements for a multi-step task. Creates comprehensive implementation plans with bite-sized tasks, exact file paths, and complete code examples. | `software-development/writing-plans` |
