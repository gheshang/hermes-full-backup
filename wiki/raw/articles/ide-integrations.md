# IDE integrations - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/ide-integrations  
**Category:** ide-integrations  
**Scraped:** 2025-06-09 06:36:21

---

## Original Content

Claude Code seamlessly integrates with popular Integrated Development Environments (IDEs) to enhance your coding workflow. This integration allows you to leverage Claude’s capabilities directly within your preferred development environment.

## 

​

Supported IDEs

Claude Code currently supports two major IDE families:

  * **Visual Studio Code** (including popular forks like Cursor and Windsurf)
  * **JetBrains IDEs** (including PyCharm, WebStorm, IntelliJ, and GoLand)

## 

​

Features

  * **Quick launch** : Use `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux) to open Claude Code directly from your editor, or click the Claude Code button in the UI
  * **Diff viewing** : Code changes can be displayed directly in the IDE diff viewer instead of the terminal. You can configure this in `/config`
  * **Selection context** : The current selection/tab in the IDE is automatically shared with Claude Code
  * **File reference shortcuts** : Use `Cmd+Option+K` (Mac) or `Alt+Ctrl+K` (Linux/Windows) to insert file references (e.g., @File#L1-99)
  * **Diagnostic sharing** : Diagnostic errors (lint, syntax, etc.) from the IDE are automatically shared with Claude as you work

## 

​

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

The plugin may also be auto-installed when you run `claude` in the integrated terminal. The IDE must be restarted completely to take effect.

**Remote Development Limitations** : When using JetBrains Remote Development, you must install the plugin in the remote host via `Settings > Plugin (Host)`.

## 

​

Configuration

Both integrations work with Claude Code’s configuration system. To enable IDE-specific features:

  1. Connect Claude Code to your IDE by running `claude` in the built-in terminal
  2. Run the `/config` command
  3. Set the diff tool to `auto` for automatic IDE detection
  4. Claude Code will automatically use the appropriate viewer based on your IDE

If you’re using an external terminal (not the IDE’s built-in terminal), you can still connect to your IDE by using the `/ide` command after launching Claude Code. This allows you to benefit from IDE integration features even when running Claude from a separate terminal application. This works for both VS Code and JetBrains IDEs.

When using an external terminal, to ensure Claude has default access to the same files as your IDE, start Claude from the same directory as your IDE project root.

## 

​

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
  * Check that VS Code has permission to install extensions

### 

​

JetBrains plugin not working

  * Ensure you’re running Claude Code from the project root directory
  * Check that the JetBrains plugin is enabled in the IDE settings
  * Completely restart the IDE. You may need to do this multiple times
  * For JetBrains Remote Development, ensure that the Claude Code plugin is installed in the remote host and not locally on the client

For additional help, refer to our [troubleshooting guide](/en/docs/claude-code/troubleshooting) or reach out to support.

Was this page helpful?

YesNo

[CLI usage](/en/docs/claude-code/cli-usage)[Memory management](/en/docs/claude-code/memory)


---

## AI Analysis

```markdown
## Analysis of Claude Code IDE Integrations Documentation

### 1. Concise Summary
This documentation outlines how Claude Code integrates with popular IDEs like Visual Studio Code and JetBrains products to enhance the coding workflow. It details supported IDEs, key features such as quick launch and diff viewing, installation procedures for each IDE family, and configuration steps. The document also provides troubleshooting tips for common installation and functionality issues.

### 2. Key Topics Covered
*   Supported IDEs for Claude Code integration
*   Features of Claude Code within IDEs
*   Installation instructions for VS Code and JetBrains IDEs
*   Configuration of IDE-specific features
*   Troubleshooting common integration problems

### 3. Important Technical Details
*   **Supported IDEs:** Visual Studio Code (and forks like Cursor, Windsurf), JetBrains IDEs (PyCharm, WebStorm, IntelliJ, GoLand).
*   **Quick Launch Shortcuts:** `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux).
*   **File Reference Shortcuts:** `Cmd+Option+K` (Mac) / `Alt+Ctrl+K` (Linux/Windows) for `@File#L1-99` format.
*   **Automatic Context Sharing:** Current selection/tab and diagnostic errors (lint, syntax) are automatically shared with Claude.
*   **Installation (VS Code):** Run `claude` in the integrated terminal; extension auto-installs.
*   **Installation (JetBrains):** Install "Claude Code plugin" from marketplace or via `claude` command in integrated terminal (requires IDE restart).
*   **Remote Development (JetBrains):** Plugin must be installed on the *remote host* via `Settings > Plugin (Host)`.
*   **Configuration:** Run `claude` in built-in terminal, then `/config`, set diff tool to `auto`.
*   **External Terminal Integration:** Use `/ide` command after launching Claude Code to connect to an IDE from an external terminal. Start Claude from the project root for file access.
*   **Troubleshooting (VS Code):** Ensure `claude` is run from integrated terminal, and the IDE's CLI command (`code`, `cursor`, `windsurf`) is in PATH.
*   **Troubleshooting (JetBrains):** Run Claude from project root, check plugin enablement, restart IDE multiple times if needed, verify remote host installation for remote development.

### 4. Code Examples
*   `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux) - Quick launch shortcut.
*   `Cmd+Option+K` (Mac) or `Alt+Ctrl+K` (Linux/Windows) - File reference shortcut.
*   `@File#L1-99` - Example file reference format.
*   `claude` - Command to install VS Code extension or connect to IDE.
*   `/ide` - Command to connect to IDE from an external terminal.
*   `/config` - Command to access Claude Code configuration.
*   `auto` - Value for diff tool setting in configuration.
*   `code` - VS Code CLI command.
*   `cursor` - Cursor IDE CLI command.
*   `windsurf` - Windsurf IDE CLI command.
*   `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux) - VS Code command palette shortcut.
*   "Shell Command: Install ‘code’ command in PATH" - VS Code command palette search term.

### 5. Related Concepts or Prerequisites
*   **Integrated Development Environments (IDEs):** Basic understanding of VS Code and JetBrains IDEs.
*   **Command Line Interface (CLI):** Familiarity with running commands in a terminal.
*   **Text Editors/Code Editors:** Understanding of code selection, diff viewers, and diagnostic output.
*   **Plugin/Extension Management:** Knowledge of installing and managing IDE extensions/plugins.
*   **File Paths and References:** Understanding of how files are referenced in a project.
*   **Remote Development:** Awareness of how remote development environments work, especially with JetBrains.
*   **Configuration Files:** Basic understanding of how software configurations are managed.
```
