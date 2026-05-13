---
title: Troubleshooting - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/troubleshooting.md]
---

# Troubleshooting - Anthropic

源文档：[Troubleshooting - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/troubleshooting/troubleshooting.md)

# Troubleshooting - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/troubleshooting  
**Category:** troubleshooting  
**Scraped:** 2025-06-09 06:37:21

---

## ​

Common installation issues

### 

​

Linux permission issues

When installing Claude Code with npm, you may encounter permission errors if your npm global prefix is not user writable (eg. `/usr`, or `/usr/local`).

#### 

​

Recommended solution: Create a user-writable npm prefix

The safest approach is to configure npm to use a directory within your home folder:
    
    # First, save a list of your existing global packages for later migration
    npm list -g --depth=0 > ~/npm-global-packages.txt
    
    # Create a directory for your global packages
    mkdir -p ~/.npm-global
    
    # Conf...

## ​

Auto-updater issues

If Claude Code can’t update automatically, it may be due to permission issues with your npm global prefix directory. Follow the [recommended solution](/_sites/docs.anthropic.com/en/docs/claude-code/troubleshooting#recommended-solution-create-a-user-writable-npm-prefix) above to fix this.

If you prefer to disable the auto-updater instead, you can use: If you prefer to disable the auto-updater instead , you can set the `DISABLE_AUTOUPDATER` [environment variable](settings#environment-variables) to `1`...

## ​

Permissions and authentication

### 

​

Repeated permission prompts

If you find yourself repeatedly approving the same commands, you can allow specific tools to run without approval using the `/permissions` command. See [Permissions docs](settings#permissions).

### 

​

Authentication issues

If you’re experiencing authentication problems:

  1. Run `/logout` to sign out completely
  2. Close Claude Code
  3. Restart with `claude` and complete the authentication process again

If problems persist, try:
    
    rm -rf ~/.config/claude-code/auth.json
    claude
    
This removes your stored ...

## ​

Performance and stability

### 

​

High CPU or memory usage

Claude Code is designed to work with most development environments, but may consume significant resources when processing large codebases. If you’re experiencing performance issues:

  1. Use `/compact` regularly to reduce context size
  2. Close and restart Claude Code between major tasks
  3. Consider adding large build directories to your `.gitignore` file

### 

​

Command hangs or freezes

If Claude Code seems unresponsive:

  1. Press Ctrl+C to attempt to cancel the current operation
  2. If unresponsive, you may need to close...

## ​

Getting more help

If you’re experiencing issues not covered here:

  1. Use the `/bug` command within Claude Code to report problems directly to Anthropic
  2. Check the [GitHub repository](https://github.com/anthropics/claude-code) for known issues
  3. Run `/doctor` to check the health of your Claude Code installation

Was this page helpful?

YesNo

[Tutorials](/en/docs/claude-code/tutorials)[Overview](/en/docs/claude-code/third-party-integrations)


---...

## Analysis of Claude Code Troubleshooting Documentation

### 1. Concise Summary

This documentation provides comprehensive troubleshooting steps for common issues encountered while using Claude Code, particularly focusing on installation, auto-updater, permissions, authentication, and performance. It offers detailed solutions for Linux permission errors, including a recommended user-writable npm prefix setup and critical system recovery steps for damaged installations. Additionally, it addresses specific problems like repeated permission prompts, authentication failures, high resource usage, command freezes, and JetBrains terminal keybinding conflic...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
