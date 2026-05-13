---
name: github-repo-create-push
version: 1.1
description: 通过 SSH key 在 GitHub 创建新仓库并推送本地文件
trigger: 用户要求创建 GitHub 仓库并上传/推送文件，且服务器已有 SSH key
---

# GitHub 创建仓库 + 推送文件

## 核心认知

**SSH key 只能 git push/pull，不能调 GitHub REST API 创建仓库。** 创建仓库必须通过 API，需要 Personal Access Token (PAT) 或 `gh` CLI 登录。这是最常见的坑——有 SSH key 不等于能创建仓库。

## 前置检查

```bash
# 确认 SSH 认证和用户名
ssh -T git@github.com 2>&1  # 应返回 "Hi username! ..."
ssh -T git@github.com 2>&1 | grep -oP 'Hi \K[^!]+'  # 提取用户名

# 检查 gh CLI 是否可用且已登录
gh auth status 2>&1
```

## 创建仓库的三条路（按优先级）

### 路径1: gh CLI（最简单，需 sudo 安装 + 交互式登录）

```bash
gh repo create OWNER/REPO_NAME --public --description "xxx"
```

注意：`gh auth login` 是交互式的，agent 场景下需用户手动完成或提供 token。

### 路径2: PyGithub + PAT（无需 sudo，需用户提供 token）

```python
from github import Github
g = Github("用户的PAT")  # 需要 repo 权限
user = g.get_user()
repo = user.create_repo("REPO_NAME", description="xxx", private=False)
print(repo.clone_url)
```

### 路径3: 用户手动建仓库 + SSH push（零依赖，最兜底）

让用户在 GitHub 网页上手动创建空仓库，然后本地直接 push：

```bash
mkdir -p /tmp/REPO_NAME && cd /tmp/REPO_NAME
git init && git checkout -b main
cp <files> .
git add -A && git commit -m "Initial commit"
git remote add origin git@github.com:OWNER/REPO_NAME.git
git push -u origin main
```

## 推送本地文件的标准流程

```bash
# 1. 准备目录 + 复制文件
mkdir -p /tmp/REPO_NAME && cp <files> /tmp/REPO_NAME/

# 2. 初始化 + 提交
cd /tmp/REPO_NAME
git init && git checkout -b main
git add -A && git commit -m "Initial commit"

# 3. SSH 推送
git remote add origin git@github.com:OWNER/REPO_NAME.git
git push -u origin main
```

## 坑点

1. **SSH key 不能创建仓库** — 别浪费时间尝试 curl API + SSH，GitHub API 创建仓库必须 token 认证。
2. **GitHub 不支持 git push 自动创建仓库** — GitLab 支持，GitHub 不支持，仓库必须先存在。
3. **gh auth login 是交互式的** — agent 场景无法自动完成，必须用户提供 PAT 或手动登录。
4. **sudo 不可用时** — 装 gh CLI 需要 sudo，没有就走 PyGithub 或让用户手动建仓库。
5. **GitHub API 未认证返回 401** — 直接调 `api.github.com/user/repos` 不带 token 会 401。
