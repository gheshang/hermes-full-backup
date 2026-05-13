---
title: Amazon Bedrock integration - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/amazon-bedrock.md]
---

# Amazon Bedrock integration - Anthropic

源文档：[Amazon Bedrock integration - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/amazon-bedrock/amazon-bedrock.md)

# Amazon Bedrock integration - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/amazon-bedrock  
**Category:** amazon-bedrock  
**Scraped:** 2025-06-09 06:37:30

---

## Original Content

This page provides instructions on configuring Claude Code through Amazon Bedrock, including setup, IAM configuration, cost tracking, and troubleshooting....

## ​

Prerequisites

Before configuring Claude Code with Bedrock, ensure you have:

  * An AWS account with Bedrock access enabled
  * Access to desired Claude models (e.g., Claude Sonnet 4) in Bedrock
  * AWS CLI installed and configured (optional - only needed if you don’t have another mechanism for getting credentials)
  * Appropriate IAM permissions...

## ​

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

Claude Code does not currently support dynamic credential manag...

## ​

IAM configuration

Create an IAM policy with the required permissions for Claude Code.

For details, see [Bedrock IAM documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

We recommend creating a dedicated AWS account for Claude Code to simplify cost tracking and access control....

## ​

Troubleshooting

If you encounter region issues:

  * Check model availability: `aws bedrock list-inference-profiles --region your-region`
  * Switch to a supported region: `export AWS_REGION=us-east-1`
  * Consider using inference profiles for cross-region access

If you receive an error “on-demand throughput isn’t supported”:

  * Specify the model as an [inference profile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ID...

## ​

Additional resources

  * [Bedrock documentation](https://docs.aws.amazon.com/bedrock/)
  * [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
  * [Bedrock inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

Was this page helpful?

YesNo

[Overview](/en/docs/claude-code/third-party-integrations)[Google Vertex AI](/en/docs/claude-code/google-vertex-ai)


---...

## AI Analysis

```markdown...

## Analysis of Claude Code Configuration with Amazon Bedrock

### 1. Concise Summary

This documentation outlines the steps to integrate and configure Claude Code with Amazon Bedrock, covering prerequisites, setup procedures, and essential environment variable configurations. It details how to enable model access, manage AWS credentials, and specify Claude models for use within Bedrock, while also touching upon IAM best practices and troubleshooting common issues.

### 2. Key Topics Covered

*   **Prerequisites:** AWS account with Bedrock access, desired Claude models, AWS CLI (optional), IAM permissions.
*   **Setup:**
    *   Enabling model access in B...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
