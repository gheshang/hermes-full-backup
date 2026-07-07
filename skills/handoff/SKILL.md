---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. Use when you need to transfer context to another session, agent, or person.
---

# Handoff

Create a concise handoff document:

1. **What was done?** — Summary of completed work, decisions made, code changes.
2. **What's next?** — Open tasks, pending decisions, known issues.
3. **What context matters?** — Key files, relevant discussions, constraints, gotchas.
4. **What should the next agent know?** — Anything that would save them time or prevent mistakes.

**Output format:**
```
## Completed
- ...

## Next Steps
- ...

## Context
- ...

## Gotchas
- ...
```

**Rules:**
- Be concise. The next agent should be able to scan this in 30 seconds.
- Include file paths. Don't say "the config file" — say "config.yaml, line 42".
- Include decisions and their rationale. Not just what, but why.