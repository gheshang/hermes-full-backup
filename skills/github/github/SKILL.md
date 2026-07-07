---
name: github
description: Complete GitHub workflow — authentication, pull requests, issues, code review, repository management, and CI/CD. Works with gh CLI or falls back to git + GitHub REST API via curl.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Authentication, Pull-Requests, Issues, Code-Review, Repositories, CI/CD, Git, gh-cli, Automation]
    related_skills: []
---

# GitHub — Complete Workflow

This umbrella skill consolidates all GitHub-related operations into one comprehensive guide. It covers authentication setup, pull request lifecycle, issue management, code review workflows, and repository administration.

**Choose your section based on the task:**

- [Authentication Setup](#1-authentication-setup) — Set up GitHub access via `gh` CLI or git + SSH
- [Pull Request Workflow](#2-pull-request-workflow) — Create branches, commit, open PRs, monitor CI, merge
- [Code Review](#3-code-review) — Review local changes and PRs with structured feedback
- [Issues Management](#4-issues-management) — Create, triage, label, assign, and close issues
- [Repository Management](#5-repository-management) — Clone, create, fork, configure repos, manage secrets, releases, workflows

---

## 1. Authentication Setup

### Detection Flow

```bash
# Check what's available
git --version
gh --version 2>/dev/null || echo "gh not installed"

# Check if already authenticated
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**Decision tree:**
1. If `gh auth status` shows authenticated → use `gh` for everything
2. If `gh` is installed but not authenticated → use "gh auth" method
3. If `gh` is not installed → use "git-only" method (no sudo needed)

### Method 1: Git-Only Authentication (No gh, No sudo)

#### Option A: HTTPS with Personal Access Token (Recommended)

**Step 1: Create a personal access token**

Go to: **https://github.com/settings/tokens**

- Click "Generate new token (classic)"
- Name: "hermes-agent"
- Scopes: `repo`, `workflow`, `read:org` (if needed)
- Expiration: 90 days

**Step 2: Configure git to store the token**

```bash
git config --global credential.helper store
git ls-remote https://github.com/<username>/<repo>.git
# Enter username and PAT when prompted
```

**Step 3: Configure git identity**

```bash
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

#### Option B: SSH Key Authentication

```bash
# Check for existing keys
ls -la ~/.ssh/id_*.pub 2>/dev/null || echo "No SSH keys found"

# Generate ed25519 key
ssh-keygen -t ed25519 -C "your-email@example.com" -f ~/.ssh/id_ed25519 -N ""

# Display public key
cat ~/.ssh/id_ed25519.pub
```

Add the public key at: **https://github.com/settings/keys**

```bash
# Configure git to use SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

### Method 2: gh CLI Authentication

```bash
# Interactive browser login
gh auth login

# Token-based login (headless)
echo "<TOKEN>" | gh auth login --with-token
gh auth setup-git

# Verify
gh auth status
```

### Using GitHub API Without gh

```bash
export GITHUB_TOKEN="<your-token>"

curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### Auth Detection Helper

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH_METHOD="gh"
elif [ -n "$GITHUB_TOKEN" ]; then
  AUTH_METHOD="curl"
else
  AUTH_METHOD="none"
fi
```

---

## 2. Pull Request Workflow

### Prerequisites

- Authenticated with GitHub (see Section 1)
- Inside a git repository

### Branch Creation

```bash
git fetch origin
git checkout main && git pull origin main
git checkout -b feat/your-feature-name
```

Branch naming conventions:
- `feat/description` — new features
- `fix/description` — bug fixes
- `refactor/description` — code restructuring
- `docs/description` — documentation
- `ci/description` — CI/CD changes

### Making Commits

```bash
git add src/file.py
git commit -m "feat(scope): brief description

- Detailed explanation
- More details"
```

Conventional Commits format:
```
type(scope): short description

Longer explanation if needed. Wrap at 72 characters.
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `ci`, `chore`, `perf`

### Pushing and Creating PR

```bash
git push -u origin HEAD
```

**With gh:**
```bash
gh pr create \
  --title "feat: add user authentication" \
  --body "## Summary
- Adds login and register endpoints

Closes #42" \
  --label "enhancement"
```

**With curl:**
```bash
BRANCH=$(git branch --show-current)
OWNER_REPO=$(echo "$(git remote get-url origin)" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  https://api.github.com/repos/$OWNER/$REPO/pulls \
  -d "{\"title\":\"feat: add authentication\",\"head\":\"$BRANCH\",\"base\":\"main\"}"
```

### Monitoring CI Status

**With gh:**
```bash
gh pr checks
gh pr checks --watch  # poll until complete
```

**With curl:**
```bash
SHA=$(git rev-parse HEAD)
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/commits/$SHA/status
```

### Auto-Fix CI Failures

```bash
# Get failed job logs
gh run list --branch $(git branch --show-current) --limit 5
gh run view <RUN_ID> --log-failed

# Fix and push
git add <fixed_files>
git commit -m "fix: resolve CI failure"
git push

# Re-check
gh pr checks
```

### Merging

**With gh:**
```bash
gh pr merge --squash --delete-branch
gh pr merge --auto --squash --delete-branch  # auto-merge when green
```

**With curl:**
```bash
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/merge \
  -d "{\"merge_method\":\"squash\",\"commit_title\":\"feat: description (#$PR_NUMBER)\"}"
```

---

## 3. Code Review

### Reviewing Local Changes (Pre-Push)

```bash
# Get diff summary
git diff main...HEAD --stat

# Full diff
git diff main...HEAD

# Check for common issues
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|debugger"
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*="
git diff main...HEAD | grep -n "<<<<<<\|>>>>>>\|======="
```

### Review Output Format

```
## Code Review Summary

### Critical
- **src/auth.py:45** — SQL injection vulnerability. Use parameterized queries.

### Warnings
- **src/models.py:23** — Plaintext password storage. Hash with bcrypt.

### Suggestions
- **src/utils.py:8** — Duplicated logic. Consider extracting to helper.

### Looks Good
- Clean API design
- Good error handling
```

### Reviewing a PR on GitHub

**With gh:**
```bash
gh pr view 123
gh pr diff 123
gh pr diff 123 --name-only
```

**Check out PR locally:**
```bash
gh pr checkout 123
# or: git fetch origin pull/123/head:pr-123 && git checkout pr-123
```

### Leaving Comments

**General comment:**
```bash
gh pr comment 123 --body "Overall looks good."
```

**Inline comment:**
```bash
HEAD_SHA=$(gh pr view 123 --json headRefOid --jq '.headRefOid')
gh api repos/$OWNER/$REPO/pulls/123/comments \
  --method POST \
  -f body="This could be simplified." \
  -f path="src/auth.py" \
  -f commit_id="$HEAD_SHA" \
  -f line=45 \
  -f side="RIGHT"
```

### Submitting a Formal Review

```bash
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "See inline comments."
gh pr review 123 --comment --body "Some suggestions."
```

### Review Checklist

- **Correctness**: Does the code do what it claims? Edge cases handled?
- **Security**: No hardcoded secrets? Input validation? SQL injection/XSS?
- **Code Quality**: Clear naming? No unnecessary complexity? DRY?
- **Testing**: New paths tested? Happy path and error cases?
- **Performance**: No N+1 queries? Appropriate caching?
- **Documentation**: Public APIs documented? Comments explain "why"?

---

## 4. Issues Management

### Viewing Issues

**With gh:**
```bash
gh issue list
gh issue list --state open --label "bug"
gh issue view 42
gh issue list --search "authentication error"
```

**With curl:**
```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&per_page=20"
```

### Creating Issues

**With gh:**
```bash
gh issue create \
  --title "Login redirect ignores ?next= parameter" \
  --body "## Description
After logging in, users always land on /dashboard." \
  --label "bug,backend" \
  --assignee "username"
```

**With curl:**
```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues \
  -d '{"title":"Login redirect bug","body":"## Description...","labels":["bug"],"assignees":["username"]}'
```

### Managing Issues

**Add/Remove labels:**
```bash
gh issue edit 42 --add-label "priority:high,bug"
gh issue edit 42 --remove-label "needs-triage"
```

**Assign:**
```bash
gh issue edit 42 --add-assignee username
gh issue edit 42 --add-assignee @me
```

**Comment:**
```bash
gh issue comment 42 --body "Investigated — working on a fix."
```

**Close/Reopen:**
```bash
gh issue close 42
gh issue close 42 --reason "not planned"
gh issue reopen 42
```

### Issue Triage Workflow

1. List untriaged issues: `gh issue list --label "needs-triage" --state open`
2. Read and categorize each issue
3. Apply labels and priority
4. Assign if owner is clear
5. Comment with triage notes

### Bulk Operations

```bash
# Close all issues with a specific label
gh issue list --label "wontfix" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --reason "not planned"
```

### Linking Issues to PRs

Use keywords in PR body:
```
Closes #42
Fixes #42
Resolves #42
```

---

## 5. Repository Management

### Cloning Repositories

```bash
git clone https://github.com/owner/repo-name.git
git clone https://github.com/owner/repo-name.git ./my-dir
git clone --depth 1 https://github.com/owner/repo-name.git
git clone --branch develop https://github.com/owner/repo-name.git
```

**With gh:**
```bash
gh repo clone owner/repo-name
gh repo clone owner/repo-name -- --depth 1
```

### Creating Repositories

**With gh:**
```bash
gh repo create my-new-project --public --clone
gh repo create my-new-project --private --description "A tool" --license MIT --clone
gh repo create my-org/my-new-project --public --clone
```

**With curl:**
```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{"name":"my-new-project","description":"A tool","private":false,"auto_init":true,"license_template":"mit"}'
```

### Forking Repositories

**With gh:**
```bash
gh repo fork owner/repo-name --clone
```

**With curl:**
```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/owner/repo-name/forks
sleep 3
git clone https://github.com/$GH_USER/repo-name.git
```

**Keep fork in sync:**
```bash
git remote add upstream https://github.com/owner/repo-name.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

### Repository Information

**With gh:**
```bash
gh repo view owner/repo-name
gh repo list --limit 20
gh search repos "machine learning" --language python --sort stars
```

### Repository Settings

**With gh:**
```bash
gh repo edit --description "Updated" --visibility public
gh repo edit --enable-wiki=false --enable-issues=true
gh repo edit --default-branch main
```

**With curl:**
```bash
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO \
  -d '{"description":"Updated","has_wiki":false}'
```

### Branch Protection

```bash
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/branches/main/protection \
  -d '{"required_status_checks":{"strict":true,"contexts":["ci/test"]},"enforce_admins":false,"required_pull_request_reviews":{"required_approving_review_count":1}}'
```

### Secrets Management

**With gh:**
```bash
gh secret set API_KEY --body "your-secret-value"
gh secret set SSH_KEY < ~/.ssh/id_rsa
gh secret list
gh secret delete API_KEY
```

**With curl** (requires encryption with repo's public key):
```bash
# Get public key
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/secrets/public-key

# Set encrypted secret (requires PyNaCl)
python3 -c "
from base64 import b64encode
from nacl import encoding, public
# Encrypt and output
"
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/secrets/API_KEY \
  -d '<encrypted_value>'
```

### Releases

**With gh:**
```bash
gh release create v1.0.0 --title "v1.0.0" --generate-notes
gh release create v2.0.0-rc1 --draft --prerelease
gh release list
gh release download v1.0.0 --dir ./downloads
```

**With curl:**
```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/releases \
  -d '{"tag_name":"v1.0.0","name":"v1.0.0","body":"## Changelog","draft":false,"prerelease":false}'
```

### GitHub Actions Workflows

**With gh:**
```bash
gh workflow list
gh run list --limit 10
gh run view <RUN_ID>
gh run view <RUN_ID> --log-failed
gh run rerun <RUN_ID>
gh workflow run ci.yml --ref main
```

**With curl:**
```bash
# List workflows
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/workflows

# List runs
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/actions/runs?per_page=10"

# Rerun failed run
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/runs/$RUN_ID/rerun

# Trigger workflow manually
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/actions/workflows/$WORKFLOW_ID/dispatches \
  -d '{"ref":"main","inputs":{"environment":"staging"}}'
```

### Gists

**With gh:**
```bash
gh gist create script.py --public --desc "Useful script"
gh gist list
```

**With curl:**
```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/gists \
  -d '{"description":"Useful script","public":true,"files":{"script.py":{"content":"print(\"hello\")"}}}'
```

---

## Quick Reference Table

| Action | gh | curl endpoint |
|--------|-----|--------------|
| Auth status | `gh auth status` | — |
| List PRs | `gh pr list` | `GET /repos/{o}/{r}/pulls` |
| Create PR | `gh pr create` | `POST /repos/{o}/{r}/pulls` |
| View PR | `gh pr view N` | `GET /repos/{o}/{r}/pulls/N` |
| Merge PR | `gh pr merge` | `PUT /repos/{o}/{r}/pulls/N/merge` |
| List issues | `gh issue list` | `GET /repos/{o}/{r}/issues` |
| Create issue | `gh issue create` | `POST /repos/{o}/{r}/issues` |
| Close issue | `gh issue close` | `PATCH /repos/{o}/{r}/issues/N` |
| View repo | `gh repo view` | `GET /repos/{o}/{r}` |
| Create repo | `gh repo create` | `POST /user/repos` |
| List secrets | `gh secret list` | `GET /repos/{o}/{r}/actions/secrets` |
| List workflows | `gh workflow list` | `GET /repos/{o}/{r}/actions/workflows` |
| Rerun CI | `gh run rerun ID` | `POST /repos/{o}/{r}/actions/runs/ID/rerun` |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `git push` asks for password | Use PAT as password, or switch to SSH |
| `remote: Permission denied` | Token lacks `repo` scope — regenerate |
| `fatal: Authentication failed` | Clear cached credentials: `git credential reject` |
| `ssh: connect to host github.com port 22: Connection refused` | Use SSH over HTTPS: `Host github.com Port 443` in `~/.ssh/config` |
| `gh: command not found` | Use git-only method — no installation needed |
| CI check runs not showing | Use `gh pr checks` or check `/commits/{SHA}/check-runs` |