---
title: Claude Code overview - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/overview.md]
---

# Claude Code overview - Anthropic

源文档：[Claude Code overview - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/overview/overview.md)

# Claude Code overview - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/overview  
**Category:** overview  
**Scraped:** 2025-06-09 06:36:01

---

## Original Content

Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster through natural language commands. By integrating directly with your development environment, Claude Code streamlines your workflow without requiring additional servers or complex setup.
    
    npm install -g @anthropic-ai/claude-code
    
Claude Code’s key capabilities include:

  * Editing files and fixing bugs across your codebase
  * Answering questions about your code’s architecture and logic
  * Executing and fixing tests, linting, and other commands
  * Searching thr...

## ​

Why Claude Code?

Claude Code operates directly in your terminal, understanding your project context and taking real actions. No need to manually add files to context - Claude will explore your codebase as needed.

### 

​

Enterprise integration

Claude Code seamlessly integrates with enterprise AI platforms. You can connect to [Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/bedrock-vertex-proxies) for secure, compliant deployments that meet your organization’s requirements.

### 

​

Security and privacy by design

Your code’s security is paramount. Claude Code’s architecture ensur...

## ​

Getting started

To get started with Claude Code, follow our [installation guide](/en/docs/claude-code/getting-started) which covers system requirements, installation steps, and authentication process....

## ​

Quick tour

Here’s what you can accomplish with Claude Code:

### 

​

From questions to solutions in seconds
    
    # Ask questions about your codebase
    claude
    > how does our authentication system work?
    
    # Create a commit with one command
    claude commit
    
    # Fix issues across multiple files
    claude "fix the type errors in the auth module"
    
### 

​

Understand unfamiliar code
    
    > what does the payment processing system do?
    > find where user permissions are checked
    > explain how the caching layer works
    
### 

​

Automate Git operations
    
  ...

## ​

Next steps...

## ​

Additional resources...

## ​

License and data usage

Claude Code is provided under Anthropic’s [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms).

### 

​

How we use your data

We aim to be fully transparent about how we use your data. We may use feedback to improve our products and services, but we will not train generative models using your feedback from Claude Code. Given their potentially sensitive nature, we store user feedback transcripts for only 30 days.

#### 

​

Feedback transcripts

If you choose to send us feedback about Claude Code, such as transcripts of your usage, Anthropic ...

## AI Analysis

```markdown...

## Analysis of Claude Code Documentation

### 1. Concise Summary

Claude Code is an AI-powered, agentic coding tool designed to operate directly within a developer's terminal. It understands the codebase context, allowing users to interact with it using natural language commands to perform various coding tasks, from editing files and fixing bugs to managing Git operations and answering code-related questions. It emphasizes seamless integration with existing development environments and offers enterprise deployment options with platforms like Amazon Bedrock and Google Vertex AI, while prioritizing security and privacy.

### 2. Key Topi...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
