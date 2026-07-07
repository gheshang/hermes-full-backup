# Building Domain Wikis: OpenCode CLI Pattern

## Session Context
Successfully built a comprehensive OpenCode CLI knowledge base at `~/wiki/opencode/` in a single session. This pattern can be reused for other CLI tools, frameworks, or technical domains.

## What Worked

### 1. Source Collection Strategy
- **Official docs first**: opencode.ai/docs/cli/, GitHub READMEs
- **Community sources**: Reddit r/opencodeCLI, comparison articles
- **Technical deep dives**: glukhov.org guides, HackMD community docs
- **Use `web_extract` for URLs**, `web_search` for discovery

### 2. Wiki Structure (Proven)
```
~/wiki/opencode/
├── SCHEMA.md           # Domain-specific conventions
├── index.md            # Content catalog with summaries
├── log.md              # Chronological action log
├── entities/           # 3 pages: opencode-cli, crush-ai, anomalyco-opencode
├── concepts/           # 9 pages: architecture, providers, sessions, tools, etc.
├── comparisons/        # 3 pages: vs Claude Code, vs Codex, vs Aider
├── queries/            # 2 pages: usage tips, workflow best practices
└── raw/articles/       # 10 source documents with frontmatter
```

### 3. Key Decisions
- **Entity pages** for tools/projects with multiple facets (CLI, successor, fork)
- **Concept pages** for mechanisms (architecture, providers, sessions, tools, MCP, LSP, permissions, custom commands)
- **Comparison pages** for decision-making context
- **Query pages** for practical guidance (tips, best practices)
- **Raw sources** with `sha256` frontmatter for drift detection

### 4. Cross-Linking
- Every concept page links to at least 2 other pages
- Entity pages link to related concepts and comparisons
- Query pages link to relevant concepts and entities
- Uses `[[wikilinks]]` format for Obsidian compatibility

### 5. Frontmatter Consistency
All wiki pages include:
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy]
sources: [raw/articles/source-name.md]
confidence: high | medium | low
---
```

## Lessons Learned

### 1. Start with SCHEMA.md
Define the domain, tag taxonomy, and conventions BEFORE creating content pages. This prevents tag sprawl and inconsistent structure.

### 2. Index First, Then Content
Create `index.md` with placeholder entries, then fill in pages. This gives you a map to work from and ensures nothing is missed.

### 3. Batch Source Ingestion
Collect all sources first, then create/update pages in one pass. Avoids redundant updates and ensures comprehensive coverage.

### 4. Update index.md and log.md After Each Batch
These are the navigational backbone. Skipping updates makes the wiki degrade over time.

### 5. Confidence Levels Matter
For fast-moving domains (AI tools), set `confidence: medium` for single-source claims. Don't mark `high` unless corroborated.

## Template: SCHEMA.md for CLI Tool Wikis

```markdown
# Wiki Schema — [Tool Name]

## Domain
[What this wiki covers — e.g., "[Tool] CLI, its ecosystem, and comparisons"]

## Conventions
- File names: lowercase, hyphens, no spaces
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]`

## Tag Taxonomy
- **Core**: [tool], cli, [key-feature-1], [key-feature-2]
- **Architecture**: [architecture-concept-1], [architecture-concept-2]
- **Features**: [feature-1], [feature-2], [feature-3]
- **Integration**: [integration-1], [integration-2]
- **Comparison**: [competitor-1], [competitor-2], comparison
- **Usage**: workflow, tips, tricks, best-practices, pitfalls
- **Platform**: linux, macos, windows, wsl

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions, minor details, or things outside the domain
- **Split a page** when it exceeds ~200 lines
- **Archive a page** when its content is fully superseded

## Update Policy
When new information conflicts with existing content:
1. Check the dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark the contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in the lint report
```

## Reuse Checklist

For building a new domain wiki:

- [ ] Create directory structure (`entities/`, `concepts/`, `comparisons/`, `queries/`, `raw/articles/`)
- [ ] Write `SCHEMA.md` with domain-specific tag taxonomy
- [ ] Write initial `index.md` with section headers
- [ ] Write initial `log.md` with creation entry
- [ ] Search and collect sources (official docs, community, comparisons)
- [ ] Ingest sources to `raw/articles/` with frontmatter
- [ ] Create entity pages for main tools/projects
- [ ] Create concept pages for mechanisms and features
- [ ] Create comparison pages for decision context
- [ ] Create query pages for practical guidance
- [ ] Update `index.md` with all pages
- [ ] Update `log.md` with all actions
- [ ] Verify cross-links (each page has 2+ outbound wikilinks)
