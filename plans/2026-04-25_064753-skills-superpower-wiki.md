# 每日自审 Skill v3 优化计划

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 将 daily-self-audit 从 v2（被动巡检+人工确认）升级到 v3（自愈+可观测+深浅分离），解决当前核心痛点：cron空输出无感知、Memory容量逼近极限无自动压缩、skill生态退化无检测。

**Architecture:** 三层不变，但每层增加"自愈"能力——Layer 1 从"清理"扩展为"清理+修复"，Layer 2 从"只报"扩展为"报+自动处理低风险项"，新增 Layer 1.5 自愈层处理 cron 健康检查。深度审从 skill 内的一个模式拆为独立 cron job，与每日浅审解耦。

**Tech Stack:** Hermes cronjob tool, shell hooks, bash scripts, skill_manage, memory tool

---

## 当前问题诊断

| 问题 | 根因 | 影响 |
|------|------|------|
| cron 空输出 → error 但无人知 | 无执行前健康检查、无失败告警 | 今早就是案例，3天没报告用户才发现 |
| Memory 93% (2054/2200) 逼近上限 | v2 只报不压，每次人工确认太慢 | 再加几条就溢出，关键信息丢失 |
| Skill 退化无检测 | v2 不做深度审，只检查文件存在性 | 过时的 skill（如旧cron prompt依赖）在暗处腐烂 |
| 层间无衔接 | Layer 1 清完缓存就完了，不和 Layer 2 联动 | 缓存清理释放的空间不反馈到容量告警 |
| 深度审和浅审绑定 | "深度自审"只是 skill 内一个 if 分支 | 执行时机不确定，用户忘记就永远不深审 |
| Hindsight 记忆未纳入 | 自审完全忽略 hindsight_retain/reflect | 长期记忆和短期记忆各管各的，无一致性检查 |

---

## 优化方案：6 项改进

### 改进 1：Cron 自愈（Layer 1.5 新增）

**来源：** DEV Community "Cron Jobs That Fix Themselves" + Reddit r/hermesagent self-healing heartbeat 讨论

**做什么：** 在每日自审中增加 cron 健康检查环节——

1. 执行 `cronjob action=list`，对每个任务检查 `last_status`
2. `last_status == "error"` 的任务 → 读取最近输出日志，判断是否为"空输出"类故障
3. 空输出故障 → 自动重建 prompt（从 skill 重新加载）并更新 cron job
4. 连续 3 次 error → 在报告中 **加粗告警**，附手动修复命令
5. 检查 `next_run_at` 是否合理（不在过去、不在1年后）

**文件变更：**
- 修改: `~/.hermes/skills/devops/daily-self-audit/SKILL.md`

**验证：** 手动暂停一个 cron job 或注入 error 状态，下次自审应自动检测并报告

---

### 改进 2：Memory 自动压缩（Layer 2 → Layer 1 降级）

**来源：** MemSkill 论文 (arXiv 2602.02474) — agent 应自主学习何时压缩记忆，而非依赖人工裁决

**做什么：** 当 Memory 占用 > 80% 时，将部分"只报不压"的操作自动执行——

1. 扫描所有 memory 条目，按长度降序排列
2. 单条 > 300 字符 → 自动压缩（删冗余措辞，保留事实断言）
3. 两条含完全相同子串 > 40 字符 → 自动合并（保留更完整版本）
4. 含明确过期日期且日期已过 14 天的条目 → 自动移除
5. 其他疑似重复但表述不同的条目 → **不动，留给深度审处理**
5. 以上自动操作 **先备份到 Layer 0 快照**，然后直接执行，不等人确认
6. 压缩后在报告中列出"已自动压缩 N 条，释放 X 字符"
7. **安全阀补充：** 表述不同但疑似重复的条目一律不动——宁占位不误删，这类留给每周深度审在充足时间窗口下逐条语义判断

**安全阀：** 占用 < 80% 时仍走旧的"只报"模式；自动压缩每条节省 < 30 字符的不动（不值得冒风险）

**文件变更：**
- 修改: `~/.hermes/skills/devops/daily-self-audit/SKILL.md`

**验证：** 手动添加一条冗长的 memory 条目使容量超 80%，触发自审后应自动压缩

---

### 改进 3：Skill 健康评分（Layer 2 增强）

**来源：** Hermes wiki `features-skills.md` — Progressive Disclosure 模式；Skill 过时是 agent 退化的隐性杀手

**做什么：** 给每个 skill 计算一个简易健康分数——

| 检查项 | 分值 | 方法 |
|--------|------|------|
| SKILL.md 存在且非空 | +1 | `read_file` |
| description 与 name 不矛盾 | +1 | 字符串包含检查 |
| 引用文件存在 | +1 | `read_file` 验证 references/templates/scripts |
| metadata.tags 非空 | +0.5 | YAML 解析 |
| 最近 30 天被 skill_view 加载过 | +1 | 检查 `~/.hermes/cron/output/` 日志中是否出现 skill 名 |

总分 < 2 的 skill → 在报告中标记为 "退化风险"，建议 review 或删除

**文件变更：**
- 修改: `~/.hermes/skills/devops/daily-self-audit/SKILL.md`

**验证：** 添加一个空壳 skill，触发自审应检测到低分

---

### 改进 4：Hindsight 记忆一致性检查（Layer 2 扩展）

**来源：** 当前 MEMORY 93% 但 hindsight 长期记忆未被纳入自审范围，两套记忆系统可能冲突

**做什么：** 在 Layer 2 Memory 审计中增加——

1. 检查 Hindsight 可用性（`hindsight_recall` 测试调用），不可用 → 报告标红提醒，跳过后续 Hindsight 检查
2. Hindsight 可用时：对 MEMORY.md 中的每条关键事实，用 `hindsight_recall` 搜索是否有冲突记录
3. 如果 hindsight 中存在更新/矛盾的记录 → 标记"待同步"
4. 如果 MEMORY.md 中有过时信息但 hindsight 中有更新版 → 建议用 hindsight 版本替换
5. 不自动执行（hindsight 是长期记忆，替换需用户确认）

**文件变更：**
- 修改: `~/.hermes/skills/devops/daily-self-audit/SKILL.md`

**验证：** 在 MEMORY 中存一条已知过时的信息，在 hindsight 中存更新版，触发自审应检测到不一致

---

### 改进 5：深浅审分离（架构变更）

**来源：** Addy Osmani "Self-Improving Coding Agents" — 小任务+清晰标准比大任务+模糊目标可靠；wiki `features-cron.md` — cron skill-backed job 设计

**做什么：**

- **浅审（现有 cron）：** 凌晨 2:30，15 分钟内完成，只做 Layer 0/1/1.5/2 结构性检查
- **深审（新 cron job）：** 每周日 3:00，60 分钟窗口，做——
  - 逐一 `skill_view` 每个 skill 的完整内容，检查过时
  - `session_search` 回顾近 7 个 session，提取重复模式和该存未存
  - 外部仓库 `git pull --dry-run` 检查是否有更新
  - Hindsight 语义冲突深度分析
  - 生成一份独立的 "深度自审报告"

**新增 cron job：**
```python
cronjob(
  action="create",
  name="每周深度自审",
  skills=["daily-self-audit"],
  schedule="0 3 * * 0",  # 每周日 3:00
  prompt="## 每周深度自审\n\n你是上河一号，正在执行每周深度审核。...\n\n执行深度审模式：逐一 skill_view 检查每个skill内容，session_search 回顾近7个session...",
  deliver="origin",
  enabled_toolsets=["terminal", "file", "web"]
)
```

**文件变更：**
- 修改: `~/.hermes/skills/devops/daily-self-audit/SKILL.md`（拆分深浅模式）
- 新增: cron job "每周深度自审"

**验证：** 手动 `cronjob action=run` 深度审 job，确认输出完整

---

### 改进 6：报告可观测性增强

**来源：** wiki `features-hooks.md` — Gateway Event Hooks 可用于告警；DEV Community 自愈 cron 三层模式

**做什么：**

1. 报告增加 **趋势列**——与上次报告对比：
   - Memory 容量变化（上升/下降 X%）
   - Skill 数量变化
   - Cron 成功率变化
   - 缓存总量变化
2. 报告增加 **执行元数据**：
   - 本次耗时
   - Layer 1 自动执行了多少项操作
   - 是否触发了自愈逻辑
3. 连续 2 次 error 的 cron → 报告标题加 `🚨` 前缀（在飞书中更醒目）

**实现：** 自审结束时读取上次报告（`~/.hermes/backups/前一天/` 中的报告），计算 diff

**文件变更：**
- 修改: `~/.hermes/skills/devops/daily-self-audit/SKILL.md`

**验证：** 连续两次运行自审，第二次报告应包含趋势对比

---

## 文件变更汇总

| 文件 | 操作 | 关联改进 |
|------|------|---------|
| `~/.hermes/skills/devops/daily-self-audit/SKILL.md` | 重写（v2→v3） | 全部6项 |
| `~/.hermes/cron/jobs.json` | 新增 job | 改进5（深度审cron） |

---

## 风险与权衡

| 风险 | 缓解措施 |
|------|---------|
| Memory 自动压缩误删关键信息 | 压缩前 Layer 0 快照兜底；>80% 才触发；单条压缩<30字符的不动 |
| Skill 健康评分假阳性（低分但有用的skill） | 低分只标记不删；由用户在深度审中裁决 |
| 深度审 cron 也可能空输出 | 同改进1的自愈逻辑覆盖 |
| 报告 diff 逻辑依赖上次报告存在 | 首次运行跳过趋势列，标记"首次基线" |
| Hindsight 模块不可用（当前已报错） | 降级为跳过，不阻塞其他检查 |

---

## 开放问题

1. **Memory 压缩的"相似度 70%"阈值** → **已放弃语义相似度方案**。cron 场景下无法做 embedding，关键词重叠误判率高（"偏好grok聊天"vs"偏好glm干活"关键词重叠但语义不同，合并即丢信息）。
   
   **替代方案：纯结构化规则，零语义判断——**
   
   | 规则 | 操作 | 依据 |
   |------|------|------|
   | 单条 > 300 字符 | 自动压缩（删冗余措辞，保留事实断言） | 长度客观，不需语义 |
   | 两条含完全相同子串 > 40 字符 | 自动合并（保留更完整版本） | 完全相同=直接复制，不存在误判 |
   | 条目含明确过期日期且已过 14 天 | 自动移除 | 日期是结构化信息 |
   | 其他疑似重复但表述不同 | **不动，等深度审** | 宁可占位，不可逆删错 |
2. **深度审 60 分钟窗口**是否充分？30+ 个 skill 逐一 view 可能消耗大量 token，是否需要分批（如每次只审 10 个）？
3. **Cron 自愈是否应主动重跑失败任务**？还是只修复配置等下次自动跑？主动重跑可能产生意外副作用。
4. **Hindsight 不可用时的降级策略** → **已确定：报告标红提醒，不静默跳过。** 修复另开任务。
