# Corporate proxy configuration - Anthropic

**URL:** https://docs.anthropic.com/en/docs/claude-code/corporate-proxy  
**Category:** corporate-proxy  
**Scraped:** 2025-06-09 06:37:37

---

## Original Content

This page covers how to configure Claude Code to work with corporate proxy servers, including environment variable configuration, authentication, and SSL/TLS certificate handling.

## 

​

Overview

Claude Code supports standard HTTP/HTTPS proxy configurations through environment variables. This allows you to route all Claude Code traffic through your organization’s proxy servers for security, compliance, and monitoring purposes.

## 

​

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

Claude Code does not support SOCKS proxies.

## 

​

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

Ensure that you set the correct certificate bundle path:
    
    export SSL_CERT_FILE=/path/to/certificate-bundle.crt
    export NODE_EXTRA_CA_CERTS=/path/to/certificate-bundle.crt
    
## 

​

Additional resources

  * [Claude Code settings](/en/docs/claude-code/settings)
  * [Environment variables reference](/en/docs/claude-code/settings#environment-variables)
  * [Troubleshooting guide](/en/docs/claude-code/troubleshooting)

Was this page helpful?

YesNo

[Google Vertex AI](/en/docs/claude-code/google-vertex-ai)[LLM gateway](/en/docs/claude-code/llm-gateway)


---

## AI Analysis

```markdown
## Analysis of Claude Code Corporate Proxy Configuration

### 1. Concise Summary

This documentation outlines how to configure Claude Code to operate behind corporate proxy servers. It primarily focuses on using standard environment variables (`HTTPS_PROXY`, `HTTP_PROXY`) for basic proxy routing and addresses authentication methods like basic authentication. The guide also provides solutions for common SSL/TLS certificate issues encountered with custom proxy certificates.

### 2. Key Topics Covered

*   **Proxy Configuration:** Setting up Claude Code to use HTTP/HTTPS proxies.
*   **Environment Variables:** Utilizing standard environment variables for proxy settings.
*   **Authentication:** Handling basic authentication for proxies.
*   **SSL/TLS Certificates:** Resolving certificate errors with custom proxy certificates.
*   **Limitations:** Specific unsupported features (e.g., `NO_PROXY`, SOCKS proxies, advanced authentication).

### 3. Important Technical Details

*   Claude Code supports standard HTTP/HTTPS proxy configurations via environment variables.
*   It respects `HTTPS_PROXY` (recommended) and `HTTP_PROXY`.
*   The `NO_PROXY` environment variable is *not* supported; all traffic will be routed through the configured proxy.
*   SOCKS proxies are *not* supported.
*   Basic authentication credentials can be embedded directly in the proxy URL (e.g., `http://username:password@proxy.example.com:8080`).
*   For advanced authentication (NTLM, Kerberos), an LLM Gateway service is recommended as Claude Code does not directly support them.
*   SSL certificate issues with custom proxy certificates can be resolved by setting `SSL_CERT_FILE` and `NODE_EXTRA_CA_CERTS` environment variables to the path of the certificate bundle.

### 4. Code Examples

```bash
# HTTPS proxy (recommended)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP proxy (if HTTPS not available)
export HTTP_PROXY=http://proxy.example.com:8080

# Basic authentication with credentials in URL
export HTTPS_PROXY=http://username:password@proxy.example.com:8080

# Setting custom SSL certificate bundle path
export SSL_CERT_FILE=/path/to/certificate-bundle.crt
export NODE_EXTRA_CA_CERTS=/path/to/certificate-bundle.crt
```

### 5. Related Concepts or Prerequisites

*   **Environment Variables:** Basic understanding of how to set and use environment variables in a shell or operating system.
*   **HTTP/HTTPS Proxies:** Familiarity with the concept of proxy servers and their role in network communication.
*   **Basic Authentication:** Knowledge of how basic authentication works for web services.
*   **SSL/TLS Certificates:** Understanding of SSL/TLS, certificate authorities, and certificate bundles.
*   **LLM Gateway:** Awareness that for complex proxy authentication scenarios, an intermediary LLM Gateway service might be necessary.
*   **Security Best Practices:** Awareness of not hardcoding sensitive credentials directly in scripts.
```
