---
title: Using Hermes as a Python Library
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-python-library.md]
---

# Using Hermes as a Python Library

源文档：[Using Hermes as a Python Library](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/python-library.md)

# Using Hermes as a Python Library

Hermes isn't just a CLI tool. You can import `AIAgent` directly and use it programmatically in your own Python scripts, web applications, or automation pipelines. This guide shows you how.

---

## Installation

Install Hermes directly from the repository:

```bash
pip install git+https://github.com/NousResearch/hermes-agent.git
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install git+https://github.com/NousResearch/hermes-agent.git
```

You can also pin it in your `requirements.txt`:

```text
hermes-agent @ git+https://github.com/NousResearch/hermes-agent.git
```

:::tip
The same environment variables used by the CLI are required when using Hermes as a library. At minimum, set `OPENROUTER_API_KEY` (or `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` if using direct provider access).
:::

---...

## Basic Usage

The simplest way to use Hermes is the `chat()` method — pass a message, get a string back:

```python
from run_agent import AIAgent

agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    quiet_mode=True,
)
response = agent.chat("What is the capital of France?")
print(response)
```

`chat()` handles the full conversation loop internally — tool calls, retries, everything — and returns just the final text response.

:::warning
Always set `quiet_mode=True` when embedding Hermes in your own code. Without it, the agent prints CLI spinners, progress indicators, and other terminal output that wi...

## Full Conversation Control

For more control over the conversation, use `run_conversation()` directly. It returns a dictionary with the full response, message history, and metadata:

```python
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    quiet_mode=True,
)

result = agent.run_conversation(
    user_message="Search for recent Python 3.13 features",
    task_id="my-task-1",
)

print(result["final_response"])
print(f"Messages exchanged: {len(result['messages'])}")
```

The returned dictionary contains:
- **`final_response`** — The agent's final text reply
- **`messages`** — The complete message history (syste...

## Configuring Tools

Control which toolsets the agent has access to using `enabled_toolsets` or `disabled_toolsets`:

```python
# Only enable web tools (browsing, search)
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    enabled_toolsets=["web"],
    quiet_mode=True,
)

# Enable everything except terminal access
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    disabled_toolsets=["terminal"],
    quiet_mode=True,
)
```

:::tip
Use `enabled_toolsets` when you want a minimal, locked-down agent (e.g., only web search for a research bot). Use `disabled_toolsets` when you want most capabilities but ...

## Multi-turn Conversations

Maintain conversation state across multiple turns by passing the message history back in:

```python
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    quiet_mode=True,
)

# First turn
result1 = agent.run_conversation("My name is Alice")
history = result1["messages"]

# Second turn — agent remembers the context
result2 = agent.run_conversation(
    "What's my name?",
    conversation_history=history,
)
print(result2["final_response"])  # "Your name is Alice."
```

The `conversation_history` parameter accepts the `messages` list from a previous result. The agent copies it internally, s...

## Saving Trajectories

Enable trajectory saving to capture conversations in ShareGPT format — useful for generating training data or debugging:

```python
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    save_trajectories=True,
    quiet_mode=True,
)

agent.chat("Write a Python function to sort a list")
# Saves to trajectory_samples.jsonl in ShareGPT format
```

Each conversation is appended as a single JSONL line, making it easy to collect datasets from automated runs.

---...

## Custom System Prompts

Use `ephemeral_system_prompt` to set a custom system prompt that guides the agent's behavior but is **not** saved to trajectory files (keeping your training data clean):

```python
agent = AIAgent(
    model="anthropic/claude-sonnet-4",
    ephemeral_system_prompt="You are a SQL expert. Only answer database questions.",
    quiet_mode=True,
)

response = agent.chat("How do I write a JOIN query?")
print(response)
```

This is ideal for building specialized agents — a code reviewer, a documentation writer, a SQL assistant — all using the same underlying tooling.

---...

## Batch Processing

For running many prompts in parallel, Hermes includes `batch_runner.py`. It manages concurrent `AIAgent` instances with proper resource isolation:

```bash
python batch_runner.py --input prompts.jsonl --output results.jsonl
```

Each prompt gets its own `task_id` and isolated environment. If you need custom batch logic, you can build your own using `AIAgent` directly:

```python
import concurrent.futures
from run_agent import AIAgent

prompts = [
    "Explain recursion",
    "What is a hash table?",
    "How does garbage collection work?",
]

def process_prompt(prompt):
    # Create a fresh ag...

## Integration Examples

### FastAPI Endpoint

```python
from fastapi import FastAPI
from pydantic import BaseModel
from run_agent import AIAgent

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    model: str = "anthropic/claude-sonnet-4"

@app.post("/chat")
async def chat(request: ChatRequest):
    agent = AIAgent(
        model=request.model,
        quiet_mode=True,
        skip_context_files=True,
        skip_memory=True,
    )
    response = agent.chat(request.message)
    return {"response": response}
```

### Discord Bot

```python
import discord
from run_agent import AIAgent

client = discord...

## Key Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `model` | `str` | `"anthropic/claude-opus-4.6"` | Model in OpenRouter format |
| `quiet_mode` | `bool` | `False` | Suppress CLI output |
| `enabled_toolsets` | `List[str]` | `None` | Whitelist specific toolsets |
| `disabled_toolsets` | `List[str]` | `None` | Blacklist specific toolsets |
| `save_trajectories` | `bool` | `False` | Save conversations to JSONL |
| `ephemeral_system_prompt` | `str` | `None` | Custom system prompt (not saved to trajectories) |
| `max_iterations` | `int` | `90` | Max tool-ca...

## Important Notes

:::tip
- Set **`skip_context_files=True`** if you don't want `AGENTS.md` files from the working directory loaded into the system prompt.
- Set **`skip_memory=True`** to prevent the agent from reading or writing persistent memory — recommended for stateless API endpoints.
- The `platform` parameter (e.g., `"discord"`, `"telegram"`) injects platform-specific formatting hints so the agent adapts its output style.
:::

:::warning
- **Thread safety**: Create one `AIAgent` per thread or task. Never share an instance across concurrent calls.
- **Resource cleanup**: The agent automatically cleans up r...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
