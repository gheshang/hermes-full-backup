---
name: kanban
description: Hermes Kanban workflow — task decomposition, multi-agent orchestration, worker lifecycle, pitfalls, and best practices for routing work through Kanban boards.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, routing, workflow, collaboration, pitfalls]
    related_skills: []
---

# Kanban — Multi-Agent Orchestration

This umbrella skill consolidates all Kanban-related knowledge for Hermes Agent. It covers both the orchestrator role (decomposition, routing) and the worker role (execution, pitfalls).

**Choose your section:**

- [Orchestrator Playbook](#1-orchestrator-playbook) — Decomposition, task graph design, routing
- [Worker Pitfalls](#2-worker-pitfalls) — Execution guidance, handoff patterns, retry handling

---

## 1. Orchestrator Playbook

### Overview

The orchestrator's job is to **route, not execute**. The "don't do the work yourself" rule and basic lifecycle are auto-injected into every worker's system prompt. This section covers the deeper playbook for decomposition and routing.

### Profiles Are User-Configured

There is **no default specialist roster**. Before fanning out, discover available profiles:

```bash
hermes profile list
```

Or ask the user: "What profiles do you have set up?"

Cache the result for the rest of the conversation. The dispatcher silently fails to spawn unknown assignees.

### When to Use Kanban (vs delegate_task)

| | Kanban | delegate_task |
|-|--------|---------------|
| Duration | Hours/days | Minutes |
| Isolation | Cross-agent handoffs | Within parent session |
| Human-in-the-loop | Yes (blocks, comments) | No |
| Audit trail | SQLite persists forever | Session-bound |
| Parallel fan-out | Yes | Limited (max 3) |

**Create Kanban tasks when:**
1. Multiple specialists are needed
2. Work should survive crash/restart
3. User might want to interject
4. Multiple subtasks can run in parallel
5. Review/iteration is expected
6. Audit trail matters

### The Anti-Temptation Rules

- **Do not execute the work yourself.** Your restricted toolset usually doesn't include terminal/file/code/web. If you find yourself "just fixing this quickly" — stop and create a task.
- **For any concrete task, create a Kanban task and assign it.** Every single time.
- **Split multi-lane requests before creating cards.** Extract lanes first, then create one card per lane.
- **Run independent lanes in parallel.** Leave unlinked so dispatcher can fan out. Link only true data dependencies.
- **Never create dependent work as independent ready cards.** Use `parents=[...]` in the original `kanban_create` call.
- **If no specialist fits, ask the user.** Do not invent profile names.
- **Decompose, route, and summarize — that's the whole job.**

### Decomposition Playbook

#### Step 1: Understand the Goal

Ask clarifying questions if ambiguous. Cheap to ask; expensive to spawn wrong fleet.

#### Step 2: Sketch the Task Graph

Before creating anything, draft the graph:

1. Extract lanes from request
2. Map each lane to a profile from Step 0
3. Decide: independent or gated?
4. Create independent lanes as parallel cards (no parents)
5. Create synthesis/review cards with parent links

**Example:**
```python
t1 = kanban_create(
    title="research: Postgres cost vs current",
    assignee="researcher",
    body="Compare estimated infrastructure costs over 3-year window.",
)[ "task_id" ]

t2 = kanban_create(
    title="research: Postgres performance vs current",
    assignee="researcher",
    body="Compare query latency, throughput at expected data volume.",
)[ "task_id" ]

t3 = kanban_create(
    title="synthesize migration recommendation",
    assignee="analyst",
    body="Read T1 (cost) and T2 (performance). Produce 1-page recommendation.",
    parents=[t1, t2],
)[ "task_id" ]

t4 = kanban_create(
    title="draft decision memo",
    assignee="writer",
    body="Turn recommendation into 2-page memo for CTO.",
    parents=[t3],
)[ "task_id" ]
```

`parents=[...]` gates promotion — children stay in `todo` until all parents reach `done`, then auto-promote to `ready`.

#### Step 3: Create Tasks and Link

Use actual profile names from Step 0. Show the graph to user before creating cards.

#### Step 4: Complete Your Own Task

```python
kanban_complete(
    summary="decomposed into T1-T4: 2 research lanes parallel, 1 synthesis, 1 prose draft",
    metadata={
        "task_graph": {
            "T1": {"assignee": "researcher", "parents": []},
            "T2": {"assignee": "researcher", "parents": []},
            "T3": {"assignee": "analyst", "parents": ["T1", "T2"]},
            "T4": {"assignee": "writer", "parents": ["T3"]},
        },
    },
)
```

#### Step 5: Report Back

Tell user what you created in plain prose, naming actual profiles.

### Common Patterns

**Fan-out + fan-in (research → synthesize):**
- N research cards with no parents
- 1 synthesis card with all as parents

**Parallel implementation + validation:**
- 1 implementer card makes change
- 1 explorer/researcher card verifies config/docs
- Reviewer card can depend on both

**Pipeline with gates:**
- `planner → implementer → reviewer`
- Each stage's `parents=[previous_task]`

**Same-profile queue:**
- N tasks, all same profile, no dependencies
- Dispatcher serializes — profile processes in priority order

**Human-in-the-loop:**
- Any task can `kanban_block()` to wait for input
- Dispatcher respawns after `/unblock`
- Comment thread carries full context

### Goal-Mode Cards (Persistent Workers)

For open-ended cards where one turn rarely finishes:

```python
kanban_create(
    title="Translate full docs site to French",
    body="Acceptance: every page translated, no English left, links intact.",
    assignee="translator",
    goal_mode=True,        # judge re-checks after each turn
    goal_max_turns=15,     # optional budget (default 20)
)[ "task_id" ]
```

**Behavior:**
- After each turn, judge evaluates against title + body
- Not done + budget remains → worker keeps going (same session)
- Worker calls `kanban_complete`/`kanban_block` → loop stops
- Budget exhausted without completion → card blocked for human review

**Write body as explicit acceptance criteria.** "Translate README" is weaker than "Translate every section of README to French; no English sentences remain."

### Recovering Stuck Workers

When worker keeps crashing/hallucinating/blocked:

1. **Reclaim** (`hermes kanban reclaim <task_id>`) — abort running worker, reset to `ready`
2. **Reassign** (`hermes kanban reassign <task_id> <new-profile> --reclaim`) — switch to different profile
3. **Change profile model** — edit profile config on disk, then Reclaim

Hallucination warnings appear when:
- `kanban_complete(created_cards=[...])` includes IDs that don't exist
- Summary references `t_<hex>` IDs that don't resolve

---

## 2. Worker Pitfalls

### Overview

This section is for workers dispatched by the Kanban dispatcher. The lifecycle (6 steps: orient → work → heartbeat → block/complete) is auto-injected as `KANBAN_GUIDANCE` in your system prompt.

### Workspace Handling

Your workspace kind determines behavior:

| Kind | What it is | How to work |
|------|-----------|-------------|
| `scratch` | Fresh tmp dir, yours alone | Read/write freely; gets GC'd when task archived |
| `dir:<path>` | Shared persistent directory | Other runs will read what you write. Treat as long-lived state |
| `worktree` | Git worktree | If `.git` missing, run `git worktree add <path> ${HERMES_KANBAN_BRANCH:-wt/$HERMES_KANBAN_TASK}` from main repo first |

### Tenant Isolation

If `$HERMES_TENANT` is set, prefix memory entries with tenant:

- Good: `business-a: Acme is our biggest customer`
- Bad (leaks): `Acme is our biggest customer`

### Good Summary + Metadata Shapes

**Coding task:**
```python
kanban_complete(
    summary="shipped rate limiter — token bucket, keys on user_id with IP fallback, 14 tests pass",
    metadata={
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14,
        "tests_passed": 14,
        "decisions": ["user_id primary, IP fallback for unauthenticated requests"],
    },
)
```

**Coding task needing human review (review-required):**

Block instead of complete, with `reason` prefixed `review-required: `:

```python
kanban_comment(
    body="review-required handoff:\n" + json.dumps({
        "changed_files": ["rate_limiter.py", "tests/test_rate_limiter.py"],
        "tests_run": 14,
        "tests_passed": 14,
        "diff_path": "/path/to/worktree",
        "decisions": ["user_id primary, IP fallback"],
    }, indent=2),
)
kanban_block(
    reason="review-required: rate limiter shipped, 14/14 tests pass — needs eyes on user_id/IP fallback choice before merging",
)
```

**Research task:**
```python
kanban_complete(
    summary="3 libraries reviewed; vLLM wins on throughput, SGLang on latency",
    metadata={
        "sources_read": 12,
        "recommendation": "vLLM",
        "benchmarks": {"vllm": 1.0, "sglang": 0.87, "trtllm": 0.72},
    },
)
```

**Review task:**
```python
kanban_complete(
    summary="reviewed PR #123; 2 blocking issues (SQL injection, missing CSRF)",
    metadata={
        "pr_number": 123,
        "findings": [
            {"severity": "critical", "file": "api/search.py", "line": 42, "issue": "raw SQL concat"},
            {"severity": "high", "file": "api/settings.py", "issue": "missing CSRF middleware"},
        ],
        "approved": False,
    },
)
```

Shape `metadata` so downstream parsers can use it without re-reading prose.

### Claiming Cards You Actually Created

If your run produced new Kanban tasks, pass IDs in `created_cards`:

```python
# GOOD — capture return values
c1 = kanban_create(title="remediate SQL injection", assignee="security-worker")
c2 = kanban_create(title="fix CSRF middleware", assignee="web-worker")

kanban_complete(
    summary="Review done; spawned remediations for both findings.",
    metadata={"pr_number": 123, "approved": False},
    created_cards=[c1["task_id"], c2["task_id"]],
)

# BAD — hallucinated IDs
kanban_complete(
    summary="Created remediation cards t_a1b2c3d4, t_deadbeef",
    created_cards=["t_a1b2c3d4", "t_deadbeef"],  # → gate rejects
)
```

Only list IDs you captured from successful `kanban_create` return values. Never invent IDs from prose.

### Block Reasons That Get Answered Fast

**Bad:** `"stuck"` — human has no context

**Good:** One sentence naming specific decision needed. Leave longer context as comment:

```python
kanban_comment(
    task_id=os.environ["HERMES_KANBAN_TASK"],
    body="Full context: I have user IPs from Cloudflare headers but some users are behind NATs with thousands of peers. Keying on IP alone causes false positives.",
)
kanban_block(reason="Rate limit key choice: IP (simple, NAT-unsafe) or user_id (requires auth, skips anonymous)?")
```

### Heartbeats Worth Sending

**Good:** Name progress: `"epoch 12/50, loss 0.31"`, `"scanned 1.2M/2.4M rows"`

**Bad:** `"still working"`, empty notes, sub-second intervals. Every few minutes max; skip for tasks under ~2 minutes.

### Retry Scenarios

If `kanban_show` returns `runs: [...]` with closed runs, you're a retry. Prior runs' `outcome`/`summary`/`error` tell you what didn't work.

| Outcome | Meaning | Action |
|---------|---------|--------|
| `timed_out` | Hit `max_runtime_seconds` | Chunk work or shorten |
| `crashed` | OOM or segfault | Reduce memory footprint |
| `spawn_failed` + error | Profile config issue | Block with question |
| `reclaimed` + "task archived" | Operator archived | Check status, probably shouldn't run |
| `blocked` | Previous attempt blocked | Unblock comment should be in thread |

### Notification Routing

Add `notification_sources` to `~/.hermes/config.yaml`:

- `notification_sources: ['*']` — accept from all profiles
- `notification_sources: ['default', 'zilor-ppt']` — restrict to specific profiles
- Omit — profile isolation (default)

### DO NOT

- Call `delegate_task` as substitute for `kanban_create`
- Call `clarify` to ask human — you're headless, no live user. Use `kanban_comment` + `kanban_block` instead
- Modify files outside `$HERMES_KANBAN_WORKSPACE` unless task body says to
- Create follow-up tasks assigned to yourself — assign to right specialist
- Complete a task you didn't finish — block it instead

### Pitfalls

1. **Task state can change between dispatch and startup.** Always `kanban_show` first. If `blocked` or `archived`, stop.

2. **Workspace may have stale artifacts.** Especially `dir:` and `worktree`. Read comment thread for context.

3. **Don't rely on CLI when guidance available.** `kanban_*` tools work across all backends. `hermes kanban <verb>` may fail in containerized backends.

### CLI Fallback

| Tool | CLI Equivalent |
|------|----------------|
| `kanban_show` | `hermes kanban show <id> --json` |
| `kanban_complete` | `hermes kanban complete <id> --summary "..." --metadata '{...}'` |
| `kanban_block` | `hermes kanban block <id> "reason"` |
| `kanban_create` | `hermes kanban create "title" --assignee <profile> [--parent <id>]` |

Use tools from inside agent; CLI exists for human at terminal.

---

## Quick Reference

### Orchestrator Checklist

- [ ] Discover available profiles (`hermes profile list`)
- [ ] Sketch task graph before creating cards
- [ ] Create independent lanes in parallel (no parents)
- [ ] Create dependent cards with `parents=[...]`
- [ ] Use actual profile names, not invented ones
- [ ] Show graph to user before creating
- [ ] Report back in plain prose with actual profile names

### Worker Checklist

- [ ] `kanban_show` first to check state
- [ ] Read comment thread for context
- [ ] Work inside `$HERMES_KANBAN_WORKSPACE`
- [ ] Prefix memory entries with tenant if set
- [ ] Shape `metadata` for downstream parsers
- [ ] Capture `kanban_create` return values for `created_cards`
- [ ] Use `kanban_comment` + `kanban_block` for questions (not `clarify`)
- [ ] Send named progress heartbeats (not "still working")
- [ ] Check retry diagnostics before retrying
- [ ] Block instead of completing unfinished work