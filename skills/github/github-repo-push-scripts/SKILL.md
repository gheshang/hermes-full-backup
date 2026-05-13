---
name: github-repo-push-scripts
description: 将服务器上的脚本文件推送至GitHub仓库的完整流程——SSH key认证 + API创建仓库 + git push。
version: 1.0.0
author: 上河一号
metadata:
  hermes:
    tags: [github, push, scripts, ssh, token]
---

# GitHub 推送脚本到仓库

## 前提条件

- 服务器有 SSH key 且已添加到 GitHub（`ssh -T git@github.com` 验证）
- SSH key 只能用于 git push/pull，**不能**用于 GitHub API 创建仓库

## 流程

### 1. 创建仓库（需 API token）

SSH key 无法调 GitHub API 创建仓库，必须有 Personal Access Token。

**Token 要求：**
- Fine-grained PAT 需要 `Administration` 写权限才能创建仓库
- Classic PAT（`ghp_` 开头）勾选 `repo` scope 即可
- 用 PyGithub 创建：`pip install PyGithub` → `Github(auth=Auth.Token(token)).get_user().create_repo(name, ...)`

**如果 token 权限不够（403）：** 让用户手动在网页创建仓库，然后用 SSH push 即可。

### 2. 克隆 + 复制文件 + 推送

```bash
cd /tmp && rm -rf <repo-name>  # 清理旧克隆（/tmp临时目录，安全）
git clone git@github.com:<user>/<repo-name>.git
cd <repo-name>
cp /path/to/scripts/* .
git config user.name "<username>"
git config user.email "<email>"
git add -A && git commit -m "feat: 描述" && git push origin main
```

**注意：** git 需要先配置 user.name/user.email，否则 commit 报错 `empty ident name`。

### 3. 下载脚本的正确方式

用户在服务器上拉取脚本时，**必须用 raw 链接**：
```bash
curl -O https://raw.githubusercontent.com/<user>/<repo>/main/<file>
```

用网页链接（`/blob/main/...`）下载到的是 HTML，bash 执行会报 `syntax error near unexpected token 'newline'` + `<!DOCTYPE html>`。

## 坑点速查

| 坑 | 表现 | 解决 |
|----|------|------|
| Fine-grained PAT 无 Administration 权限 | 403 Forbidden | 换 Classic PAT 或网页建仓库 |
| git 未配置 user.name/email | `empty ident name` fatal | `git config user.name/email` |
| 用网页链接下载脚本 | `syntax error: <!DOCTYPE html>` | 用 `raw.githubusercontent.com` 链接 |
| gh CLI 未安装 | `command not found: gh` | 用 PyGithub 替代或手动建仓库 |
