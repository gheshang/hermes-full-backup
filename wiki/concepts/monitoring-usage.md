---
title: Monitoring usage - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/monitoring-usage.md]
---

# Monitoring usage - Anthropic

源文档：[Monitoring usage - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/monitoring-usage/monitoring-usage.md)

# Monitoring usage - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/monitoring-usage  
**Category:** monitoring-usage  
**Scraped:** 2025-06-09 06:36:45

---

## Original Content

OpenTelemetry support is currently in beta and details are subject to change.

# 

​

OpenTelemetry in Claude Code

Claude Code supports OpenTelemetry (OTel) metrics and events for monitoring and observability. This document explains how to enable and configure OTel for Claude Code.

All metrics are time series data exported via OpenTelemetry’s standard metrics protocol, and events are exported via OpenTelemetry’s logs/events protocol. It is the user’s responsibility to ensure their metrics and logs backends are properly configured and that the aggregation granularity meets their monitoring re...

## ​

Quick Start

Configure OpenTelemetry using environment variables:
    
    # 1. Enable telemetry
    export CLAUDE_CODE_ENABLE_TELEMETRY=1
    
    # 2. Choose exporters (both are optional - configure only what you need)
    export OTEL_METRICS_EXPORTER=otlp       # Options: otlp, prometheus, console
    export OTEL_LOGS_EXPORTER=otlp          # Options: otlp, console
    
    # 3. Configure OTLP endpoint (for OTLP exporter)
    export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
    export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
    
    # 4. Set authentication (if required)
    export OTEL_EXP...

## ​

Administrator Configuration

Administrators can configure OpenTelemetry settings for all users through the managed settings file. This allows for centralized control of telemetry settings across an organization. See the [settings precedence](/en/docs/claude-code/settings#settings-precedence) for more information about how settings are applied.

The managed settings file is located at:

  * macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`
  * Linux: `/etc/claude-code/managed-settings.json`

Example managed settings configuration:
    
    {
      "env": {
        "CLAUDE_C...

## ​

Configuration Details

### 

​

Common Configuration Variables

Environment Variable| Description| Example Values  
---|---|---  
`CLAUDE_CODE_ENABLE_TELEMETRY`| Enables telemetry collection (required)| `1`  
`OTEL_METRICS_EXPORTER`| Metrics exporter type(s) (comma-separated)| `console`, `otlp`, `prometheus`  
`OTEL_LOGS_EXPORTER`| Logs/events exporter type(s) (comma-separated)| `console`, `otlp`  
`OTEL_EXPORTER_OTLP_PROTOCOL`| Protocol for OTLP exporter (all signals)| `grpc`, `http/json`, `http/protobuf`  
`OTEL_EXPORTER_OTLP_ENDPOINT`| OTLP collector endpoint (all signals)| `http://localhos...

## ​

Available Metrics and Events

### 

​

Metrics

Claude Code exports the following metrics:

Metric Name| Description| Unit  
---|---|---  
`claude_code.session.count`| Count of CLI sessions started| count  
`claude_code.lines_of_code.count`| Count of lines of code modified| count  
`claude_code.pull_request.count`| Number of pull requests created| count  
`claude_code.commit.count`| Number of git commits created| count  
`claude_code.cost.usage`| Cost of the Claude Code session| USD  
`claude_code.token.usage`| Number of tokens used| tokens  
`claude_code.code_edit_tool.decision`| Count of cod...

## ​

Interpreting Metrics and Events Data

The metrics exported by Claude Code provide valuable insights into usage patterns and productivity. Here are some common visualizations and analyses you can create:

### 

​

Usage Monitoring

Metric| Analysis Opportunity  
---|---  
`claude_code.token.usage`| Break down by `type` (input/output), user, team, or model  
`claude_code.session.count`| Track adoption and engagement over time  
`claude_code.lines_of_code.count`| Measure productivity by tracking code additions/removals  
`claude_code.commit.count` & `claude_code.pull_request.count`| Understand im...

## ​

Backend Considerations

Your choice of metrics and logs backends will determine the types of analyses you can perform:

### 

​

For Metrics:

  * **Time series databases (e.g., Prometheus)** : Rate calculations, aggregated metrics
  * **Columnar stores (e.g., ClickHouse)** : Complex queries, unique user analysis
  * **Full-featured observability platforms (e.g., Honeycomb, Datadog)** : Advanced querying, visualization, alerting

### 

​

For Events/Logs:

  * **Log aggregation systems (e.g., Elasticsearch, Loki)** : Full-text search, log analysis
  * **Columnar stores (e.g., ClickHouse)** : S...

## ​

Service Information

All metrics are exported with:

  * Service Name: `claude-code`
  * Service Version: Current Claude Code version
  * Meter Name: `com.anthropic.claude_code`...

## ​

Security/Privacy Considerations

  * Telemetry is opt-in and requires explicit configuration
  * Sensitive information like API keys or file contents are never included in metrics or events
  * User prompt content is redacted by default - only prompt length is recorded. To enable user prompt logging, set `OTEL_LOG_USER_PROMPTS=1`

Was this page helpful?

YesNo

[Team setup](/en/docs/claude-code/team)[Costs](/en/docs/claude-code/costs)


---...

## AI Analysis

```markdown...

## Analysis of Claude Code OpenTelemetry Monitoring Documentation

### 1. Concise Summary

This documentation details how to enable and configure OpenTelemetry (OTel) for monitoring Claude Code, allowing users to export metrics and events for observability. It covers quick-start environment variable configurations for individual users and centralized managed settings for administrators. The guide also provides a comprehensive list of available configuration variables, example setups, and the specific metrics and events exported by Claude Code.

### 2. Key Topics Covered

*   **OpenTelemetry Integration:** How Claude Code supports OTel for metrics and logs.
* ...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
