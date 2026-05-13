---
title: Manage Claude's memory - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/memory.md]
---

# Manage Claude's memory - Anthropic

源文档：[Manage Claude's memory - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/memory/memory.md)

# Manage Claude's memory - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/memory  
**Category:** memory  
**Scraped:** 2025-06-09 06:36:21

---

## Original Content

Claude Code can remember your preferences across sessions, like style guidelines and common commands in your workflow....

## ​

Determine memory type

Claude Code offers three memory locations, each serving a different purpose:

Memory Type| Location| Purpose| Use Case Examples  
---|---|---|---  
**Project memory**| `./CLAUDE.md`| Team-shared instructions for the project| Project architecture, coding standards, common workflows  
**User memory**| `~/.claude/CLAUDE.md`| Personal preferences for all projects| Code styling preferences, personal tooling shortcuts  
**Project memory (local)**| `./CLAUDE.local.md`| Personal project-specific preferences|  _(Deprecated, see below)_ Your sandbox URLs, preferred test data  
  
...

## ​

CLAUDE.md imports

CLAUDE.md files can import additional files using `@path/to/import` syntax. The following example imports 3 files:
    
    See @README for project overview and @package.json for available npm commands for this project.
    
    # Additional Instructions
    - git workflow @docs/git-instructions.md
    
Both relative and absolute paths are allowed. In particular, importing files in user’s home dir is a convenient way for your team members to provide individual instructions that are not checked into the repository. Previously CLAUDE.local.md served a similar purpose, but is n...

## ​

How Claude looks up memories

Claude Code reads memories recursively: starting in the cwd, Claude Code recurses up to _/_ and reads any CLAUDE.md or CLAUDE.local.md files it finds. This is especially convenient when working in large repositories where you run Claude Code in _foo/bar/_ , and have memories in both _foo/CLAUDE.md_ and _foo/bar/CLAUDE.md_.

Claude will also discover CLAUDE.md nested in subtrees under your current working directory. Instead of loading them at launch, they are only included when Claude reads files in those subtrees....

## ​

Quickly add memories with the `#` shortcut

The fastest way to add a memory is to start your input with the `#` character:
    
    # Always use descriptive variable names
    
You’ll be prompted to select which memory file to store this in....

## ​

Directly edit memories with `/memory`

Use the `/memory` slash command during a session to open any memory file in your system editor for more extensive additions or organization....

## ​

Memory best practices

  * **Be specific** : “Use 2-space indentation” is better than “Format code properly”.
  * **Use structure to organize** : Format each individual memory as a bullet point and group related memories under descriptive markdown headings.
  * **Review periodically** : Update memories as your project evolves to ensure Claude is always using the most up to date information and context.

Was this page helpful?

YesNo

[IDE integrations](/en/docs/claude-code/ide-integrations)[Settings](/en/docs/claude-code/settings)


---...

## Analysis of Claude Code Memory Documentation

### 1. Concise Summary

Claude Code offers persistent memory capabilities to remember user and project preferences across sessions. It utilizes specific Markdown files (`CLAUDE.md`, `CLAUDE.local.md`) located in project directories or the user's home directory to store instructions, coding standards, and personal preferences. These memory files can import other files and are automatically loaded into Claude's context, allowing for a highly customizable and context-aware interaction.

### 2. Key Topics Covered

*   **Memory Types and Locations:** Defines different types of memory (Project, User...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
