---
title: Google Vertex AI integration - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/google-vertex-ai.md]
---

# Google Vertex AI integration - Anthropic

源文档：[Google Vertex AI integration - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/google-vertex-ai/google-vertex-ai.md)

# Google Vertex AI integration - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai  
**Category:** google-vertex-ai  
**Scraped:** 2025-06-09 06:37:30

---

## Original Content

This page provides instructions on configuring Claude Code through Google Vertex AI, including setup, IAM configuration, cost tracking, and troubleshooting....

## ​

Prerequisites

Before configuring Claude Code with Vertex AI, ensure you have:

  * A Google Cloud Platform (GCP) account with billing enabled
  * A GCP project with Vertex AI API enabled
  * Access to desired Claude models (e.g., Claude Sonnet 4)
  * Google Cloud SDK (`gcloud`) installed and configured
  * Quota allocated in desired GCP region

Vertex AI may not support the Claude Code default models on non-`us-east5` regions. Ensure you are using `us-east5` and have quota allocated, or switch to supported models....

## ​

Setup

### 

​

1\. Enable Vertex AI API

Enable the Vertex AI API in your GCP project:
    
    # Set your project ID
    gcloud config set project YOUR-PROJECT-ID
    
    # Enable Vertex AI API
    gcloud services enable aiplatform.googleapis.com
    
### 

​

2\. Request model access

Request access to Claude models in Vertex AI:

  1. Navigate to the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
  2. Search for “Claude” models
  3. Request access to desired Claude models (e.g., Claude Sonnet 4)
  4. Wait for approval (may take 24-48 hours)

### 

​

3\....

## ​

IAM configuration

Grant the required IAM roles for Claude Code.

For details, see [Vertex IAM documentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

We recommend creating a dedicated GCP project for Claude Code to simplify cost tracking and access control....

## ​

Troubleshooting

If you encounter quota issues:

  * Check current quotas or request quota increase through [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

If you encounter “model not found” 404 errors:

  * Verify you have access to the specified region
  * Confirm model is Enabled in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)

If you encounter 429 errors:

  * Ensure the primary model and small/fast model are supported in your selected region...

## ​

Additional resources

  * [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
  * [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing)
  * [Vertex AI quotas and limits](https://cloud.google.com/vertex-ai/docs/quotas)

Was this page helpful?

YesNo

[Amazon Bedrock](/en/docs/claude-code/amazon-bedrock)[Corporate proxy](/en/docs/claude-code/corporate-proxy)


---...

## AI Analysis

```markdown
1.  **Concise Summary:**
    This documentation outlines the process of integrating Claude Code with Google Vertex AI, covering essential setup steps, IAM configuration, and troubleshooting tips. It emphasizes prerequisites like a GCP account and specific region usage (`us-east5`) for optimal model support, guiding users through API enablement, model access requests, and environment variable configuration.

2.  **Key Topics Covered:**
    *   Prerequisites for Vertex AI integration
    *   Step-by-step setup process (API enablement, model access, credentials, configuration)
    *  ...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
