---
title: CLI usage and controls - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/cli-usage.md]
---

# CLI usage and controls - Anthropic

源文档：[CLI usage and controls - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/cli-usage/cli-usage.md)

# CLI usage and controls - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/cli-usage  
**Category:** cli-usage  
**Scraped:** 2025-06-09 06:36:11

---

## ​

Getting started

Claude Code provides two main ways to interact:

  * **Interactive mode** : Run `claude` to start a REPL session
  * **One-shot mode** : Use `claude -p "query"` for quick commands

    # Start interactive mode
    claude
    
    # Start with an initial query
    claude "explain this project"
    
    # Run a single command and exit
    claude -p "what does this function do?"
    
    # Process piped content
    cat logs.txt | claude -p "analyze these errors"...

## ​

CLI commands

Command| Description| Example  
---|---|---  
`claude`| Start interactive REPL| `claude`  
`claude "query"`| Start REPL with initial prompt| `claude "explain this project"`  
`claude -p "query"`| Run one-off query, then exit| `claude -p "explain this function"`  
`cat file | claude -p "query"`| Process piped content| `cat logs.txt | claude -p "explain"`  
`claude -c`| Continue most recent conversation| `claude -c`  
`claude -c -p "query"`| Continue in print mode| `claude -c -p "Check for type errors"`  
`claude -r "<session-id>" "query"`| Resume session by ID| `claude -r "abc123"...

## ​

CLI flags

Customize Claude Code’s behavior with these command-line flags:

Flag| Description| Example  
---|---|---  
`--allowedTools`| A list of tools that should be allowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings)| `"Bash(git log:*)" "Bash(git diff:*)" "Write"`  
`--disallowedTools`| A list of tools that should be disallowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings)| `"Bash(git log:*)" "Bash(git diff:*)" "Write"`  
`--print`, `-p`| Print response without...

## ​

Slash commands

Control Claude’s behavior during an interactive session:

Command| Purpose  
---|---  
`/bug`| Report bugs (sends conversation to Anthropic)  
`/clear`| Clear conversation history  
`/compact [instructions]`| Compact conversation with optional focus instructions  
`/config`| View/modify configuration  
`/cost`| Show token usage statistics  
`/doctor`| Checks the health of your Claude Code installation  
`/help`| Get usage help  
`/init`| Initialize project with CLAUDE.md guide  
`/login`| Switch Anthropic accounts  
`/logout`| Sign out from your Anthropic account  
`/memory`| E...

## ​

Special shortcuts

### 

​

Quick memory with `#`

Add memories instantly by starting your input with `#`:
    
    # Always use descriptive variable names
    
You’ll be prompted to select which memory file to store this in.

### 

​

Line breaks in terminal

Enter multiline commands using:

  * **Quick escape** : Type `\` followed by Enter
  * **Keyboard shortcut** : Option+Enter (or Shift+Enter if configured)

To set up Option+Enter in your terminal:

**For Mac Terminal.app:**

  1. Open Settings → Profiles → Keyboard
  2. Check “Use Option as Meta Key”

**For iTerm2 and VSCode terminal:**
...

## ​

Vim Mode

Claude Code supports a subset of Vim keybindings that can be enabled with `/vim` or configured via `/config`.

The supported subset includes:

  * Mode switching: `Esc` (to NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (to INSERT)
  * Navigation: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`
  * Editing: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (repeat)

Was this page helpful?

YesNo

[Common tasks](/en/docs/claude-code/common-tasks)[IDE integrations](/en/docs/claude-code/ide-integrations)


---...

## Analysis of Claude Code CLI Usage Documentation

### 1. Concise Summary

This documentation outlines how to interact with Claude Code via its command-line interface (CLI). It details two primary interaction modes: interactive REPL sessions and one-shot commands. The guide also covers various CLI commands, flags for customization, in-session slash commands, and special shortcuts for memory management and multiline input, including basic Vim mode support.

### 2. Key Topics Covered

*   **CLI Interaction Modes:** Interactive REPL vs. One-shot commands.
*   **Core CLI Commands:** Starting sessions, querying, continuing conversations, resuming s...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
