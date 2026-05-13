---
title: GitHub Actions - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/github-actions.md]
---

# GitHub Actions - Anthropic

源文档：[GitHub Actions - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/github-actions/github-actions.md)

# GitHub Actions - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/github-actions  
**Category:** github-actions  
**Scraped:** 2025-06-09 06:36:56

---

## Original Content

Claude Code GitHub Actions brings AI-powered automation to your GitHub workflow. With a simple `@claude` mention in any PR or issue, Claude can analyze your code, create pull requests, implement features, and fix bugs - all while following your project’s standards.

Claude Code GitHub Actions is currently in beta. Features and functionality may evolve as we refine the experience.

Claude Code GitHub Actions is built on top of the [Claude Code SDK](/en/docs/claude-code/sdk), which enables programmatic integration of Claude Code into your applications. You can use the SDK to build custom automat...

## ​

Why use Claude Code GitHub Actions?

  * **Instant PR creation** : Describe what you need, and Claude creates a complete PR with all necessary changes
  * **Automated code implementation** : Turn issues into working code with a single command
  * **Follows your standards** : Claude respects your `CLAUDE.md` guidelines and existing code patterns
  * **Simple setup** : Get started in minutes with our installer and API key
  * **Secure by default** : Your code stays on Github’s runners...

## ​

What can Claude do?

Claude Code provides powerful GitHub Actions that transform how you work with code:

### 

​

Claude Code Action

This GitHub Action allows you to run Claude Code within your GitHub Actions workflows. You can use this to build any custom workflow on top of Claude Code.

[View repository →](https://github.com/anthropics/claude-code-action)

### 

​

Claude Code Action (Base)

The foundation for building custom GitHub workflows with Claude. This extensible framework gives you full access to Claude’s capabilities for creating tailored automation.

[View repository →](https://...

## ​

Quick start

The easiest way to set up this action is through Claude Code in the terminal. Just open claude and run `/install-github-app`.

This command will guide you through setting up the GitHub app and required secrets.

  * You must be a repository admin to install the GitHub app and add secrets
  * This quickstart method is only available for direct Anthropic API users. If you’re using AWS Bedrock or Google Vertex AI, please see the [Using with AWS Bedrock & Google Vertex AI](/_sites/docs.anthropic.com/en/docs/claude-code/github-actions#using-with-aws-bedrock-%26-google-vertex-ai) sectio...

## ​

Example use cases

Claude Code GitHub Actions can help you with a variety of tasks. For complete working examples, see the [examples directory](https://github.com/anthropics/claude-code-action/tree/main/examples).

### 

​

Turn issues into PRs
    
    # In an issue comment:
    @claude implement this feature based on the issue description
    
Claude will analyze the issue, write the code, and create a PR for review.

### 

​

Get implementation help
    
    # In a PR comment:
    @claude how should I implement user authentication for this endpoint?
    
Claude will analyze your code and pr...

## ​

Best practices

### 

​

CLAUDE.md configuration

Create a `CLAUDE.md` file in your repository root to define code style guidelines, review criteria, project-specific rules, and preferred patterns. This file guides Claude’s understanding of your project standards.

### 

​

Security considerations

**⚠️ IMPORTANT: Never commit API keys directly to your repository!**

Always use GitHub Secrets for API keys:

  * Add your API key as a repository secret named `ANTHROPIC_API_KEY`
  * Reference it in workflows: `anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
  * Limit action permissions to on...

## ​

Configuration examples

For ready-to-use workflow configurations for different use cases, including:

  * Basic workflow setup for issue and PR comments
  * Automated code reviews on pull requests
  * Custom implementations for specific needs

Visit the [examples directory](https://github.com/anthropics/claude-code-action/tree/main/examples) in the Claude Code Action repository.

The examples repository includes complete, tested workflows that you can copy directly into your `.github/workflows/` directory....

## ​

Using with AWS Bedrock & Google Vertex AI

For enterprise environments, you can use Claude Code GitHub Actions with your own cloud infrastructure. This approach gives you control over data residency and billing while maintaining the same functionality.

### 

​

Prerequisites

Before setting up Claude Code GitHub Actions with cloud providers, you need:

#### 

​

For Google Cloud Vertex AI:

  1. A Google Cloud Project with Vertex AI enabled
  2. Workload Identity Federation configured for GitHub Actions
  3. A service account with the required permissions
  4. A GitHub App (recommended) or us...

## ​

Troubleshooting

### 

​

Claude not responding to @claude commands

Verify the GitHub App is installed correctly, check that workflows are enabled, ensure API key is set in repository secrets, and confirm the comment contains `@claude` (not `/claude`).

### 

​

CI not running on Claude’s commits

Ensure you’re using the GitHub App or custom app (not Actions user), check workflow triggers include the necessary events, and verify app permissions include CI triggers.

### 

​

Authentication errors

Confirm API key is valid and has sufficient permissions. For Bedrock/Vertex, check credentials c...

## ​

Advanced configuration

### 

​

Action parameters

The Claude Code Action supports these key parameters:

Parameter| Description| Required  
---|---|---  
`prompt`| The prompt to send to Claude| Yes*  
`prompt_file`| Path to file containing prompt| Yes*  
`anthropic_api_key`| Anthropic API key| Yes**  
`max_turns`| Maximum conversation turns| No  
`timeout_minutes`| Execution timeout| No  
  
*Either `prompt` or `prompt_file` required  
**Required for direct Anthropic API, not for Bedrock/Vertex

### 

​

Alternative integration methods

While the `/install-github-app` command is the recommen...

## AI Analysis

```markdown...

## Analysis of Claude Code GitHub Actions Documentation

### 1. Concise Summary

Claude Code GitHub Actions integrates Anthropic's Claude AI directly into GitHub workflows, enabling AI-powered automation for code development. It allows users to leverage Claude for tasks like creating pull requests, implementing features, and fixing bugs by simply mentioning `@claude` in PRs or issues. The system adheres to project standards defined in a `CLAUDE.md` file and emphasizes secure setup using GitHub Secrets.

### 2. Key Topics Covered

*   **Introduction to Claude Code GitHub Actions**: What it is and its purpose.
*   **Benefits**: Instant PR creation, au...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
