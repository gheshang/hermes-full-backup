# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [2026-04-24] create | Wiki initialized
- Domain: AI Agent 技术栈
- Path: ~/.hermes/wiki
- Structure created with SCHEMA.md, index.md, log.md

## [2026-04-24] ingest | Hermes Agent v0.11.0 Release Notes + AGENTS.md
- Sources:
  - raw/articles/hermes-v0.11.0-release-notes.md
  - raw/articles/hermes-agents-md-developer-guide.md
- Pages created:
  - entities/hermes-agent.md
  - entities/hermes-v0.11.0.md
  - concepts/transport-abc.md
  - concepts/orchestrator-role.md
  - concepts/compression-anti-thrashing.md
  - concepts/feishu-improvements.md
  - concepts/wecom-setup.md
  - concepts/browser-cdp.md
  - concepts/shell-hooks.md
  - concepts/cron-toolsets.md
  - concepts/tui-ink.md
  - concepts/plugin-surface.md
  - concepts/session-resume.md

## [2026-04-24] ingest | VPS Init Script + Hermes Config Setup
- Sources:
  - raw/articles/vps-init-script-guide.md
  - raw/articles/hermes-config-setup-guide.md
- Pages created:
  - concepts/vps-init-script.md
  - concepts/hermes-config-setup.md

## [2026-04-24] ingest | Hermes Bundled Skills Catalog
- Source: https://hermes-agent.nousresearch.com/docs/reference/skills-catalog
- Method: browser + JS extraction
- Pages created:
  - entities/hermes-bundled-skills-catalog.md (87 skills / 28 categories)

## [2026-04-24] ingest | Hermes Optional Skills Catalog
- Source: https://hermes-agent.nousresearch.com/docs/reference/optional-skills-catalog
- Method: browser + JS extraction
- Pages created:
  - entities/hermes-optional-skills-catalog.md (57 skills / 14 categories)

## [2026-04-24] ingest | Hermes Reference Docs Batch (8 pages)
- Source: GitHub raw (NousResearch/hermes-agent repo)
- Method: curl from raw.githubusercontent.com
- Pages created:
  - concepts/hermes-cli-commands.md (35KB raw)
  - concepts/hermes-slash-commands.md (12KB raw)
  - concepts/hermes-profile-commands.md (7.5KB raw)
  - concepts/hermes-environment-variables.md (36KB raw)
  - concepts/hermes-built-in-tools.md (16KB raw)
  - concepts/hermes-toolsets.md (8KB raw)
  - concepts/hermes-mcp-config.md (5.8KB raw)
  - concepts/hermes-faq-troubleshooting.md (31KB raw)
- Total wiki pages: 23

## [2026-04-24] ingest | getting-started-installation
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/installation.md | 3677 bytes

## [2026-04-24] ingest | getting-started-learning-path
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/learning-path.md | 8686 bytes

## [2026-04-24] ingest | getting-started-nix-setup
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/nix-setup.md | 35506 bytes

## [2026-04-24] ingest | getting-started-quickstart
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/quickstart.md | 10626 bytes

## [2026-04-24] ingest | getting-started-termux
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/termux.md | 6400 bytes

## [2026-04-24] ingest | getting-started-updating
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/updating.md | 5960 bytes

## [2026-04-24] ingest | features-acp
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/acp.md | 4123 bytes

## [2026-04-24] ingest | features-api-server
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/api-server.md | 14087 bytes

## [2026-04-24] ingest | features-batch-processing
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/batch-processing.md | 8680 bytes

## [2026-04-24] ingest | features-browser
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/browser.md | 20856 bytes

## [2026-04-24] ingest | features-built-in-plugins
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/built-in-plugins.md | 5582 bytes

## [2026-04-24] ingest | features-code-execution
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/code-execution.md | 10189 bytes

## [2026-04-24] ingest | features-context-files
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/context-files.md | 9224 bytes

## [2026-04-24] ingest | features-context-references
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/context-references.md | 5390 bytes

## [2026-04-24] ingest | features-credential-pools
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/credential-pools.md | 8491 bytes

## [2026-04-24] ingest | features-cron
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/cron.md | 11416 bytes

## [2026-04-24] ingest | features-dashboard-plugins
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/dashboard-plugins.md | 10186 bytes

## [2026-04-24] ingest | features-delegation
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/delegation.md | 10985 bytes

## [2026-04-24] ingest | features-fallback-providers
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/fallback-providers.md | 14369 bytes

## [2026-04-24] ingest | features-honcho
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/honcho.md | 13425 bytes

## [2026-04-24] ingest | features-hooks
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/hooks.md | 39312 bytes

## [2026-04-24] ingest | features-image-generation
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/image-generation.md | 6945 bytes

## [2026-04-24] ingest | features-mcp
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/mcp.md | 16120 bytes

## [2026-04-24] ingest | features-memory-providers
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/memory-providers.md | 23277 bytes

## [2026-04-24] ingest | features-memory
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/memory.md | 9757 bytes

## [2026-04-24] ingest | features-overview
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/overview.md | 6460 bytes

## [2026-04-24] ingest | features-personality
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/personality.md | 8353 bytes

## [2026-04-24] ingest | features-plugins
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/plugins.md | 10893 bytes

## [2026-04-24] ingest | features-provider-routing
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/provider-routing.md | 5217 bytes

## [2026-04-24] ingest | features-rl-training
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/rl-training.md | 9139 bytes

## [2026-04-24] ingest | features-skills
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skills.md | 21692 bytes

## [2026-04-24] ingest | features-skins
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/skins.md | 11396 bytes

## [2026-04-24] ingest | features-tool-gateway
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/tool-gateway.md | 7584 bytes

## [2026-04-24] ingest | features-tools
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/tools.md | 6470 bytes

## [2026-04-24] ingest | features-tts
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/tts.md | 8206 bytes

## [2026-04-24] ingest | features-vision
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/vision.md | 8245 bytes

## [2026-04-24] ingest | features-voice-mode
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/voice-mode.md | 18179 bytes

## [2026-04-24] ingest | features-web-dashboard
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/web-dashboard.md | 24677 bytes

## [2026-04-24] ingest | reference-cli-commands
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/cli-commands.md | 35673 bytes

## [2026-04-24] ingest | reference-environment-variables
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/environment-variables.md | 36007 bytes

## [2026-04-24] ingest | reference-faq
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/faq.md | 31305 bytes

## [2026-04-24] ingest | reference-mcp-config-reference
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/mcp-config-reference.md | 5789 bytes

## [2026-04-24] ingest | reference-optional-skills-catalog
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/optional-skills-catalog.md | 19910 bytes

## [2026-04-24] ingest | reference-profile-commands
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/profile-commands.md | 7513 bytes

## [2026-04-24] ingest | reference-skills-catalog
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/skills-catalog.md | 24711 bytes

## [2026-04-24] ingest | reference-slash-commands
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/slash-commands.md | 11599 bytes

## [2026-04-24] ingest | reference-tools-reference
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/tools-reference.md | 16676 bytes

## [2026-04-24] ingest | reference-toolsets-reference
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/reference/toolsets-reference.md | 8514 bytes

## [2026-04-24] ingest | guides-automate-with-cron
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/automate-with-cron.md | 9750 bytes

## [2026-04-24] ingest | guides-automation-templates
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/automation-templates.md | 19092 bytes

## [2026-04-24] ingest | guides-aws-bedrock
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/aws-bedrock.md | 5608 bytes

## [2026-04-24] ingest | guides-build-a-hermes-plugin
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/build-a-hermes-plugin.md | 25443 bytes

## [2026-04-24] ingest | guides-cron-troubleshooting
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/cron-troubleshooting.md | 9188 bytes

## [2026-04-24] ingest | guides-daily-briefing-bot
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/daily-briefing-bot.md | 10297 bytes

## [2026-04-24] ingest | guides-delegation-patterns
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/delegation-patterns.md | 10155 bytes

## [2026-04-24] ingest | guides-github-pr-review-agent
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/github-pr-review-agent.md | 9398 bytes

## [2026-04-24] ingest | guides-local-llm-on-mac
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/local-llm-on-mac.md | 9168 bytes

## [2026-04-24] ingest | guides-migrate-from-openclaw
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/migrate-from-openclaw.md | 15144 bytes

## [2026-04-24] ingest | guides-python-library
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/python-library.md | 10161 bytes

## [2026-04-24] ingest | guides-team-telegram-assistant
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/team-telegram-assistant.md | 13656 bytes

## [2026-04-24] ingest | guides-tips
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/tips.md | 11943 bytes

## [2026-04-24] ingest | guides-use-mcp-with-hermes
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/use-mcp-with-hermes.md | 9731 bytes

## [2026-04-24] ingest | guides-use-soul-with-hermes
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/use-soul-with-hermes.md | 6953 bytes

## [2026-04-24] ingest | guides-use-voice-mode-with-hermes
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/use-voice-mode-with-hermes.md | 9586 bytes

## [2026-04-24] ingest | guides-webhook-github-pr-review
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/webhook-github-pr-review.md | 15168 bytes

## [2026-04-24] ingest | guides-work-with-skills
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/guides/work-with-skills.md | 8826 bytes

## [2026-04-24] ingest | integrations-index
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/index.md | 7357 bytes

## [2026-04-24] ingest | integrations-providers
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/integrations/providers.md | 53099 bytes

## [2026-04-24] ingest | getting-started-installation
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/installation.md | 3677 bytes

## [2026-04-24] ingest | getting-started-learning-path
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/learning-path.md | 8686 bytes

## [2026-04-24] ingest | getting-started-nix-setup
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/nix-setup.md | 35506 bytes

## [2026-04-24] ingest | getting-started-quickstart
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/quickstart.md | 10626 bytes

## [2026-04-24] ingest | getting-started-termux
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/termux.md | 6400 bytes

## [2026-04-24] ingest | getting-started-updating
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/getting-started/updating.md | 5960 bytes

## [2026-04-24] ingest | configuration
- Source: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/configuration.md | 70523 bytes | Method: github-raw

## [2026-04-24] ingest | cli
- Source: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/cli.md | 14903 bytes | Method: github-raw

## [2026-04-24] ingest | docker
- Source: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/docker.md | 9683 bytes | Method: github-raw

## [2026-04-24] ingest | profiles
- Source: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/profiles.md | 8643 bytes | Method: github-raw

## [2026-04-24] ingest | security
- Source: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/security.md | 23488 bytes | Method: github-raw

## [2026-04-24] ingest | sessions
- Source: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/sessions.md | 16224 bytes | Method: github-raw

## [2026-04-24] ingest | tui
- Source: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/tui.md | 8863 bytes | Method: github-raw

## [2026-04-24] ingest | git-worktrees
- Source: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/git-worktrees.md | 5509 bytes | Method: github-raw

## [2026-04-24] ingest | checkpoints-and-rollback
- Source: https://raw.githubusercontent.com/NousResearch/hermes-agent/main/website/docs/user-guide/checkpoints-and-rollback.md | 6722 bytes | Method: github-raw

## [2026-04-24] ingest | messaging-bluebubbles
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/bluebubbles.md | 5123 bytes

## [2026-04-24] ingest | messaging-dingtalk
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/dingtalk.md | 10749 bytes

## [2026-04-24] ingest | messaging-discord
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/discord.md | 32511 bytes

## [2026-04-24] ingest | messaging-email
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/email.md | 7484 bytes

## [2026-04-24] ingest | messaging-feishu
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/feishu.md | 22259 bytes

## [2026-04-24] ingest | messaging-homeassistant
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/homeassistant.md | 8598 bytes

## [2026-04-24] ingest | messaging-index
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/index.md | 16504 bytes

## [2026-04-24] ingest | messaging-matrix
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/matrix.md | 25614 bytes

## [2026-04-24] ingest | messaging-mattermost
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/mattermost.md | 12503 bytes

## [2026-04-24] ingest | messaging-open-webui
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/open-webui.md | 9772 bytes

## [2026-04-24] ingest | messaging-qqbot
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/qqbot.md | 4517 bytes

## [2026-04-24] ingest | messaging-signal
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/signal.md | 8858 bytes

## [2026-04-24] ingest | messaging-slack
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/slack.md | 17277 bytes

## [2026-04-24] ingest | messaging-sms
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/sms.md | 6532 bytes

## [2026-04-24] ingest | messaging-telegram
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/telegram.md | 25043 bytes

## [2026-04-24] ingest | messaging-webhooks
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/webhooks.md | 19471 bytes

## [2026-04-24] ingest | messaging-wecom-callback
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/wecom-callback.md | 5349 bytes

## [2026-04-24] ingest | messaging-wecom
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/wecom.md | 12057 bytes

## [2026-04-24] ingest | messaging-weixin
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/weixin.md | 13931 bytes

## [2026-04-24] ingest | messaging-whatsapp
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/messaging/whatsapp.md | 10475 bytes

## [2026-04-24] ingest | developer-guide-acp-internals
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/acp-internals.md | 4620 bytes

## [2026-04-24] ingest | developer-guide-adding-platform-adapters
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/adding-platform-adapters.md | 9457 bytes

## [2026-04-24] ingest | developer-guide-adding-providers
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/adding-providers.md | 13644 bytes

## [2026-04-24] ingest | developer-guide-adding-tools
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/adding-tools.md | 6082 bytes

## [2026-04-24] ingest | developer-guide-agent-loop
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/agent-loop.md | 10660 bytes

## [2026-04-24] ingest | developer-guide-architecture
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/architecture.md | 16542 bytes

## [2026-04-24] ingest | developer-guide-browser-supervisor
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/browser-supervisor.md | 10503 bytes

## [2026-04-24] ingest | developer-guide-context-compression-and-caching
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/context-compression-and-caching.md | 14557 bytes

## [2026-04-24] ingest | developer-guide-context-engine-plugin
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/context-engine-plugin.md | 6921 bytes

## [2026-04-24] ingest | developer-guide-contributing
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/contributing.md | 7376 bytes

## [2026-04-24] ingest | developer-guide-creating-skills
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/creating-skills.md | 15435 bytes

## [2026-04-24] ingest | developer-guide-cron-internals
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/cron-internals.md | 9314 bytes

## [2026-04-24] ingest | developer-guide-environments
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/environments.md | 20370 bytes

## [2026-04-24] ingest | developer-guide-extending-the-cli
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/extending-the-cli.md | 7034 bytes

## [2026-04-24] ingest | developer-guide-gateway-internals
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/gateway-internals.md | 12340 bytes

## [2026-04-24] ingest | developer-guide-memory-provider-plugin
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/memory-provider-plugin.md | 9161 bytes

## [2026-04-24] ingest | developer-guide-prompt-assembly
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/prompt-assembly.md | 9065 bytes

## [2026-04-24] ingest | developer-guide-provider-runtime
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/provider-runtime.md | 7307 bytes

## [2026-04-24] ingest | developer-guide-session-storage
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/session-storage.md | 11398 bytes

## [2026-04-24] ingest | developer-guide-tools-runtime
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/tools-runtime.md | 10117 bytes

## [2026-04-24] ingest | developer-guide-trajectory-format
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/developer-guide/trajectory-format.md | 8286 bytes

## [2026-04-24] ingest | apple-apple-apple-notes
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/apple/apple-apple-notes.md | 2903 bytes

## [2026-04-24] ingest | apple-apple-apple-reminders
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/apple/apple-apple-reminders.md | 3198 bytes

## [2026-04-24] ingest | apple-apple-findmy
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/apple/apple-findmy.md | 4356 bytes

## [2026-04-24] ingest | apple-apple-imessage
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/apple/apple-imessage.md | 3048 bytes

## [2026-04-24] ingest | autonomous-ai-agents-autonomous-ai-agents-claude-code
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-claude-code.md | 35310 bytes

## [2026-04-24] ingest | autonomous-ai-agents-autonomous-ai-agents-codex
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-codex.md | 4908 bytes

## [2026-04-24] ingest | autonomous-ai-agents-autonomous-ai-agents-hermes-agent
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-hermes-agent.md | 28938 bytes

## [2026-04-24] ingest | autonomous-ai-agents-autonomous-ai-agents-opencode
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-opencode.md | 8290 bytes

## [2026-04-24] ingest | creative-creative-architecture-diagram
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-architecture-diagram.md | 7342 bytes

## [2026-04-24] ingest | creative-creative-ascii-art
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-ascii-art.md | 11329 bytes

## [2026-04-24] ingest | creative-creative-ascii-video
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-ascii-video.md | 15371 bytes

## [2026-04-24] ingest | creative-creative-baoyu-comic
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-baoyu-comic.md | 16317 bytes

## [2026-04-24] ingest | creative-creative-baoyu-infographic
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-baoyu-infographic.md | 11267 bytes

## [2026-04-24] ingest | creative-creative-creative-ideation
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-creative-ideation.md | 6792 bytes

## [2026-04-24] ingest | creative-creative-design-md
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-design-md.md | 7956 bytes

## [2026-04-24] ingest | creative-creative-excalidraw
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-excalidraw.md | 7867 bytes

## [2026-04-24] ingest | creative-creative-manim-video
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-manim-video.md | 12701 bytes

## [2026-04-24] ingest | creative-creative-p5js
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-p5js.md | 28229 bytes

## [2026-04-24] ingest | creative-creative-pixel-art
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-pixel-art.md | 8319 bytes

## [2026-04-24] ingest | creative-creative-popular-web-designs
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-popular-web-designs.md | 9858 bytes

## [2026-04-24] ingest | creative-creative-songwriting-and-ai-music
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/creative/creative-songwriting-and-ai-music.md | 10831 bytes

## [2026-04-24] ingest | data-science-data-science-jupyter-live-kernel
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/data-science/data-science-jupyter-live-kernel.md | 6255 bytes

## [2026-04-24] ingest | devops-devops-webhook-subscriptions
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/devops/devops-webhook-subscriptions.md | 7647 bytes

## [2026-04-24] ingest | dogfood-dogfood-dogfood
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/dogfood/dogfood-dogfood.md | 6890 bytes

## [2026-04-24] ingest | email-email-himalaya
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/email/email-himalaya.md | 6507 bytes

## [2026-04-24] ingest | gaming-gaming-minecraft-modpack-server
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/gaming/gaming-minecraft-modpack-server.md | 7320 bytes

## [2026-04-24] ingest | gaming-gaming-pokemon-player
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/gaming/gaming-pokemon-player.md | 9405 bytes

## [2026-04-24] ingest | github-github-codebase-inspection
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/github/github-codebase-inspection.md | 4438 bytes

## [2026-04-24] ingest | github-github-github-auth
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/github/github-github-auth.md | 8671 bytes

## [2026-04-24] ingest | github-github-github-code-review
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/github/github-github-code-review.md | 14459 bytes

## [2026-04-24] ingest | github-github-github-issues
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/github/github-github-issues.md | 10119 bytes

## [2026-04-24] ingest | github-github-github-pr-workflow
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/github/github-github-pr-workflow.md | 10892 bytes

## [2026-04-24] ingest | github-github-github-repo-management
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/github/github-github-repo-management.md | 14667 bytes

## [2026-04-24] ingest | mcp-mcp-native-mcp
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mcp/mcp-native-mcp.md | 13270 bytes

## [2026-04-24] ingest | media-media-gif-search
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/media/media-gif-search.md | 3323 bytes

## [2026-04-24] ingest | media-media-heartmula
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/media/media-heartmula.md | 7093 bytes

## [2026-04-24] ingest | media-media-songsee
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/media/media-songsee.md | 3054 bytes

## [2026-04-24] ingest | media-media-youtube-content
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/media/media-youtube-content.md | 3794 bytes

## [2026-04-24] ingest | mlops-mlops-evaluation-lm-evaluation-harness
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-evaluation-lm-evaluation-harness.md | 13104 bytes

## [2026-04-24] ingest | mlops-mlops-evaluation-weights-and-biases
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-evaluation-weights-and-biases.md | 13214 bytes

## [2026-04-24] ingest | mlops-mlops-huggingface-hub
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-huggingface-hub.md | 4410 bytes

## [2026-04-24] ingest | mlops-mlops-inference-llama-cpp
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-inference-llama-cpp.md | 9938 bytes

## [2026-04-24] ingest | mlops-mlops-inference-obliteratus
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-inference-obliteratus.md | 16178 bytes

## [2026-04-24] ingest | mlops-mlops-inference-outlines
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-inference-outlines.md | 16684 bytes

## [2026-04-24] ingest | mlops-mlops-inference-vllm
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-inference-vllm.md | 10122 bytes

## [2026-04-24] ingest | mlops-mlops-models-audiocraft
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-models-audiocraft.md | 17180 bytes

## [2026-04-24] ingest | mlops-mlops-models-segment-anything
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-models-segment-anything.md | 14498 bytes

## [2026-04-24] ingest | mlops-mlops-research-dspy
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-research-dspy.md | 16009 bytes

## [2026-04-24] ingest | mlops-mlops-training-axolotl
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-training-axolotl.md | 5506 bytes

## [2026-04-24] ingest | mlops-mlops-training-trl-fine-tuning
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-training-trl-fine-tuning.md | 13691 bytes

## [2026-04-24] ingest | mlops-mlops-training-unsloth
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/bundled/mlops/mlops-training-unsloth.md | 3001 bytes

## [2026-04-24] ingest | skills-godmode
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/godmode.md | 14029 bytes

## [2026-04-24] ingest | skills-google-workspace
- GitHub: https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/skills/google-workspace.md | 6417 bytes

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/README.md | 22522 bytes | Method: github-raw

## [2026-04-26] ingest | readmezh
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/README_ZH.md | 21466 bytes | Method: github-raw

## [2026-04-26] ingest | release-note-v531-en
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/release-note-v5.3.1-en.md | 2175 bytes | Method: github-raw

## [2026-04-26] ingest | release-note-v531-zh
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/release-note-v5.3.1-zh.md | 1863 bytes | Method: github-raw

## [2026-04-26] ingest | roadmap
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/roadmap.md | 1645 bytes | Method: github-raw

## [2026-04-26] ingest | 2026-03-10-proxy-phase-c-manual-takeover
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-10-proxy-phase-c-manual-takeover.md | 10820 bytes | Method: github-raw

## [2026-04-26] ingest | 2026-03-11-app-specific-managed-proxy
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-11-app-specific-managed-proxy.md | 8598 bytes | Method: github-raw

## [2026-04-26] ingest | 2026-03-14-claude-provider-switch-ux
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-14-claude-provider-switch-ux.md | 4916 bytes | Method: github-raw

## [2026-04-26] ingest | 2026-03-09-proxy-b-single-provider-ux
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-09-proxy-b-single-provider-ux.md | 5462 bytes | Method: github-raw

## [2026-04-26] ingest | 2026-03-09-proxy-b-multiapp-skeleton
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-03-09-proxy-b-multiapp-skeleton.md | 9684 bytes | Method: github-raw

## [2026-04-26] ingest | v370-unified-mcp-refactor
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/v3.7.0-unified-mcp-refactor.md | 26195 bytes | Method: github-raw

## [2026-04-26] ingest | 2026-04-24-common-config-backend-consolidation
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/plans/2026-04-24-common-config-backend-consolidation.md | 20794 bytes | Method: github-raw

## [2026-04-26] ingest | changelog
- Source: https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/CHANGELOG.md | 42043 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/README.md | 2873 bytes | Method: github-raw

## [2026-04-26] ingest | changelog
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md | 255309 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/README.md | 6530 bytes | Method: github-raw

## [2026-04-26] ingest | security
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/SECURITY.md | 693 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/feature-dev/README.md | 11697 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/README.md | 7703 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/plugin-dev/README.md | 14592 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/frontend-design/README.md | 977 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/hookify/README.md | 7710 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/commit-commands/README.md | 5908 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/agent-sdk-dev/README.md | 6397 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/claude-opus-4-5-migration/README.md | 707 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/explanatory-output-style/README.md | 2470 bytes | Method: github-raw

## [2026-04-26] ingest | readme
- Source: https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/learning-output-style/README.md | 4687 bytes | Method: github-raw

## [2026-04-26] ingest | overview
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/overview/overview.md | 9584 bytes | Method: github-raw

## [2026-04-26] ingest | getting-started
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/getting-started/getting-started.md | 6937 bytes | Method: github-raw

## [2026-04-26] ingest | cli-usage
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/cli-usage/cli-usage.md | 10544 bytes | Method: github-raw

## [2026-04-26] ingest | settings
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/settings/settings.md | 18698 bytes | Method: github-raw

## [2026-04-26] ingest | memory
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/memory/memory.md | 7604 bytes | Method: github-raw

## [2026-04-26] ingest | costs
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/costs/costs.md | 5955 bytes | Method: github-raw

## [2026-04-26] ingest | security
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/security/security.md | 9962 bytes | Method: github-raw

## [2026-04-26] ingest | sdk
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/sdk/sdk.md | 22369 bytes | Method: github-raw

## [2026-04-26] ingest | troubleshooting
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/troubleshooting/troubleshooting.md | 12217 bytes | Method: github-raw

## [2026-04-26] ingest | github-actions
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/github-actions/github-actions.md | 26124 bytes | Method: github-raw

## [2026-04-26] ingest | ide-integrations
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/ide-integrations/ide-integrations.md | 8105 bytes | Method: github-raw

## [2026-04-26] ingest | common-tasks
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/common-tasks/common-tasks.md | 6061 bytes | Method: github-raw

## [2026-04-26] ingest | tutorials
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/tutorials/tutorials.md | 32685 bytes | Method: github-raw

## [2026-04-26] ingest | team
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/team/team.md | 19777 bytes | Method: github-raw

## [2026-04-26] ingest | llm-gateway
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/llm-gateway/llm-gateway.md | 11011 bytes | Method: github-raw

## [2026-04-26] ingest | corporate-proxy
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/corporate-proxy/corporate-proxy.md | 5310 bytes | Method: github-raw

## [2026-04-26] ingest | amazon-bedrock
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/amazon-bedrock/amazon-bedrock.md | 8909 bytes | Method: github-raw

## [2026-04-26] ingest | google-vertex-ai
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/google-vertex-ai/google-vertex-ai.md | 7008 bytes | Method: github-raw

## [2026-04-26] ingest | third-party-integrations
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/third-party-integrations/third-party-integrations.md | 10247 bytes | Method: github-raw

## [2026-04-26] ingest | monitoring-usage
- Source: https://raw.githubusercontent.com/btcjon/claude-code-docs/main/monitoring-usage/monitoring-usage.md | 22026 bytes | Method: github-raw
