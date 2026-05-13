---
title: Code Execution (Programmatic Tool Calling)
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-code-execution.md]
---

# Code Execution (Programmatic Tool Calling)

源文档：[Code Execution (Programmatic Tool Calling)](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/code-execution.md)

# Code Execution (Programmatic Tool Calling)

The `execute_code` tool lets the agent write Python scripts that call Hermes tools programmatically, collapsing multi-step workflows into a single LLM turn. The script runs in a child process on the agent host, communicating with Hermes over a Unix domain socket RPC.

## How It Works

1. The agent writes a Python script using `from hermes_tools import ...`
2. Hermes generates a `hermes_tools.py` stub module with RPC functions
3. Hermes opens a Unix domain socket and starts an RPC listener thread
4. The script runs in a child process — tool calls travel over the socket back to Hermes
5. Only the script's `print()` output is returned to the LLM; intermediate tool results never enter the context window

```python
# The agent can write scripts like:
from hermes_tools import web_search, web_extract

results = web_search("Python 3.13 features", limit=5)
for r in results["data"]["...

## When the Agent Uses This

The agent uses `execute_code` when there are:

- **3+ tool calls** with processing logic between them
- Bulk data filtering or conditional branching
- Loops over results

The key benefit: intermediate tool results never enter the context window — only the final `print()` output comes back, dramatically reducing token usage....

## Practical Examples

### Data Processing Pipeline

```python
from hermes_tools import search_files, read_file
import json

# Find all config files and extract database settings
matches = search_files("database", path=".", file_glob="*.yaml", limit=20)
configs = []
for match in matches.get("matches", []):
    content = read_file(match["path"])
    configs.append({"file": match["path"], "preview": content["content"][:200]})

print(json.dumps(configs, indent=2))
```

### Multi-Step Web Research

```python
from hermes_tools import web_search, web_extract
import json

# Search, extract, and summarize in one turn
result...

## Execution Mode

`execute_code` has two execution modes controlled by `code_execution.mode` in `~/.hermes/config.yaml`:

| Mode | Working directory | Python interpreter |
|------|-------------------|--------------------|
| **`project`** (default) | The session's working directory (same as `terminal()`) | Active `VIRTUAL_ENV` / `CONDA_PREFIX` python, falling back to Hermes's own python |
| `strict` | A temp staging directory isolated from the user's project | `sys.executable` (Hermes's own python) |

**When to leave it on `project`:** you want `import pandas`, `from my_project import foo`, or relative paths lik...

## Resource Limits

| Resource | Limit | Notes |
|----------|-------|-------|
| **Timeout** | 5 minutes (300s) | Script is killed with SIGTERM, then SIGKILL after 5s grace |
| **Stdout** | 50 KB | Output truncated with `[output truncated at 50KB]` notice |
| **Stderr** | 10 KB | Included in output on non-zero exit for debugging |
| **Tool calls** | 50 per execution | Error returned when limit reached |

All limits are configurable via `config.yaml`:

```yaml
# In ~/.hermes/config.yaml
code_execution:
  mode: project      # project (default) | strict
  timeout: 300       # Max seconds per script (default: 300)
  m...

## How Tool Calls Work Inside Scripts

When your script calls a function like `web_search("query")`:

1. The call is serialized to JSON and sent over a Unix domain socket to the parent process
2. The parent dispatches through the standard `handle_function_call` handler
3. The result is sent back over the socket
4. The function returns the parsed result

This means tool calls inside scripts behave identically to normal tool calls — same rate limits, same error handling, same capabilities. The only restriction is that `terminal()` is foreground-only (no `background` or `pty` parameters)....

## Error Handling

When a script fails, the agent receives structured error information:

- **Non-zero exit code**: stderr is included in the output so the agent sees the full traceback
- **Timeout**: Script is killed and the agent sees `"Script timed out after 300s and was killed."`
- **Interruption**: If the user sends a new message during execution, the script is terminated and the agent sees `[execution interrupted — user sent a new message]`
- **Tool call limit**: When the 50-call limit is hit, subsequent tool calls return an error message

The response always includes `status` (success/error/timeout/interr...

## Security

:::danger Security Model
The child process runs with a **minimal environment**. API keys, tokens, and credentials are stripped by default. The script accesses tools exclusively via the RPC channel — it cannot read secrets from environment variables unless explicitly allowed.
:::

Environment variables containing `KEY`, `TOKEN`, `SECRET`, `PASSWORD`, `CREDENTIAL`, `PASSWD`, or `AUTH` in their names are excluded. Only safe system variables (`PATH`, `HOME`, `LANG`, `SHELL`, `PYTHONPATH`, `VIRTUAL_ENV`, etc.) are passed through.

### Skill Environment Variable Passthrough

When a skill declares `r...

## execute_code vs terminal

| Use Case | execute_code | terminal |
|----------|-------------|----------|
| Multi-step workflows with tool calls between | ✅ | ❌ |
| Simple shell command | ❌ | ✅ |
| Filtering/processing large tool outputs | ✅ | ❌ |
| Running a build or test suite | ❌ | ✅ |
| Looping over search results | ✅ | ❌ |
| Interactive/background processes | ❌ | ✅ |
| Needs API keys in environment | ⚠️ Only via [passthrough](/docs/user-guide/security#environment-variable-passthrough) | ✅ (most pass through) |

**Rule of thumb:** Use `execute_code` when you need to call Hermes tools programmatically with logic betwee...

## Platform Support

Code execution requires Unix domain sockets and is available on **Linux and macOS only**. It is automatically disabled on Windows — the agent falls back to regular sequential tool calls....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
