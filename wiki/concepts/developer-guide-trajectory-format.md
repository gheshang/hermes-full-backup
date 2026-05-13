---
title: Trajectory Format
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-trajectory-format.md]
---

# Trajectory Format

源文档：[Trajectory Format](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/trajectory-format.md)

# Trajectory Format

Hermes Agent saves conversation trajectories in ShareGPT-compatible JSONL format
for use as training data, debugging artifacts, and reinforcement learning datasets.

Source files: `agent/trajectory.py`, `run_agent.py` (search for `_save_trajectory`), `batch_runner.py`

## File Naming Convention

Trajectories are written to files in the current working directory:

| File | When |
|------|------|
| `trajectory_samples.jsonl` | Conversations that completed successfully (`completed=True`) |
| `failed_trajectories.jsonl` | Conversations that failed or were interrupted (`completed=False`) |

The batch runner (`batch_runner.py`) writes to a custom output file per batch
(e.g., `batch_001_output.jsonl`) with additional metadata fields.

You can override the filename via the `filename` parameter in `save_trajectory()`....

## JSONL Entry Format

Each line in the file is a self-contained JSON object. There are two variants:

### CLI/Interactive Format (from `_save_trajectory`)

```json
{
  "conversations": [ ... ],
  "timestamp": "2026-03-30T14:22:31.456789",
  "model": "anthropic/claude-sonnet-4.6",
  "completed": true
}
```

### Batch Runner Format (from `batch_runner.py`)

```json
{
  "prompt_index": 42,
  "conversations": [ ... ],
  "metadata": { "prompt_source": "gsm8k", "difficulty": "hard" },
  "completed": true,
  "partial": false,
  "api_calls": 7,
  "toolsets_used": ["code_tools", "file_tools"],
  "tool_stats": {
    "termina...

## Conversations Array (ShareGPT Format)

The `conversations` array uses ShareGPT role conventions:

| API Role | ShareGPT `from` |
|----------|-----------------|
| system | `"system"` |
| user | `"human"` |
| assistant | `"gpt"` |
| tool | `"tool"` |

### Complete Example

```json
{
  "conversations": [
    {
      "from": "system",
      "value": "You are a function calling AI model. You are provided with function signatures within <tools> </tools> XML tags. You may call one or more functions to assist with the user query. If available tools are not relevant in assisting with user query, just respond in natural conversational langua...

## Normalization Rules

### Reasoning Content Markup

The trajectory converter normalizes ALL reasoning into `<think>` tags, regardless
of how the model originally produced it:

1. **Native thinking tokens** (`msg["reasoning"]` field from providers like
   Anthropic, OpenAI o-series): Wrapped as `<think>\n{reasoning}\n</think>\n`
   and prepended before the content.

2. **REASONING_SCRATCHPAD XML** (when native thinking is disabled and the model
   reasons via system-prompt-instructed XML): `<REASONING_SCRATCHPAD>` tags are
   converted to `<think>` via `convert_scratchpad_to_think()`.

3. **Empty think blocks**: Eve...

## Loading Trajectories

Trajectories are standard JSONL — load with any JSON-lines reader:

```python
import json

def load_trajectories(path: str):
    """Load trajectory entries from a JSONL file."""
    entries = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries

# Filter to successful completions only
successful = [e for e in load_trajectories("trajectory_samples.jsonl")
              if e.get("completed")]

# Extract just the conversations for training
training_data = ...

## Controlling Trajectory Saving

In the CLI, trajectory saving is controlled by:

```yaml
# config.yaml
agent:
  save_trajectories: true  # default: false
```

Or via the `--save-trajectories` flag. When the agent initializes with
`save_trajectories=True`, the `_save_trajectory()` method is called at the end
of each conversation turn.

The batch runner always saves trajectories (that's its primary purpose).

Samples with zero reasoning across all turns are automatically discarded by the
batch runner to avoid polluting training data with non-reasoning examples....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
