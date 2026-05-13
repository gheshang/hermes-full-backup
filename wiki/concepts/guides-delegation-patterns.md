---
title: Delegation & Parallel Work
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-delegation-patterns.md]
---

# Delegation & Parallel Work

源文档：[Delegation & Parallel Work](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/delegation-patterns.md)

# Delegation & Parallel Work

Hermes can spawn isolated child agents to work on tasks in parallel. Each subagent gets its own conversation, terminal session, and toolset. Only the final summary comes back — intermediate tool calls never enter your context window.

For the full feature reference, see [Subagent Delegation](/docs/user-guide/features/delegation).

---

## When to Delegate

**Good candidates for delegation:**
- Reasoning-heavy subtasks (debugging, code review, research synthesis)
- Tasks that would flood your context with intermediate data
- Parallel independent workstreams (research A and B simultaneously)
- Fresh-context tasks where you want the agent to approach without bias

**Use something else:**
- Single tool call → just use the tool directly
- Mechanical multi-step work with logic between steps → `execute_code`
- Tasks needing user interaction → subagents can't use `clarify`
- Quick file edits → do them directly

---...

## Pattern: Parallel Research

Research three topics simultaneously and get structured summaries back:

```
Research these three topics in parallel:
1. Current state of WebAssembly outside the browser
2. RISC-V server chip adoption in 2025
3. Practical quantum computing applications

Focus on recent developments and key players.
```

Behind the scenes, Hermes uses:

```python
delegate_task(tasks=[
    {
        "goal": "Research WebAssembly outside the browser in 2025",
        "context": "Focus on: runtimes (Wasmtime, Wasmer), cloud/edge use cases, WASI progress",
        "toolsets": ["web"]
    },
    {
        "goal": "R...

## Pattern: Code Review

Delegate a security review to a fresh-context subagent that approaches the code without preconceptions:

```
Review the authentication module at src/auth/ for security issues.
Check for SQL injection, JWT validation problems, password handling,
and session management. Fix anything you find and run the tests.
```

The key is the `context` field — it must include everything the subagent needs:

```python
delegate_task(
    goal="Review src/auth/ for security issues and fix any found",
    context="""Project at /home/user/webapp. Python 3.11, Flask, PyJWT, bcrypt.
    Auth files: src/auth/login.p...

## Pattern: Compare Alternatives

Evaluate multiple approaches to the same problem in parallel, then pick the best:

```
I need to add full-text search to our Django app. Evaluate three approaches
in parallel:
1. PostgreSQL tsvector (built-in)
2. Elasticsearch via django-elasticsearch-dsl
3. Meilisearch via meilisearch-python

For each: setup complexity, query capabilities, resource requirements,
and maintenance overhead. Compare them and recommend one.
```

Each subagent researches one option independently. Because they're isolated, there's no cross-contamination — each evaluation stands on its own merits. The parent agent ge...

## Pattern: Multi-File Refactoring

Split a large refactoring task across parallel subagents, each handling a different part of the codebase:

```python
delegate_task(tasks=[
    {
        "goal": "Refactor all API endpoint handlers to use the new response format",
        "context": """Project at /home/user/api-server.
        Files: src/handlers/users.py, src/handlers/auth.py, src/handlers/billing.py
        Old format: return {"data": result, "status": "ok"}
        New format: return APIResponse(data=result, status=200).to_dict()
        Import: from src.responses import APIResponse
        Run tests after: pytest tests/hand...

## Pattern: Gather Then Analyze

Use `execute_code` for mechanical data gathering, then delegate the reasoning-heavy analysis:

```python
# Step 1: Mechanical gathering (execute_code is better here — no reasoning needed)
execute_code("""
from hermes_tools import web_search, web_extract

results = []
for query in ["AI funding Q1 2026", "AI startup acquisitions 2026", "AI IPOs 2026"]:
    r = web_search(query, limit=5)
    for item in r["data"]["web"]:
        results.append({"title": item["title"], "url": item["url"], "desc": item["description"]})

# Extract full content from top 5 most relevant
urls = [r["url"] for r in resul...

## Toolset Selection

Choose toolsets based on what the subagent needs:

| Task type | Toolsets | Why |
|-----------|----------|-----|
| Web research | `["web"]` | web_search + web_extract only |
| Code work | `["terminal", "file"]` | Shell access + file operations |
| Full-stack | `["terminal", "file", "web"]` | Everything except messaging |
| Read-only analysis | `["file"]` | Can only read files, no shell |

Restricting toolsets keeps the subagent focused and prevents accidental side effects (like a research subagent running shell commands).

---...

## Constraints

- **Default 3 parallel tasks** — batches default to 3 concurrent subagents (configurable via `delegation.max_concurrent_children` in config.yaml — no hard ceiling, only a floor of 1)
- **Nested delegation is opt-in** — leaf subagents (default) cannot call `delegate_task`, `clarify`, `memory`, `send_message`, or `execute_code`. Orchestrator subagents (`role="orchestrator"`) retain `delegate_task` for further delegation, but only when `delegation.max_spawn_depth` is raised above the default of 1 (1-3 supported); the other four remain blocked. Disable globally via `delegation.orchestrator_enabled...

## Tips

**Be specific in goals.** "Fix the bug" is too vague. "Fix the TypeError in api/handlers.py line 47 where process_request() receives None from parse_body()" gives the subagent enough to work with.

**Include file paths.** Subagents don't know your project structure. Always include absolute paths to relevant files, the project root, and the test command.

**Use delegation for context isolation.** Sometimes you want a fresh perspective. Delegating forces you to articulate the problem clearly, and the subagent approaches it without the assumptions that built up in your conversation.

**Check resu...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
