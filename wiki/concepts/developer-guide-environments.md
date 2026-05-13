---
title: Environments, Benchmarks & Data Generation
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-environments.md]
---

# Environments, Benchmarks & Data Generation

源文档：[Environments, Benchmarks & Data Generation](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/environments.md)

# Environments, Benchmarks & Data Generation

Hermes Agent includes a full environment framework that connects its tool-calling capabilities to the [Atropos](https://github.com/NousResearch/atropos) RL training framework. This enables three workflows:

1. **RL Training** — Train language models on multi-turn agentic tasks with GRPO
2. **Benchmarks** — Evaluate models on standardised agentic benchmarks
3. **Data Generation** — Generate SFT training data from agent rollouts

All three share the same core: an **environment** class that defines tasks, runs an agent loop, and scores the output.

:::info Repo environments vs RL training tools
The Python environment framework documented here lives under the repo's `environments/` directory and is the implementation-level API for Hermes/Atropos in

## Architecture

The environment system is built on a three-layer inheritance chain:

```mermaid
classDiagram
    class BaseEnv {
      Server management
      Worker scheduling
      Wandb logging
      CLI: serve / process / evaluate
    }

    class HermesAgentBaseEnv {
      Terminal backend configuration
      Tool resolution
      Agent loop engine
      ToolContext access
    }

    class TerminalTestEnv {
      Stack testing
    }

    class HermesSweEnv {
      SWE training
    }

    class TerminalBench2EvalEnv {
      Benchmark evaluation
    }

    class TBLiteEvalEnv {
      Fast benchmark
    }

...

## Core Components

### Agent Loop

`HermesAgentLoop` (`environments/agent_loop.py`) is the reusable multi-turn agent engine. It runs the same tool-calling pattern as hermes-agent's main loop:

1. Send messages + tool schemas to the API via `server.chat_completion()`
2. If the response contains `tool_calls`, dispatch each via `handle_function_call()`
3. Append tool results to the conversation, go back to step 1
4. If no `tool_calls`, the agent is done

Tool calls execute in a thread pool (`ThreadPoolExecutor(128)`) so that async backends (Modal, Docker) don't deadlock inside Atropos's event loop.

Returns an `Age...

## Available Benchmarks

### TerminalBench2

**89 challenging terminal tasks** with per-task Docker sandbox environments.

| | |
|---|---|
| **What it tests** | Single-task coding/sysadmin ability |
| **Scoring** | Binary pass/fail (test suite verification) |
| **Sandbox** | Modal cloud sandboxes (per-task Docker images) |
| **Tools** | `terminal` + `file` |
| **Tasks** | 89 tasks across multiple categories |
| **Cost** | ~$50–200 for full eval (parallel execution) |
| **Time** | ~2–4 hours |

```bash
python environments/benchmarks/terminalbench_2/terminalbench2_env.py evaluate \
    --config environments/benchmarks/t...

## Training Environments

### TerminalTestEnv

A minimal self-contained environment with inline tasks (no external dataset). Used for **validating the full stack** end-to-end. Each task asks the model to create a file at a known path; the verifier checks the content.

```bash
# Process mode (saves rollouts to JSONL, no training server needed)
python environments/terminal_test_env/terminal_test_env.py process \
    --env.data_path_to_save_groups terminal_test_output.jsonl

# Serve mode (connects to Atropos API for RL training)
python environments/terminal_test_env/terminal_test_env.py serve
```

### HermesSweEnv

SWE-be...

## Running Environments

Every environment is a standalone Python script with three CLI subcommands:

### `evaluate` — Run a benchmark

For eval-only environments (benchmarks). Runs all items, computes metrics, logs to wandb.

```bash
python environments/benchmarks/tblite/tblite_env.py evaluate \
    --config environments/benchmarks/tblite/default.yaml \
    --openai.model_name anthropic/claude-sonnet-4.6
```

No training server or `run-api` needed. The environment handles everything.

### `process` — Generate SFT data

Runs rollouts and saves scored trajectories to JSONL. Useful for generating training data without a...

## Two-Phase Operation

### Phase 1: OpenAI Server (Eval / SFT)

Uses `server.chat_completion()` with `tools=` parameter. The server (VLLM, SGLang, OpenRouter, OpenAI) handles tool call parsing natively. Returns `ChatCompletion` objects with structured `tool_calls`.

- **Use for**: evaluation, SFT data generation, benchmarks, testing
- **Placeholder tokens** are created for the Atropos pipeline (since real token IDs aren't available from the OpenAI API)

### Phase 2: VLLM ManagedServer (Full RL)

Uses ManagedServer for exact token IDs + logprobs via `/generate`. A client-side [tool call parser](#tool-call-parsers) re...

## Creating Environments

### Training Environment

```python
from environments.hermes_base_env import HermesAgentBaseEnv, HermesAgentEnvConfig
from atroposlib.envs.server_handling.server_manager import APIServerConfig

class MyEnvConfig(HermesAgentEnvConfig):
    my_custom_field: str = "default_value"

class MyEnv(HermesAgentBaseEnv):
    name = "my-env"
    env_config_cls = MyEnvConfig

    @classmethod
    def config_init(cls):
        env_config = MyEnvConfig(
            enabled_toolsets=["terminal", "file"],
            terminal_backend="modal",
            max_agent_turns=30,
        )
        server_configs = [...

## Configuration Reference

### HermesAgentEnvConfig Fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `enabled_toolsets` | `List[str]` | `None` (all) | Which hermes toolsets to enable |
| `disabled_toolsets` | `List[str]` | `None` | Toolsets to filter out |
| `distribution` | `str` | `None` | Probabilistic toolset distribution name |
| `max_agent_turns` | `int` | `30` | Max LLM calls per rollout |
| `agent_temperature` | `float` | `1.0` | Sampling temperature |
| `system_prompt` | `str` | `None` | System message for the agent |
| `terminal_backend` | `str` | `"local"` | `local`,...

## Prerequisites

### For all environments

- Python >= 3.11
- `atroposlib`: `pip install git+https://github.com/NousResearch/atropos.git`
- An LLM API key (OpenRouter, OpenAI, or self-hosted VLLM/SGLang)

### For Modal-sandboxed benchmarks (TB2, TBLite)

- [Modal](https://modal.com) account and CLI: `pip install "hermes-agent[modal]"`
- `MODAL_TOKEN_ID` and `MODAL_TOKEN_SECRET` environment variables

### For YC-Bench

- `pip install "hermes-agent[yc-bench]"` (installs the yc-bench CLI + SQLAlchemy)
- No Modal needed — runs with local terminal backend

### For RL training

- `TINKER_API_KEY` — API key for the [...

## Directory Structure

```
environments/
├── hermes_base_env.py          # Abstract base class (HermesAgentBaseEnv)
├── agent_loop.py               # Multi-turn agent engine (HermesAgentLoop)
├── tool_context.py             # Per-rollout tool access for reward functions
├── patches.py                  # Async-safety patches for Modal backend
│
├── tool_call_parsers/          # Phase 2 client-side parsers
│   ├── hermes_parser.py        # Hermes/ChatML <tool_call> format
│   ├── mistral_parser.py       # Mistral [TOOL_CALLS] format
│   ├── llama_parser.py         # Llama 3 JSON tool calling
│   ├── qwen_parser.py    ...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
