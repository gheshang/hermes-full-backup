---
title: Optional Skills Catalog
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/reference-optional-skills-catalog.md]
---

# Optional Skills Catalog

源文档：[Optional Skills Catalog](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/optional-skills-catalog.md)

# Optional Skills Catalog

Optional skills ship with hermes-agent under `optional-skills/` but are **not active by default**. Install them explicitly:

```bash
hermes skills install official/<category>/<skill>
```

For example:

```bash
hermes skills install official/blockchain/solana
hermes skills install official/mlops/flash-attention
```

Each skill below links to a dedicated page with its full definition, setup, and usage.

To uninstall:

```bash
hermes skills uninstall <skill-name>
```

## autonomous-ai-agents

| Skill | Description |
|-------|-------------|
| [**blackbox**](/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-blackbox) | Delegate coding tasks to Blackbox AI CLI agent. Multi-model agent with built-in judge that runs tasks through multiple LLMs and picks the best result. Requires the blackbox CLI and a Blackbox AI API key. |
| [**honcho**](/docs/user-guide/skills/optional/autonomous-ai-agents/autonomous-ai-agents-honcho) | Configure and use Honcho memory with Hermes -- cross-session user modeling, multi-profile peer isolation, observation config, dialectic reason...

## blockchain

| Skill | Description |
|-------|-------------|
| [**base**](/docs/user-guide/skills/optional/blockchain/blockchain-base) | Query Base (Ethereum L2) blockchain data with USD pricing — wallet balances, token info, transaction details, gas analysis, contract inspection, whale detection, and live network stats. Uses Base RPC + CoinGecko. No API key required. |
| [**solana**](/docs/user-guide/skills/optional/blockchain/blockchain-solana) | Query Solana blockchain data with USD pricing — wallet balances, token portfolios with values, transaction details, NFTs, whale detection, and live network stat...

## communication

| Skill | Description |
|-------|-------------|
| [**one-three-one-rule**](/docs/user-guide/skills/optional/communication/communication-one-three-one-rule) | Structured decision-making framework for technical proposals and trade-off analysis. When the user faces a choice between multiple approaches (architecture decisions, tool selection, refactoring strategies, migration paths), this skill p... |...

## creative

| Skill | Description |
|-------|-------------|
| [**blender-mcp**](/docs/user-guide/skills/optional/creative/creative-blender-mcp) | Control Blender directly from Hermes via socket connection to the blender-mcp addon. Create 3D objects, materials, animations, and run arbitrary Blender Python (bpy) code. Use when user wants to create or modify anything in Blender. |
| [**concept-diagrams**](/docs/user-guide/skills/optional/creative/creative-concept-diagrams) | Generate flat, minimal light/dark-aware SVG diagrams as standalone HTML files, using a unified educational visual language with 9 seman...

## devops

| Skill | Description |
|-------|-------------|
| [**inference-sh-cli**](/docs/user-guide/skills/optional/devops/devops-cli) | Run 150+ AI apps via inference.sh CLI (infsh) — image generation, video creation, LLMs, search, 3D, social automation. Uses the terminal tool. Triggers: inference.sh, infsh, ai apps, flux, veo, image generation, video generation, seedrea... |
| [**docker-management**](/docs/user-guide/skills/optional/devops/devops-docker-management) | Manage Docker containers, images, volumes, networks, and Compose stacks — lifecycle ops, debugging, cleanup, and Dockerfile optimization...

## dogfood

| Skill | Description |
|-------|-------------|
| [**adversarial-ux-test**](/docs/user-guide/skills/optional/dogfood/dogfood-adversarial-ux-test) | Roleplay the most difficult, tech-resistant user for your product. Browse the app as that persona, find every UX pain point, then filter complaints through a pragmatism layer to separate real problems from noise. Creates actionable ticke... |...

## email

| Skill | Description |
|-------|-------------|
| [**agentmail**](/docs/user-guide/skills/optional/email/email-agentmail) | Give the agent its own dedicated email inbox via AgentMail. Send, receive, and manage email autonomously using agent-owned email addresses (e.g. hermes-agent@agentmail.to). |...

## health

| Skill | Description |
|-------|-------------|
| [**fitness-nutrition**](/docs/user-guide/skills/optional/health/health-fitness-nutrition) | Gym workout planner and nutrition tracker. Search 690+ exercises by muscle, equipment, or category via wger. Look up macros and calories for 380,000+ foods via USDA FoodData Central. Compute BMI, TDEE, one-rep max, macro splits, and body... |
| [**neuroskill-bci**](/docs/user-guide/skills/optional/health/health-neuroskill-bci) | Connect to a running NeuroSkill instance and incorporate the user's real-time cognitive and emotional state (focus, relaxation,...

## mcp

| Skill | Description |
|-------|-------------|
| [**fastmcp**](/docs/user-guide/skills/optional/mcp/mcp-fastmcp) | Build, test, inspect, install, and deploy MCP servers with FastMCP in Python. Use when creating a new MCP server, wrapping an API or database as MCP tools, exposing resources or prompts, or preparing a FastMCP server for Claude Code, Cur... |
| [**mcporter**](/docs/user-guide/skills/optional/mcp/mcp-mcporter) | Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation. |...

## migration

| Skill | Description |
|-------|-------------|
| [**openclaw-migration**](/docs/user-guide/skills/optional/migration/migration-openclaw-migration) | Migrate a user's OpenClaw customization footprint into Hermes Agent. Imports Hermes-compatible memories, SOUL.md, command allowlists, user skills, and selected workspace assets from ~/.openclaw, then reports exactly what could not be mig... |...

## mlops

| Skill | Description |
|-------|-------------|
| [**huggingface-accelerate**](/docs/user-guide/skills/optional/mlops/mlops-accelerate) | Simplest distributed training API. 4 lines to add distributed support to any PyTorch script. Unified API for DeepSpeed/FSDP/Megatron/DDP. Automatic device placement, mixed precision (FP16/BF16/FP8). Interactive config, single launch comm... |
| [**chroma**](/docs/user-guide/skills/optional/mlops/mlops-chroma) | Open-source embedding database for AI applications. Store embeddings and metadata, perform vector and full-text search, filter by metadata. Simple 4-...

## productivity

| Skill | Description |
|-------|-------------|
| [**canvas**](/docs/user-guide/skills/optional/productivity/productivity-canvas) | Canvas LMS integration — fetch enrolled courses and assignments using API token authentication. |
| [**memento-flashcards**](/docs/user-guide/skills/optional/productivity/productivity-memento-flashcards) | Spaced-repetition flashcard system. Create cards from facts or text, chat with flashcards using free-text answers graded by the agent, generate quizzes from YouTube transcripts, review due cards with adaptive scheduling, and export/impor... |
| [**siyuan**](/doc...

## research

| Skill | Description |
|-------|-------------|
| [**bioinformatics**](/docs/user-guide/skills/optional/research/research-bioinformatics) | Gateway to 400+ bioinformatics skills from bioSkills and ClawBio. Covers genomics, transcriptomics, single-cell, variant calling, pharmacogenomics, metagenomics, structural biology, and more. Fetches domain-specific reference material on... |
| [**domain-intel**](/docs/user-guide/skills/optional/research/research-domain-intel) | Passive domain reconnaissance using Python stdlib. Subdomain discovery, SSL certificate inspection, WHOIS lookups, DNS records, d...

## security

| Skill | Description |
|-------|-------------|
| [**1password**](/docs/user-guide/skills/optional/security/security-1password) | Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in, and reading/injecting secrets for commands. |
| [**oss-forensics**](/docs/user-guide/skills/optional/security/security-oss-forensics)

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
