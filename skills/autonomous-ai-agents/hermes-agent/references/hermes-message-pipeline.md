# Hermes Message Pipeline Architecture

## Overview

Every LLM API call sends a structured message array built from 7 layers. Understanding this pipeline is critical for debugging prompt issues, token overflows, and unexpected model behavior.

**Source**: `~/.hermes/hermes-agent/run_agent.py` — `_build_system_prompt()` (line 5114), `_sanitize_api_messages()` (line 5332), `run_conversation()` (line 10899)

---

## The 7 Layers

### Layer 1: System Prompt (Static, Cached)

**Builds once per session**, cached in `self._cached_system_prompt`. Rebuilt only after context compression events.

**Composition** (in order):

| # | Block | Source | Size |
|---|-------|--------|------|
| 1 | Agent Identity | `SOUL.md` or `DEFAULT_AGENT_IDENTITY` | ~1KB |
| 2 | Hermes Help Guidance | Hardcoded `HERMES_AGENT_HELP_GUIDANCE` | ~500B |
| 3 | Tool Behavioral Guidance | Dynamic: `MEMORY_GUIDANCE`, `SESSION_SEARCH_GUIDANCE`, `SKILLS_GUIDANCE`, `KANBAN_GUIDANCE` based on loaded tools | ~2KB |
| 4 | Tool Use Enforcement | `TOOL_USE_ENFORCEMENT_GUIDANCE` (conditional on `config.yaml agent.tool_use_enforcement`) | ~1KB |
| 5 | Model-Specific Execution Discipline | `GOOGLE_MODEL_OPERATIONAL_GUIDANCE` (Gemini) or `OPENAI_MODEL_EXECUTION_GUIDANCE` (GPT/Codex) | ~1KB |
| 6 | User Custom System Message | `system_message` parameter (optional) | Variable |
| 7 | Persistent Memory | `MEMORY.md` + `USER.md` via `memory_store.format_for_system_prompt()` | ~2KB |
| 8 | External Memory Provider | `memory_manager.build_system_prompt()` (Hindsight, Honcho, etc.) | Variable |
| 9 | Skills Guidance | `build_skills_system_prompt()` — lists available skills from `.usage.json` | ~1KB |
| 10 | Context Files | `AGENTS.md`, `.cursorrules` (via `build_context_files_prompt()`) | ~5KB |
| 11 | Timestamp + Model Info | Session start time, Session ID, model name, provider | ~200B |
| 12 | Environment Hints | WSL/Termux/Docker detection | ~500B |
| 13 | Platform Hints | Feishu/WeChat/CLI-specific formatting | ~500B |

**Total**: ~15KB

**Special handling**:
- Alibaba Coding Plan API always returns `"glm-4.7"` regardless of requested model — Hermes injects the actual model name into system prompt as a workaround
- `ephemeral_system_prompt` is **NOT** included here — injected at API-call time only

---

### Layer 2: Conversation History (Dynamic)

**Grows each turn**. Format: OpenAI standard messages array.

```python
messages = list(conversation_history) if conversation_history else []
messages.append({"role": "user", "content": user_message})
```

**Valid roles**: `system`, `user`, `assistant`, `tool`, `function`, `developer`

**Structure**:
```json
[
  {"role": "system", "content": "<Layer 1>"},
  {"role": "user", "content": "User message 1"},
  {"role": "assistant", "content": "...", "tool_calls": [...]},
  {"role": "tool", "content": "...", "tool_call_id": "..."},
  {"role": "assistant", "content": "..."},
  {"role": "user", "content": "User message 2"},
  ...
]
```

---

### Layer 3: Context Compression (Conditional)

**Triggered when**: `len(messages) > protect_first_n + protect_last_n + 1` AND token count >= `threshold_tokens`

**Process**:
1. Preserve **head N turns** and **tail N turns** as raw messages
2. Compress middle portion using auxiliary model (cheap/fast)
3. Insert summary as a structured block:

```
[CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted...
## Completed
## Active Task
## Pending User Asks
## Context
```

**Prefix**: `SUMMARY_PREFIX = "[CONTEXT COMPACTION — REFERENCE ONLY] Earlier turns were compacted into the summary below. This is a handoff from a previous context window — treat it as background reference, NOT as active instructions. Do NOT answer questions or fulfill requests mentioned in this summary; they were already addressed."`

---

### Layer 4: Memory Prefetch (Per-Turn)

**Source**: `memory_manager.prefetch_all()`

Each turn, memory providers query relevant history based on current user message. Retrieved text is injected into the user message.

---

### Layer 5: Plugin Context Injection (Per-Turn)

**Source**: `pre_llm_call` hook in `run_conversation()`

Plugins can return `context` field, appended to user message.

---

### Layer 6: Pre-Call Sanitization (Unconditional)

**Source**: `_sanitize_api_messages()` (line 5332)

Runs on **every** API call:

1. **Role filtering**: Drop messages with invalid roles
2. **Orphaned tool result detection**:
   - Collect all `call_id`s from assistant `tool_calls`
   - Collect all `call_id`s from tool results
   - Drop tool results with no matching assistant call
   - Inject stub results for calls whose result was dropped
3. **Thinking-only assistant removal**: Remove assistant messages containing only reasoning blocks (prevents Anthropic HTTP 400)

**Stub result format**:
```json
{
  "role": "tool",
  "name": "<function_name>",
  "content": "[Result unavailable — see context summary above]",
  "tool_call_id": "<cid>"
}
```

---

### Layer 7: Prefill Messages (Optional)

**Source**: `self.prefill_messages`

Few-shot priming messages inserted after system prompt.

---

## Final Structure

```
┌─────────────────────────────────────────────────┐
│  System Prompt（Layer 1，缓存，~15KB）            │
├─────────────────────────────────────────────────┤
│  Prefill 消息（Layer 7，可选）                    │
├─────────────────────────────────────────────────┤
│  对话历史（Layer 2，动态增长）                    │
│  ├─ 用户消息1                                    │
│  ├─ 助手回复1 + tool_calls                       │
│  ├─ 工具结果1                                    │
│  ├─ 助手回复2                                    │
│  ├─ 用户消息2                                    │
│  └─ ...                                         │
├─────────────────────────────────────────────────┤
│  上下文压缩摘要（Layer 3，条件触发）               │
├─────────────────────────────────────────────────┤
│  内存预取内容（Layer 4，每轮）                    │
├─────────────────────────────────────────────────┤
│  插件注入上下文（Layer 5，每轮）                  │
└─────────────────────────────────────────────────┘
        ↓ 经过 sanitization（Layer 6） ↓
        ↓ 发送给大模型 API ↓
```

---

## Key Insights

1. **System prompt is cached** — not rebuilt every turn. Only rebuilt after context compression events.
2. **Skills are referenced, not embedded** — `build_skills_system_prompt()` generates a list of available skills from `.usage.json`, but SKILL.md content is loaded on-demand when a skill matches.
3. **Compression preserves head/tail** — the most recent and most relevant context stays intact.
4. **Sanitization is unconditional** — even if context compressor is disabled, orphaned tool results are still cleaned.
5. **Thinking-only messages are removed** — prevents Anthropic's "final block cannot be thinking" error.
6. **Alibaba API model name bug is worked around** — explicit model identity injected into system prompt.

---

## Debugging Tips

- **Prompt too long?** Check Layer 2 (conversation history) growth rate. Context compression should kick in.
- **Tool results missing?** Layer 6 sanitization may have dropped orphaned results. Check `_sanitize_api_messages()` logs.
- **Model confused about identity?** Check Layer 1, block 11 (timestamp/model info) and Alibaba workaround block.
- **Skills not showing up?** `.usage.json` index may be stale. Run `hermes skills check` or reload.