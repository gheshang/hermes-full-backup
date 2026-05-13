---
title: Adding Providers
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/developer-guide-adding-providers.md]
---

# Adding Providers

源文档：[Adding Providers](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/adding-providers.md)

# Adding Providers

Hermes can already talk to any OpenAI-compatible endpoint through the custom provider path. Do not add a built-in provider unless you want first-class UX for that service:

- provider-specific auth or token refresh
- a curated model catalog
- setup / `hermes model` menu entries
- provider aliases for `provider:model` syntax
- a non-OpenAI API shape that needs an adapter

If the provider is just "another OpenAI-compatible base URL and API key", a named custom provider may be enough.

## The mental model

A built-in provider has to line up across a few layers:

1. `hermes_cli/auth.py` decides how credentials are found.
2. `hermes_cli/runtime_provider.py` turns that into runtime data:
   - `provider`
   - `api_mode`
   - `base_url`
   - `api_key`
   - `source`
3. `run_agent.py` uses `api_mode` to decide how requests are built and sent.
4. `hermes_cli/models.py` and `hermes_cli/main.py` make the provider show up in the CLI. (`hermes_cli/setup.py` delegates to `main.py` automatically — no changes needed there.)
5. `agent/auxiliary_client.py` and `agent/model_metadata.py` keep side tasks and token ...

## Choose the implementation path first

### Path A — OpenAI-compatible provider

Use this when the provider accepts standard chat-completions style requests.

Typical work:

- add auth metadata
- add model catalog / aliases
- add runtime resolution
- add CLI menu wiring
- add aux-model defaults
- add tests and user docs

You usually do not need a new adapter or a new `api_mode`.

### Path B — Native provider

Use this when the provider does not behave like OpenAI chat completions.

Examples in-tree today:

- `codex_responses`
- `anthropic_messages`

This path includes everything from Path A plus:

- a provider adapter in `agent/`
- ...

## File checklist

### Required for every built-in provider

1. `hermes_cli/auth.py`
2. `hermes_cli/models.py`
3. `hermes_cli/runtime_provider.py`
4. `hermes_cli/main.py`
5. `agent/auxiliary_client.py`
6. `agent/model_metadata.py`
7. tests
8. user-facing docs under `website/docs/`

:::tip
`hermes_cli/setup.py` does **not** need changes. The setup wizard delegates provider/model selection to `select_provider_and_model()` in `main.py` — any provider added there is automatically available in `hermes setup`.
:::

### Additional for native / non-OpenAI providers

10. `agent/<provider>_adapter.py`
11. `run_agent.py`
1...

## Step 1: Pick one canonical provider id

Choose a single provider id and use it everywhere.

Examples from the repo:

- `openai-codex`
- `kimi-coding`
- `minimax-cn`

That same id should appear in:

- `PROVIDER_REGISTRY` in `hermes_cli/auth.py`
- `_PROVIDER_LABELS` in `hermes_cli/models.py`
- `_PROVIDER_ALIASES` in both `hermes_cli/auth.py` and `hermes_cli/models.py`
- CLI `--provider` choices in `hermes_cli/main.py`
- setup / model selection branches
- auxiliary-model defaults
- tests

If the id differs between those files, the provider will feel half-wired: auth may work while `/model`, setup, or runtime resolution silently misses ...

## Step 2: Add auth metadata in `hermes_cli/auth.py`

For API-key providers, add a `ProviderConfig` entry to `PROVIDER_REGISTRY` with:

- `id`
- `name`
- `auth_type="api_key"`
- `inference_base_url`
- `api_key_env_vars`
- optional `base_url_env_var`

Also add aliases to `_PROVIDER_ALIASES`.

Use the existing providers as templates:

- simple API-key path: Z.AI, MiniMax
- API-key path with endpoint detection: Kimi, Z.AI
- native token resolution: Anthropic
- OAuth / auth-store path: Nous, OpenAI Codex

Questions to answer here:

- What env vars should Hermes check, and in what priority order?
- Does the provider need base-URL overrides?
- Does it ...

## Step 3: Add model catalog and aliases in `hermes_cli/models.py`

Update the provider catalog so the provider works in menus and in `provider:model` syntax.

Typical edits:

- `_PROVIDER_MODELS`
- `_PROVIDER_LABELS`
- `_PROVIDER_ALIASES`
- provider display order inside `list_available_providers()`
- `provider_model_ids()` if the provider supports a live `/models` fetch

If the provider exposes a live model list, prefer that first and keep `_PROVIDER_MODELS` as the static fallback.

This file is also what makes inputs like these work:

```text
anthropic:claude-sonnet-4-6
kimi:model-name
```

If aliases are missing here, the provider may authenticate correctly...

## Step 4: Resolve runtime data in `hermes_cli/runtime_provider.py`

`resolve_runtime_provider()` is the shared path used by CLI, gateway, cron, ACP, and helper clients.

Add a branch that returns a dict with at least:

```python
{
    "provider": "your-provider",
    "api_mode": "chat_completions",  # or your native mode
    "base_url": "https://...",
    "api_key": "...",
    "source": "env|portal|auth-store|explicit",
    "requested_provider": requested_provider,
}
```

If the provider is OpenAI-compatible, `api_mode` should usually stay `chat_completions`.

Be careful with API-key precedence. Hermes already contains logic to avoid leaking an OpenRouter key ...

## Step 5: Wire the CLI in `hermes_cli/main.py`

A provider is not discoverable until it shows up in the interactive `hermes model` flow.

Update these in `hermes_cli/main.py`:

- `provider_labels` dict
- `providers` list in `select_provider_and_model()`
- provider dispatch (`if selected_provider == ...`)
- `--provider` argument choices
- login/logout choices if the provider supports those flows
- a `_model_flow_<provider>()` function, or reuse `_model_flow_api_key_provider()` if it fits

:::tip
`hermes_cli/setup.py` does not need changes — it calls `select_provider_and_model()` from `main.py`, so your new provider appears in both `hermes mo...

## Step 6: Keep auxiliary calls working

Two files matter here:

### `agent/auxiliary_client.py`

Add a cheap / fast default aux model to `_API_KEY_PROVIDER_AUX_MODELS` if this is a direct API-key provider.

Auxiliary tasks include things like:

- vision summarization
- web extraction summarization
- context compression summaries
- session-search summaries
- memory flushes

If the provider has no sensible aux default, side tasks may fall back badly or use an expensive main model unexpectedly.

### `agent/model_metadata.py`

Add context lengths for the provider's models so token budgeting, compression thresholds, and limits stay sane....

## Step 7: If the provider is native, add an adapter and `run_agent.py` support

If the provider is not plain chat completions, isolate the provider-specific logic in `agent/<provider>_adapter.py`.

Keep `run_agent.py` focused on orchestration. It should call adapter helpers, not hand-build provider payloads inline all over the file.

A native provider usually needs work in these places:

### New adapter file

Typical responsibilities:

- build the SDK / HTTP client
- resolve tokens
- convert OpenAI-style conversation messages to the provider's request format
- convert tool schemas if needed
- normalize provider responses back into what `run_agent.py` expects
- extract usa...

## Step 8: Tests

At minimum, touch the tests that guard provider wiring.

Common places:

- `tests/test_runtime_provider_resolution.py`
- `tests/test_cli_provider_resolution.py`
- `tests/test_cli_model_command.py`
- `tests/test_setup_model_selection.py`
- `tests/test_provider_parity.py`
- `tests/test_run_agent.py`
- `tests/test_<provider>_adapter.py` for a native provider

For docs-only examples, the exact file set may differ. The point is to cover:

- auth resolution
- CLI menu / provider selection
- runtime provider resolution
- agent execution path
- provider:model parsing
- any adapter-specific message con...

## Step 9: Live verification

After tests, run a real smoke test.

```bash
source venv/bin/activate
python -m hermes_cli.main chat -q "Say hello" --provider your-provider --model your-model
```

Also test the interactive flows if you changed menus:

```bash
source venv/bin/activate
python -m hermes_cli.main model
python -m hermes_c

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
