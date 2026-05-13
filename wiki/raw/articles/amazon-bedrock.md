# Amazon Bedrock integration - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock  
**Category:** amazon-bedrock  
**Scraped:** 2025-06-09 06:37:30

---

## Original Content

This page provides instructions on configuring Claude Code through Amazon Bedrock, including setup, IAM configuration, cost tracking, and troubleshooting.

## 

​

Prerequisites

Before configuring Claude Code with Bedrock, ensure you have:

  * An AWS account with Bedrock access enabled
  * Access to desired Claude models (e.g., Claude Sonnet 4) in Bedrock
  * AWS CLI installed and configured (optional - only needed if you don’t have another mechanism for getting credentials)
  * Appropriate IAM permissions

## 

​

Setup

### 

​

1\. Enable model access

First, ensure you have access to the required Claude models in your AWS account:

  1. Navigate to the [Amazon Bedrock console](https://console.aws.amazon.com/bedrock/)
  2. Go to **Model access** in the left navigation
  3. Request access to desired Claude models (e.g., Claude Sonnet 4)
  4. Wait for approval (usually instant for most regions)

### 

​

2\. Configure AWS credentials

Claude Code uses the default AWS SDK credential chain. Set up your credentials using one of these methods:

Claude Code does not currently support dynamic credential management (such as automatically calling `aws sts assume-role`). You will need to run `aws configure`, `aws sso login`, or set the `AWS_` environment variables yourself.

**Option A: AWS CLI configuration**
    
    aws configure
    
**Option B: Environment variables (access key)**
    
    export AWS_ACCESS_KEY_ID=your-access-key-id
    export AWS_SECRET_ACCESS_KEY=your-secret-access-key
    export AWS_SESSION_TOKEN=your-session-token
    
**Option C: Environment variables (SSO profile)**
    
    aws sso login --profile=<your-profile-name>
    
    export AWS_PROFILE=your-profile-name
    
### 

​

3\. Configure Claude Code

Set the following environment variables to enable Bedrock:
    
    # Enable Bedrock integration
    export CLAUDE_CODE_USE_BEDROCK=1
    export AWS_REGION=us-east-1  # or your preferred region
    
`AWS_REGION` is a required environment variable. Claude Code does not read from the `.aws` config file for this setting.
    
    # Optional: Disable prompt caching if not enabled in your account
    export DISABLE_PROMPT_CACHING=1
    
Contact AWS support to enable prompt caching for reduced costs and higher rate limits. Once enabled, remove the `DISABLE_PROMPT_CACHING` setting.

### 

​

4\. Model configuration

Claude Code uses these default models for Bedrock:

Model type| Default value  
---|---  
Primary model| `us.anthropic.claude-3-7-sonnet-20250219-v1:0`  
Small/fast model| `us.anthropic.claude-3-5-haiku-20241022-v1:0`  
  
To customize models, use one of these methods:
    
    # Using inference profile ID
    export ANTHROPIC_MODEL='us.anthropic.claude-opus-4-20250514-v1:0'
    export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'
    
    # Using application inference profile ARN
    export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'
    
## 

​

IAM configuration

Create an IAM policy with the required permissions for Claude Code.

For details, see [Bedrock IAM documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

We recommend creating a dedicated AWS account for Claude Code to simplify cost tracking and access control.

## 

​

Troubleshooting

If you encounter region issues:

  * Check model availability: `aws bedrock list-inference-profiles --region your-region`
  * Switch to a supported region: `export AWS_REGION=us-east-1`
  * Consider using inference profiles for cross-region access

If you receive an error “on-demand throughput isn’t supported”:

  * Specify the model as an [inference profile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ID

## 

​

Additional resources

  * [Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
  * [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
  * [Bedrock inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

Was this page helpful?

YesNo

[Overview](/en/docs/claude-code/third-party-integrations)[Google Vertex AI](/en/docs/claude-code/google-vertex-ai)


---

## AI Analysis

```markdown
## Analysis of Claude Code Configuration with Amazon Bedrock

### 1. Concise Summary

This documentation outlines the steps to integrate and configure Claude Code with Amazon Bedrock, covering prerequisites, setup procedures, and essential environment variable configurations. It details how to enable model access, manage AWS credentials, and specify Claude models for use within Bedrock, while also touching upon IAM best practices and troubleshooting common issues.

### 2. Key Topics Covered

*   **Prerequisites:** AWS account with Bedrock access, desired Claude models, AWS CLI (optional), IAM permissions.
*   **Setup:**
    *   Enabling model access in Bedrock console.
    *   Configuring AWS credentials (CLI, environment variables).
    *   Configuring Claude Code environment variables (`CLAUDE_CODE_USE_BEDROCK`, `AWS_REGION`, `DISABLE_PROMPT_CACHING`).
    *   Customizing Claude model configurations.
*   **IAM Configuration:** Recommendations for dedicated AWS accounts and policy creation.
*   **Troubleshooting:** Addressing region issues and "on-demand throughput" errors.
*   **Cost Tracking:** Implicitly covered by IAM recommendations.

### 3. Important Technical Details

*   **Credential Management:** Claude Code uses the default AWS SDK credential chain. It *does not* support dynamic credential management like `aws sts assume-role` automatically; users must configure credentials manually via `aws configure`, `aws sso login`, or environment variables.
*   **Environment Variables:**
    *   `CLAUDE_CODE_USE_BEDROCK=1`: Essential to enable Bedrock integration.
    *   `AWS_REGION`: **Required** and must be set as an environment variable; Claude Code does not read it from `.aws` config files.
    *   `DISABLE_PROMPT_CACHING=1`: Optional, used if prompt caching is not enabled in the AWS account. Should be removed once enabled by AWS support for cost reduction and higher rate limits.
    *   `ANTHROPIC_MODEL` and `ANTHROPIC_SMALL_FAST_MODEL`: Used to specify custom Claude models, either by inference profile ID (e.g., `us.anthropic.claude-3-7-sonnet-20250219-v1:0`) or application inference profile ARN.
*   **Default Models:**
    *   Primary: `us.anthropic.claude-3-7-sonnet-20250219-v1:0`
    *   Small/Fast: `us.anthropic.claude-3-5-haiku-20241022-v1:0`
*   **IAM Best Practice:** Recommend a dedicated AWS account for Claude Code for simplified cost tracking and access control.
*   **Troubleshooting Tips:**
    *   Use `aws bedrock list-inference-profiles --region your-region` to check model availability.
    *   Specify models as inference profile IDs to resolve "on-demand throughput isn't supported" errors.

### 4. Code Examples

```bash
# Option A: AWS CLI configuration
aws configure

# Option B: Environment variables (access key)
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token

# Option C: Environment variables (SSO profile)
aws sso login --profile=<your-profile-name>
export AWS_PROFILE=your-profile-name

# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # or your preferred region

# Optional: Disable prompt caching if not enabled in your account
export DISABLE_PROMPT_CACHING=1

# Customize models using inference profile ID
export ANTHROPIC_MODEL='us.anthropic.claude-opus-4-20250514-v1:0'
export ANTHROPIC_SMALL_FAST_MODEL='us.anthropic.claude-3-5-haiku-20241022-v1:0'

# Customize models using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'
```

### 5. Related Concepts or Prerequisites

*   **Amazon Bedrock:** Fundamental understanding of AWS's fully managed service for foundation models.
*   **AWS IAM:** Knowledge of Identity and Access Management, including policies, roles, and permissions.
*   **AWS CLI:** Familiarity with the AWS Command Line Interface for configuration and management.
*   **Environment Variables:** Basic understanding of how to set and use environment variables in a shell.
*   **AWS SDK Credential Chain:** Awareness of how AWS SDKs find and use credentials.
*   **Inference Profiles:** Understanding of Bedrock's inference profiles for model access and configuration.
*   **Prompt Caching:** Concept of caching prompts for efficiency and cost optimization in AI model interactions.
```
