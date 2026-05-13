---
title: Getting started with Claude Code - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/getting-started.md]
---

# Getting started with Claude Code - Anthropic

源文档：[Getting started with Claude Code - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/getting-started/getting-started.md)

# Getting started with Claude Code - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/getting-started  
**Category:** getting-started  
**Scraped:** 2025-06-09 06:36:01

---

## ​

Check system requirements

  * **Operating Systems** : macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows via WSL
  * **Hardware** : 4GB RAM minimum
  * **Software** :
    * Node.js 18+
    * [git](https://git-scm.com/downloads) 2.23+ (optional)
    * [GitHub](https://cli.github.com/) or [GitLab](https://gitlab.com/gitlab-org/cli) CLI for PR workflows (optional)
    * [ripgrep](https://github.com/BurntSushi/ripgrep?tab=readme-ov-file#installation) (rg) for enhanced file search (optional)
  * **Network** : Internet connection required for authentication and AI processing
  * **Location** : Avai...

## ​

Install and authenticate

1

Install Claude Code

Install [NodeJS 18+](https://nodejs.org/en/download), then run:
    
    npm install -g @anthropic-ai/claude-code
    
Do NOT use `sudo npm install -g` as this can lead to permission issues and security risks. If you encounter permission errors, see [configure Claude Code](/en/docs/claude-code/troubleshooting#linux-permission-issues) for recommended solutions.

2

Navigate to your project
    
    cd your-project-directory 
    
3

Start Claude Code
    
    claude
    
4

Complete authentication

Claude Code offers multiple authentication opti...

## ​

Initialize your project

For first-time users, we recommend:

1

Start Claude Code
    
    claude
    
2

Run a simple command
    
    summarize this project
    
3

Generate a CLAUDE.md project guide
    
    /init 
    
4

Commit the generated CLAUDE.md file

Ask Claude to commit the generated CLAUDE.md file to your repository.

Was this page helpful?

YesNo

[Overview](/en/docs/claude-code/overview)[Common tasks](/en/docs/claude-code/common-tasks)


---...

## Analysis of Claude Code Getting Started Documentation

### 1. Concise Summary

This documentation outlines the essential steps to get started with Claude Code, a tool for AI-assisted coding. It covers system requirements, installation, authentication methods, and initial project setup. Special attention is given to troubleshooting common issues, particularly for Windows users relying on WSL.

### 2. Key Topics Covered

*   System Requirements (OS, Hardware, Software, Network, Location)
*   WSL Troubleshooting for Windows users
*   Installation of Claude Code via npm
*   Authentication methods (Anthropic Console, Claude App, Enterprise platforms)
*...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
