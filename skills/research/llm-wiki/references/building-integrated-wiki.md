# Building Domain Wikis: Integration Pattern

> When to integrate a domain wiki into the main wiki vs. creating a separate subdirectory.

## Two Patterns

### Pattern A: Separate Subdirectory (Old Approach)
Create `~/wiki/<tool-name>/` with its own `SCHEMA.md`, `index.md`, `log.md`.

**Best for:**
- Standalone domain wiki you want to browse independently (e.g., in Obsidian as a separate vault)
- Domain has 50+ pages and needs its own navigation
- You want to share/sync this wiki separately from other knowledge

**Example:** `~/wiki/opencode/` — the original OpenCode wiki with 17 pages.

### Pattern B: Integrated into Main Wiki (New Approach)
Create entity/concept pages directly in the main wiki's `entities/` and `concepts/` directories.

**Best for:**
- Domain is related to your main wiki's focus (e.g., AI Agent tooling)
- You want cross-domain discovery (e.g., OpenCode concepts linking to Hermes concepts)
- The domain has <50 pages and doesn't need separate navigation
- You want a single source of truth across all knowledge

**Example:** `~/.hermes/wiki/` — OpenCode pages integrated alongside Hermes Agent, Claude Code, etc.

## Decision Matrix

| Factor | Separate Subdirectory | Integrated |
|--------|----------------------|------------|
| Page count | 50+ | <50 |
| Cross-domain links needed | No | Yes |
| Separate Obsidian vault | Yes | No |
| Shared with team separately | Yes | No |
| Part of larger knowledge ecosystem | No | Yes |

## Integrated Pattern: Session Checklist

For building a domain wiki integrated into the main wiki:

- [ ] **Check existing pages** — `search_files` for the domain name in `entities/` and `concepts/`
- [ ] **Read `index.md`** — see where the new pages fit in the existing structure
- [ ] **Read recent `log.md`** — understand recent activity and naming conventions
- [ ] **Create entity pages** in `entities/` with consistent frontmatter
- [ ] **Create concept pages** in `concepts/` with consistent frontmatter
- [ ] **Copy to `raw/articles/`** — maintain the immutable source layer
- [ ] **Update `index.md`** — add entries under correct sections (Entities/Concepts), update total count
- [ ] **Update `log.md`** — append batch ingestion entry
- [ ] **Verify cross-links** — each new page links to ≥2 existing pages (can be from other domains)
- [ ] **Check tag consistency** — use tags from the main wiki's SCHEMA.md taxonomy

## Frontmatter for Integrated Pages

```yaml
---
title: OpenCode
type: entity
tags: [opencode, ai-coding-agent, cli, tui, open-source]
related: [[opencode-cli-commands]], [[opencode-tui]], [[opencode-agents]], [[hermes-agent]]
---
```

Note the `related` field — it can link to pages in the same domain OR cross-domain (e.g., `[[hermes-agent]]`).

## Cross-Domain Linking Strategy

When integrating a domain wiki:
1. Link to **related concepts in the same domain** (e.g., `[[opencode-agents]]`)
2. Link to **related concepts in other domains** (e.g., `[[hermes-agent]]`, `[[mcp]]`)
3. Link to **comparisons** (e.g., `[[opencode-vs-claude-code]]`)
4. Use `related:` frontmatter to declare all cross-links explicitly

## Pitfalls

- **Don't duplicate** — check if the domain already has pages before creating new ones
- **Don't orphan** — every new page must link to ≥2 existing pages (cross-domain links count!)
- **Don't skip index.md** — integrated pages are invisible without index entries
- **Don't ignore SCHEMA.md** — even integrated wikis need tag taxonomy consistency
- **Don't mix patterns** — pick one pattern per domain; don't create both `~/wiki/opencode/` AND `~/.hermes/wiki/entities/opencode.md`

## Migration: Separate → Integrated

If you have a separate subdirectory wiki and want to integrate it:

1. Copy `entities/*.md` → main wiki `entities/`
2. Copy `concepts/*.md` → main wiki `concepts/`
3. Copy `comparisons/*.md` → main wiki `concepts/` (or create `comparisons/` in main wiki)
4. Copy `queries/*.md` → main wiki `concepts/`
5. Update all `[[wikilinks]]` to use the new slug format (no directory prefix needed)
6. Update `index.md` with all new entries
7. Update `log.md` with migration entry
8. Archive or delete the separate subdirectory
