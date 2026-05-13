---
title: Build a Hermes Plugin
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-build-a-hermes-plugin.md]
---

# Build a Hermes Plugin

源文档：[Build a Hermes Plugin](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/build-a-hermes-plugin.md)

# Build a Hermes Plugin

This guide walks through building a complete Hermes plugin from scratch. By the end you'll have a working plugin with multiple tools, lifecycle hooks, shipped data files, and a bundled skill — everything the plugin system supports.

## What you're building

A **calculator** plugin with two tools:
- `calculate` — evaluate math expressions (`2**16`, `sqrt(144)`, `pi * 5**2`)
- `unit_convert` — convert between units (`100 F → 37.78 C`, `5 km → 3.11 mi`)

Plus a hook that logs every tool call, and a bundled skill file....

## Step 1: Create the plugin directory

```bash
mkdir -p ~/.hermes/plugins/calculator
cd ~/.hermes/plugins/calculator
```...

## Step 2: Write the manifest

Create `plugin.yaml`:

```yaml
name: calculator
version: 1.0.0
description: Math calculator — evaluate expressions and convert units
provides_tools:
  - calculate
  - unit_convert
provides_hooks:
  - post_tool_call
```

This tells Hermes: "I'm a plugin called calculator, I provide tools and hooks." The `provides_tools` and `provides_hooks` fields are lists of what the plugin registers.

Optional fields you could add:
```yaml
author: Your Name
requires_env:          # gate loading on env vars; prompted during install
  - SOME_API_KEY       # simple format — plugin disabled if missing
  - name: ...

## Step 3: Write the tool schemas

Create `schemas.py` — this is what the LLM reads to decide when to call your tools:

```python
"""Tool schemas — what the LLM sees."""

CALCULATE = {
    "name": "calculate",
    "description": (
        "Evaluate a mathematical expression and return the result. "
        "Supports arithmetic (+, -, *, /, **), functions (sqrt, sin, cos, "
        "log, abs, round, floor, ceil), and constants (pi, e). "
        "Use this for any math the user asks about."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
  ...

## Step 4: Write the tool handlers

Create `tools.py` — this is the code that actually executes when the LLM calls your tools:

```python
"""Tool handlers — the code that runs when the LLM calls each tool."""

import json
import math

# Safe globals for expression evaluation — no file/network access
_SAFE_MATH = {
    "abs": abs, "round": round, "min": min, "max": max,
    "pow": pow, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
    "tan": math.tan, "log": math.log, "log2": math.log2, "log10": math.log10,
    "floor": math.floor, "ceil": math.ceil,
    "pi": math.pi, "e": math.e,
    "factorial": math.factorial,
}


def ...

## Step 5: Write the registration

Create `__init__.py` — this wires schemas to handlers:

```python
"""Calculator plugin — registration."""

import logging

from . import schemas, tools

logger = logging.getLogger(__name__)

# Track tool usage via hooks
_call_log = []

def _on_post_tool_call(tool_name, args, result, task_id, **kwargs):
    """Hook: runs after every tool call (not just ours)."""
    _call_log.append({"tool": tool_name, "session": task_id})
    if len(_call_log) > 100:
        _call_log.pop(0)
    logger.debug("Tool called: %s (session %s)", tool_name, task_id)


def register(ctx):
    """Wire schemas to handler...

## Step 6: Test it

Start Hermes:

```bash
hermes
```

You should see `calculator: calculate, unit_convert` in the banner's tool list.

Try these prompts:
```
What's 2 to the power of 16?
Convert 100 fahrenheit to celsius
What's the square root of 2 times pi?
How many gigabytes is 1.5 terabytes?
```

Check plugin status:
```
/plugins
```

Output:
```
Plugins (1):
  ✓ calculator v1.0.0 (2 tools, 1 hooks)
```...

## Your plugin's final structure

```
~/.hermes/plugins/calculator/
├── plugin.yaml      # "I'm calculator, I provide tools and hooks"
├── __init__.py      # Wiring: schemas → handlers, register hooks
├── schemas.py       # What the LLM reads (descriptions + parameter specs)
└── tools.py         # What runs (calculate, unit_convert functions)
```

Four files, clear separation:
- **Manifest** declares what the plugin is
- **Schemas** describe tools for the LLM
- **Handlers** implement the actual logic
- **Registration** connects everything...

## What else can plugins do?

### Ship data files

Put any files in your plugin directory and read them at import time:

```python
# In tools.py or __init__.py
from pathlib import Path

_PLUGIN_DIR = Path(__file__).parent
_DATA_FILE = _PLUGIN_DIR / "data" / "languages.yaml"

with open(_DATA_FILE) as f:
    _DATA = yaml.safe_load(f)
```

### Bundle skills

Plugins can ship skill files that the agent loads via `skill_view("plugin:skill")`. Register them in your `__init__.py`:

```
~/.hermes/plugins/my-plugin/
├── __init__.py
├── plugin.yaml
└── skills/
    ├── my-workflow/
    │   └── SKILL.md
    └── my-checklist/
        └...

## Common mistakes

**Handler doesn't return JSON string:**
```python
# Wrong — returns a dict
def handler(args, **kwargs):
    return {"result": 42}

# Right — returns a JSON string
def handler(args, **kwargs):
    return json.dumps({"result": 42})
```

**Missing `**kwargs` in handler signature:**
```python
# Wrong — will break if Hermes passes extra context
def handler(args):
    ...

# Right
def handler(args, **kwargs):
    ...
```

**Handler raises exceptions:**
```python
# Wrong — exception propagates, tool call fails
def handler(args, **kwargs):
    result = 1 / int(args["value"])  # ZeroDivisionError!
    ...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
