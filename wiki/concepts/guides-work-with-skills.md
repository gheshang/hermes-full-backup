---
title: Working with Skills
created: 2026-04-24
updated: 2026-04-24
type: concept
tags: ["concept"]
sources: [raw/articles/guides-work-with-skills.md]
---

# Working with Skills

源文档：[Working with Skills](https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md)

# Working with Skills

Skills are on-demand knowledge documents that teach Hermes how to handle specific tasks — from generating ASCII art to managing GitHub PRs. This guide walks you through using them day to day.

For the full technical reference, see [Skills System](/docs/user-guide/features/skills).

---

## Finding Skills

Every Hermes installation ships with bundled skills. See what's available:

```bash
# In any chat session:
/skills

# Or from the CLI:
hermes skills list
```

This shows a compact list with names and descriptions:

```
ascii-art         Generate ASCII art using pyfiglet, cowsay, boxes...
arxiv             Search and retrieve academic papers from arXiv...
github-pr-workflow Full PR lifecycle — create branches, commit...
plan              Plan mode — inspect context, write a markdown...
excalidraw        Create hand-drawn style diagrams using Excalidraw...
```

### Searching for a Skill

```bash...

## Using a Skill

Every installed skill is automatically a slash command. Just type its name:

```bash
# Load a skill and give it a task
/ascii-art Make a banner that says "HELLO WORLD"
/plan Design a REST API for a todo app
/github-pr-workflow Create a PR for the auth refactor

# Just the skill name (no task) loads it and lets you describe what you need
/excalidraw
```

You can also trigger skills through natural conversation — ask Hermes to use a specific skill, and it will load it via the `skill_view` tool.

### Progressive Disclosure

Skills use a token-efficient loading pattern. The agent doesn't load ever...

## Installing from the Hub

Official optional skills ship with Hermes but aren't active by default. Install them explicitly:

```bash
# Install an official optional skill
hermes skills install official/research/arxiv

# Install from the hub in a chat session
/skills install official/creative/songwriting-and-ai-music
```

What happens:
1. The skill directory is copied to `~/.hermes/skills/`
2. It appears in your `skills_list` output
3. It becomes available as a slash command

:::tip
Installed skills take effect in new sessions. If you want it available in the current session, use `/reset` to start fresh, or add `--now` to...

## Plugin-Provided Skills

Plugins can bundle their own skills using namespaced names (`plugin:skill`). This prevents name collisions with built-in skills.

```bash
# Load a plugin skill by its qualified name
skill_view("superpowers:writing-plans")

# Built-in skill with the same base name is unaffected
skill_view("writing-plans")
```

Plugin skills are **not** listed in the system prompt and don't appear in `skills_list`. They're opt-in — load them explicitly when you know a plugin provides one. When loaded, the agent sees a banner listing sibling skills from the same plugin.

For how to ship skills in your own plugin,...

## Configuring Skill Settings

Some skills declare configuration they need in their frontmatter:

```yaml
metadata:
  hermes:
    config:
      - key: tenor.api_key
        description: "Tenor API key for GIF search"
        prompt: "Enter your Tenor API key"
        url: "https://developers.google.com/tenor/guides/quickstart"
```

When a skill with config is first loaded, Hermes prompts you for the values. They're stored in `config.yaml` under `skills.config.*`.

Manage skill config from the CLI:

```bash
# Interactive config for a specific skill
hermes skills config gif-search

# View all skill config
hermes config get sk...

## Creating Your Own Skill

Skills are just markdown files with YAML frontmatter. Creating one takes under five minutes.

### 1. Create the Directory

```bash
mkdir -p ~/.hermes/skills/my-category/my-skill
```

### 2. Write SKILL.md

```markdown title="~/.hermes/skills/my-category/my-skill/SKILL.md"
---
name: my-skill
description: Brief description of what this skill does
version: 1.0.0
metadata:
  hermes:
    tags: [my-tag, automation]
    category: my-category
---

# My Skill...

## When to Use

Use this skill when the user asks about [specific topic] or needs to [specific task]....

## Procedure

1. First, check if [prerequisite] is available
2. Run `command --with-flags`
3. Parse the output and present results...

## Pitfalls

- Common failure: [description]. Fix: [solution]
- Watch out for [edge case]...

## Verification

Run `check-command` to confirm the result is correct.
```

### 3. Add Reference Files (Optional)

Skills can include supporting files the agent loads on demand:

```
my-skill/
├── SKILL.md                    # Main skill document
├── references/
│   ├── api-docs.md             # API reference the agent can consult
│   └── examples.md             # Example inputs/outputs
├── templates/
│   └── config.yaml             # Template files the agent can use
└── scripts/
    └── setup.sh                # Scripts the agent can execute
```

Reference these in your SKILL.md:

```markdown
For API details,...

## Per-Platform Skill Management

Control which skills are available on which platforms:

```bash
hermes skills
```

This opens an interactive TUI where you can enable or disable skills per platform (CLI, Telegram, Discord, etc.). Useful when you want certain skills only available in specific contexts — for example, keeping development skills off Telegram.

---...

## Skills vs Memory

Both are persistent across sessions, but they serve different purposes:

| | Skills | Memory |
|---|---|---|
| **What** | Procedural knowledge — how to do things | Factual knowledge — what things are |
| **When** | Loaded on demand, only when relevant | Injected into every session automatically |
| **Size** | Can be large (hundreds of lines) | Should be compact (key facts only) |
| **Cost** | Zero tokens until loaded | Small but constant token cost |
| **Examples** | "How to deploy to Kubernetes" | "User prefers dark mode, lives in PST" |
| **Who creates** | You, the agent, or installed from H...

## Tips

**Keep skills focused.** A skill that tries to cover "all of DevOps" will be too long and too vague. A skill that covers "deploy a Python app to Fly.io" is specific enough to be genuinely useful.

**Let the agent create skills.** After a complex multi-step task, Hermes will often offer to save the approach as a skill. Say yes — these agent-authored skills capture the exact workflow including pitfalls that were discovered along the way.

**Use categories.** Organize skills into subdirectories (`~/.hermes/skills/devops/`, `~/.hermes/skills/research/`, etc.). This keeps the list manageable and he...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[hermes-environment-variables]]
