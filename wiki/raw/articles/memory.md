# Manage Claude's memory - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/memory  
**Category:** memory  
**Scraped:** 2025-06-09 06:36:21

---

## Original Content

Claude Code can remember your preferences across sessions, like style guidelines and common commands in your workflow.

## 

​

Determine memory type

Claude Code offers three memory locations, each serving a different purpose:

Memory Type| Location| Purpose| Use Case Examples  
---|---|---|---  
**Project memory**| `./CLAUDE.md`| Team-shared instructions for the project| Project architecture, coding standards, common workflows  
**User memory**| `~/.claude/CLAUDE.md`| Personal preferences for all projects| Code styling preferences, personal tooling shortcuts  
**Project memory (local)**| `./CLAUDE.local.md`| Personal project-specific preferences|  _(Deprecated, see below)_ Your sandbox URLs, preferred test data  
  
All memory files are automatically loaded into Claude Code’s context when launched.

## 

​

CLAUDE.md imports

CLAUDE.md files can import additional files using `@path/to/import` syntax. The following example imports 3 files:
    
    See @README for project overview and @package.json for available npm commands for this project.
    
    # Additional Instructions
    - git workflow @docs/git-instructions.md
    
Both relative and absolute paths are allowed. In particular, importing files in user’s home dir is a convenient way for your team members to provide individual instructions that are not checked into the repository. Previously CLAUDE.local.md served a similar purpose, but is now deprecated in favor of imports since they work better across multiple git worktrees.
    
    # Individual Preferences
    - @~/.claude/my-project-instructions.md
    
To avoid potential collisions, imports are not evaluated inside markdown code spans and code blocks.
    
    This code span will not be treated as an import: `@anthropic-ai/claude-code`
    
Imported files can recursively import additional files, with a max-depth of 5 hops. You can see what memory files are loaded by running `/memory` command.

## 

​

How Claude looks up memories

Claude Code reads memories recursively: starting in the cwd, Claude Code recurses up to _/_ and reads any CLAUDE.md or CLAUDE.local.md files it finds. This is especially convenient when working in large repositories where you run Claude Code in _foo/bar/_ , and have memories in both _foo/CLAUDE.md_ and _foo/bar/CLAUDE.md_.

Claude will also discover CLAUDE.md nested in subtrees under your current working directory. Instead of loading them at launch, they are only included when Claude reads files in those subtrees.

## 

​

Quickly add memories with the `#` shortcut

The fastest way to add a memory is to start your input with the `#` character:
    
    # Always use descriptive variable names
    
You’ll be prompted to select which memory file to store this in.

## 

​

Directly edit memories with `/memory`

Use the `/memory` slash command during a session to open any memory file in your system editor for more extensive additions or organization.

## 

​

Memory best practices

  * **Be specific** : “Use 2-space indentation” is better than “Format code properly”.
  * **Use structure to organize** : Format each individual memory as a bullet point and group related memories under descriptive markdown headings.
  * **Review periodically** : Update memories as your project evolves to ensure Claude is always using the most up to date information and context.

Was this page helpful?

YesNo

[IDE integrations](/en/docs/claude-code/ide-integrations)[Settings](/en/docs/claude-code/settings)


---

## AI Analysis

## Analysis of Claude Code Memory Documentation

### 1. Concise Summary

Claude Code offers persistent memory capabilities to remember user and project preferences across sessions. It utilizes specific Markdown files (`CLAUDE.md`, `CLAUDE.local.md`) located in project directories or the user's home directory to store instructions, coding standards, and personal preferences. These memory files can import other files and are automatically loaded into Claude's context, allowing for a highly customizable and context-aware interaction.

### 2. Key Topics Covered

*   **Memory Types and Locations:** Defines different types of memory (Project, User, Project Local) and their respective file paths.
*   **Memory Loading Mechanism:** Explains how Claude Code discovers and loads memory files, including recursive lookup.
*   **Memory File Imports:** Details the `@path/to/import` syntax for including external files within `CLAUDE.md` files.
*   **Adding and Editing Memories:** Provides methods for quickly adding new memories (`#` shortcut) and directly editing memory files (`/memory` command).
*   **Memory Best Practices:** Offers guidelines for effective memory management.

### 3. Important Technical Details

*   **Memory File Naming Conventions:**
    *   `./CLAUDE.md`: Project-specific, team-shared instructions.
    *   `~/.claude/CLAUDE.md`: User-specific, personal preferences across all projects.
    *   `./CLAUDE.local.md`: Deprecated for personal project-specific preferences; replaced by imports.
*   **Automatic Context Loading:** All memory files are automatically loaded into Claude Code's context upon launch.
*   **Recursive Memory Lookup:** Claude searches for `CLAUDE.md` and `CLAUDE.local.md` files by recursing up from the current working directory to the root (`/`). It also discovers nested `CLAUDE.md` files in subtrees, loading them only when files in those subtrees are read.
*   **Import Syntax:** `@path/to/import` allows including other files. Both relative and absolute paths are supported.
*   **Import Limitations:** Imports are not evaluated inside Markdown code spans or code blocks to prevent collisions.
*   **Import Depth:** Recursive imports are supported up to a maximum depth of 5 hops.
*   **Memory Management Commands:**
    *   `/memory`: Slash command to open any memory file in the system editor.
    *   `/memory` (without arguments): Displays currently loaded memory files.
    *   `#` shortcut: Prepending input with `#` prompts for memory storage location.
*   **Deprecation of `CLAUDE.local.md`:** Replaced by the more flexible import mechanism, especially beneficial for multiple Git worktrees.

### 4. Code Examples

```markdown
See @README for project overview and @package.json for available npm commands for this project.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

```markdown
# Individual Preferences
- @~/.claude/my-project-instructions.md
```

```markdown
This code span will not be treated as an import: `@anthropic-ai/claude-code`
```

```
# Always use descriptive variable names
```

### 5. Related Concepts or Prerequisites

*   **Markdown:** Understanding Markdown syntax is essential as memory files are written in Markdown.
*   **File System Navigation:** Familiarity with file paths (relative and absolute) and directory structures is crucial for managing memory files and imports.
*   **Command Line Interface (CLI):** Basic understanding of CLI commands for interacting with Claude Code (e.g., `/memory`).
*   **Version Control (Git):** Implicitly related, especially concerning shared project memories and the rationale behind deprecating `CLAUDE.local.md` for better multi-worktree support.
*   **Context Management (AI/LLMs):** The concept of "context" in large language models, as memory files directly contribute to Claude's understanding of the current task and environment.
