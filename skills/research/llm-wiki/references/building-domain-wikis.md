# Building Domain Wikis for CLI Tools

> Pattern for creating wikis focused on a specific CLI tool or framework (e.g., OpenCode, Kubernetes, Docker).

## Workflow

### 1. Define Scope

Before creating pages, clarify:
- **What tool/domain?** — Be specific (e.g., "OpenCode CLI" not "AI tools")
- **What's the goal?** — Reference wiki? Learning resource? Troubleshooting guide?
- **Who's the audience?** — Yourself? Team? Public?

### 2. Create Directory Structure

```bash
mkdir -p ~/wiki/<tool-name>/{raw/articles,entities,concepts,comparisons,queries}
```

### 3. Initialize Core Files

Create `SCHEMA.md`, `index.md`, `log.md` following the standard wiki pattern.

### 4. Gather Sources

| Source Type | Tool | Notes |
|-------------|------|-------|
| Official docs | `web_extract`, `web_search` | Always try GitHub raw source first |
| GitHub README | `web_extract` | Get full content, not truncated summary |
| Community tips | Reddit, Discord, forums | Extract practical observations |
| Comparison articles | `web_search` + `web_extract` | Find "X vs Y" articles |
| Technical deep-dives | `web_search` | Look for architecture, internals |

### 5. Extract and Organize

For each source:
1. Save raw content to `raw/articles/<source-name>.md`
2. Add frontmatter: `source_url`, `ingested`, `sha256`
3. Extract key information into wiki pages

### 6. Structure Pages

| Type | Purpose | Example |
|------|---------|---------|
| `entities/` | What is this thing? | `opencode-cli.md`, `crush-ai.md` |
| `concepts/` | How does it work? | `opencode-architecture.md`, `opencode-providers.md` |
| `comparisons/` | How does it compare? | `opencode-vs-claude-code.md` |
| `queries/` | How do I use it? | `opencode-usage-tips.md`, `opencode-workflow-best-practices.md` |

### 7. Link Everything

Every page must have at least 2 outbound `[[wikilinks]]`. Cross-reference:
- Entities → Concepts (what it is → how it works)
- Concepts → Entities (how it works → what components)
- Comparisons → Both entities being compared
- Queries → Relevant concepts and entities

### 8. Update Index and Log

After each batch of pages:
1. Update `index.md` with new entries
2. Append to `log.md` with action details

## Page Thresholds for CLI Tools

| Signal | Action |
|--------|--------|
| Tool mentioned in 2+ sources | Create entity page |
| Concept appears in multiple contexts | Create concept page |
| Comparison with another tool exists | Create comparison page |
| Community tips collected | Create query page |
| Page exceeds 200 lines | Split into sub-topics |

## Source Extraction Tips

### Official Docs (GitHub-based)

```bash
# Find raw source
curl -sL 'https://api.github.com/repos/<org>/<repo>/contents/docs/<path>'

# Extract raw content
curl -sL 'https://raw.githubusercontent.com/<org>/<repo>/main/docs/<page>.md'
```

### Official Docs (Website-based)

```bash
# web_extract for small pages (<5000 chars)
web_extract(urls=["https://example.com/docs/cli"])

# For large pages with tables, use browser extraction
# (see llm-wiki skill for browser console extraction pattern)
```

### Community Tips (Reddit)

```bash
# Search for relevant threads
web_search(query="site:reddit.com/r/<subreddit> tips tricks")

# Extract key observations from top comments
# Focus on practical patterns, not opinions
```

## Example: OpenCode Wiki

```
~/wiki/opencode/
├── SCHEMA.md              # Domain: OpenCode CLI, tags: opencode, cli, coding-agent
├── index.md               # 16 pages: 3 entities, 8 concepts, 3 comparisons, 2 queries
├── log.md                 # 6 ingestion actions
├── entities/
│   ├── opencode-cli.md    # Main tool entity
│   ├── crush-ai.md        # Successor project
│   └── anomalyco-opencode.md  # Active fork
├── concepts/
│   ├── opencode-architecture.md
│   ├── opencode-providers.md
│   ├── opencode-sessions.md
│   ├── opencode-tools.md
│   ├── opencode-mcp.md
│   ├── opencode-lsp.md
│   ├── opencode-permissions.md
│   └── opencode-custom-commands.md
├── comparisons/
│   ├── opencode-vs-claude-code.md
│   ├── opencode-vs-codex.md
│   └── opencode-vs-aider.md
├── queries/
│   ├── opencode-usage-tips.md
│   └── opencode-workflow-best-practices.md
└── raw/articles/
    ├── opencode-official-docs.md
    ├── opencode-github-readme.md
    ├── opencode-quickstart.md
    ├── opencode-technical-docs.md
    ├── claude-code-vs-opencode-aimagicx.md
    └── opencode-reddit-tips.md
```

## Pitfalls

- **Don't mirror upstream docs** — extract and synthesize, don't copy-paste
- **Don't create pages for passing mentions** — follow the 2+ source threshold
- **Don't skip cross-references** — isolated pages are invisible
- **Don't forget to update index.md** — this is the navigation backbone
- **Don't use web_extract for large reference docs** — it truncates at ~5000 chars; use GitHub raw source instead
