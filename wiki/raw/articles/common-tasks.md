# Core tasks and workflows - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/common-tasks  
**Category:** common-tasks  
**Scraped:** 2025-06-09 06:36:11

---

## Original Content

Claude Code operates directly in your terminal, understanding your project context and taking real actions. No need to manually add files to context - Claude will explore your codebase as needed.

## 

​

Understand unfamiliar code
    
    > what does the payment processing system do?
    > find where user permissions are checked
    > explain how the caching layer works
    
## 

​

Automate Git operations
    
    > commit my changes
    > create a pr
    > which commit added tests for markdown back in December?
    > rebase on main and resolve any merge conflicts
    
## 

​

Edit code intelligently
    
    > add input validation to the signup form
    > refactor the logger to use the new API
    > fix the race condition in the worker queue
    
## 

​

Test and debug your code
    
    > run tests for the auth module and fix failures
    > find and fix security vulnerabilities
    > explain why this test is failing
    
## 

​

Encourage deeper thinking

For complex problems, explicitly ask Claude to think more deeply:
    
    > think about how we should architect the new payment service
    > think hard about the edge cases in our authentication flow
    
Claude Code will show when the model is using extended thinking. You can proactively prompt Claude to “think” or “think deeply” for more planning-intensive tasks. We suggest that you first tell Claude about your task and let it gather context from your project. Then, ask it to “think” to create a plan.

Claude will think more based on the words you use. For example, “think hard” will trigger more extended thinking than saying “think” alone.

For more tips, see [Extended thinking tips](/en/docs/build-with-claude/prompt-engineering/extended-thinking-tips).

## 

​

Automate CI and infra workflows

Claude Code comes with a non-interactive mode for headless execution. This is especially useful for running Claude Code in non-interactive contexts like scripts, pipelines, and Github Actions.

Use `--print` (`-p`) to run Claude in non-interactive mode. In this mode, you can set the `ANTHROPIC_API_KEY` environment variable to provide a custom API key.

Non-interactive mode is especially useful when you pre-configure the set of commands Claude is allowed to use:
    
    export ANTHROPIC_API_KEY=sk_...
    claude -p "update the README with the latest changes" --allowedTools "Bash(git diff:*)" "Bash(git log:*)" Write --disallowedTools ...
    
Was this page helpful?

YesNo

[Getting started](/en/docs/claude-code/getting-started)[CLI usage](/en/docs/claude-code/cli-usage)


---

## AI Analysis

```markdown
## Analysis of Claude Code Documentation

### 1. Concise Summary

Claude Code is an AI assistant designed to operate directly within a developer's terminal, understanding project context and performing real actions. It streamlines various coding tasks, from understanding unfamiliar code and automating Git operations to intelligently editing, testing, and debugging code. It also supports "extended thinking" for complex problems and offers a non-interactive mode for CI/CD and infrastructure automation.

### 2. Key Topics Covered

*   **Core Functionality:** Terminal-based operation, context awareness, real action execution.
*   **Use Cases:**
    *   Code understanding and explanation.
    *   Git operations automation.
    *   Intelligent code editing (refactoring, validation, bug fixing).
    *   Code testing and debugging.
*   **Advanced Features:**
    *   Extended thinking for complex problem-solving.
    *   Non-interactive mode for CI/CD and automation.
*   **Configuration:** API key usage, tool permissions in non-interactive mode.

### 3. Important Technical Details

*   **Contextual Understanding:** Claude Code explores the codebase as needed, eliminating the need for manual file additions to context.
*   **Extended Thinking:** Users can prompt Claude to "think" or "think deeply" for more planning-intensive tasks. The model indicates when it's using extended thinking. The phrasing of the prompt (e.g., "think hard" vs. "think") influences the depth of thinking.
*   **Non-interactive Mode (`--print` or `-p`):**
    *   Enables headless execution for scripts, pipelines, and GitHub Actions.
    *   Requires `ANTHROPIC_API_KEY` environment variable for custom API keys.
    *   Supports pre-configuration of allowed and disallowed commands/tools using `--allowedTools` and `--disallowedTools` arguments. This is crucial for security and control in automated environments.

### 4. Code Examples

**Automate CI and infra workflows (Non-interactive mode):**

```bash
export ANTHROPIC_API_KEY=sk_...
claude -p "update the README with the latest changes" --allowedTools "Bash(git diff:*)" "Bash(git log:*)" Write --disallowedTools ...
```

**Example Prompts for Claude Code:**

*   `> what does the payment processing system do?`
*   `> commit my changes`
*   `> add input validation to the signup form`
*   `> run tests for the auth module and fix failures`
*   `> think about how we should architect the new payment service`

### 5. Related Concepts or Prerequisites

*   **Terminal/CLI Usage:** Users need familiarity with command-line interfaces.
*   **Git:** Basic understanding of Git commands and workflows is beneficial for leveraging Git automation features.
*   **Software Development Concepts:** Familiarity with common coding tasks like refactoring, testing, debugging, and architectural design.
*   **API Keys:** Understanding how to set and manage environment variables for API keys.
*   **CI/CD Pipelines:** Knowledge of continuous integration and continuous deployment concepts for utilizing the non-interactive mode.
*   **Prompt Engineering:** The "Extended thinking tips" link suggests that effective prompting is key to maximizing Claude's capabilities, especially for complex tasks.
