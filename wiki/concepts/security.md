---
title: Manage permissions and security - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/security.md]
---

# Manage permissions and security - Anthropic

源文档：[Manage permissions and security - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/security/security.md)

# Manage permissions and security - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/security  
**Category:** security  
**Scraped:** 2025-06-09 06:36:32

---

## Original Content

Claude Code uses a tiered permission system to balance power and safety:

Tool Type| Example| Approval Required| ”Yes, don’t ask again” Behavior  
---|---|---|---  
Read-only| File reads, LS, Grep| No| N/A  
Bash Commands| Shell execution| Yes| Permanently per project directory and command  
File Modification| Edit/write files| Yes| Until session end...

## ​

Tools available to Claude

Claude Code has access to a set of powerful tools that help it understand and modify your codebase:

Tool| Description| Permission Required  
---|---|---  
**Agent**|  Runs a sub-agent to handle complex, multi-step tasks| No  
**Bash**|  Executes shell commands in your environment| Yes  
**Edit**|  Makes targeted edits to specific files| Yes  
**Glob**|  Finds files based on pattern matching| No  
**Grep**|  Searches for patterns in file contents| No  
**LS**|  Lists files and directories| No  
**MultiEdit**|  Performs multiple edits on a single file atomically| Yes ...

## ​

Protect against prompt injection

Prompt injection is a technique where an attacker attempts to override or manipulate an AI assistant’s instructions by inserting malicious text. Claude Code includes several safeguards against these attacks:

  * **Permission system** : Sensitive operations require explicit approval
  * **Context-aware analysis** : Detects potentially harmful instructions by analyzing the full request
  * **Input sanitization** : Prevents command injection by processing user inputs
  * **Command blocklist** : Blocks risky commands that fetch arbitrary content from the web like...

## ​

Configure network access

Claude Code requires access to:

  * api.anthropic.com
  * statsig.anthropic.com
  * sentry.io

Allowlist these URLs when using Claude Code in containerized environments....

## ​

Development container reference implementation

Claude Code provides a development container configuration for teams that need consistent, secure environments. This preconfigured [devcontainer setup](https://code.visualstudio.com/docs/devcontainers/containers) works seamlessly with VS Code’s Remote - Containers extension and similar tools.

The container’s enhanced security measures (isolation and firewall rules) allow you to run `claude --dangerously-skip-permissions` to bypass permission prompts for unattended operation. We’ve included a [reference implementation](https://github.com/anthropi...

## Analysis of Claude Code Security Documentation

### 1. Concise Summary

This documentation outlines the security features and best practices for using Claude Code, focusing on its tiered permission system for tool access and safeguards against prompt injection. It also provides guidance on configuring network access and a reference implementation for a secure development container, emphasizing isolation and controlled network access for enhanced security.

### 2. Key Topics Covered

*   **Permission System:** How Claude Code manages access to various tools, including required approvals and "don't ask again" behaviors.
*   **Available Tools:...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
