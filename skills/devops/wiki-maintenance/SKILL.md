--- 
name: wiki-maintenance
title: Hermes Wiki Maintenance
domain: devops
priority: medium
triggers: 
  - user asks to update/clean/maintain/fix the wiki
  - user mentions "wiki outdated" or "wiki stale"
  - user asks to sync wiki to GitHub
  - user asks to review wiki content quality
description: "Audit, clean, update, and sync the Hermes wiki (~/.hermes/wiki/). Covers stale-content removal, version updates, batch ingestion from Hermes source docs, index/log maintenance, and GitHub push."
---

# Hermes Wiki Maintenance

Systematic process to review, clean, and update `~/.hermes/wiki/`.

## Prerequisites
- `~/.hermes/hermes-agent/` — cloned Hermes Agent repo (source for latest docs)
- Git remote at `origin git@github.com:gheshang/hermes-wiki.git` (or `~/.hermes/scripts/wiki-sync.sh`)

## Step 1 — Audit the Wiki

1. **Read the index** — `~/.hermes/wiki/index.md` shows current pages by category (Entities, Concepts).
2. **Read the log** — `~/.hermes/wiki/log.md` shows what was ingested when and from where.
3. **Compare against source** — List Hermes source docs and check each against wiki concept pages:

```bash
# Check features missing from wiki
for f in ~/.hermes/hermes-agent/website/docs/user-guide/features/*.md; do
  base=$(basename "$f" .md)
  if [ ! -f ~/.hermes/wiki/concepts/features-"$base".md ] && \
     [ ! -f ~/.hermes/wiki/concepts/"$base".md ]; then
    echo "MISSING: $base"
  fi
done

# Check messaging docs
for f in ~/.hermes/hermes-agent/website/docs/user-guide/messaging/*.md; do
  base=$(basename "$f" .md)
  if [ ! -f ~/.hermes/wiki/concepts/messaging-"$base".md ] && \
     [ ! -f ~/.hermes/wiki/concepts/"$base".md ]; then
    echo "MISSING: messaging-$base"
  fi
done
```

4. **Version check** — Compare `entities/hermes-v*.md` with the current version from `~/.hermes/hermes-agent/pyproject.toml` (`version =`). If >1 version behind:
   - Create new entity page (`entities/hermes-v{new}.md`) summarizing new features from git log
   - Delete old entity file (`rm entities/hermes-v{old}.md`)
   - Update the version link in `index.md`

### Source paths (where docs live)

Feature docs are at `website/docs/user-guide/features/`.  
Messaging docs are at `website/docs/user-guide/messaging/`.  
**Guides are at `website/docs/guides/`** (NOT under user-guide).  
**User-guide pages are at `website/docs/user-guide/*.md`** (excluding `features/` and `messaging/` subdirs).

Check missing guides:
```bash
for f in ~/.hermes/hermes-agent/website/docs/guides/*.md; do
  base=$(basename "$f" .md)
  if [ ! -f ~/.hermes/wiki/concepts/guides-"$base".md ]; then
    echo "MISSING: guides-$base"
  fi
done
```

Check missing user-guide pages:
```bash
for f in ~/.hermes/hermes-agent/website/docs/user-guide/*.md; do
  base=$(basename "$f" .md)
  [[ "$base" =~ ^(features|messaging)$ ]] && continue
  if [ ! -f ~/.hermes/wiki/concepts/"$base".md ] && \
     [ ! -f ~/.hermes/wiki/concepts/user-guide-"$base".md ]; then
    echo "MISSING: user-guide-$base"
  fi
done
```

## Step 2 — Remove Stale Content

### Candidates for deletion

Determine staleness by source URL pattern, not by guessing content topics:

- **`btcjon/claude-code-docs`** — Claude Code renamed to OpenCode; all pages sourced from this repo are stale
- **`SaladDay/cc-switch-cli`** — Separate project unrelated to Hermes
- **`anthropics/claude-code`** — Same as Claude Code, stale
- Pages referencing removed features — search for: `google-gemini-cli`, `google-antigravity`
- **Old version entities** (e.g., `hermes-v0.11.0.md` when current is v0.17.0+) — check `pyproject.toml` for `version =` and compare

What to KEEP (accelerated):
- Pages sourced from `NousResearch/hermes-agent` or `hermes-agent.nousresearch.com` — these are Hermes Agent content
- Pages sourced from `opencode.ai` — OpenCode docs are still valid
- Legacy proxy-plan pages (2026-03-09-proxy-b-*) — CC-Switch related, but proxy plans != CC-Switch docs

### Delete procedure
```bash
cd ~/.hermes/wiki
rm -f concepts/{page1.md,page2.md,...}
rm -f entities/old-version.md
```

### Update index.md
- Remove the deleted entries from the wiki index
- Search for the page name in index.md and remove that line
- ⚠️ **Be careful not to delete Hermes reference pages** — only delete pages sourced from third-party repos (btcjon, anthropics, SaladyDay/cc-switch-cli). Pages sourced from `NousResearch/hermes-agent` are Hermes Agent content and should be kept.

### Check raw articles
- Check if there are corresponding `raw/articles/` files that also need deletion
- Files sourced from btcjon/claude-code-docs — check the log.md for ingestion dates

## Step 3 — Ingest New Docs

For each missing page, create TWO files:

### Concept page (`concepts/features-{name}.md`)
```markdown
---
title: {Title}
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
type: concept
---

# {Title}

2-3 paragraph summary of the feature...

Source: [Hermes Docs]({source-url})
```

### Raw article (`raw/articles/features-{name}.md`)
Full source content (exact copy from the Hermes source file).

### Batch strategy — direct copy for raw, write concepts directly

For large batches (5+ docs), DO NOT delegate to subagents — they timeout at 600s with only 3-5 API calls and produce zero files. Instead:

1. **Raw articles**: `cp` source files directly — fastest path:
   ```bash
   SRC=~/.hermes/hermes-agent/website/docs/user-guide/features
   RAW=~/.hermes/wiki/raw/articles
   for f in feature-name-1 feature-name-2; do
     cp "$SRC/$f.md" "$RAW/features-$f.md"
   done
   ```

2. **Concept pages**: Write inline (2-3 paras + source link). Each `write_file` call takes <1s.

3. Alternative: group by batch into a `delegate_task` with `toolsets: ["file", "terminal"]` for 3-5 docs max, but **always fall back to (1)+(2) if subagents haven't returned within 120s**.

4. Keep max 3 concurrent delegations (per `delegation.max_concurrent_children`).

## Step 4 — Update Index and Log

### Update `index.md`
- Header line: `> Last updated: YYYY-MM-DD | Total pages: N (X concepts + Y entities)`
- Add new entries in alphabetical order
- Update the version entity line (current → new)

### Append to `log.md`
Format:
```markdown
## [{date}] cleanup | {description}
- Deleted: {count} pages ({detail})
- Updated: {entity} → {new entity}

## [{date}] ingest | {description}
- Source: {source}
- New pages: {list}
```

## Step 5 — Push to GitHub

```bash
cd ~/.hermes/wiki
git add -A
git diff --cached --quiet || git commit -m "sync: {date} {description}"
git push origin master
```

## Pitfalls

- **Don't delete Hermes reference pages** — Only pages sourced from `btcjon/claude-code-docs`, `anthropics/claude-code`, or `SaladDay/cc-switch-cli` are stale. Pages from `NousResearch/hermes-agent` are valid Hermes content.
- **Index formatting** — Each line in index.md starts with `- ` (not `|- `). After batch patches, check for formatting artifacts at line wrapping points.
- **Subagent naming** — When delegating, specify the exact file path pattern (`features-{name}.md`, `messaging-{name}.md`) so results land in the right place.
- **Raw article count** — The "32 features raw articles" number includes ALL existing ones, not just new ones. Check by modification date.
- **Index formatting artifacts** — After batch `patch` operations, index lines can get extra prefix characters (`|- ` instead of `- `) or become duplicated. Always re-read the tail of index.md after bulk edits and fix any formatting drift.
- **Duplicate wecom-setup lines** — A recurring artifact from multiple patches hitting the same area. Check for duplicate entries at the end of the concepts section after batch patches.
- **Git branch** — Remote is `master`, not `main`. Use `git push origin master`.
- **Duplicate header** — Don't accidentally create `# Wiki Index\\n# Wiki Index` during index patching.
- **Stale index entries linger** — After deleting concept files, search the index for remaining dangling links by the old source URL pattern (`btcjon`, `anthropics`, `SaladDay`) and remove those lines too. Deleting the file isn't enough — the index entry must also go.