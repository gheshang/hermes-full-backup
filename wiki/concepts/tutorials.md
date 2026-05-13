---
title: Tutorials - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/tutorials.md]
---

# Tutorials - Anthropic

源文档：[Tutorials - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/tutorials/tutorials.md)

# Tutorials - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/tutorials  
**Category:** tutorials  
**Scraped:** 2025-06-09 06:37:10

---

## Original Content

This guide provides step-by-step tutorials for common workflows with Claude Code. Each tutorial includes clear instructions, example commands, and best practices to help you get the most from Claude Code....

## ​

* [Resume previous conversations](/_sites/docs.anthropic.com/en/docs/claude-code/tutorials#resume-previous-conversations)
  * [Understand new codebases](/_sites/docs.anthropic.com/en/docs/claude-code/tutorials#understand-new-codebases)
  * [Fix bugs efficiently](/_sites/docs.anthropic.com/en/docs/claude-code/tutorials#fix-bugs-efficiently)
  * [Refactor code](/_sites/docs.anthropic.com/en/docs/claude-code/tutorials#refactor-code)
  * [Work with tests](/_sites/docs.anthropic.com/en/docs/claude-code/tutorials#work-with-tests)
  * [Create pull requests](/_sites/docs.anthropic.com/en/docs/claude-c...

## ​

Resume previous conversations

### 

​

Continue your work seamlessly

**When to use:** You’ve been working on a task with Claude Code and need to continue where you left off in a later session.

Claude Code provides two options for resuming previous conversations:

  * `--continue` to automatically continue the most recent conversation
  * `--resume` to display a conversation picker

1

Continue the most recent conversation
    
    claude --continue
    
This immediately resumes your most recent conversation without any prompts.

2

Continue in non-interactive mode
    
    claude --continue...

## ​

Understand new codebases

### 

​

Get a quick codebase overview

**When to use:** You’ve just joined a new project and need to understand its structure quickly.

1

Navigate to the project root directory
    
    cd /path/to/project 
    
2

Start Claude Code
    
    claude 
    
3

Ask for a high-level overview
    
    > give me an overview of this codebase 
    
4

Dive deeper into specific components
    
    > explain the main architecture patterns used here 
    
    > what are the key data models?
    
    > how is authentication handled?
    
**Tips:**

  * Start with broad questions...

## ​

Fix bugs efficiently

### 

​

Diagnose error messages

**When to use:** You’ve encountered an error message and need to find and fix its source.

1

Share the error with Claude
    
    > I'm seeing an error when I run npm test 
    
2

Ask for fix recommendations
    
    > suggest a few ways to fix the @ts-ignore in user.ts 
    
3

Apply the fix
    
    > update user.ts to add the null check you suggested 
    
**Tips:**

  * Tell Claude the command to reproduce the issue and get a stack trace
  * Mention any steps to reproduce the error
  * Let Claude know if the error is intermittent or...

## ​

Refactor code

### 

​

Modernize legacy code

**When to use:** You need to update old code to use modern patterns and practices.

1

Identify legacy code for refactoring
    
    > find deprecated API usage in our codebase 
    
2

Get refactoring recommendations
    
    > suggest how to refactor utils.js to use modern JavaScript features 
    
3

Apply the changes safely
    
    > refactor utils.js to use ES2024 features while maintaining the same behavior 
    
4

Verify the refactoring
    
    > run tests for the refactored code 
    
**Tips:**

  * Ask Claude to explain the benefits of...

## ​

Work with tests

### 

​

Add test coverage

**When to use:** You need to add tests for uncovered code.

1

Identify untested code
    
    > find functions in NotificationsService.swift that are not covered by tests 
    
2

Generate test scaffolding
    
    > add tests for the notification service 
    
3

Add meaningful test cases
    
    > add test cases for edge conditions in the notification service 
    
4

Run and verify tests
    
    > run the new tests and fix any failures 
    
**Tips:**

  * Ask for tests that cover edge cases and error conditions
  * Request both unit and integ...

## ​

Create pull requests

### 

​

Generate comprehensive PRs

**When to use:** You need to create a well-documented pull request for your changes.

1

Summarize your changes
    
    > summarize the changes I've made to the authentication module 
    
2

Generate a PR with Claude
    
    > create a pr 
    
3

Review and refine
    
    > enhance the PR description with more context about the security improvements 
    
4

Add testing details
    
    > add information about how these changes were tested 
    
**Tips:**

  * Ask Claude directly to make a PR for you
  * Review Claude’s generated ...

## ​

Handle documentation

### 

​

Generate code documentation

**When to use:** You need to add or update documentation for your code.

1

Identify undocumented code
    
    > find functions without proper JSDoc comments in the auth module 
    
2

Generate documentation
    
    > add JSDoc comments to the undocumented functions in auth.js 
    
3

Review and enhance
    
    > improve the generated documentation with more context and examples 
    
4

Verify documentation
    
    > check if the documentation follows our project standards 
    
**Tips:**

  * Specify the documentation style yo...

## ​

Work with images

### 

​

Analyze images and screenshots

**When to use:** You need to work with images in your codebase or get Claude’s help analyzing image content.

1

Add an image to the conversation

You can use any of these methods:

  1. Drag and drop an image into the Claude Code window
  2. Copy an image and paste it into the CLI with cmd+v (on Mac)
  3. Provide an image path claude “Analyze this image: /path/to/your/image.png”

2

Ask Claude to analyze the image
    
    > What does this image show? 
    > Describe the UI elements in this screenshot 
    > Are there any problematic ...

## ​

Use extended thinking

### 

​

Leverage Claude’s extended thinking for complex tasks

**When to use:** When working on complex architectural decisions, challenging bugs, or planning multi-step implementations that require deep reasoning.

1

Provide context and ask Claude to think
    
    > I need to implement a new authentication system using OAuth2 for our API. Think deeply about the best approach for implementing this in our codebase. 
    
Claude will gather relevant information from your codebase and use extended thinking, which will be visible in the interface.

2

Refine the thinking ...

## ​

Set up project memory

### 

​

Create an effective CLAUDE.md file

**When to use:** You want to set up a CLAUDE.md file to store important project information, conventions, and frequently used commands.

1

Bootstrap a CLAUDE.md for your codebase
    
    > /init 
    
**Tips:**

  * Include frequently used commands (build, test, lint) to avoid repeated searches
  * Document code style preferences and naming conventions
  * Add important architectural patterns specific to your project
  * CLAUDE.md memories can be used for both instructions shared with your team and for your individual prefer...

## ​

Set up Model Context Protocol (MCP)

Model Context Protocol (MCP) is an open protocol that enables LLMs to access external tools and data sources. For more details, see the [MCP documentation](https://modelcontextprotocol.io/introduction).

Use third party MCP servers at your own risk. Make sure you trust the MCP servers, and be especially careful when using MCP servers that talk to the internet, as these can expose you to prompt injection risk.

### 

​

Configure MCP servers

**When to use:** You want to enhance Claude’s capabilities by connecting it to specialized tools and external servers...

## ​

Use Claude as a unix-style utility

### 

​

Add Claude to your verification process

**When to use:** You want to use Claude Code as a linter or code reviewer.

**Steps:**

1

Add Claude to your build script
    
    // package.json
    {
        ...
        "scripts": {
 

> 完整内容见 raw 源文件

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
