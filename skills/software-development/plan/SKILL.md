---
name: plan
description: Plan mode for Hermes — inspect context, write a markdown plan into the active workspace's `.hermes/plans/` directory, and do not execute the work.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [planning, plan-mode, implementation, workflow]
    related_skills: [writing-plans, subagent-driven-development]
---

# Plan Mode

Use this skill when the user wants a plan instead of execution.

## Core behavior

For this turn, you are planning only.

- Do not implement code.
- Do not edit project files except the plan markdown file.
- Do not run mutating terminal commands, commit, push, or perform external actions.
- You may inspect the repo or other context with read-only commands/tools when needed.
- Your deliverable is a markdown plan saved inside the active workspace under `.hermes/plans/`.

## Output requirements

Write a markdown plan that is concrete and actionable.

Include, when relevant:
- Goal
- Current context / assumptions
- Proposed approach
- Step-by-step plan
- Files likely to change
- Tests / validation
- Risks, tradeoffs, and open questions

If the task is code-related, include exact file paths, likely test targets, and verification steps.

## Save location

Save the plan with `write_file` under:
- `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`

Treat that as relative to the active working directory / backend workspace. Hermes file tools are backend-aware, so using this relative path keeps the plan with the workspace on local, docker, ssh, modal, and daytona backends.

If the runtime provides a specific target path, use that exact path.
If not, create a sensible timestamped filename yourself under `.hermes/plans/`.

## Interaction style

- If the request is clear enough, write the plan directly.
- If no explicit instruction accompanies `/plan`, infer the task from the current conversation context.
- If it is genuinely underspecified, ask a brief clarifying question instead of guessing.
- After saving the plan, reply briefly with what you planned and the saved path.
- **Do not offer to execute the plan** unless the user explicitly asks. The plan skill is for planning only — execution belongs to `subagent-driven-development` or direct implementation. If the user says "执行" (execute), confirm they want to proceed before dispatching agents.
- **User prefers document delivery over text summary**: When user says "把方案文件发过来" or "我要文档不是要你文字", send the file as a MEDIA attachment directly. Do not paste the full document content as chat text — the file attachment is the deliverable.

## Pitfalls

- **File path typo**: The save location is `.hermes/plans/` — not `.herms/`. A single-character typo creates a dead-end file that can't be read back. Always double-check the path before writing.
- **Read-loop trap**: After a file write failure, do not repeatedly retry `read_file` on the same path. If the file doesn't exist, verify the path first, then fix the write. The system will block after ~10 consecutive identical failures.
- **Clarify tool availability**: The `clarify` tool may not be available in all execution contexts. Use `terminal` or `web_search` for clarification instead.
