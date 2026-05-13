# Manage costs effectively - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/costs  
**Category:** costs  
**Scraped:** 2025-06-09 06:36:56

---

## Original Content

Claude Code consumes tokens for each interaction. The average cost is $6 per developer per day, with daily costs remaining below $12 for 90% of users.

## 

​

Track your costs

  * Use `/cost` to see current session usage
  * **Anthropic Console users** :
    * Check [historical usage](https://support.anthropic.com/en/articles/9534590-cost-and-usage-reporting-in-console) in the Anthropic Console (requires Admin or Billing role)
    * Set [workspace spend limits](https://support.anthropic.com/en/articles/9796807-creating-and-managing-workspaces) for the Claude Code workspace (requires Admin role)
  * **Pro and Max plan users** : Usage is included in your subscription

## 

​

Reduce token usage

  * **Compact conversations:**

    * Claude uses auto-compact by default when context exceeds 95% capacity

    * Toggle auto-compact: Run `/config` and navigate to “Auto-compact enabled”

    * Use `/compact` manually when context gets large

    * Add custom instructions: `/compact Focus on code samples and API usage`

    * Customize compaction by adding to CLAUDE.md:
        
                # Summary instructions
        
        When you are using compact, please focus on test output and code changes
        
  * **Write specific queries:** Avoid vague requests that trigger unnecessary scanning

  * **Break down complex tasks:** Split large tasks into focused interactions

  * **Clear history between tasks:** Use `/clear` to reset context

Costs can vary significantly based on:

  * Size of codebase being analyzed
  * Complexity of queries
  * Number of files being searched or modified
  * Length of conversation history
  * Frequency of compacting conversations
  * Background processes (haiku generation, conversation summarization)

## 

​

Background token usage

Claude Code uses tokens for some background functionality even when idle:

  * **Haiku generation** : Small creative messages that appear while you type (approximately 1 cent per day)
  * **Conversation summarization** : Background jobs that summarize previous conversations for the `claude --resume` feature
  * **Command processing** : Some commands like `/cost` may generate requests to check status

These background processes consume a small amount of tokens (typically under $0.04 per session) even without active interaction.

For team deployments, we recommend starting with a small pilot group to establish usage patterns before wider rollout.

Was this page helpful?

YesNo

[Monitoring usage](/en/docs/claude-code/monitoring-usage)[GitHub Actions](/en/docs/claude-code/github-actions)


---

## AI Analysis

## Analysis of Claude Code Costs Documentation

### 1. Concise Summary

This documentation outlines the cost structure for Claude Code, emphasizing token consumption as the primary driver. It provides tools and strategies for users to track and reduce their spending, including in-app commands, console features, and best practices for conversation management. The document also details background token usage for features like Haiku generation and conversation summarization.

### 2. Key Topics Covered

*   Claude Code pricing model (token-based)
*   Average and typical daily costs
*   Methods for tracking usage (`/cost`, Anthropic Console)
*   Strategies for reducing token consumption (compacting, specific queries, task breakdown, clearing history)
*   Factors influencing cost variability
*   Background token usage (Haiku, summarization, command processing)
*   Recommendations for team deployments

### 3. Important Technical Details

*   **Cost Model:** Token consumption.
*   **Average Cost:** $6 per developer per day.
*   **Cost Cap:** 90% of users stay below $12 per day.
*   **Usage Tracking Commands:**
    *   `/cost`: Current session usage.
    *   `/config`: Toggle auto-compact.
    *   `/compact`: Manually compact conversation.
    *   `/clear`: Clear conversation history.
*   **Anthropic Console Features (for Console users):**
    *   Historical usage reporting (requires Admin/Billing role).
    *   Workspace spend limits (requires Admin role).
*   **Pro/Max Plan Users:** Usage included in subscription.
*   **Auto-compact:** Default behavior when context exceeds 95% capacity.
*   **Custom Compaction:** Can be configured via `CLAUDE.md` with `# Summary instructions`.
*   **Factors Affecting Cost:** Codebase size, query complexity, file search/modification count, conversation history length, compaction frequency, background processes.
*   **Background Token Usage:**
    *   Haiku generation: ~1 cent/day.
    *   Conversation summarization (for `claude --resume`).
    *   Command processing (e.g., `/cost`).
    *   Typically under $0.04 per session for background processes.

### 4. Code Examples

```markdown
# Summary instructions
When you are using compact, please focus on test output and code changes
```
This example demonstrates how to customize the compaction behavior by adding specific instructions to the `CLAUDE.md` file, guiding Claude on what information to prioritize during compaction.

### 5. Related Concepts or Prerequisites

*   **Tokenization:** Fundamental understanding of how AI models process text into tokens and how this relates to cost.
*   **Context Window:** Awareness of the concept of a model's context window and how conversation history fills it.
*   **Anthropic Console:** Familiarity with the Anthropic Console for administrative tasks, billing, and workspace management.
*   **Command-Line Interface (CLI) Usage:** Basic understanding of interacting with applications via commands (e.g., `/cost`, `/compact`).
*   **Version Control (Implicit):** The mention of "code changes" and "test output" implies interaction with codebases, often managed via version control systems.
