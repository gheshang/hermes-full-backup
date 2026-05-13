---
title: Overview - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/third-party-integrations.md]
---

# Overview - Anthropic

源文档：[Overview - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/third-party-integrations/third-party-integrations.md)

# Overview - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/third-party-integrations  
**Category:** third-party-integrations  
**Scraped:** 2025-06-09 06:37:21

---

## Original Content

Claude Code can integrate with various third-party services and infrastructure to meet enterprise requirements. This page provides an overview of available integration options and helps you choose the right configuration for your organization....

## ​

Provider comparison

Feature| Anthropic| Amazon Bedrock| Google Vertex AI  
---|---|---|---  
Regions| Supported [countries](https://www.anthropic.com/supported-countries)| Multiple AWS [regions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)| Multiple GCP [regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)  
Prompt caching| Enabled by default| Contact AWS for enablement| Contact Google for enablement  
Authentication| API key| AWS credentials (IAM)| GCP credentials (OAuth/Service Account)  
Cost tracking| Dashboard| AWS Cost Explorer| GC...

## ​

Integration options

### 

​

Cloud providers...

## [Amazon BedrockUse Claude models through AWS infrastructure with IAM-based authentication and AWS-native monitoring](/en/docs/claude-code/amazon-bedrock)## [Google Vertex AIAccess Claude models via Google Cloud Platform with enterprise-grade security and compliance](/en/docs/claude-code/google-vertex-ai)

### 

​

Corporate infrastructure...

## ​

Mixing and matching settings

Claude Code supports flexible configuration options that allow you to combine different providers and infrastructure:

Understand the difference between:

  * **Corporate proxy** : An HTTP/HTTPS proxy for routing traffic (set via `HTTPS_PROXY` or `HTTP_PROXY`)
  * **LLM Gateway** : A service that handles authentication and provides provider-compatible endpoints (set via `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, or `ANTHROPIC_VERTEX_BASE_URL`)

Both configurations can be used in tandem.

### 

​

Using Bedrock with corporate proxy

Route Bedrock traffic t...

## ​

Choosing the right integration

Consider these factors when selecting your integration approach:

### 

​

Direct provider access

Best for organizations that:

  * Want the simplest setup
  * Have existing AWS or GCP infrastructure
  * Need provider-native monitoring and compliance

### 

​

Corporate proxy

Best for organizations that:

  * Have existing corporate proxy requirements
  * Need traffic monitoring and compliance
  * Must route all traffic through specific network paths

### 

​

LLM Gateway

Best for organizations that:

  * Need usage tracking across teams
  * Want to dynamical...

## ​

Debugging

When debugging your third-party integration configuration:

  * Use the `claude /status` [slash command](/en/docs/claude-code/cli-usage#slash-command). This command provides observability into any applied authentication, proxy, and URL settings.
  * Set environment variable `export ANTHROPIC_LOG=debug` to log requests....

## ​

Next steps

  * [Set up Amazon Bedrock](/en/docs/claude-code/amazon-bedrock) for AWS-native integration
  * [Configure Google Vertex AI](/en/docs/claude-code/google-vertex-ai) for GCP deployment
  * [Implement Corporate Proxy](/en/docs/claude-code/corporate-proxy) for network requirements
  * [Deploy LLM Gateway](/en/docs/claude-code/llm-gateway) for enterprise management
  * [Settings](/en/docs/claude-code/settings) for configuration options and environment variables

Was this page helpful?

YesNo

[Troubleshooting](/en/docs/claude-code/troubleshooting)[Amazon Bedrock](/en/docs/claude-code/am...

## AI Analysis

```markdown...

## Analysis of Claude Code Third-Party Integrations Documentation

### 1. Concise Summary
This documentation outlines how Claude Code integrates with various third-party services, primarily focusing on cloud providers like Amazon Bedrock and Google Vertex AI, and corporate infrastructure components such as proxies and LLM Gateways. It provides a comparative overview of features across Anthropic's direct offering and the cloud providers, details different integration options, and explains how to combine these settings for flexible deployments. The guide also offers advice on choosing the appropriate integration strategy and debugging tips.

### 2. Key Topics C...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
