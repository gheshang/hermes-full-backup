---
title: Batch Processing
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-batch-processing.md]
---

# Batch Processing

源文档：[Batch Processing](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/batch-processing.md)

# Batch Processing

Batch processing lets you run the Hermes agent across hundreds or thousands of prompts in parallel, generating structured trajectory data. This is primarily used for **training data generation** — producing ShareGPT-format trajectories with tool usage statistics that can be used for fine-tuning or evaluation.

## Overview

The batch runner (`batch_runner.py`) processes a JSONL dataset of prompts, running each through a full agent session with tool access. Each prompt gets its own isolated environment. The output is structured trajectory data with full conversation history, tool call statistics, and reasoning coverage metrics....

## Quick Start

```bash
# Basic batch run
python batch_runner.py \
    --dataset_file=data/prompts.jsonl \
    --batch_size=10 \
    --run_name=my_first_run \
    --model=anthropic/claude-sonnet-4.6 \
    --num_workers=4

# Resume an interrupted run
python batch_runner.py \
    --dataset_file=data/prompts.jsonl \
    --batch_size=10 \
    --run_name=my_first_run \
    --resume

# List available toolset distributions
python batch_runner.py --list_distributions
```...

## Dataset Format

The input dataset is a JSONL file (one JSON object per line). Each entry must have a `prompt` field:

```jsonl
{"prompt": "Write a Python function that finds the longest palindromic substring"}
{"prompt": "Create a REST API endpoint for user authentication using Flask"}
{"prompt": "Debug this error: TypeError: cannot unpack non-iterable NoneType object"}
```

Entries can optionally include:
- `image` or `docker_image`: A container image to use for this prompt's sandbox (works with Docker, Modal, and Singularity backends)
- `cwd`: Working directory override for the task's terminal session...

## Configuration Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--dataset_file` | (required) | Path to JSONL dataset |
| `--batch_size` | (required) | Prompts per batch |
| `--run_name` | (required) | Name for this run (used for output dir and checkpointing) |
| `--distribution` | `"default"` | Toolset distribution to sample from |
| `--model` | `claude-sonnet-4.6` | Model to use |
| `--base_url` | `https://openrouter.ai/api/v1` | API base URL |
| `--api_key` | (env var) | API key for model |
| `--max_turns` | `10` | Maximum tool-calling iterations per prompt |
| `--num_workers`...

## Toolset Distributions

Each prompt gets a randomly sampled set of toolsets from a **distribution**. This ensures training data covers diverse tool combinations. Use `--list_distributions` to see all available distributions.

In the current implementation, distributions assign a probability to **each individual toolset**. The sampler flips each toolset independently, then guarantees that at least one toolset is enabled. This is different from a hand-authored table of prebuilt combinations....

## Output Format

All output goes to `data/<run_name>/`:

```text
data/my_run/
├── trajectories.jsonl    # Combined final output (all batches merged)
├── batch_0.jsonl         # Individual batch results
├── batch_1.jsonl
├── ...
├── checkpoint.json       # Resume checkpoint
└── statistics.json       # Aggregate tool usage stats
```

### Trajectory Format

Each line in `trajectories.jsonl` is a JSON object:

```json
{
  "prompt_index": 42,
  "conversations": [
    {"from": "human", "value": "Write a function..."},
    {"from": "gpt", "value": "I'll create that function...",
     "tool_calls": [...]},
    {"from"...

## Checkpointing

The batch runner has robust checkpointing for fault tolerance:

- **Checkpoint file:** Saved after each batch completes, tracking which prompt indices are done
- **Content-based resume:** On `--resume`, the runner scans existing batch files and matches completed prompts by their actual text content (not just indices), enabling recovery even if the dataset order changes
- **Failed prompts:** Only successfully completed prompts are marked as done — failed prompts will be retried on resume
- **Batch merging:** On completion, all batch files (including from previous runs) are merged into a single ...

## Quality Filtering

The batch runner applies automatic quality filtering:

- **No-reasoning filter:** Samples where zero assistant turns contain reasoning (no `<REASONING_SCRATCHPAD>` or native thinking tokens) are discarded
- **Corrupted entry filter:** Entries with hallucinated tool names (not in the valid tool list) are filtered out during the final merge
- **Reasoning statistics:** Tracks percentage of turns with/without reasoning across the entire run...

## Statistics

After completion, the runner prints comprehensive statistics:

- **Tool usage:** Call counts, success/failure rates per tool
- **Reasoning coverage:** Percentage of assistant turns with reasoning
- **Samples discarded:** Count of samples filtered for lacking reasoning
- **Duration:** Total processing time

Statistics are also saved to `statistics.json` for programmatic analysis....

## Use Cases

### Training Data Generation

Generate diverse tool-use trajectories for fine-tuning:

```bash
python batch_runner.py \
    --dataset_file=data/coding_prompts.jsonl \
    --batch_size=20 \
    --run_name=coding_v1 \
    --model=anthropic/claude-sonnet-4.6 \
    --num_workers=8 \
    --distribution=default \
    --max_turns=15
```

### Model Evaluation

Evaluate how well a model uses tools across standardized prompts:

```bash
python batch_runner.py \
    --dataset_file=data/eval_suite.jsonl \
    --batch_size=10 \
    --run_name=eval_gpt4 \
    --model=openai/gpt-4o \
    --num_workers=4 \
   ...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
