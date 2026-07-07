# Memory File Management

## File Locations

| File | Path | Purpose |
|------|------|---------|
| USER.md | `~/.hermes/memories/USER.md` | User profile: name, role, preferences, habits |
| MEMORY.md | `~/.hermes/memories/MEMORY.md` | Agent notes: environment facts, project conventions, lessons learned |

**⚠️ Critical path note**: The directory is `~/.hermes/memories/` (plural), NOT `~/.hermes/memory/`. Files are `USER.md` and `MEMORY.md` (uppercase), NOT `user.md` and `memory.md`.

## Entry Format

- Each entry starts with `§` on its own line
- Empty entries are just `§` with no content following
- Entries are separated by blank lines
- Content follows the `§` marker on the same line

## Editing Workflow

### Safe Edit Pattern

1. **Read** the current file to understand structure
2. **Identify** exact line numbers or content to modify
3. **Backup** (automatic: `USER.md.bak` / `MEMORY.md.bak` exist)
4. **Patch** using `memory` tool with `action=replace` or `action=remove`
5. **Verify** by reading the file after edit

### Using `memory` Tool

```
# Remove an entry
memory(action="remove", target="user"|"memory", old_text="<unique substring>")

# Replace an entry
memory(action="replace", target="user"|"memory", old_text="<old>", content="<new>")

# Add a new entry
memory(action="add", target="user"|"memory", content="<new entry>")
```

**⚠️ Pitfall**: `old_text` uses substring matching. Short substrings (like `§`) can match multiple entries. Always include enough context to ensure uniqueness.

### Using `patch` Tool for Bulk Edits

For removing multiple lines or restructuring:
1. Read the full file
2. Use `patch` with `old_string`/`new_string` to replace a block
3. Ensure `old_string` is unique within the file

## Maintenance Tips

- **Remove duplicates**: USER.md often accumulates duplicate entries across sessions. Periodically review and deduplicate.
- **Remove empty entries**: Lines that are just `§` with no content should be cleaned up.
- **Keep USER.md under 1375 chars** (config limit: `memory.user_char_limit`)
- **Keep MEMORY.md under 2200 chars** (config limit: `memory.memory_char_limit`)
- **Backup exists**: `USER.md.bak` and `MEMORY.md.bak` are automatically maintained. Use them to restore if needed.

## Common Operations

### Restore from backup
```bash
cp ~/.hermes/memories/USER.md.bak ~/.hermes/memories/USER.md
cp ~/.hermes/memories/MEMORY.md.bak ~/.hermes/memories/MEMORY.md
```

### Check file size
```bash
wc -c ~/.hermes/memories/USER.md ~/.hermes/memories/MEMORY.md
```

### List all entries
```bash
grep -n "^§" ~/.hermes/memories/USER.md ~/.hermes/memories/MEMORY.md
```