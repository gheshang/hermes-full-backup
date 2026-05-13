---
title: IDE integrations - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/ide-integrations.md]
---

# IDE integrations - Anthropic

源文档：[IDE integrations - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/ide-integrations/ide-integrations.md)

# IDE integrations - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/ide-integrations  
**Category:** ide-integrations  
**Scraped:** 2025-06-09 06:36:21

---

## Original Content

Claude Code seamlessly integrates with popular Integrated Development Environments (IDEs) to enhance your coding workflow. This integration allows you to leverage Claude’s capabilities directly within your preferred development environment....

## ​

Supported IDEs

Claude Code currently supports two major IDE families:

  * **Visual Studio Code** (including popular forks like Cursor and Windsurf)
  * **JetBrains IDEs** (including PyCharm, WebStorm, IntelliJ, and GoLand)...

## ​

Features

  * **Quick launch** : Use `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux) to open Claude Code directly from your editor, or click the Claude Code button in the UI
  * **Diff viewing** : Code changes can be displayed directly in the IDE diff viewer instead of the terminal. You can configure this in `/config`
  * **Selection context** : The current selection/tab in the IDE is automatically shared with Claude Code
  * **File reference shortcuts** : Use `Cmd+Option+K` (Mac) or `Alt+Ctrl+K` (Linux/Windows) to insert file references (e.g., @File#L1-99)
  * **Diagnostic sharing** : Diagnosti...

## ​

Installation

### 

​

VS Code

  1. Open VSCode
  2. Open the integrated terminal
  3. Run `claude` \- the extension will auto-install

Going forward you can also use the `/ide` command in any external terminal to connect to the IDE.

These installation instructions also apply to VS Code forks like Cursor and Windsurf.

### 

​

JetBrains IDEs

Install the [Claude Code plugin](https://docs.anthropic.com/s/claude-code-jetbrains) from the marketplace and restart your IDE.

The plugin may also be auto-installed when you run `claude` in the integrated terminal. The IDE must be restarted completel...

## ​

Configuration

Both integrations work with Claude Code’s configuration system. To enable IDE-specific features:

  1. Connect Claude Code to your IDE by running `claude` in the built-in terminal
  2. Run the `/config` command
  3. Set the diff tool to `auto` for automatic IDE detection
  4. Claude Code will automatically use the appropriate viewer based on your IDE

If you’re using an external terminal (not the IDE’s built-in terminal), you can still connect to your IDE by using the `/ide` command after launching Claude Code. This allows you to benefit from IDE integration features even when r...

## ​

Troubleshooting

### 

​

VS Code extension not installing

  * Ensure you’re running Claude Code from VS Code’s integrated terminal
  * Ensure that the CLI corresponding to your IDE is installed:
    * For VS Code: `code` command should be available
    * For Cursor: `cursor` command should be available
    * For Windsurf: `windsurf` command should be available
    * If not installed, use `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux) and search for “Shell Command: Install ‘code’ command in PATH” (or the equivalent for your IDE)
  * Check that VS Code has permission to install extensio...

## AI Analysis

```markdown...

## Analysis of Claude Code IDE Integrations Documentation

### 1. Concise Summary
This documentation outlines how Claude Code integrates with popular IDEs like Visual Studio Code and JetBrains products to enhance the coding workflow. It details supported IDEs, key features such as quick launch and diff viewing, installation procedures for each IDE family, and configuration steps. The document also provides troubleshooting tips for common installation and functionality issues.

### 2. Key Topics Covered
*   Supported IDEs for Claude Code integration
*   Features of Claude Code within IDEs
*   Installation instructions for VS Code and JetBrains IDEs
*  ...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
