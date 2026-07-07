---
name: review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
---

# Review

Two-axis review of the diff between HEAD and a fixed point:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

The issue tracker should have been provided to you — run `/setup-matt-pocock-skills` if `docs/agents/issue-tracker.md` is missing.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point — a commit SHA, branch name, tag, `main`, `HEAD~5`, etc. Don't be opinionated; pass it through. If they didn't specify one, ask: "Review against what — a branch, a commit, or `main`?" Don't proceed until you have it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot, so the comparison is against the merge-base). Also note the list of commits via `git log <fixed-point>..HEAD --oneline`.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab `!67`, etc.) — fetch via the workflow in `docs/agents/issue-tracker.md`.
2. A path the user passed as an argument.
3. Ask the user.

### 3. Run parallel reviews

Spin up two sub-agents:

- **Standards sub-agent**: Given the diff and the repo's coding standards (from `CONTRIBUTING.md`, `.editorconfig`, linter configs, etc.), check for violations.
- **Spec sub-agent**: Given the diff and the spec (issue/PRD), check for deviations, missing requirements, or over-engineering.

### 4. Aggregate findings

Present findings side by side:

```
## Standards Review
- [ ] Violation 1
- [ ] Violation 2

## Spec Review
- [ ] Deviation 1
- [ ] Missing requirement 2
```

## Rules

- Never skip the fixed point. If the user didn't specify one, ask.
- Never review without a spec source. If there's no issue/PRD, ask what the code is supposed to do.
- Be specific. "This function is too long" → "This function is 120 lines; the repo standard is 50."