# Google Vertex AI integration - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/google-vertex-ai  
**Category:** google-vertex-ai  
**Scraped:** 2025-06-09 06:37:30

---

## Original Content

This page provides instructions on configuring Claude Code through Google Vertex AI, including setup, IAM configuration, cost tracking, and troubleshooting.

## 

​

Prerequisites

Before configuring Claude Code with Vertex AI, ensure you have:

  * A Google Cloud Platform (GCP) account with billing enabled
  * A GCP project with Vertex AI API enabled
  * Access to desired Claude models (e.g., Claude Sonnet 4)
  * Google Cloud SDK (`gcloud`) installed and configured
  * Quota allocated in desired GCP region

Vertex AI may not support the Claude Code default models on non-`us-east5` regions. Ensure you are using `us-east5` and have quota allocated, or switch to supported models.

## 

​

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

3\. Configure GCP credentials

Claude Code uses standard Google Cloud authentication.

For more information, see [Google Cloud authentication documentation](https://cloud.google.com/docs/authentication).

### 

​

4\. Configure Claude Code

Set the following environment variables:
    
    # Enable Vertex AI integration
    export CLAUDE_CODE_USE_VERTEX=1
    export CLOUD_ML_REGION=us-east5
    export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID
    
    # Optional: Disable prompt caching if not enabled
    export DISABLE_PROMPT_CACHING=1
    
For heightened rate limits and prompt caching enablement, contact Google Cloud support. Once enabled, remove the `DISABLE_PROMPT_CACHING` setting.

### 

​

5\. Model configuration

Claude Code uses these default models for Vertex AI:

Model type| Default value  
---|---  
Primary model| `claude-sonnet-4@20250514`  
Small/fast model| `claude-3-5-haiku@20241022`  
  
To customize models:
    
    export ANTHROPIC_MODEL='claude-opus-4@20250514'
    export ANTHROPIC_SMALL_FAST_MODEL='claude-3-5-haiku@20241022'
    
## 

​

IAM configuration

Grant the required IAM roles for Claude Code.

For details, see [Vertex IAM documentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

We recommend creating a dedicated GCP project for Claude Code to simplify cost tracking and access control.

## 

​

Troubleshooting

If you encounter quota issues:

  * Check current quotas or request quota increase through [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

If you encounter “model not found” 404 errors:

  * Verify you have access to the specified region
  * Confirm model is Enabled in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)

If you encounter 429 errors:

  * Ensure the primary model and small/fast model are supported in your selected region

## 

​

Additional resources

  * [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
  * [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing)
  * [Vertex AI quotas and limits](https://cloud.google.com/vertex-ai/docs/quotas)

Was this page helpful?

YesNo

[Amazon Bedrock](/en/docs/claude-code/amazon-bedrock)[Corporate proxy](/en/docs/claude-code/corporate-proxy)


---

## AI Analysis

```markdown
1.  **Concise Summary:**
    This documentation outlines the process of integrating Claude Code with Google Vertex AI, covering essential setup steps, IAM configuration, and troubleshooting tips. It emphasizes prerequisites like a GCP account and specific region usage (`us-east5`) for optimal model support, guiding users through API enablement, model access requests, and environment variable configuration.

2.  **Key Topics Covered:**
    *   Prerequisites for Vertex AI integration
    *   Step-by-step setup process (API enablement, model access, credentials, configuration)
    *   IAM (Identity and Access Management) recommendations
    *   Troubleshooting common issues (quota, model not found, rate limits)
    *   Model configuration and customization

3.  **Important Technical Details:**
    *   **Region Specificity:** `us-east5` is the recommended and potentially only supported region for Claude Code default models on Vertex AI. Users must ensure quota allocation in this region.
    *   **API Enablement:** `aiplatform.googleapis.com` must be enabled.
    *   **Model Access:** Access to Claude models (e.g., Claude Sonnet 4) must be requested via the Vertex AI Model Garden and may take 24-48 hours for approval.
    *   **Authentication:** Standard Google Cloud authentication is used.
    *   **Environment Variables:** Key variables for integration are `CLAUDE_CODE_USE_VERTEX=1`, `CLOUD_ML_REGION=us-east5`, and `ANTHROPIC_VERTEX_PROJECT_ID`.
    *   **Default Models:** `claude-sonnet-4@20250514` (primary) and `claude-3-5-haiku@20241022` (small/fast) are the defaults.
    *   **Model Customization:** `ANTHROPIC_MODEL` and `ANTHROPIC_SMALL_FAST_MODEL` environment variables can override default models.
    *   **Prompt Caching:** Disabled by default (`DISABLE_PROMPT_CACHING=1`) unless enabled by Google Cloud support.
    *   **IAM:** Recommends a dedicated GCP project for simplified cost tracking and access control.

4.  **Code Examples:**

    *   **Enable Vertex AI API:**
        ```bash
        # Set your project ID
        gcloud config set project YOUR-PROJECT-ID

        # Enable Vertex AI API
        gcloud services enable aiplatform.googleapis.com
        ```

    *   **Configure Claude Code Environment Variables:**
        ```bash
        # Enable Vertex AI integration
        export CLAUDE_CODE_USE_VERTEX=1
        export CLOUD_ML_REGION=us-east5
        export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

        # Optional: Disable prompt caching if not enabled
        export DISABLE_PROMPT_CACHING=1
        ```

    *   **Customize Models:**
        ```bash
        export ANTHROPIC_MODEL='claude-opus-4@20250514'
        export ANTHROPIC_SMALL_FAST_MODEL='claude-3-5-haiku@20241022'
        ```

5.  **Related Concepts or Prerequisites:**
    *   Google Cloud Platform (GCP) account with billing enabled.
    *   GCP project with Vertex AI API enabled.
    *   Google Cloud SDK (`gcloud`) installed and configured.
    *   Understanding of GCP IAM roles and access control.
    *   Familiarity with environment variables.
    *   Knowledge of Vertex AI Model Garden for model access.
    *   Quota management within GCP.
```
