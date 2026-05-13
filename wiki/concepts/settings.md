---
title: Claude Code settings - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/settings.md]
---

# Claude Code settings - Anthropic

源文档：[Claude Code settings - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/settings/settings.md)

# Claude Code settings - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/settings  
**Category:** settings  
**Scraped:** 2025-06-09 06:36:32

---

## Original Content

Claude Code offers a variety of settings to configure its behavior to meet your needs. You can configure Claude Code by running the `/config` command when using the interactive REPL....

## ​

Settings files

The new `settings.json` file format is our official mechanism for configuring Claude Code through hierarchical settings:

  * **User settings** are defined in `~/.claude/settings.json` and apply to all projects.
  * **Project settings** are saved in your project directory under `.claude/settings.json` for shared settings, and `.claude/settings.local.json` for local project settings. Claude Code will configure git to ignore `.claude/settings.local.json` when it is created.
  * For enterprise deployments of Claude Code, we also support **enterprise managed policy settings**. Thes...

## ​

Permissions

You can view & manage Claude Code’s tool permissions with `/permissions`. This UI lists all permission rules and the settings.json file they are sourced from.

  * **Allow** rules will allow Claude Code to use the specified tool without further manual approval.
  * **Deny** rules will prevent Claude Code from using the specified tool. Deny rules take precedence over allow rules.

Permission rules use the format: `Tool(optional-specifier)`

A rule that is just the tool name matched any use of that tool. For example, adding `Bash` to the list of allow rules would allow Claude Code t...

## ​

Auto-updater permission options

When Claude Code detects that it doesn’t have sufficient permissions to write to your global npm prefix directory (required for automatic updates), you’ll see a warning that points to this documentation page. For detailed solutions to auto-updater issues, see the [troubleshooting guide](/en/docs/claude-code/troubleshooting#auto-updater-issues).

### 

​

Recommended: Create a new user-writable npm prefix
    
    # First, save a list of your existing global packages for later migration
    npm list -g --depth=0 > ~/npm-global-packages.txt
    
    # Create a di...

## ​

Optimize your terminal setup

Claude Code works best when your terminal is properly configured. Follow these guidelines to optimize your experience.

**Supported shells** :

  * Bash
  * Zsh
  * Fish

### 

​

Themes and appearance

Claude cannot control the theme of your terminal. That’s handled by your terminal application. You can match Claude Code’s theme to your terminal during onboarding or any time via the `/config` command

### 

​

Line breaks

You have several options for entering linebreaks into Claude Code:

  * **Quick escape** : Type `\` followed by Enter to create a newline
  * ...

## ​

Environment variables

Claude Code supports the following environment variables to control its behavior:

All environment variables can also be configured in [`settings.json`](/_sites/docs.anthropic.com/en/docs/claude-code/settings#available-settings). This is useful as a way to automatically set environment variables for each session, or to roll out a set of environment variables for your whole team or organization.

Variable| Purpose  
---|---  
`ANTHROPIC_API_KEY`| API key sent as `X-Api-Key` header, typically for the Claude SDK (for interactive usage, run `/login`)  
`ANTHROPIC_AUTH_TOKEN`...

## ​

Configuration options

We are in the process of migration global configuration to `settings.json`.

`claude config` will be deprecated in place of [settings.json](/_sites/docs.anthropic.com/en/docs/claude-code/settings#settings-files)

To manage your configurations, use the following commands:

  * List settings: `claude config list`
  * See a setting: `claude config get <key>`
  * Change a setting: `claude config set <key> <value>`
  * Push to a setting (for lists): `claude config add <key> <value>`
  * Remove from a setting (for lists): `claude config remove <key> <value>`

By default `confi...

## AI Analysis

```markdown...

## Analysis of Claude Code Settings Documentation

### 1. Concise Summary

This documentation details how to configure Claude Code's behavior through a hierarchical `settings.json` file and the interactive `/config` command. It covers various settings, including environment variables, API key helpers, and crucial permission rules that control Claude Code's access to system tools and files. The document also provides guidance on managing auto-updates and optimizing terminal setups for a better user experience.

### 2. Key Topics Covered

*   Claude Code configuration via `settings.json` and `/config` command.
*   Hierarchical settings files: Us...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
