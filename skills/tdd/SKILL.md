---
name: tdd
description: Test-driven development with red-green-refactor loop. Use when user wants to build new features, add functionality, or fix bugs with confidence.
---

# TDD (Test-Driven Development)

Red-Green-Refactor cycle:

1. **Red** — Write a failing test first. The test should fail because the feature doesn't exist yet.
2. **Green** — Write the minimum code to make the test pass. Don't over-engineer.
3. **Refactor** — Clean up the code while keeping tests green. Remove duplication, improve naming, extract methods.

**Rules:**
- Never write production code without a failing test first.
- One assertion per test. If you're testing multiple things, write multiple tests.
- Tests must be deterministic. No randomness, no time-dependent logic, no external I/O.
- If a test is hard to write, the design is probably wrong.