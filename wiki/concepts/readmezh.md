---
title: CC-Switch CLI
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/readmezh.md]
---

# CC-Switch CLI

源文档：[CC-Switch CLI](https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/README_ZH.md)

<div align="center">

# CC-Switch CLI

[![Version](https://img.shields.io/badge/version-5.3.4-blue.svg)](https://github.com/saladday/cc-switch-cli/releases)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](https://github.com/saladday/cc-switch-cli/releases)
[![Built with Rust](https://img.shields.io/badge/built%20with-Rust-orange.svg)](https://www.rust-lang.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Claude Code、Codex、Gemini、OpenCode 与 OpenClaw 的命令行管理工具**

统一管理 Claude Code、Codex、Gemini、OpenCode 与 OpenClaw 的供应商配置，并按应用提供 MCP 服务器、Skills 扩展、提示词、本地代理路由和环境检查等能力。

[English](README.md) | 中文

</div>

---

## 📖 关于本项目

本项目是原版 [CC-Switch](https://github.com/farion1231/cc-switch) 的 **CLI 分支**。🔄 WebDAV 同步功能与上游项目完全兼容。


**致谢：** 原始架构和核心功能来自 [farion1231/cc-switch](https://github.com/farion1231/cc-switch)

**更新日志：** [CHANGELOG.md](CHANGELOG.md)

---...

## ❤️赞助商

<table>
  <tr>
    <td width="180">
      <a href="https://www.packyapi.com/register?aff=cc-switch-cli">
        <img src="assets/partners/logos/packycode.png" alt="PackyCode" width="150">
      </a>
    </td>
    <td>
      感谢 <b>PackyCode</b> 赞助本项目！<br/>
      官网：<a href="https://www.packyapi.com">https://www.packyapi.com</a><br/>
      CC-Switch CLI 专属优惠：通过
      <a href="https://www.packyapi.com/register?aff=cc-switch-cli">此链接</a>
      注册，并在充值时填写优惠码 <code>cc-switch-cli</code>，即可享受 <b>9 折优惠</b>。
    </td>
  </tr>
  <tr>
    <td width="180">
      <a href="https://www.aicodemirror.com/regis...

## 📸 截图预览

<div align="center">
  <h3>首页</h3>
  <img src="assets/screenshots/home-zh.png" alt="首页" width="70%"/>
</div>

<br/>

<table>
  <tr>
    <th>切换</th>
    <th>设置</th>
  </tr>
  <tr>
    <td><img src="assets/screenshots/switch-zh.png" alt="切换" width="100%"/></td>
    <td><img src="assets/screenshots/settings-zh.png" alt="设置" width="100%"/></td>
  </tr>
</table>...

## 🚀 快速开始

**交互模式（推荐）**
```bash
cc-switch
```
🤩 按照屏幕菜单探索功能。

**命令行模式**
```bash
cc-switch provider list              # 列出供应商
cc-switch provider switch <id>       # 切换供应商
cc-switch provider export <id>       # 导出 Claude 供应商为独立 settings 文件
cc-switch provider stream-check <id> # 检查供应商流式健康
cc-switch config webdav show         # 查看 WebDAV 同步设置
cc-switch env tools                  # 检查本地 CLI 工具
cc-switch mcp sync                   # 同步 MCP 服务器
cc-switch proxy show                 # 查看代理路由和状态

# 使用全局 `--app` 参数来指定目标应用：
cc-switch --app claude provider list    # 管理 Claude 供应商
cc-switch --app codex mcp sync        ...

## 📥 安装

### 方法 1：快速安装（macOS / Linux）

> Windows 用户请参考下方手动安装。

```bash
curl -fsSL https://github.com/SaladDay/cc-switch-cli/releases/latest/download/install.sh | bash
```

默认安装到 `~/.local/bin`。设置 `CC_SWITCH_INSTALL_DIR` 可自定义安装目录。

- 如果目标文件已存在，安装脚本会在 TTY 中提示确认；在非交互环境中，只有设置 `CC_SWITCH_FORCE=1` 才会覆盖。
- Linux 如需 glibc 构建，可设置 `CC_SWITCH_LINUX_LIBC=glibc`。

<details>
<summary>手动安装</summary>

#### macOS

```bash
# 下载 Universal Binary（推荐，支持 Apple Silicon + Intel）
curl -LO https://github.com/saladday/cc-switch-cli/releases/latest/download/cc-switch-cli-darwin-universal.tar.gz

# 解压
tar -xzf cc-switch-cli-darwin...

## ✨ 功能特性

### 🔌 供应商管理

管理 **Claude Code**、**Codex**、**Gemini**、**OpenCode** 与 **OpenClaw** 的 API 配置。

**功能：** 一键切换、Claude 独立 settings 导出、多端点支持、API 密钥管理、远端模型发现，以及按应用提供的速度测试、流式健康检查等诊断能力。

```bash
cc-switch provider list              # 列出所有供应商
cc-switch provider current           # 显示当前供应商
cc-switch provider switch <id>       # 切换供应商
cc-switch provider add               # 添加新供应商
cc-switch provider edit <id>         # 编辑现有供应商
cc-switch provider duplicate <id>    # 复制供应商
cc-switch provider delete <id>       # 删除供应商
cc-switch provider export <id>       # 导出到当前目录 ./.claude/settings.local.json 并供 Claude 自动加载
cc...

## 🏗️ 架构

### 核心设计

- **SQLite 持久化**：核心数据默认存放在 `~/.cc-switch/cc-switch.db`（若设置 `CC_SWITCH_CONFIG_DIR` 则改为该目录下）；旧版 `config.json` 仅保留给兼容与迁移路径使用
- **Skills SSOT**：技能源文件默认保存在 `~/.cc-switch/skills/`（若设置 `CC_SWITCH_CONFIG_DIR` 则改为 `$CC_SWITCH_CONFIG_DIR/skills/`），安装状态和启用状态由数据库统一记录
- **安全 Live 同步（默认）**：若目标应用尚未初始化，将跳过写入 live 文件（避免意外创建 `~/.claude`、`~/.codex`、`~/.gemini`、`~/.config/opencode` 或 `~/.openclaw`）
- **原子写入**：临时文件 + 重命名模式防止损坏
- **服务层复用**：100% 复用原 GUI 版本
- **并发安全**：RwLock 配合作用域守卫

### 配置文件

**CC-Switch 存储**（默认：`~/.cc-switch`，可用 `CC_SWITCH_CONFIG_DIR` 覆盖）：
- `~/.cc-switch/cc-switch.db` - 供应商、MCP、提示词和应用状态的...

## ❓ 常见问题 (FAQ)

<details>
<summary><b>为什么切换供应商后配置没有生效？</b></summary>

<br>

首先确认目标 CLI 已经至少运行过一次（即对应配置目录已存在）。如果应用未初始化，CC-Switch 会出于安全原因跳过写入 live 文件，并提示一条 warning。请先运行一次目标 CLI（例如 `claude --help` / `codex --help` / `gemini --help` / `opencode --help` / `openclaw --help`），然后再切换一次供应商。

这通常是由**环境变量冲突**引起的。如果你在系统环境变量中设置了 API 密钥（如 `ANTHROPIC_API_KEY`、`OPENAI_API_KEY`），它们会覆盖 CC-Switch 的配置。

**解决方案：**

1. 检查冲突：
   ```bash
   cc-switch env check --app claude
   ```

2. 列出所有相关环境变量：
   ```bash
   cc-switch env list --app claude
   ```

3. 如果发现冲突，手动删除它们：
   - **macOS/Linux**：编辑 shell 配置文件（`~/.bashrc`、`~/.zshrc` 等）
     ``...

## 🛠️ 开发

### 环境要求

- **Rust**：1.85+（[rustup](https://rustup.rs/)）
- **Cargo**：与 Rust 捆绑

### 开发命令

```bash
cd src-tauri

cargo run                            # 开发模式
cargo run -- provider list           # 运行特定命令
cargo build --release                # 构建 release

cargo fmt                            # 代码格式化
cargo clippy                         # 代码检查
cargo test                           # 运行测试
```

### 代码结构

```
src-tauri/src/
├── cli/
│   ├── commands/          # CLI 子命令（provider, mcp, prompts, skills, proxy, env, ...）
│   ├── tui/               # 交互式 TUI 模式（ratatui）
│   ├── interactive/       # 交互入口 / ...

## 🤝 贡献

欢迎贡献！本分支专注于 CLI 功能。

**提交 PR 前：**
- ✅ 通过格式检查：`cargo fmt --check`
- ✅ 通过代码检查：`cargo clippy`
- ✅ 通过测试：`cargo test`
- 💡 先开 issue 讨论

---...

## 📜 许可证

- MIT © 原作者：Jason Young
- CLI 分支维护者：saladday...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
