---
title: Tips & Best Practices
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-tips.md]
---

# Tips & Best Practices

源文档：[Tips & Best Practices](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/tips.md)

# Tips & Best Practices

A quick-wins collection of practical tips that make you immediately more effective with Hermes Agent. Each section targets a different aspect — scan the headers and jump to what's relevant.

---

## Getting the Best Results

### Be Specific About What You Want

Vague prompts produce vague results. Instead of "fix the code," say "fix the TypeError in `api/handlers.py` on line 47 — the `process_request()` function receives `None` from `parse_body()`." The more context you give, the fewer iterations you need.

### Provide Context Up Front

Front-load your request with the relevant details: file paths, error messages, expected behavior. One well-crafted message beats three rounds of clarification. Paste error tracebacks directly — the agent can parse them.

### Use Context Files for Recurring Instructions

If you find...

## CLI Power User Tips

### Multi-Line Input

Press **Alt+Enter** (or **Ctrl+J**) to insert a newline without sending. This lets you compose multi-line prompts, paste code blocks, or structure complex requests before hitting Enter to send.

### Paste Detection

The CLI auto-detects multi-line pastes. Just paste a code block or error traceback directly — it won't send each line as a separate message. The paste is buffered and sent as one message.

### Interrupt and Redirect

Press **Ctrl+C** once to interrupt the agent mid-response. You can then type a new message to redirect it. Double-press Ctrl+C within 2 seconds t...

## Context Files

### AGENTS.md: Your Project's Brain

Create an `AGENTS.md` in your project root with architecture decisions, coding conventions, and project-specific instructions. This is automatically injected into every session, so the agent always knows your project's rules.

```markdown
# Project Context
- This is a FastAPI backend with SQLAlchemy ORM
- Always use async/await for database operations
- Tests go in tests/ and use pytest-asyncio
- Never commit .env files
```

### SOUL.md: Customize Personality

Want Hermes to have a stable default voice? Edit `~/.hermes/SOUL.md` (or `$HERMES_HOME/SOUL.md` if...

## Memory & Skills

### Memory vs. Skills: What Goes Where

**Memory** is for facts: your environment, preferences, project locations, and things the agent has learned about you. **Skills** are for procedures: multi-step workflows, tool-specific instructions, and reusable recipes. Use memory for "what," skills for "how."

### When to Create Skills

If you find a task that takes 5+ steps and you'll do it again, ask the agent to create a skill for it. Say "save what you just did as a skill called `deploy-staging`." Next time, just type `/deploy-staging` and the agent loads the full procedure.

### Managing Memory C...

## Performance & Cost

### Don't Break the Prompt Cache

Most LLM providers cache the system prompt prefix. If you keep your system prompt stable (same context files, same memory), subsequent messages in a session get **cache hits** that are significantly cheaper. Avoid changing the model or system prompt mid-session.

### Use /compress Before Hitting Limits

Long sessions accumulate tokens. When you notice responses slowing down or getting truncated, run `/compress`. This summarizes the conversation history, preserving key context while dramatically reducing token count. Use `/usage` to check where you stand.

### ...

## Messaging Tips

### Set a Home Channel

Use `/sethome` in your preferred Telegram or Discord chat to designate it as the home channel. Cron job results and scheduled task outputs are delivered here. Without it, the agent has nowhere to send proactive messages.

### Use /title to Organize Sessions

Name your sessions with `/title auth-refactor` or `/title research-llm-quantization`. Named sessions are easy to find with `hermes sessions list` and resume with `hermes -r "auth-refactor"`. Unnamed sessions pile up and become impossible to distinguish.

### DM Pairing for Team Access

Instead of manually collecting...

## Security

### Use Docker for Untrusted Code

When working with untrusted repositories or running unfamiliar code, use Docker or Daytona as your terminal backend. Set `TERMINAL_BACKEND=docker` in your `.env`. Destructive commands inside a container can't harm your host system.

```bash
# In your .env:
TERMINAL_BACKEND=docker
TERMINAL_DOCKER_IMAGE=hermes-sandbox:latest
```

### Avoid Windows Encoding Pitfalls

On Windows, some default encodings (such as `cp125x`) cannot represent all Unicode characters, which can cause `UnicodeEncodeError` when writing files in tests or scripts.

- Prefer opening files wi...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
