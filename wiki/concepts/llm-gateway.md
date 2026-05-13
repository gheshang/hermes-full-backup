---
title: LLM gateway configuration - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/llm-gateway.md]
---

# LLM gateway configuration - Anthropic

源文档：[LLM gateway configuration - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/llm-gateway/llm-gateway.md)

# LLM gateway configuration - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/llm-gateway  
**Category:** llm-gateway  
**Scraped:** 2025-06-09 06:37:49

---

## Original Content

This page covers how to configure Claude Code with LLM gateway solutions, including LiteLLM setup, authentication methods, and enterprise features like usage tracking and budget management....

## ​

Overview

LLM gateways provide a centralized proxy layer between Claude Code and model providers, offering:

  * **Centralized authentication** \- Single point for API key management
  * **Usage tracking** \- Monitor usage across teams and projects
  * **Cost controls** \- Implement budgets and rate limits
  * **Audit logging** \- Track all model interactions for compliance
  * **Model routing** \- Switch between providers without code changes...

## ​

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
    
    # Set in e...

## ​

Additional resources

  * [LiteLLM documentation](https://docs.litellm.ai/)
  * [Claude Code settings](/en/docs/claude-code/settings)
  * [Corporate proxy setup](/en/docs/claude-code/corporate-proxy)
  * [Third-party integrations overview](/en/docs/claude-code/third-party-integrations)

Was this page helpful?

YesNo

[Corporate proxy](/en/docs/claude-code/corporate-proxy)


---...

## Analysis of Claude Code LLM Gateway Documentation

### 1. Concise Summary

This documentation outlines how to integrate Claude Code with LLM gateway solutions, specifically focusing on LiteLLM. It details the benefits of using an LLM gateway, such as centralized authentication, usage tracking, and cost controls. The guide provides practical configurations for LiteLLM, covering various authentication methods and provider-specific setups for Anthropic API, Amazon Bedrock, and Google Vertex AI.

### 2. Key Topics Covered

*   **LLM Gateway Benefits:** Centralized authentication, usage tracking, cost controls, audit logging, model routing.
*   **L...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
