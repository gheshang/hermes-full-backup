---
title: Core tasks and workflows - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/common-tasks.md]
---

# Core tasks and workflows - Anthropic

源文档：[Core tasks and workflows - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/common-tasks/common-tasks.md)

# Core tasks and workflows - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/common-tasks  
**Category:** common-tasks  
**Scraped:** 2025-06-09 06:36:11

---

## Original Content

Claude Code operates directly in your terminal, understanding your project context and taking real actions. No need to manually add files to context - Claude will explore your codebase as needed....

## ​

Understand unfamiliar code
    
    > what does the payment processing system do?
    > find where user permissions are checked
    > explain how the caching layer works...

## ​

Automate Git operations
    
    > commit my changes
    > create a pr
    > which commit added tests for markdown back in December?
    > rebase on main and resolve any merge conflicts...

## ​

Edit code intelligently
    
    > add input validation to the signup form
    > refactor the logger to use the new API
    > fix the race condition in the worker queue...

## ​

Test and debug your code
    
    > run tests for the auth module and fix failures
    > find and fix security vulnerabilities
    > explain why this test is failing...

## ​

Encourage deeper thinking

For complex problems, explicitly ask Claude to think more deeply:
    
    > think about how we should architect the new payment service
    > think hard about the edge cases in our authentication flow
    
Claude Code will show when the model is using extended thinking. You can proactively prompt Claude to “think” or “think deeply” for more planning-intensive tasks. We suggest that you first tell Claude about your task and let it gather context from your project. Then, ask it to “think” to create a plan.

Claude will think more based on the words you use. For exampl...

## ​

Automate CI and infra workflows

Claude Code comes with a non-interactive mode for headless execution. This is especially useful for running Claude Code in non-interactive contexts like scripts, pipelines, and Github Actions.

Use `--print` (`-p`) to run Claude in non-interactive mode. In this mode, you can set the `ANTHROPIC_API_KEY` environment variable to provide a custom API key.

Non-interactive mode is especially useful when you pre-configure the set of commands Claude is allowed to use:
    
    export ANTHROPIC_API_KEY=sk_...
    claude -p "update the README with the latest changes" --...

## AI Analysis

```markdown...

## Analysis of Claude Code Documentation

### 1. Concise Summary

Claude Code is an AI assistant designed to operate directly within a developer's terminal, understanding project context and performing real actions. It streamlines various coding tasks, from understanding unfamiliar code and automating Git operations to intelligently editing, testing, and debugging code. It also supports "extended thinking" for complex problems and offers a non-interactive mode for CI/CD and infrastructure automation.

### 2. Key Topics Covered

*   **Core Functionality:** Terminal-based operation, context awareness, real action execution.
*   **Use Ca...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
