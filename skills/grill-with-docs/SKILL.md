---
name: grill-with-docs
description: Grilling session that challenges your plan against the existing domain model, shared understanding, and documented constraints. Use when you want to validate a plan against the project's documentation before implementing.
---

# Grill With Docs

Challenge your plan against the project's existing documentation:

1. **Read the docs** — Find relevant documentation: README, API docs, design docs, ADRs, comments.
2. **Extract constraints** — What does the docs say about this area? What patterns are established? What's explicitly forbidden?
3. **Cross-check your plan** — Does your plan align with documented conventions? Where does it diverge?
4. **Identify gaps** — What's missing from the docs that your plan assumes? Is the docs outdated?
5. **Propose doc updates** — If your plan is valid but the docs don't reflect it, propose doc changes.

**Rules:**
- Never implement a plan that contradicts documented conventions without explicit approval.
- If docs are missing or outdated, flag it and propose updates.
- The docs are the source of truth. Your plan must justify any deviation.