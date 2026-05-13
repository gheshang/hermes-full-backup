# Wiki Schema

## Domain
AI Agent 技术栈 — 爬虫工具、LLM应用、开源Agent框架、自部署基础设施

## Conventions
- File names: lowercase, hyphens, no spaces (e.g., `transformer-architecture.md`)
- Every wiki page starts with YAML frontmatter
- Use `[[wikilinks]]` to link between pages (minimum 2 outbound links per page)
- When updating a page, always bump the `updated` date
- Every new page must be added to `index.md` under the correct section
- Every action must be appended to `log.md`
- **Provenance markers:** On pages that synthesize 3+ sources, append `^[raw/articles/source-file.md]` at the end of paragraphs whose claims come from a specific source.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
confidence: high | medium | low
contested: true  # optional
contradictions: [other-page-slug]  # optional
---
```

## Tag Taxonomy
- Tools: scraper, crawler, browser, proxy, anti-bot, llm, agent, framework
- Infrastructure: self-hosted, docker, vps, deploy, monitoring
- People/Orgs: person, company, lab, open-source
- Techniques: extraction, rendering, stealth, structuring, fine-tuning, inference
- Platforms: feishu, weixin, wecom, telegram, discord
- Meta: comparison, timeline, controversy, prediction, tutorial

## Page Thresholds
- **Create a page** when an entity/concept appears in 2+ sources OR is central to one source
- **Add to existing page** when a source mentions something already covered
- **DON'T create a page** for passing mentions or minor details
- **Split a page** when it exceeds ~200 lines
- **Archive a page** when fully superseded — move to `_archive/`

## Update Policy
When new information conflicts with existing content:
1. Check dates — newer sources generally supersede older ones
2. If genuinely contradictory, note both positions with dates and sources
3. Mark contradiction in frontmatter: `contradictions: [page-name]`
4. Flag for user review in lint report
