# Getting started with Claude Code - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/getting-started  
**Category:** getting-started  
**Scraped:** 2025-06-09 06:36:01

---

## Original Content

## 

​

Check system requirements

  * **Operating Systems** : macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows via WSL
  * **Hardware** : 4GB RAM minimum
  * **Software** :
    * Node.js 18+
    * [git](https://git-scm.com/downloads) 2.23+ (optional)
    * [GitHub](https://cli.github.com/) or [GitLab](https://gitlab.com/gitlab-org/cli) CLI for PR workflows (optional)
    * [ripgrep](https://github.com/BurntSushi/ripgrep?tab=readme-ov-file#installation) (rg) for enhanced file search (optional)
  * **Network** : Internet connection required for authentication and AI processing
  * **Location** : Available only in [supported countries](https://www.anthropic.com/supported-countries)

**Troubleshooting WSL installation**

Currently, Claude Code does not run directly in Windows, and instead requires WSL. If you encounter issues in WSL:

  1. **OS/platform detection issues** : If you receive an error during installation, WSL may be using Windows `npm`. Try:

     * Run `npm config set os linux` before installation
     * Install with `npm install -g @anthropic-ai/claude-code --force --no-os-check` (Do NOT use `sudo`)
  2. **Node not found errors** : If you see `exec: node: not found` when running `claude`, your WSL environment may be using a Windows installation of Node.js. You can confirm this with `which npm` and `which node`, which should point to Linux paths starting with `/usr/` rather than `/mnt/c/`. To fix this, try installing Node via your Linux distribution’s package manager or via [`nvm`](https://github.com/nvm-sh/nvm).

## 

​

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

Claude Code offers multiple authentication options:

  1. **Anthropic Console** : The default option. Connect through the Anthropic Console and complete the OAuth process. Requires active billing at [console.anthropic.com](https://console.anthropic.com).
  2. **Claude App (with Pro or Max plan)** : Subscribe to Claude’s [Pro or Max plan](https://www.anthropic.com/pricing) for a unified subscription that includes both Claude Code and the web interface. Get more value at the same price point while managing your account in one place. Log in with your Claude.ai account. During launch, choose the option that matches your subscription type.
  3. **Enterprise platforms** : Configure Claude Code to use [Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/bedrock-vertex-proxies) for enterprise deployments with your existing cloud infrastructure.

## 

​

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


---

## AI Analysis

## Analysis of Claude Code Getting Started Documentation

### 1. Concise Summary

This documentation outlines the essential steps to get started with Claude Code, a tool for AI-assisted coding. It covers system requirements, installation, authentication methods, and initial project setup. Special attention is given to troubleshooting common issues, particularly for Windows users relying on WSL.

### 2. Key Topics Covered

*   System Requirements (OS, Hardware, Software, Network, Location)
*   WSL Troubleshooting for Windows users
*   Installation of Claude Code via npm
*   Authentication methods (Anthropic Console, Claude App, Enterprise platforms)
*   Initial project setup and usage (e.g., `summarize this project`, `/init`)

### 3. Important Technical Details

*   **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, Windows via WSL. Direct Windows support is not available.
*   **Hardware**: Minimum 4GB RAM.
*   **Software Dependencies**: Node.js 18+ is mandatory. Optional tools include Git, GitHub/GitLab CLI, and ripgrep.
*   **Installation Method**: Primarily via `npm install -g @anthropic-ai/claude-code`.
*   **WSL Troubleshooting**:
    *   `npm config set os linux` to resolve OS/platform detection.
    *   `npm install -g @anthropic-ai/claude-code --force --no-os-check` for installation issues.
    *   Verify `which npm` and `which node` point to Linux paths (e.g., `/usr/`) to avoid Node not found errors.
    *   Avoid `sudo npm install -g` due to permission and security risks.
*   **Authentication Options**:
    *   **Anthropic Console**: Default, requires active billing.
    *   **Claude App**: For Pro or Max plan subscribers, unified subscription.
    *   **Enterprise Platforms**: Integration with Amazon Bedrock or Google Vertex AI.
*   **Initial Commands**: `claude` to start, `summarize this project` for a simple command, `/init` to generate `CLAUDE.md`.

### 4. Code Examples

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Navigate to your project directory
cd your-project-directory

# Start Claude Code
claude

# Run a simple command within Claude Code
summarize this project

# Generate a CLAUDE.md project guide
/init
```

**WSL Troubleshooting Commands:**

```bash
# Before installation to resolve OS/platform detection
npm config set os linux

# Install with force and no OS check
npm install -g @anthropic-ai/claude-code --force --no-os-check

# Check Node.js and npm paths in WSL
which npm
which node
```

### 5. Related Concepts or Prerequisites

*   **Node.js and npm**: Fundamental for installation and execution. Users should be familiar with Node.js environment setup.
*   **Command Line Interface (CLI)**: Claude Code is a CLI tool, requiring comfort with terminal commands.
*   **WSL (Windows Subsystem for Linux)**: Essential for Windows users, implying familiarity with Linux environments on Windows.
*   **Git/GitHub/GitLab**: Recommended for version control and PR workflows, though optional for basic usage.
*   **Authentication/OAuth**: Understanding of how to authenticate with cloud services.
*   **AI/LLM Concepts**: Basic understanding of how AI tools can assist in coding.
*   **Anthropic Account/Billing**: Required for most authentication methods.
