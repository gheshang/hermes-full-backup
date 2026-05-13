---
title: RL Training
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/features-rl-training.md]
---

# RL Training

源文档：[RL Training](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/rl-training.md)

# RL Training

Hermes Agent includes an integrated RL (Reinforcement Learning) training pipeline built on **Tinker-Atropos**. This enables training language models on environment-specific tasks using GRPO (Group Relative Policy Optimization) with LoRA adapters, orchestrated entirely through the agent's tool interface.

## Overview

The RL training system consists of three components:

1. **[Atropos](https://github.com/NousResearch/atropos)** — A trajectory API server that coordinates environment interactions, manages rollout groups, and computes advantages
2. **[Tinker](https://thinkingmachines.ai/tinker/)** — A training service that handles model weights, LoRA training, sampling/inference, and optimizer steps
3. **Environments** — Python classes that define tasks, scoring, and reward functions (e.g., GSM8K math problems)

The agent can discover environments, configure training parameters, launch training runs, and monit...

## Requirements

RL training requires:

- **Python >= 3.11** (Tinker package requirement)
- **TINKER_API_KEY** — API key for the Tinker training service
- **WANDB_API_KEY** — API key for [Weights & Biases](https://wandb.ai/) metrics tracking
- The `tinker-atropos` submodule (at `tinker-atropos/` relative to the Hermes root)

```bash
# Set up API keys
hermes config set TINKER_API_KEY your-tinker-key
hermes config set WANDB_API_KEY your-wandb-key
```

When both keys are present and Python >= 3.11 is available, the `rl` toolset is automatically enabled....

## Available Tools

| Tool | Description |
|------|-------------|
| `rl_list_environments` | Discover available RL environments |
| `rl_select_environment` | Select an environment and load its config |
| `rl_get_current_config` | View configurable and locked fields |
| `rl_edit_config` | Modify configurable training parameters |
| `rl_start_training` | Launch a training run (spawns 3 processes) |
| `rl_check_status` | Monitor training progress and WandB metrics |
| `rl_stop_training` | Stop a running training job |
| `rl_get_results` | Get final metrics and model weights path |
| `rl_list_runs` | List all active ...

## Workflow

### 1. Discover Environments

```
List the available RL environments
```

The agent calls `rl_list_environments()` which scans `tinker-atropos/tinker_atropos/environments/` using AST parsing to find Python classes inheriting from `BaseEnv`. Each environment defines:

- **Dataset loading** — where training data comes from (e.g., HuggingFace datasets)
- **Prompt construction** — how to format items for the model
- **Scoring/verification** — how to evaluate model outputs and assign rewards

### 2. Select and Configure

```
Select the GSM8K environment and show me the configuration
```

The agent ...

## Inference Testing

Before committing to a full training run, you can test if an environment works correctly using `rl_test_inference`. This runs a few steps of inference and scoring using OpenRouter — no Tinker API needed, just an `OPENROUTER_API_KEY`.

```
Test the selected environment with inference
```

Default configuration:
- **3 steps × 16 completions = 48 rollouts per model**
- Tests 3 models at different scales for robustness:
  - `qwen/qwen3-8b` (small)
  - `z-ai/glm-4.7-flash` (medium)
  - `minimax/minimax-m2.7` (large)
- Total: ~144 rollouts

This validates:
- Environment loads correctly
- Prompt cons...

## Tinker API Integration

The trainer uses the [Tinker](https://tinker.computer) API for model training operations:

- **ServiceClient** — Creates training and sampling clients
- **Training client** — Handles forward-backward passes with importance sampling loss, optimizer steps (Adam), and weight checkpointing
- **Sampling client** — Provides inference using the latest trained weights

The training loop:
1. Fetches a batch of rollouts from Atropos (prompt + completions + scores)
2. Converts to Tinker Datum objects with padded logprobs and advantages
3. Runs forward-backward pass with importance sampling loss
4. Takes ...

## Architecture Diagram

```mermaid
flowchart LR
    api["Atropos API<br/>run-api<br/>port 8000"]
    env["Environment<br/>BaseEnv implementation"]
    infer["OpenAI / sglang<br/>inference API<br/>port 8001"]
    trainer["Tinker Trainer<br/>LoRA training + FastAPI"]

    env <--> api
    env --> infer
    api -->|"batches: tokens, scores, logprobs"| trainer
    trainer -->|"serves inference"| infer
```...

## Creating Custom Environments

To create a new RL environment:

1. Create a Python file in `tinker-atropos/tinker_atropos/environments/`
2. Define a class that inherits from `BaseEnv`
3. Implement the required methods:
   - `load_dataset()` — Load your training data
   - `get_next_item()` — Provide the next item to the model
   - `score_answer()` — Score model outputs and assign rewards
   - `collect_trajectories()` — Collect and return trajectories
4. Optionally define a custom config class inheriting from `BaseEnvConfig`

Study the existing `gsm8k_tinker.py` as a template. The agent can help you create new environments — ...

## WandB Metrics

Training runs log to Weights & Biases with these key metrics:

| Metric | Description |
|--------|-------------|
| `train/loss` | Training loss (importance sampling) |
| `train/learning_rate` | Current learning rate |
| `reward/mean` | Mean reward across groups |
| `logprobs/mean` | Mean reference logprobs |
| `logprobs/mean_training` | Mean training logprobs |
| `logprobs/diff` | Logprob drift (reference - training) |
| `advantages/mean` | Mean advantage values |
| `advantages/std` | Advantage standard deviation |...

## Log Files

Each training run generates log files in `~/.hermes/logs/rl_training/`:

```
logs/
├── api_{run_id}.log        # Atropos API server logs
├── trainer_{run_id}.log    # Tinker trainer logs
├── env_{run_id}.log        # Environment process logs
└── inference_tests/        # Inference test results
    ├── test_{env}_{model}.jsonl
    └── test_{env}_{model}.log
```

These are invaluable for debugging when training fails or produces unexpected results....

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
