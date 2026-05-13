# Claude Code overview - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/overview  
**Category:** overview  
**Scraped:** 2025-06-09 06:36:01

---

## Original Content

Claude Code is an agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster through natural language commands. By integrating directly with your development environment, Claude Code streamlines your workflow without requiring additional servers or complex setup.
    
    npm install -g @anthropic-ai/claude-code
    
Claude Code’s key capabilities include:

  * Editing files and fixing bugs across your codebase
  * Answering questions about your code’s architecture and logic
  * Executing and fixing tests, linting, and other commands
  * Searching through git history, resolving merge conflicts, and creating commits and PRs
  * Browsing documentation and resources from the internet using web search
  * Works with [Amazon Bedrock and Google Vertex AI](/en/docs/claude-code/bedrock-vertex-proxies) for enterprise deployments

## 

​

Why Claude Code?

Claude Code operates directly in your terminal, understanding your project context and taking real actions. No need to manually add files to context - Claude will explore your codebase as needed.

### 

​

Enterprise integration

Claude Code seamlessly integrates with enterprise AI platforms. You can connect to [Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/bedrock-vertex-proxies) for secure, compliant deployments that meet your organization’s requirements.

### 

​

Security and privacy by design

Your code’s security is paramount. Claude Code’s architecture ensures:

  * **Direct API connection** : Your queries go straight to Anthropic’s API without intermediate servers
  * **Works where you work** : Operates directly in your terminal
  * **Understands context** : Maintains awareness of your entire project structure
  * **Takes action** : Performs real operations like editing files and creating commits

## 

​

Getting started

To get started with Claude Code, follow our [installation guide](/en/docs/claude-code/getting-started) which covers system requirements, installation steps, and authentication process.

## 

​

Quick tour

Here’s what you can accomplish with Claude Code:

### 

​

From questions to solutions in seconds
    
    # Ask questions about your codebase
    claude
    > how does our authentication system work?
    
    # Create a commit with one command
    claude commit
    
    # Fix issues across multiple files
    claude "fix the type errors in the auth module"
    
### 

​

Understand unfamiliar code
    
    > what does the payment processing system do?
    > find where user permissions are checked
    > explain how the caching layer works
    
### 

​

Automate Git operations
    
    > commit my changes
    > create a pr
    > which commit added tests for markdown back in December?
    > rebase on main and resolve any merge conflicts
    
## 

​

Next steps

## [Getting startedInstall Claude Code and get up and running](/en/docs/claude-code/getting-started)## [Core featuresExplore what Claude Code can do for you](/en/docs/claude-code/common-tasks)## [CommandsLearn about CLI commands and controls](/en/docs/claude-code/cli-usage)## [ConfigurationCustomize Claude Code for your workflow](/en/docs/claude-code/settings)

## 

​

Additional resources

## [Claude Code tutorialsStep-by-step guides for common tasks](/en/docs/claude-code/tutorials)## [TroubleshootingSolutions for common issues with Claude Code](/en/docs/claude-code/troubleshooting)## [Bedrock & Vertex integrationsConfigure Claude Code with Amazon Bedrock or Google Vertex AI](/en/docs/claude-code/bedrock-vertex-proxies)## [Reference implementationClone our development container reference implementation.](https://github.com/anthropics/claude-code/tree/main/.devcontainer)

## 

​

License and data usage

Claude Code is provided under Anthropic’s [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms).

### 

​

How we use your data

We aim to be fully transparent about how we use your data. We may use feedback to improve our products and services, but we will not train generative models using your feedback from Claude Code. Given their potentially sensitive nature, we store user feedback transcripts for only 30 days.

#### 

​

Feedback transcripts

If you choose to send us feedback about Claude Code, such as transcripts of your usage, Anthropic may use that feedback to debug related issues and improve Claude Code’s functionality (e.g., to reduce the risk of similar bugs occurring in the future). We will not train generative models using this feedback.

### 

​

Privacy safeguards

We have implemented several safeguards to protect your data, including limited retention periods for sensitive information, restricted access to user session data, and clear policies against using feedback for model training.

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) and [Privacy Policy](https://www.anthropic.com/legal/privacy).

### 

​

License

© Anthropic PBC. All rights reserved. Use is subject to Anthropic’s [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms).

Was this page helpful?

YesNo

[Getting started](/en/docs/claude-code/getting-started)


---

## AI Analysis

```markdown
## Analysis of Claude Code Documentation

### 1. Concise Summary

Claude Code is an AI-powered, agentic coding tool designed to operate directly within a developer's terminal. It understands the codebase context, allowing users to interact with it using natural language commands to perform various coding tasks, from editing files and fixing bugs to managing Git operations and answering code-related questions. It emphasizes seamless integration with existing development environments and offers enterprise deployment options with platforms like Amazon Bedrock and Google Vertex AI, while prioritizing security and privacy.

### 2. Key Topics Covered

*   **Product Overview:** What Claude Code is and its core purpose.
*   **Key Capabilities:** Specific tasks Claude Code can perform.
*   **Value Proposition:** Why developers should use Claude Code (terminal integration, context awareness).
*   **Enterprise Integration:** Support for Bedrock and Vertex AI.
*   **Security and Privacy:** Data handling, direct API connection, and safeguards.
*   **Getting Started:** Installation and authentication.
*   **Use Cases/Quick Tour:** Practical examples of how to use Claude Code.
*   **Further Resources:** Links to detailed documentation (installation, features, commands, configuration, tutorials, troubleshooting).
*   **Licensing and Data Usage:** Terms of service, data retention, and privacy policies.

### 3. Important Technical Details

*   **Deployment Model:** Terminal-based agentic tool; no additional servers required.
*   **Installation:** Via `npm` global package manager.
*   **Core Functionality:**
    *   Code editing and bug fixing.
    *   Codebase architecture and logic understanding.
    *   Test execution and fixing, linting.
    *   Git operations: history search, merge conflict resolution, commit/PR creation.
    *   Web search for documentation.
*   **Enterprise Support:** Integrates with Amazon Bedrock and Google Vertex AI for secure, compliant deployments.
*   **Security Architecture:**
    *   Direct API connection to Anthropic's API (no intermediate servers).
    *   Operates locally in the terminal.
    *   Maintains awareness of the entire project structure.
    *   Performs real actions (file edits, commits).
*   **Data Usage Policy:**
    *   Feedback may be used for debugging and improving Claude Code functionality.
    *   **Crucially, Anthropic states they will NOT train generative models using user feedback from Claude Code.**
    *   User feedback transcripts are stored for only 30 days.
    *   Limited retention periods and restricted access to user session data.

### 4. Code Examples

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Ask questions about your codebase
claude
> how does our authentication system work?

# Create a commit with one command
claude commit

# Fix issues across multiple files
claude "fix the type errors in the auth module"

# Understand unfamiliar code
> what does the payment processing system do?
> find where user permissions are checked
> explain how the caching layer works

# Automate Git operations
> commit my changes
> create a pr
> which commit added tests for markdown back in December?
> rebase on main and resolve any merge conflicts
```

### 5. Related Concepts or Prerequisites

*   **Node.js and npm:** Required for installation.
*   **Terminal/Command Line Interface (CLI):** Claude Code operates within the terminal.
*   **Git:** Deep integration with Git for version control operations.
*   **Software Development Concepts:** Understanding of codebases, debugging, testing, linting, and common development workflows.
*   **AI Agents:** Understanding of how AI can act autonomously within a system.
*   **Cloud AI Platforms (Optional):** Familiarity with Amazon Bedrock or Google Vertex AI for enterprise deployments.
*   **Anthropic API:** Claude Code communicates directly with Anthropic's API.
*   **Privacy and Data Security Best Practices:** Important for users to understand the implications of using such a tool with their codebase.
