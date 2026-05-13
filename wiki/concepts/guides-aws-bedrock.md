---
title: AWS Bedrock
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-aws-bedrock.md]
---

# AWS Bedrock

源文档：[AWS Bedrock](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/aws-bedrock.md)

# AWS Bedrock

Hermes Agent supports Amazon Bedrock as a native provider using the **Converse API** — not the OpenAI-compatible endpoint. This gives you full access to the Bedrock ecosystem: IAM authentication, Guardrails, cross-region inference profiles, and all foundation models.

## Prerequisites

- **AWS credentials** — any source supported by the [boto3 credential chain](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html):
  - IAM instance role (EC2, ECS, Lambda — zero config)
  - `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` environment variables
  - `AWS_PROFILE` for SSO or named profiles
  - `aws configure` for local development
- **boto3** — install with `pip install hermes-agent[bedrock]`
- **IAM permissions** — at minimum:
  - `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` (for inference)
  - `bedrock:ListFoundationModels` and `bedr...

## Quick Start

```bash
# Install with Bedrock support
pip install hermes-agent[bedrock]

# Select Bedrock as your provider
hermes model
# → Choose "More providers..." → "AWS Bedrock"
# → Select your region and model

# Start chatting
hermes chat
```...

## Configuration

After running `hermes model`, your `~/.hermes/config.yaml` will contain:

```yaml
model:
  default: us.anthropic.claude-sonnet-4-6
  provider: bedrock
  base_url: https://bedrock-runtime.us-east-2.amazonaws.com

bedrock:
  region: us-east-2
```

### Region

Set the AWS region in any of these ways (highest priority first):

1. `bedrock.region` in `config.yaml`
2. `AWS_REGION` environment variable
3. `AWS_DEFAULT_REGION` environment variable
4. Default: `us-east-1`

### Guardrails

To apply [Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) to all m...

## Available Models

Bedrock models use **inference profile IDs** for on-demand invocation. The `hermes model` picker shows these automatically, with recommended models at the top:

| Model | ID | Notes |
|-------|-----|-------|
| Claude Sonnet 4.6 | `us.anthropic.claude-sonnet-4-6` | Recommended — best balance of speed and capability |
| Claude Opus 4.6 | `us.anthropic.claude-opus-4-6-v1` | Most capable |
| Claude Haiku 4.5 | `us.anthropic.claude-haiku-4-5-20251001-v1:0` | Fastest Claude |
| Amazon Nova Pro | `us.amazon.nova-pro-v1:0` | Amazon's flagship |
| Amazon Nova Micro | `us.amazon.nova-micro-v1:0` | Faste...

## Switching Models Mid-Session

Use the `/model` command during a conversation:

```
/model us.amazon.nova-pro-v1:0
/model deepseek.v3.2
/model us.anthropic.claude-opus-4-6-v1
```...

## Diagnostics

```bash
hermes doctor
```

The doctor checks:
- Whether AWS credentials are available (env vars, IAM role, SSO)
- Whether `boto3` is installed
- Whether the Bedrock API is reachable (ListFoundationModels)
- Number of available models in your region...

## Gateway (Messaging Platforms)

Bedrock works with all Hermes gateway platforms (Telegram, Discord, Slack, Feishu, etc.). Configure Bedrock as your provider, then start the gateway normally:

```bash
hermes gateway setup
hermes gateway start
```

The gateway reads `config.yaml` and uses the same Bedrock provider configuration....

## Troubleshooting

### "No API key found" / "No AWS credentials"

Hermes checks for credentials in this order:
1. `AWS_BEARER_TOKEN_BEDROCK`
2. `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`
3. `AWS_PROFILE`
4. EC2 instance metadata (IMDS)
5. ECS container credentials
6. Lambda execution role

If none are found, run `aws configure` or attach an IAM role to your compute instance.

### "Invocation of model ID ... with on-demand throughput isn't supported"

Use an **inference profile ID** (prefixed with `us.` or `global.`) instead of the bare foundation model ID. For example:
- ❌ `anthropic.claude-sonnet-4-6`
- ✅ `u...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
