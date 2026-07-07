§ memory remove/replace 用 old_text 子串匹配，短条目删除可能误伤。Claude Code 模型不可用（所有别名均报错），解决：不带 --model 或用默认模型。Hindsight 已完全卸载（2026-06-23），勿再引用。
§
research-paper-writing skill SKILL.md is 102,927 chars — exceeds 100,000 char patch limit. Cannot add table-handling reference via patch. Skill needs restructuring into smaller SKILL.md + references/ files. Current gap: no automated JSON→LaTeX table converter; agents manually write tabular.
§
Wiki 更新（2026-06-23）：删除 28 页过期内容（Claude Code 文档 22 页 + CC-Switch 5 页 + ide-integrations 1 页），新增 44 页最新 Hermes 文档（12 个 feature + 11 个 messaging + 13 个 guide + 8 个 user-guide + 实体 v0.17.0）。已推送到 github.com:gheshang/hermes-wiki（3 次提交: 0be00e2, de3f389, 5ee91eb）。wiki 知识库已覆盖全部 Hermes 官方文档。
§
wiki-maintenance skill updated (2026-06-23): added subagent timeout fallback pattern (direct cp for raw articles), source-URL-based stale detection, version entity replacement procedure, and index formatting artifacts pitfall.
§
Skill created: devops/vps-python-dev-env — VPS Python dev environment + Jupyter + remote access via SSH tunnel/ngrok for mobile devices. Covers venv setup, jupyter daemon, ngrok install/config, Android tablet (Termux) access.
§
Jupyter Lab 配置：端口 18080，base_url=/lab/，仅绑 127.0.0.1，通过 nginx 反代（location /lab/ -> proxy_pass http://127.0.0.1:18080）。启动时必须加 --ServerApp.allow_remote_access=True，否则 nginx 传入的 Host 头（hangskf.xyz）被 Jupyter 当作远程访问拒绝，返回 403 Forbidden。camoufox font cache 1G+ 可以安全独立删除（rm -rf ~/.cache/camoufox/fonts/），浏览器工具照常使用。旧 Hermes session 文件可按月份批量删除。
§
~/wiki 是知识库主目录，不要误删。~/superpowers 是 skill 仓库（装载在 .agents 中），不是废弃项目。~/smart-construction-ai、~/agency-agents-zh、~/novel 也有用途，均保留。这些目录在磁盘清理时已确认为非废弃项目。