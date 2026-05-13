---
title: SDK - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/sdk.md]
---

# SDK - Anthropic

源文档：[SDK - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/sdk/sdk.md)

# SDK - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/sdk  
**Category:** sdk  
**Scraped:** 2025-06-09 06:37:10

---

## Original Content

The Claude Code SDK allows developers to programmatically integrate Claude Code into their applications. It enables running Claude Code as a subprocess, providing a way to build AI-powered coding assistants and tools that leverage Claude’s capabilities.

The SDK currently support command line usage. TypeScript and Python SDKs are coming soon....

## ​

Authentication

To use the Claude Code SDK, we recommend creating a dedicated API key:

  1. Create an Anthropic API key in the [Anthropic Console](https://console.anthropic.com/)
  2. Then, set the `ANTHROPIC_API_KEY` environment variable. We recommend storing this key securely (eg. using a Github [secret](https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions))...

## ​

Basic SDK usage

The Claude Code SDK allows you to use Claude Code in non-interactive mode from your applications. Here’s a basic example:
    
    # Run a single prompt and exit (print mode)
    $ claude -p "Write a function to calculate Fibonacci numbers"
    
    # Using a pipe to provide stdin
    $ echo "Explain this code" | claude -p
    
    # Output in JSON format with metadata
    $ claude -p "Generate a hello world function" --output-format json
    
    # Stream JSON output as it arrives
    $ claude -p "Build a React component" --output-format stream-json...

## ​

Advanced usage

### 

​

Multi-turn conversations

For multi-turn conversations, you can resume conversations or continue from the most recent session:
    
    # Continue the most recent conversation
    $ claude --continue
    
    # Continue and provide a new prompt
    $ claude --continue "Now refactor this for better performance"
    
    # Resume a specific conversation by session ID
    $ claude --resume 550e8400-e29b-41d4-a716-446655440000
    
    # Resume in print mode (non-interactive)
    $ claude -p --resume 550e8400-e29b-41d4-a716-446655440000 "Update the tests"
    
    # Contin...

## ​

Available CLI options

The SDK leverages all the CLI options available in Claude Code. Here are the key ones for SDK usage:

Flag| Description| Example  
---|---|---  
`--print`, `-p`| Run in non-interactive mode| `claude -p "query"`  
`--output-format`| Specify output format (`text`, `json`, `stream-json`)| `claude -p --output-format json`  
`--resume`, `-r`| Resume a conversation by session ID| `claude --resume abc123`  
`--continue`, `-c`| Continue the most recent conversation| `claude --continue`  
`--verbose`| Enable verbose logging| `claude --verbose`  
`--max-turns`| Limit agentic turns...

## ​

Output formats

The SDK supports multiple output formats:

### 

​

Text output (default)

Returns just the response text:
    
    $ claude -p "Explain file src/components/Header.tsx"
    # Output: This is a React component showing...
    
### 

​

JSON output

Returns structured data including metadata:
    
    $ claude -p "How does the data layer work?" --output-format json
    
Response format:
    
    {
      "type": "result",
      "subtype": "success",
      "cost_usd": 0.003,
      "is_error": false,
      "duration_ms": 1234,
      "duration_api_ms": 800,
      "num_turns": 6,
     ...

## ​

Message schema

Messages returned from the JSON API are strictly typed according to the following schema:
    
    type SDKMessage =
      // An assistant message
      | {
          type: "assistant";
          message: Message; // from Anthropic SDK
          session_id: string;
        }
    
      // A user message
      | {
          type: "user";
          message: MessageParam; // from Anthropic SDK
          session_id: string;
        }
    
      // Emitted as the last message
      | {
          type: "result";
          subtype: "success";
          cost_usd: float;
          durat...

## ​

Examples

### 

​

Simple script integration
    
    #!/bin/bash
    
    # Simple function to run Claude and check exit code
    run_claude() {
        local prompt="$1"
        local output_format="${2:-text}"
    
        if claude -p "$prompt" --output-format "$output_format"; then
            echo "Success!"
        else
            echo "Error: Claude failed with exit code $?" >&2
            return 1
        fi
    }
    
    # Usage examples
    run_claude "Write a Python function to read CSV files"
    run_claude "Optimize this database query" "json"
    
### 

​

Processing files wi...

## ​

Best practices

  1. **Use JSON output format** for programmatic parsing of responses:
    
        # Parse JSON response with jq
    result=$(claude -p "Generate code" --output-format json)
    code=$(echo "$result" | jq -r '.result')
    cost=$(echo "$result" | jq -r '.cost_usd')
    
  2. **Handle errors gracefully** \- check exit codes and stderr:
    
        if ! claude -p "$prompt" 2>error.log; then
        echo "Error occurred:" >&2
        cat error.log >&2
        exit 1
    fi
    
  3. **Use session management** for maintaining context in multi-turn conversations

  4. **Consider t...

## ​

Real-world applications

The Claude Code SDK enables powerful integrations with your development workflow. One notable example is the [Claude Code GitHub Actions](/en/docs/claude-code/github-actions), which uses the SDK to provide automated code review, PR creation, and issue triage capabilities directly in your GitHub workflow....

## ​

Related resources

  * [CLI usage and controls](/en/docs/claude-code/cli-usage) \- Complete CLI documentation
  * [GitHub Actions integration](/en/docs/claude-code/github-actions) \- Automate your GitHub workflow with Claude
  * [Tutorials](/en/docs/claude-code/tutorials) \- Step-by-step guides for common use cases

Was this page helpful?

YesNo

[GitHub Actions](/en/docs/claude-code/github-actions)[Tutorials](/en/docs/claude-code/tutorials)


---...

## Analysis of Claude Code SDK Documentation

### 1. Concise Summary

The Claude Code SDK enables programmatic integration of Claude Code into applications, primarily through command-line usage. It facilitates building AI-powered coding tools by allowing non-interactive execution of Claude Code, multi-turn conversations, and advanced configurations like custom system prompts and integration with external tools via the Model Context Protocol (MCP). Authentication is handled via an Anthropic API key set as an environment variable.

### 2. Key Topics Covered

*   **SDK Overview and Purpose:** What the SDK is and what it's used for.
*   **Aut...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
