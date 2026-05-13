---
title: Hermes Optional Skills Catalog
created: 2026-04-24
updated: 2026-05-07
type: entity
tags: [hermes, skills, catalog, optional]
sources: [raw/articles/hermes-optional-skills-catalog.md]
---

# Hermes Optional Skills Catalog

官方可选 skill，仓库内 `optional-skills/` 目录，**默认不启用**。需手动安装：

```bash
hermes skills install <skill-name>
```

卸载：`hermes skills uninstall <skill-name>`

共 **71 个 skill**，覆盖 **15 个分类**。

源文档：[Optional Skills Catalog](https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog)

## Autonomous AI Agents (2)

| Skill | 描述 |
|-------|------|
| `blackbox` | Delegate coding tasks to Blackbox AI CLI agent. Multi-model agent with built-in judge that runs tasks through multiple LLMs and picks the best result. |
| `honcho` | Configure and use Honcho memory with Hermes — cross-session user modeling, multi-profile peer isolation, observation config, and dialectic reasoning. |

## Blockchain (2)

| Skill | 描述 |
|-------|------|
| `base` | Query Base (Ethereum L2) blockchain data with USD pricing — wallet balances, token info, transaction details, gas analysis, contract inspection, whale detection, and live network stats. No API key required. |
| `solana` | Query Solana blockchain data with USD pricing — wallet balances, token portfolios with values, transaction details, NFTs, whale detection, and live network stats. No API key required. |

## Communication (1)

| Skill | 描述 |
|-------|------|
| `one-three-one-rule` | Structured communication framework for proposals and decision-making. |

## Creative (5)

| Skill | 描述 |
|-------|------|
| `blender-mcp` | Control Blender directly from Hermes via socket connection to the blender-mcp addon. Create 3D objects, materials, animations, and run arbitrary Blender Python (bpy) code. |
| `concept-diagrams` | Generate flat, minimal light/dark-aware SVG diagrams as standalone HTML files, using a unified educational visual language (9 semantic color ramps, automatic dark mode). Best for physics setups, chemistry mechanisms, math curves, physical objects (aircraft, turbines, smartphones), floor plans, cross-sections, lifecycle/process narratives, and hub-spoke system diagrams. Ships with 15 example diagrams. |
| `hyperframes` | Create animated HTML5 video from static images using GSAP — turn concept art, product renders, or illustrations into motion graphics with camera moves, parallax, and transitions. |
| `kanban-video-orchestrator` | Orchestrates video production pipelines using Kanban board — intake, script, assets, render, review stages with monitoring and role archetypes. |
| `meme-generation` | Generate real meme images by picking a template and overlaying text with Pillow. Produces actual .png meme files. |

## DevOps (2)

| Skill | 描述 |
|-------|------|
| `cli` | Run 150+ AI apps via inference.sh CLI (infsh) — image generation, video creation, LLMs, search, 3D, and social automation. |
| `docker-management` | Manage Docker containers, images, volumes, networks, and Compose stacks — lifecycle ops, debugging, cleanup, and Dockerfile optimization. |

## Dogfood (1)

| Skill | 描述 |
|-------|------|
| `adversarial-ux-test` | Roleplay the most difficult, tech-resistant user for a product — browse in-in persona, rant, then filter through a RED/YELLOW/WHITE/GREEN pragmatism layer so only real UX friction becomes tickets. |

## Email (1)

| Skill | 描述 |
|-------|------|
| `agentmail` | Give the agent its own dedicated email inbox via AgentMail. Send, receive, and manage email autonomously using agent-owned email addresses. |

## Finance (7) ⭐ NEW

| Skill | 描述 |
|-------|------|
| `3-statement-model` | Build integrated financial models with income statement, balance sheet, and cash flow statement — automated linking, variance analysis, and sensitivity tables. |
| `comps-analysis` | Comparable company analysis — screen peers, normalize financials, build trading multiples tables, and generate valuation summaries. |
| `dcf-model` | Discounted Cash Flow valuation — build full DCF models with WACC calculation, terminal value, sensitivity analysis, and football field charts. |
| `excel-author` | Professional Excel modeling — build financial models, dashboards, and reports with xlsxwriter. |
| `lbo-model` | Leveraged Buyout modeling — build LBO models with debt schedules, IRR analysis, and exit multiple scenarios. |
| `merger-model` | Merger & Acquisition accretion/dilution analysis — build merger models with purchase price allocation and pro forma financials. |
| `pptx-author` | Professional PowerPoint authoring — create pitch decks, financial presentations, and executive summaries with python-pptx. |

## Health (2)

| Skill | 描述 |
|-------|------|
| `fitness-nutrition` | Gym workout planner and nutrition tracker. Search 690+ exercises by muscle, equipment, or category via wger. Look up macros and calories for 380,000+ foods via USDA FoodData Central. Computes BMI, TDEE, one-rep max, macro splits, and body fat — pure Python, no pip installs. |
| `neuroskill-bci` | Brain-Computer Interface (BCI) integration for neuroscience research workflows. |

## MCP (2)

| Skill | 描述 |
|-------|------|
| `fastmcp` | Build, test, inspect, install, and deploy MCP servers with FastMCP in Python. Covers wrapping APIs or databases as MCP tools, exposing resources or prompts, and deployment. |
| `mcporter` | The mcporter CLI — list, configure, auth, and call MCP servers/tools directly (HTTP or stdio) from the terminal. Useful for ad-hoc MCP interactions; for always-on tool discovery use the built-in native-mcp client instead. |

## MLOps (25)

| Skill | 描述 |
|-------|------|
| `accelerate` | Simplest distributed training API. 4 lines to add distributed support to any PyTorch script. Unified API for DeepSpeed/FSDP/Megatron/DDP. |
| `chroma` | Open-source embedding database. Store embeddings and metadata, perform vector and full-text search. Simple 4-function API for RAG and semantic search. |
| `clip` | OpenAI's vision-language model connecting images and text. Zero-shot image classification, image-text matching, and cross-modal retrieval. Trained on 400M image-text pairs. |
| `faiss` | Facebook's library for efficient similarity search and clustering of dense vectors. Supports billions of vectors, GPU acceleration, and various index types. |
| `flash-attention` | Optimize transformer attention with Flash Attention for 2-4x speedup and 10-20x memory reduction. |
| `guidance` | Control LLM output with regex and grammars, guarantee valid JSON/XML/code generation, enforce structured formats, and build multi-step workflows with Guidance — Microsoft Research's constrained generation framework. |
| `hermes-atropos-environments` | Build, test, and debug Hermes Agent RL environments for Atropos training. Covers the HermesAgentBaseEnv interface, reward functions, agent loop integration, and evaluation. |
| `huggingface-tokenizers` | Fast Rust-based tokenizers for research and production. Tokenizes 1GB in under 20 seconds. |
| `instructor` | Extract structured data from LLM responses with Pydantic validation, retry failed extractions automatically, and stream partial results. |
| `lambda-labs` | Reserved and on-demand GPU cloud instances for ML training and inference. SSH access, persistent filesystems, and multi-node clusters. |
| `llava` | Large Language and Vision Assistant — visual instruction tuning and image-based conversations combining CLIP vision with LLaMA language models. |
| `modal` | Serverless GPU cloud platform for running ML workloads. On-demand GPU access without infrastructure management. |
| `nemo-curator` | GPU-accelerated data curation for LLM training. Fuzzy deduplication (16x faster), quality filtering (30+ heuristics), semantic dedup, PII redaction. |
| `peft` | Parameter-efficient fine-tuning for LLMs using LoRA, QLoRA, and 25+ methods. Train <1% of parameters with minimal accuracy loss. |
| `pinecone` | Managed vector database for production AI. Auto-scaling, hybrid search (dense + sparse), metadata filtering, and low latency. |
| `pytorch-fsdp` | Expert guidance for Fully Sharded Data Parallel training with PyTorch FSDP — parameter sharding, mixed precision, CPU offloading, FSDP2. |
| `pytorch-lightning` | High-level PyTorch framework with Trainer class, automatic distributed training (DDP/FSDP/DeepSpeed), callbacks, and minimal boilerplate. |
| `qdrant` | High-performance vector similarity search engine. Rust-powered with fast nearest neighbor search, hybrid search with filtering, and scalable vector storage. |
| `saelens` | Train and analyze Sparse Autoencoders (SAEs) using SAELens to decompose neural network activations into interpretable features. |
| `simpo` | Simple Preference Optimization — reference-free alternative to DPO with better performance (+6.4 pts on AlpacaEval 2.0). No reference model needed. |
| `slime` | LLM post-training with RL using Megatron+SGLang framework. Custom data generation workflows and tight Megatron-LM integration for RL scaling. |
| `stable-diffusion` | State-of-the-art text-to-image generation with Stable Diffusion via HuggingFace Diffusers. |
| `tensorrt-llm` | Optimize LLM inference with NVIDIA TensorRT for maximum throughput. 10-100x faster than PyTorch on A100/H100. |
| `torchtitan` | PyTorch-native distributed LLM pretraining with 4D parallelism (FSDP2, TP, PP, CP). Scale from 8 to 512+ GPUs. |
| `whisper` | OpenAI's general-purpose speech recognition. 99 languages, transcription, translation to English, and language ID. |

## Migration (1)

| Skill | 描述 |
|-------|------|
| `openclaw-migration` | Migrate a user's OpenClaw customization footprint into Hermes Agent. Imports memories, SOUL.md, command allowlists, user skills, and selected workspace assets. |

## Productivity (7)

| Skill | 描述 |
|-------|------|
| `canvas` | Canvas LMS integration — fetch enrolled courses and assignments using API token authentication. |
| `here-now` | Real-time location sharing and proximity awareness for team coordination. |
| `memento-flashcards` | Spaced repetition flashcard system for learning and knowledge retention. |
| `shop-app` | E-commerce shop management — product catalog, inventory, orders, and customer management. |
| `shopify` | Shopify store integration — manage products, orders, customers, and analytics via Shopify API. |
| `siyuan` | SiYuan Note API for searching, reading, creating, and managing blocks and documents in a self-hosted knowledge base. |
| `telephony` | Give Hermes phone capabilities — provision a Twilio number, send/receive SMS/MMS, make calls, and place AI-driven outbound calls through Bland.ai or Vapi. |

## Research (9)

| Skill | 描述 |
|-------|------|
| `bioinformatics` | Gateway to 400+ bioinformatics skills from bioSkills and ClawBio. |
| `domain-intel` | Passive domain reconnaissance using Python stdlib. Subdomain discovery, SSL certificate inspection, WHOIS lookups, DNS records, and bulk multi-domain analysis. No API keys required. |
| `drug-discovery` | Computational drug discovery workflows — molecular docking, virtual screening, and ADMET prediction. |
| `duckduckgo-search` | Free web search via DuckDuckGo — text, news, images, videos. No API key needed. |
| `gitnexus-explorer` | Index a codebase with GitNexus and serve an interactive knowledge graph via web UI and Cloudflare tunnel. |
| `parallel-cli` | Vendor skill for Parallel CLI — agent-native web search, extraction, deep research, enrichment, and monitoring. |
| `qmd` | Search personal knowledge bases, notes, docs, and meeting transcripts locally using qmd — a hybrid retrieval engine with BM25, vector search, and LLM reranking. |
| `scrapling` | Web scraping with Scrapling — HTTP fetching, stealth browser automation, Cloudflare bypass, and spider crawling via CLI and Python. |
| `searxng-search` | Self-hosted meta-search engine with privacy focus — aggregate results from 100+ search engines. |

## Security (3)

| Skill | 描述 |
|-------|------|
| `1password` | Set up and use 1Password CLI (op). Install the CLI, enable desktop app integration, sign in, and read/inject secrets for commands. |
| `oss-forensics` | Open-source software forensics — analyze packages, dependencies, and supply chain risks. |
| `sherlock` | OSINT username search across 400+ social networks. Hunt down social media accounts by username. |

## Web Development (1) ⭐ NEW

| Skill | 描述 |
|-------|------|
| `page-agent` | Autonomous web page creation and editing — build landing pages, blogs, and documentation with AI-assisted HTML/CSS/JS generation. |

## 与爬取能力相关的 Optional Skills

| Skill | 用途 |
|-------|------|
| `scrapling` | HTTP+隐身浏览器+Cloudflare绕过+爬虫，最强爬取 skill |
| `duckduckgo-search` | 免费搜索，无需 API key |
| `domain-intel` | 域名侦察，子域名/SSL/WHOIS/DNS |
| `parallel-cli` | 原生 web 搜索+提取+深度研究+监控 |
| `searxng-search` | 自托管元搜索引擎，聚合 100+ 搜索引擎 |

> 其中 `scrapling` 是提升爬取能力的关键 skill，已作为 bundled skill 安装。Optional 版本可能是更新的版本。

## 更新日志

### 2026-05-07
- **新增 Finance 分类**（7 个技能）：3-statement-model, comps-analysis, dcf-model, excel-author, lbo-model, merger-model, pptx-author
- **新增 Web Development 分类**（1 个技能）：page-agent
- **Creative 扩展**：新增 hyperframes, kanban-video-orchestrator
- **Productivity 扩展**：新增 here-now, shop-app, shopify
- **Research 扩展**：新增 drug-discovery, searxng-search
- **总计从 57 个增至 71 个**

## 关联

- [[hermes-bundled-skills-catalog]] — 默认打包的 87 个 skill
- [[hermes-agent]] — 框架本体
