# LLM gateway configuration - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/llm-gateway  
**Category:** llm-gateway  
**Scraped:** 2025-06-09 06:37:49

---

## Original Content

This page covers how to configure Claude Code with LLM gateway solutions, including LiteLLM setup, authentication methods, and enterprise features like usage tracking and budget management.

## 

​

Overview

LLM gateways provide a centralized proxy layer between Claude Code and model providers, offering:

  * **Centralized authentication** \- Single point for API key management
  * **Usage tracking** \- Monitor usage across teams and projects
  * **Cost controls** \- Implement budgets and rate limits
  * **Audit logging** \- Track all model interactions for compliance
  * **Model routing** \- Switch between providers without code changes

## 

​

LiteLLM configuration

LiteLLM is a third-party proxy service. Anthropic doesn’t endorse, maintain, or audit LiteLLM’s security or functionality. This guide is provided for informational purposes and may become outdated. Use at your own discretion.

### 

​

Prerequisites

  * Claude Code updated to the latest version
  * LiteLLM Proxy Server deployed and accessible
  * Access to Claude models through your chosen provider

### 

​

Basic LiteLLM setup

**Configure Claude Code** :

#### 

​

Authentication methods

##### Static API key

Simplest method using a fixed API key:
    
    # Set in environment
    export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key
    
    # Or in Claude Code settings
    {
      "env": {
        "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
      }
    }
    
This value will be sent as the `Authorization` and `Proxy-Authorization` headers, although `Authorization` may be overwritten (see Vertex “Client-specified credentials” below).

##### Dynamic API key with helper

For rotating keys or per-user authentication:

  1. Create an API key helper script:

    #!/bin/bash
    # ~/bin/get-litellm-key.sh
    
    # Example: Fetch key from vault
    vault kv get -field=api_key secret/litellm/claude-code
    
    # Example: Generate JWT token
    jwt encode \
      --secret="${JWT_SECRET}" \
      --exp="+1h" \
      '{"user":"'${USER}'","team":"engineering"}'
    
  2. Configure Claude Code settings to use the helper:

    {
      "apiKeyHelper": "~/bin/get-litellm-key.sh"
    }
    
  3. Set token refresh interval:

    # Refresh every hour (3600000 ms)
    export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
    
This value will be sent as `Authorization`, `Proxy-Authorization`, and `X-Api-Key` headers, although `Authorization` may be overwritten (see [Google Vertex AI through LiteLLM](/_sites/docs.anthropic.com/en/docs/claude-code/llm-gateway#google-vertex-ai-through-litellm)). The `apiKeyHelper` has lower precedence than `ANTHROPIC_AUTH_TOKEN` or `ANTHROPIC_API_KEY`.

#### 

​

Provider-specific configurations

##### Anthropic API through LiteLLM

Using [pass-through endpoint](https://docs.litellm.ai/docs/pass_through/anthropic_completion):
    
    export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
    
##### Amazon Bedrock through LiteLLM

Using [pass-through endpoint](https://docs.litellm.ai/docs/pass_through/bedrock):
    
    export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
    export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
    export CLAUDE_CODE_USE_BEDROCK=1
    
##### Google Vertex AI through LiteLLM

Using [pass-through endpoint](https://docs.litellm.ai/docs/pass_through/vertex_ai):

**Recommended: Proxy-specified credentials**
    
    export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
    export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
    export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
    export CLAUDE_CODE_USE_VERTEX=1
    export CLOUD_ML_REGION=us-east5
    
**Alternative: Client-specified credentials**

If you prefer to use local GCP credentials:

  1. Authenticate with GCP locally:

    gcloud auth application-default login
    
  2. Set Claude Code environment:

    export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
    export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
    export CLAUDE_CODE_USE_VERTEX=1
    export CLOUD_ML_REGION=us-east5
    
  3. Update LiteLLM header configuration:

Ensure your LiteLLM config has `general_settings.litellm_key_header_name` set to `Proxy-Authorization`, since the pass-through GCP token will be located on the `Authorization` header.

#### 

​

Unified endpoint

Using LiteLLM’s [Anthropic format endpoint](https://docs.litellm.ai/docs/anthropic_unified):
    
    export ANTHROPIC_BASE_URL=https://litellm-server:4000
    
### 

​

Model selection

By default, the models will use those specified in [Model configuration](/en/docs/claude-code/bedrock-vertex-proxies#model-configuration).

If you have configured custom model names in LiteLLM, set the aforementioned environment variables to those custom names.

For more detailed information, refer to the [LiteLLM documentation](https://docs.litellm.ai/).

## 

​

Additional resources

  * [LiteLLM documentation](https://docs.litellm.ai/)
  * [Claude Code settings](/en/docs/claude-code/settings)
  * [Corporate proxy setup](/en/docs/claude-code/corporate-proxy)
  * [Third-party integrations overview](/en/docs/claude-code/third-party-integrations)

Was this page helpful?

YesNo

[Corporate proxy](/en/docs/claude-code/corporate-proxy)


---

## AI Analysis

## Analysis of Claude Code LLM Gateway Documentation

### 1. Concise Summary

This documentation outlines how to integrate Claude Code with LLM gateway solutions, specifically focusing on LiteLLM. It details the benefits of using an LLM gateway, such as centralized authentication, usage tracking, and cost controls. The guide provides practical configurations for LiteLLM, covering various authentication methods and provider-specific setups for Anthropic API, Amazon Bedrock, and Google Vertex AI.

### 2. Key Topics Covered

*   **LLM Gateway Benefits:** Centralized authentication, usage tracking, cost controls, audit logging, model routing.
*   **LiteLLM Configuration:** Prerequisites, basic setup, authentication methods (static API key, dynamic API key helper).
*   **Provider-Specific Configurations:** Anthropic API, Amazon Bedrock, Google Vertex AI (proxy-specified vs. client-specified credentials).
*   **Unified Endpoint:** Using LiteLLM's Anthropic format endpoint.
*   **Model Selection:** How Claude Code selects models with LiteLLM.

### 3. Important Technical Details

*   **LLM Gateway Functionality:** Acts as a proxy layer for API key management, monitoring, budgeting, logging, and routing.
*   **LiteLLM Disclaimer:** Anthropic does not endorse, maintain, or audit LiteLLM; use at own discretion.
*   **Authentication Methods:**
    *   **Static API Key:** Set via `ANTHROPIC_AUTH_TOKEN` environment variable or in Claude Code settings. Sent as `Authorization` and `Proxy-Authorization` headers.
    *   **Dynamic API Key Helper:** Uses a script (`apiKeyHelper`) to fetch or generate keys (e.g., from a vault, JWT). `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` controls refresh interval. Sent as `Authorization`, `Proxy-Authorization`, and `X-Api-Key` headers. Lower precedence than `ANTHROPIC_AUTH_TOKEN`.
*   **Provider-Specific Base URLs:**
    *   Anthropic API: `ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic`
    *   Amazon Bedrock: `ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock`, `CLAUDE_CODE_SKIP_BEDROCK_AUTH=1`, `CLAUDE_CODE_USE_BEDROCK=1`
    *   Google Vertex AI: `ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1`, `ANTHROPIC_VERTEX_PROJECT_ID`, `CLOUD_ML_REGION`.
        *   **Proxy-specified credentials:** `CLAUDE_CODE_SKIP_VERTEX_AUTH=1`.
        *   **Client-specified credentials:** Requires local GCP authentication (`gcloud auth application-default login`) and LiteLLM config change (`general_settings.litellm_key_header_name` to `Proxy-Authorization`).
*   **Unified Endpoint:** `ANTHROPIC_BASE_URL=https://litellm-server:4000` for LiteLLM's Anthropic format endpoint.
*   **Model Selection:** Defaults to Claude Code's internal model configuration unless custom LiteLLM model names are specified via environment variables.

### 4. Code Examples

**Static API Key (Environment Variable):**
```bash
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key
```

**Static API Key (Claude Code Settings):**
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

**Dynamic API Key Helper Script Example:**
```bash
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Example: Fetch key from vault
vault kv get -field=api_key secret/litellm/claude-code

# Example: Generate JWT token
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

**Dynamic API Key Helper (Claude Code Settings):**
```json
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

**Dynamic API Key Helper TTL:**
```bash
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

**Anthropic API through LiteLLM:**
```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

**Amazon Bedrock through LiteLLM:**
```bash
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

**Google Vertex AI through LiteLLM (Proxy-specified credentials):**
```bash
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

**Google Vertex AI through LiteLLM (Client-specified credentials):**
```bash
gcloud auth application-default login
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

**Unified Endpoint:**
```bash
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

### 5. Related Concepts or Prerequisites

*   **Claude Code:** The primary application being configured. Requires being updated to the latest version.
*   **LiteLLM Proxy Server:** Must be deployed and accessible.
*   **API Key Management:** Understanding of how API keys are used and secured.
*   **Environment Variables:** Familiarity with setting and using environment variables.
*   **JSON Configuration:** Understanding of JSON format for Claude Code settings.
*   **Shell Scripting:** For dynamic API key helpers.
*   **Cloud Provider Credentials:** Specifically for Google Cloud Platform (GCP) authentication with `gcloud auth application-default login`.
*   **Network Proxies:** General understanding of proxy servers and their role in network communication.
*   **Security Best Practices:** Awareness of the implications of using third-party tools and managing sensitive credentials.
