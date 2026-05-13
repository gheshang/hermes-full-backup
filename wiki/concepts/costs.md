---
title: Manage costs effectively - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/costs.md]
---

# Manage costs effectively - Anthropic

源文档：[Manage costs effectively - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/costs/costs.md)

# Manage costs effectively - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/costs  
**Category:** costs  
**Scraped:** 2025-06-09 06:36:56

---

## Original Content

Claude Code consumes tokens for each interaction. The average cost is $6 per developer per day, with daily costs remaining below $12 for 90% of users....

## ​

Track your costs

  * Use `/cost` to see current session usage
  * **Anthropic Console users** :
    * Check [historical usage](https://support.anthropic.com/en/articles/9534590-cost-and-usage-reporting-in-console) in the Anthropic Console (requires Admin or Billing role)
    * Set [workspace spend limits](https://support.anthropic.com/en/articles/9796807-creating-and-managing-workspaces) for the Claude Code workspace (requires Admin role)
  * **Pro and Max plan users** : Usage is included in your subscription...

## ​

Reduce token usage

  * **Compact conversations:**

    * Claude uses auto-compact by default when context exceeds 95% capacity

    * Toggle auto-compact: Run `/config` and navigate to “Auto-compact enabled”

    * Use `/compact` manually when context gets large

    * Add custom instructions: `/compact Focus on code samples and API usage`

    * Customize compaction by adding to CLAUDE.md:
        
                # Summary instructions
        
        When you are using compact, please focus on test output and code changes
        
  * **Write specific queries:** Avoid vague requests that ...

## ​

Background token usage

Claude Code uses tokens for some background functionality even when idle:

  * **Haiku generation** : Small creative messages that appear while you type (approximately 1 cent per day)
  * **Conversation summarization** : Background jobs that summarize previous conversations for the `claude --resume` feature
  * **Command processing** : Some commands like `/cost` may generate requests to check status

These background processes consume a small amount of tokens (typically under $0.04 per session) even without active interaction.

For team deployments, we recommend startin...

## Analysis of Claude Code Costs Documentation

### 1. Concise Summary

This documentation outlines the cost structure for Claude Code, emphasizing token consumption as the primary driver. It provides tools and strategies for users to track and reduce their spending, including in-app commands, console features, and best practices for conversation management. The document also details background token usage for features like Haiku generation and conversation summarization.

### 2. Key Topics Covered

*   Claude Code pricing model (token-based)
*   Average and typical daily costs
*   Methods for tracking usage (`/cost`, Anthropic Console)
*  ...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
