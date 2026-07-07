# Building OpenCode Wiki — Proven Pattern

> Session: 2026-05-14 | Target: OpenCode CLI knowledge base (76 files)
> Outcome: Full wiki built in 3 rounds, user confirmed "继续爬取" after round 1, then "插件系统还有企业部署的方面" after round 2

## Decision: Separate Subdirectory vs. Integrated

For OpenCode, we used **integrated into main wiki** (`~/.hermes/wiki/entities/` and `~/.hermes/wiki/concepts/`), NOT a separate subdirectory.

**Reasoning:**
- User already has an established wiki at `~/.hermes/wiki/` with 175+ existing pages
- OpenCode is an AI coding agent — closely related to Hermes Agent (the wiki's primary domain)
- Cross-linking between Hermes and OpenCode pages is valuable (e.g., `[[opencode]]` ↔ `[[hermes-agent]]`)
- Separate subdirectory would fragment the knowledge base

**When to use separate subdirectory instead:**
- The tool is unrelated to the wiki's existing domain
- The wiki is very large (>500 pages) and domain separation improves navigation
- The wiki is a dedicated single-tool wiki from the start

## Round-Based Crawling Pattern

### Round 1: Overview + Core Entities
**Goal:** Establish the wiki skeleton with essential reference pages.

**Sources:**
- Official docs homepage (`opencode.ai/`)
- CLI reference (`opencode.ai/docs/cli/`)
- Cheat sheets (`cheatsheets.zip/opencode`)
- High-level comparisons (vs Claude Code)

**Pages created (8 entities + 5 concepts):**
- Entity: overview, CLI commands, TUI, agents, MCP, configuration, installation, comparison
- Concept: quickstart, config guide, TUI guide, agents guide, MCP integration

**Signal for continuation:** User says "文档不止这么少，继续爬取" → proceed to Round 2.

### Round 2: Deep Dive into Specific Sections
**Goal:** Fill gaps in coverage based on what Round 1 revealed.

**Sources:**
- TUI docs (`opencode.ai/docs/tui/`) — slash commands, keybinds, editor setup
- Providers (`opencode.ai/docs/providers/`) — 75+ LLM providers
- Go subscription (`opencode.ai/docs/go/`) — pricing, limits, models
- Zen (`opencode.ai/docs/zen/`) — curated models, pricing, privacy
- Share (`opencode.ai/docs/share/`) — sharing modes, privacy
- GitHub (`opencode.ai/docs/github/`) — CI/CD integration
- Tools (`opencode.ai/docs/tools/`) — 12 built-in tools
- Rules (`opencode.ai/docs/rules/`) — AGENTS.md, precedence
- Permissions (`opencode.ai/docs/permissions/`) — allow/ask/deny
- LSP (`opencode.ai/docs/lsp/`) — 30+ language servers
- Models (`opencode.ai/docs/models/`) — variants, loading priority
- Web (`opencode.ai/docs/web/`) — browser interface
- IDE (`opencode.ai/docs/ide/`) — VS Code/Cursor integration
- ACP (`opencode.ai/docs/acp/`) — Zed/JetBrains/Avante
- Skills (`opencode.ai/docs/skills/`) — SKILL.md format
- Custom tools (`opencode.ai/docs/custom-tools/`) — TypeScript definitions
- Commands (`opencode.ai/docs/commands/`) — custom commands

**Pages created (8 entities + 9 concepts):**
- Entity: tools, rules, permissions, LSP, commands, models, share, GitHub
- Concept: custom commands, models/providers, session sharing, GitHub integration, web interface, IDE integration, ACP support, agent skills, custom tools

### Round 3: Advanced Topics (Plugins, Enterprise, SDK)
**Goal:** Cover advanced/enterprise-level topics the user specifically requested.

**Sources:**
- Plugins (`opencode.ai/docs/plugins/`) — event hooks, creation, examples
- Enterprise (`opencode.ai/docs/enterprise/`) — SSO, central config, self-hosting
- Ecosystem (`opencode.ai/docs/ecosystem/`) — 30+ community plugins
- SDK (`opencode.ai/docs/sdk/`) — TypeScript client, API reference

**Pages created (4 entities + 4 concepts):**
- Entity: plugins, enterprise, ecosystem, SDK
- Concept: plugins guide, enterprise deployment, ecosystem overview, SDK usage

**Key insight:** Round 3 was user-directed ("插件系统还有企业部署的方面"). Always wait for user signals before expanding beyond core docs — don't assume advanced topics are needed.

## Entity-First, Concept-Second Workflow

### Step 1: Create Entity Pages
Entity pages are comprehensive reference documents. They serve as the canonical source for each topic.

**Structure:**
```markdown
---
title: <Topic>
type: entity
tags: [opencode, <topic-specific-tags>]
related: [[opencode]], [[related-page-1]], [[related-page-2]]
---

# <Topic>

## Overview
Brief description (2-3 sentences).

## Key Sections
- Detailed breakdown with tables, code examples, configs
- Each subsection has a clear heading
- Include actual config snippets, not just descriptions
```

**Tips:**
- Include actual config JSON/YAML snippets from the docs
- Tables are preferred over long lists for comparisons
- Cross-link to other entity pages via `[[wikilinks]]`
- Keep each entity page under 200 lines

### Step 2: Create Concept Pages
Concept pages are condensed guides for quick reference. They summarize the entity page with actionable info.

**Structure:**
```markdown
---
title: <Topic>
type: concept
tags: [opencode, <topic-specific-tags>]
related: [[opencode]], [[opencode-<topic>]]
---

# <Topic>

## Overview
One-sentence summary.

## Quick Reference
- Bullet points, not paragraphs
- Key commands, configs, shortcuts
- "When to use" guidance
```

**Tips:**
- Concept pages should be scannable in 30 seconds
- Point to the entity page for deep dives
- Focus on "how to" not "what is"

### Step 3: Copy to raw/articles/
```bash
cp entities/opencode-*.md raw/articles/
cp concepts/opencode-*.md raw/articles/
```

This creates immutable source copies for future re-ingestion and drift detection.

### Step 4: Update index.md
Add entries under the correct section (Entities/Concepts), alphabetically within each section.

```markdown
- [[opencode-tools]] — OpenCode 内置工具参考，bash/edit/read/grep/glob/lsp/skill 等 12 种工具。
```

Update the header: `Total pages: N → N+X` and `Last updated: YYYY-MM-DD`.

### Step 5: Update log.md
Append an entry:
```markdown
## [2026-05-14] ingest | OpenCode 第二轮深度爬取
- 来源：opencode.ai/docs 官网文档（TUI/Providers/Go/Zen/Share/GitHub/Tools/Rules...）
- 构建内容：
  - **Entities (8)**: opencode-tools, opencode-rules, ...
  - **Concepts (9)**: opencode-custom-commands, opencode-models-providers, ...
  - **Raw articles (17)**: 所有 entity 和 concept 的原始副本
- 更新 index.md：Entities 新增 8 条，Concepts 新增 9 条
```

## Handling web_extract Truncation

**Problem:** Large docs pages (>5000 chars) get LLM-summarized by web_extract, losing structure.

**Solution used in this session:**
1. First, try `web_extract` — get what you can
2. If truncated, use `web_search` to find specific sub-pages
3. Extract each sub-page individually
4. Synthesize from multiple partial sources

**Example:** The providers page (59K chars) was truncated. We used web_search to find individual provider docs, then web_extract on smaller pages.

**Alternative for future:** If the docs site is built from a public GitHub repo, use `curl` to pull raw `.md` files directly (no truncation).

## Cross-Linking Discipline

Every new page must have:
- **Minimum 2 outbound wikilinks** in the body
- **`related` frontmatter** listing 2-4 related pages
- **Back-links:** When creating page B that references page A, also update page A's `related` to include page B

**Pattern:**
```
opencode (entity) ←→ opencode-cli-commands (entity)
opencode (entity) ←→ opencode-tui (entity)
opencode-tui (entity) ←→ opencode-tui-guide (concept)
opencode-agents (entity) ←→ opencode-agents-guide (concept)
opencode-agents (entity) ←→ opencode-agent-skills (concept)
```

## Final Stats

| Category | Round 1 | Round 2 | Round 3 | Total |
|----------|---------|---------|---------|-------|
| Entities | 8 | 8 | 4 | **20** |
| Concepts | 5 | 9 | 4 | **18** |
| Raw articles | 13 | 17 | 8 | **38** |
| **Total** | **26** | **34** | **16** | **76** |

Total wiki pages: 175 → 226 (+51 pages, including non-OpenCode updates from the session)
