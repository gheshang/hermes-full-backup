---
title: Corporate proxy configuration - Anthropic
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/corporate-proxy.md]
---

# Corporate proxy configuration - Anthropic

源文档：[Corporate proxy configuration - Anthropic](https://raw.githubusercontent.com/btcjon/claude-code-docs/main/corporate-proxy/corporate-proxy.md)

# Corporate proxy configuration - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/corporate-proxy  
**Category:** corporate-proxy  
**Scraped:** 2025-06-09 06:37:37

---

## Original Content

This page covers how to configure Claude Code to work with corporate proxy servers, including environment variable configuration, authentication, and SSL/TLS certificate handling....

## ​

Overview

Claude Code supports standard HTTP/HTTPS proxy configurations through environment variables. This allows you to route all Claude Code traffic through your organization’s proxy servers for security, compliance, and monitoring purposes....

## ​

Basic proxy configuration

### 

​

Environment variables

Claude Code respects standard proxy environment variables:
    
    # HTTPS proxy (recommended)
    export HTTPS_PROXY=https://proxy.example.com:8080
    
    # HTTP proxy (if HTTPS not available)
    export HTTP_PROXY=http://proxy.example.com:8080
    
Claude Code currently does not support the `NO_PROXY` environment variable. All traffic will be routed through the configured proxy.

Claude Code does not support SOCKS proxies....

## ​

Authentication

### 

​

Basic authentication

If your proxy requires basic authentication, include credentials in the proxy URL:
    
    export HTTPS_PROXY=http://username:password@proxy.example.com:8080
    
Avoid hardcoding passwords in scripts. Use environment variables or secure credential storage instead.

For proxies requiring advanced authentication (NTLM, Kerberos, etc.), consider using an LLM Gateway service that supports your authentication method.

### 

​

SSL certificate issues

If your proxy uses custom SSL certificates, you may encounter certificate errors.

Ensure that you se...

## ​

Additional resources

  * [Claude Code settings](/en/docs/claude-code/settings)
  * [Environment variables reference](/en/docs/claude-code/settings#environment-variables)
  * [Troubleshooting guide](/en/docs/claude-code/troubleshooting)

Was this page helpful?

YesNo

[Google Vertex AI](/en/docs/claude-code/google-vertex-ai)[LLM gateway](/en/docs/claude-code/llm-gateway)


---...

## AI Analysis

```markdown...

## Analysis of Claude Code Corporate Proxy Configuration

### 1. Concise Summary

This documentation outlines how to configure Claude Code to operate behind corporate proxy servers. It primarily focuses on using standard environment variables (`HTTPS_PROXY`, `HTTP_PROXY`) for basic proxy routing and addresses authentication methods like basic authentication. The guide also provides solutions for common SSL/TLS certificate issues encountered with custom proxy certificates.

### 2. Key Topics Covered

*   **Proxy Configuration:** Setting up Claude Code to use HTTP/HTTPS proxies.
*   **Environment Variables:** Utilizing standard environment variables fo...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
