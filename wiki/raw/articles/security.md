# Manage permissions and security - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/security  
**Category:** security  
**Scraped:** 2025-06-09 06:36:32

---

## Original Content

Claude Code uses a tiered permission system to balance power and safety:

Tool Type| Example| Approval Required| ”Yes, don’t ask again” Behavior  
---|---|---|---  
Read-only| File reads, LS, Grep| No| N/A  
Bash Commands| Shell execution| Yes| Permanently per project directory and command  
File Modification| Edit/write files| Yes| Until session end  
  
## 

​

Tools available to Claude

Claude Code has access to a set of powerful tools that help it understand and modify your codebase:

Tool| Description| Permission Required  
---|---|---  
**Agent**|  Runs a sub-agent to handle complex, multi-step tasks| No  
**Bash**|  Executes shell commands in your environment| Yes  
**Edit**|  Makes targeted edits to specific files| Yes  
**Glob**|  Finds files based on pattern matching| No  
**Grep**|  Searches for patterns in file contents| No  
**LS**|  Lists files and directories| No  
**MultiEdit**|  Performs multiple edits on a single file atomically| Yes  
**NotebookEdit**|  Modifies Jupyter notebook cells| Yes  
**NotebookRead**|  Reads and displays Jupyter notebook contents| No  
**Read**|  Reads the contents of files| No  
**TodoRead**|  Reads the current session’s task list| No  
**TodoWrite**|  Creates and manages structured task lists| No  
**WebFetch**|  Fetches content from a specified URL| Yes  
**WebSearch**|  Performs web searches with domain filtering| Yes  
**Write**|  Creates or overwrites files| Yes  
  
Permission rules can be configured using `/allowed-tools` or in [permission settings](/en/docs/claude-code/settings#permissions).

## 

​

Protect against prompt injection

Prompt injection is a technique where an attacker attempts to override or manipulate an AI assistant’s instructions by inserting malicious text. Claude Code includes several safeguards against these attacks:

  * **Permission system** : Sensitive operations require explicit approval
  * **Context-aware analysis** : Detects potentially harmful instructions by analyzing the full request
  * **Input sanitization** : Prevents command injection by processing user inputs
  * **Command blocklist** : Blocks risky commands that fetch arbitrary content from the web like `curl` and `wget`

**Best practices for working with untrusted content** :

  1. Review suggested commands before approval
  2. Avoid piping untrusted content directly to Claude
  3. Verify proposed changes to critical files
  4. Report suspicious behavior with `/bug`

While these protections significantly reduce risk, no system is completely immune to all attacks. Always maintain good security practices when working with any AI tool.

## 

​

Configure network access

Claude Code requires access to:

  * api.anthropic.com
  * statsig.anthropic.com
  * sentry.io

Allowlist these URLs when using Claude Code in containerized environments.

## 

​

Development container reference implementation

Claude Code provides a development container configuration for teams that need consistent, secure environments. This preconfigured [devcontainer setup](https://code.visualstudio.com/docs/devcontainers/containers) works seamlessly with VS Code’s Remote - Containers extension and similar tools.

The container’s enhanced security measures (isolation and firewall rules) allow you to run `claude --dangerously-skip-permissions` to bypass permission prompts for unattended operation. We’ve included a [reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer) that you can customize for your needs.

While the devcontainer provides substantial protections, no system is completely immune to all attacks. Always maintain good security practices and monitor Claude’s activities.

### 

​

Key features

  * **Production-ready Node.js** : Built on Node.js 20 with essential development dependencies
  * **Security by design** : Custom firewall restricting network access to only necessary services
  * **Developer-friendly tools** : Includes git, ZSH with productivity enhancements, fzf, and more
  * **Seamless VS Code integration** : Pre-configured extensions and optimized settings
  * **Session persistence** : Preserves command history and configurations between container restarts
  * **Works everywhere** : Compatible with macOS, Windows, and Linux development environments

### 

​

Getting started in 4 steps

  1. Install VS Code and the Remote - Containers extension
  2. Clone the [Claude Code reference implementation](https://github.com/anthropics/claude-code/tree/main/.devcontainer) repository
  3. Open the repository in VS Code
  4. When prompted, click “Reopen in Container” (or use Command Palette: Cmd+Shift+P → “Remote-Containers: Reopen in Container”)

### 

​

Configuration breakdown

The devcontainer setup consists of three primary components:

  * [**devcontainer.json**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/devcontainer.json): Controls container settings, extensions, and volume mounts
  * [**Dockerfile**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile): Defines the container image and installed tools
  * [**init-firewall.sh**](https://github.com/anthropics/claude-code/blob/main/.devcontainer/init-firewall.sh): Establishes network security rules

### 

​

Security features

The container implements a multi-layered security approach with its firewall configuration:

  * **Precise access control** : Restricts outbound connections to whitelisted domains only (npm registry, GitHub, Anthropic API, etc.)
  * **Default-deny policy** : Blocks all other external network access
  * **Startup verification** : Validates firewall rules when the container initializes
  * **Isolation** : Creates a secure development environment separated from your main system

### 

​

Customization options

The devcontainer configuration is designed to be adaptable to your needs:

  * Add or remove VS Code extensions based on your workflow
  * Modify resource allocations for different hardware environments
  * Adjust network access permissions
  * Customize shell configurations and developer tooling

Was this page helpful?

YesNo

[Settings](/en/docs/claude-code/settings)[Team setup](/en/docs/claude-code/team)


---

## AI Analysis

## Analysis of Claude Code Security Documentation

### 1. Concise Summary

This documentation outlines the security features and best practices for using Claude Code, focusing on its tiered permission system for tool access and safeguards against prompt injection. It also provides guidance on configuring network access and a reference implementation for a secure development container, emphasizing isolation and controlled network access for enhanced security.

### 2. Key Topics Covered

*   **Permission System:** How Claude Code manages access to various tools, including required approvals and "don't ask again" behaviors.
*   **Available Tools:** A comprehensive list of tools Claude Code can access, categorized by permission requirements.
*   **Prompt Injection Protection:** Mechanisms and best practices to prevent and mitigate prompt injection attacks.
*   **Network Access Configuration:** Required URLs for Claude Code operation and guidance for allowlisting.
*   **Development Container Reference Implementation:** A secure, pre-configured devcontainer setup for consistent and isolated development environments.

### 3. Important Technical Details

*   **Tiered Permissions:**
    *   **Read-only:** No approval (e.g., File reads, LS, Grep).
    *   **Bash Commands:** Approval required, "don't ask again" is permanent per project directory and command.
    *   **File Modification:** Approval required, "don't ask again" is until session end.
*   **Tools and Permissions:**
    *   **No Permission Required:** Agent, Glob, Grep, LS, NotebookRead, Read, TodoRead, TodoWrite.
    *   **Permission Required:** Bash, Edit, MultiEdit, NotebookEdit, WebFetch, WebSearch, Write.
*   **Prompt Injection Safeguards:** Permission system, context-aware analysis, input sanitization, command blocklist (e.g., `curl`, `wget`).
*   **Network Endpoints:** `api.anthropic.com`, `statsig.anthropic.com`, `sentry.io` must be allowlisted.
*   **Devcontainer Security:**
    *   Allows `claude --dangerously-skip-permissions` for unattended operation within the isolated environment.
    *   Custom firewall (`init-firewall.sh`) with precise access control and default-deny policy.
    *   Restricts outbound connections to whitelisted domains (npm registry, GitHub, Anthropic API).
    *   Uses `devcontainer.json` for settings and `Dockerfile` for image definition.

### 4. Code Examples (or pseudo-code/commands)

*   **Permission Configuration:** `/allowed-tools` command or settings UI.
*   **Reporting Suspicious Behavior:** `/bug` command.
*   **Devcontainer Setup (Implied):**
    *   `claude --dangerously-skip-permissions` (for use within the devcontainer).
    *   Reference to `devcontainer.json`, `Dockerfile`, and `init-firewall.sh` for configuration.
    *   VS Code Command Palette: "Remote-Containers: Reopen in Container".

### 5. Related Concepts or Prerequisites

*   **AI Security:** Understanding of prompt injection, command injection, and general AI safety principles.
*   **Containerization:** Familiarity with Docker, VS Code Dev Containers, and concepts like isolation and secure environments.
*   **Network Security:** Knowledge of firewalls, allowlisting, and default-deny policies.
*   **Version Control:** Basic understanding of Git for cloning repositories.
*   **VS Code:** Proficiency with VS Code and its extensions, specifically "Remote - Containers".
*   **Node.js:** The devcontainer is built on Node.js 20, implying familiarity with Node.js development.
