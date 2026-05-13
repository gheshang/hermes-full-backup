# CLI usage and controls - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/cli-usage  
**Category:** cli-usage  
**Scraped:** 2025-06-09 06:36:11

---

## Original Content

## 

​

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
    cat logs.txt | claude -p "analyze these errors"
    
## 

​

CLI commands

Command| Description| Example  
---|---|---  
`claude`| Start interactive REPL| `claude`  
`claude "query"`| Start REPL with initial prompt| `claude "explain this project"`  
`claude -p "query"`| Run one-off query, then exit| `claude -p "explain this function"`  
`cat file | claude -p "query"`| Process piped content| `cat logs.txt | claude -p "explain"`  
`claude -c`| Continue most recent conversation| `claude -c`  
`claude -c -p "query"`| Continue in print mode| `claude -c -p "Check for type errors"`  
`claude -r "<session-id>" "query"`| Resume session by ID| `claude -r "abc123" "Finish this PR"`  
`claude update`| Update to latest version| `claude update`  
`claude mcp`| Configure Model Context Protocol servers| [See MCP section in tutorials](/en/docs/claude-code/tutorials#set-up-model-context-protocol-mcp)  
  
## 

​

CLI flags

Customize Claude Code’s behavior with these command-line flags:

Flag| Description| Example  
---|---|---  
`--allowedTools`| A list of tools that should be allowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings)| `"Bash(git log:*)" "Bash(git diff:*)" "Write"`  
`--disallowedTools`| A list of tools that should be disallowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings)| `"Bash(git log:*)" "Bash(git diff:*)" "Write"`  
`--print`, `-p`| Print response without interactive mode (see [SDK documentation](/en/docs/claude-code/sdk) for programmatic usage details)| `claude -p "query"`  
`--output-format`| Specify output format for print mode (options: `text`, `json`, `stream-json`)| `claude -p "query" --output-format json`  
`--verbose`| Enable verbose logging, shows full turn-by-turn output (helpful for debugging in both print and interactive modes)| `claude --verbose`  
`--max-turns`| Limit the number of agentic turns in non-interactive mode| `claude -p --max-turns 3 "query"`  
`--model`| Sets the model for the current session with an alias for the latest model (`sonnet` or `opus`) or a model’s full name| `claude --model claude-sonnet-4-20250514`  
`--permission-prompt-tool`| Specify an MCP tool to handle permission prompts in non-interactive mode| `claude -p --permission-prompt-tool mcp_auth_tool "query"`  
`--resume`| Resume a specific session by ID, or by choosing in interactive mode| `claude --resume abc123 "query"`  
`--continue`| Load the most recent conversation in the current directory| `claude --continue`  
`--dangerously-skip-permissions`| Skip permission prompts (use with caution)| `claude --dangerously-skip-permissions`  
  
The `--output-format json` flag is particularly useful for scripting and automation, allowing you to parse Claude’s responses programmatically.

For detailed information about print mode (`-p`) including output formats, streaming, verbose logging, and programmatic usage, see the [SDK documentation](/en/docs/claude-code/sdk).

## 

​

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
`/memory`| Edit CLAUDE.md memory files  
`/model`| Select or change the AI model  
`/permissions`| View or update [permissions](settings#permissions)  
`/pr_comments`| View pull request comments  
`/review`| Request code review  
`/status`| View account and system statuses  
`/terminal-setup`| Install Shift+Enter key binding for newlines (iTerm2 and VSCode only)  
`/vim`| Enter vim mode for alternating insert and command modes  
  
## 

​

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

  1. Open Settings → Profiles → Keys
  2. Under General, set Left/Right Option key to “Esc+”

**Tip for iTerm2 and VSCode users** : Run `/terminal-setup` within Claude Code to automatically configure Shift+Enter as a more intuitive alternative.

See [terminal setup in settings](/en/docs/claude-code/settings#line-breaks) for configuration details.

## 

​

Vim Mode

Claude Code supports a subset of Vim keybindings that can be enabled with `/vim` or configured via `/config`.

The supported subset includes:

  * Mode switching: `Esc` (to NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (to INSERT)
  * Navigation: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`
  * Editing: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (repeat)

Was this page helpful?

YesNo

[Common tasks](/en/docs/claude-code/common-tasks)[IDE integrations](/en/docs/claude-code/ide-integrations)


---

## AI Analysis

## Analysis of Claude Code CLI Usage Documentation

### 1. Concise Summary

This documentation outlines how to interact with Claude Code via its command-line interface (CLI). It details two primary interaction modes: interactive REPL sessions and one-shot commands. The guide also covers various CLI commands, flags for customization, in-session slash commands, and special shortcuts for memory management and multiline input, including basic Vim mode support.

### 2. Key Topics Covered

*   **CLI Interaction Modes:** Interactive REPL vs. One-shot commands.
*   **Core CLI Commands:** Starting sessions, querying, continuing conversations, resuming sessions, updating.
*   **CLI Flags:** Customizing behavior (e.g., tool permissions, output format, model selection, verbose logging).
*   **Interactive Slash Commands:** In-session controls (e.g., reporting bugs, clearing history, configuring, managing memory, changing models).
*   **Special Shortcuts:** Quick memory (`#`), multiline input (`\`, Option/Shift+Enter).
*   **Vim Mode:** Basic Vim keybinding support for interactive sessions.

### 3. Important Technical Details

*   **Interactive Mode:** `claude` (starts REPL), `claude "query"` (starts REPL with initial prompt).
*   **One-shot Mode:** `claude -p "query"` (runs command and exits), `cat file | claude -p "query"` (processes piped content).
*   **Conversation Management:**
    *   `claude -c`: Continues the most recent conversation in the current directory.
    *   `claude -r "<session-id>"`: Resumes a specific conversation by ID.
*   **Tool Permissions:** `--allowedTools` and `--disallowedTools` flags control tool access, complementing `settings.json`. `--dangerously-skip-permissions` bypasses prompts (use with caution).
*   **Output Formatting:** `--output-format` flag (options: `text`, `json`, `stream-json`) is crucial for scripting and automation, especially `json` output.
*   **Model Selection:** `--model` flag allows specifying the AI model (e.g., `sonnet`, `opus`, or full model names).
*   **Debugging:** `--verbose` flag provides detailed turn-by-turn output for debugging.
*   **Agentic Turns:** `--max-turns` limits agentic turns in non-interactive mode.
*   **Memory Management:** `#` shortcut for quick memory addition, `/memory` slash command for editing `CLAUDE.md` files.
*   **Multiline Input:** `\` escape, Option+Enter (Mac Terminal, iTerm2, VSCode setup details provided), Shift+Enter (configurable via `/terminal-setup`).
*   **Vim Mode:** Enabled by `/vim` or `/config`, supports common navigation and editing commands (`h/j/k/l`, `w/e/b`, `x`, `d`, `c`, `.`, mode switching).

### 4. Code Examples

```bash
# Start interactive mode
claude

# Start with an initial query
claude "explain this project"

# Run a single command and exit
claude -p "what does this function do?"

# Process piped content
cat logs.txt | claude -p "analyze these errors"

# Continue most recent conversation
claude -c

# Continue in print mode
claude -c -p "Check for type errors"

# Resume session by ID
claude -r "abc123" "Finish this PR"

# Update to latest version
claude update

# Example with output format
claude -p "query" --output-format json

# Example with verbose logging
claude --verbose

# Example with max turns
claude -p --max-turns 3 "query"

# Example with model selection
claude --model claude-sonnet-4-20250514

# Quick memory with #
# Always use descriptive variable names
```

### 5. Related Concepts or Prerequisites

*   **Command Line Interface (CLI) Basics:** Familiarity with executing commands in a terminal.
*   **REPL (Read-Eval-Print Loop):** Understanding interactive programming environments.
*   **Piping (`|`):** Knowledge of redirecting output from one command as input to another.
*   **JSON:** Understanding JSON format for programmatic output parsing.
*   **Version Control (Git):** Implied by tool examples like `Bash(git log:*)` and `Bash(git diff:*)`.
*   **Text Editors (Vim):** Basic familiarity with Vim concepts for Vim mode.
*   **Configuration Files:** Reference to `settings.json` for tool permissions and `CLAUDE.md` for memory.
*   **Model Context Protocol (MCP):** Mentioned for server configuration and permission prompts.
*   **SDK Documentation:** Referenced for more detailed programmatic usage of print mode.
