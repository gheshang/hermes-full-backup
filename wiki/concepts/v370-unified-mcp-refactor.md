---
title: v3.7.0 统一 MCP 管理重构计划
created: 2026-04-26
updated: 2026-04-26
type: concept
tags: ["concept"]
sources: [raw/articles/v370-unified-mcp-refactor.md]
---

# v3.7.0 统一 MCP 管理重构计划

源文档：[v3.7.0 统一 MCP 管理重构计划](https://raw.githubusercontent.com/SaladDay/cc-switch-cli/main/docs/v3.7.0-unified-mcp-refactor.md)

# v3.7.0 统一 MCP 管理重构计划

## 📋 项目概述

**目标**：将原有的按应用分离的 MCP 管理（Claude/Codex/Gemini 各自独立管理）重构为统一管理面板，每个 MCP 服务器通过多选框控制应用到哪些客户端。

**版本**：v3.6.2 → v3.7.0

**开始时间**：2025-11-14

---...

## 🎯 核心需求

### 原有架构（v3.6.x）

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Claude面板  │  │ Codex面板   │  │ Gemini面板  │
│ MCP管理     │  │ MCP管理     │  │ MCP管理     │
└─────────────┘  └─────────────┘  └─────────────┘
      ↓                ↓                ↓
   mcp.claude     mcp.codex       mcp.gemini
   {servers}      {servers}       {servers}
```

### 新架构（v3.7.0）

```
┌───────────────────────────────────────┐
│        统一 MCP 管理面板              │
│  ┌────────┬────────┬────────┬────┐   │
│  │ 服务器 │ Claude │ Codex  │Gem │   │
│  ├────────┼────────┼────────┼────┤   │
│  │ mcp-1  │   ✓    │   ✓    │    ...

## 📐 技术架构

### 数据结构设计

#### 新增：McpApps（应用启用状态）

```rust
#[derive(Debug, Clone, Serialize, Deserialize, Default, PartialEq)]
pub struct McpApps {
    pub claude: bool,
    pub codex: bool,
    pub gemini: bool,
}
```

#### 更新：McpServer（统一服务器定义）

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct McpServer {
    pub id: String,
    pub name: String,
    pub server: serde_json::Value,  // 连接配置（stdio/http）
    pub apps: McpApps,               // 新增：标记应用到哪些客户端
    pub description: Option<String>,
    pub homepage: Option<String>,
    pub docs: Option<String>,
    pub tags: Vec<String>,
}
```

...

## ✅ 开发进度

### Phase 1: 后端数据结构与迁移 ✅ 已完成

#### 1.1 修改数据结构（app_config.rs）✅

**文件**：`src-tauri/src/app_config.rs`

**变更**：
- ✅ 新增 `McpApps` 结构体（lines 30-62）
- ✅ 新增 `McpServer` 结构体（lines 64-79）
- ✅ 更新 `McpRoot` 支持新旧结构（lines 81-96）
- ✅ 添加辅助方法：`is_enabled_for`, `set_enabled_for`, `enabled_apps`

**提交**：`c7b235b` - "feat(mcp): implement unified MCP management for v3.7.0"

#### 1.2 实现迁移逻辑 ✅

**文件**：`src-tauri/src/app_config.rs`

**实现**：
- ✅ `migrate_mcp_to_unified()` 方法（lines 380-509）
  - 从旧结构收集所有服务器
  - 按 id 合并重复服务器
  - 处理冲突（合并 apps 字段）
  - 清空旧结构
- ✅ 集成到 `MultiAppConfig::load()` 方法（lines 252-257）
  - 自动检测并执行迁移
...

## 🔄 迁移流程

### 用户体验

```
1. 用户升级到 v3.7.0
   ↓
2. 首次启动应用
   ↓
3. 后端自动执行迁移
   - 检测旧结构 (mcp.claude/codex/gemini.servers)
   - 合并到统一结构 (mcp.servers)
   - 保存迁移后的配置
   - 日志记录迁移详情
   ↓
4. 前端加载新面板
   - 显示所有服务器
   - 三个复选框显示各应用启用状态
   ↓
5. 用户无缝使用
```

### 数据完整性保证

1. **迁移前验证**：
   - ✅ 校验旧结构合法性
   - ✅ 记录迁移前状态

2. **迁移中处理**：
   - ✅ 合并同 id 服务器的 apps 字段
   - ✅ 处理 id 冲突（保留第一个，记录警告）
   - ✅ 保留所有元信息（描述、标签、链接）

3. **迁移后清理**：
   - ✅ 清空旧结构（claude/codex/gemini）
   - ✅ 自动保存新配置
   - ✅ 日志记录迁移完成

4. **回滚机制**：
   - 配置文件有备份（`config.v1.backup.<timestamp>.json`）
   - 迁移失败时可手动回滚

---...

## 🧪 测试计划

### 后端测试 ✅ 已验证

- [x] 编译测试（cargo check）
- [x] 数据结构序列化/反序列化
- [ ] 迁移逻辑单元测试
- [ ] 服务层方法测试
- [ ] 同步函数测试

### 前端测试 ⏳ 待进行

- [ ] TypeScript 类型检查
- [ ] API 调用测试
- [ ] 组件渲染测试
- [ ] 用户交互测试
- [ ] 国际化文本检查

### 集成测试 ⏳ 待进行

- [ ] 完整迁移流程测试
  - [ ] 从空配置启动
  - [ ] 从 v3.6.x 配置升级
  - [ ] 多服务器合并场景
  - [ ] 冲突处理验证
- [ ] 多应用同步测试
  - [ ] 启用单个应用
  - [ ] 启用多个应用
  - [ ] 动态切换应用
  - [ ] 同步到 live 配置验证
- [ ] 边界情况测试
  - [ ] 空服务器列表
  - [ ] 超长服务器名称
  - [ ] 特殊字符处理
  - [ ] 并发操作

---...

## 📦 交付清单

### 代码文件

#### 后端（Rust）✅ 已完成

- [x] `src-tauri/src/app_config.rs` - 数据结构定义与迁移
- [x] `src-tauri/src/services/mcp.rs` - 服务层重构
- [x] `src-tauri/src/mcp.rs` - 同步函数实现
- [x] `src-tauri/src/commands/mcp.rs` - Tauri 命令
- [x] `src-tauri/src/lib.rs` - 命令注册
- [x] `src-tauri/src/claude_mcp.rs` - Claude MCP 操作
- [x] `src-tauri/src/gemini_mcp.rs` - Gemini MCP 操作

#### 前端（TypeScript/React）⚠️ 部分完成

- [x] `src/types.ts` - 类型定义更新
- [x] `src/lib/api/mcp.ts` - API 层更新
- [ ] `src/hooks/useMcp.ts` - React Query Hooks
- [ ] `src/components/mcp/UnifiedMcpPanel.tsx` - 统一面板组件
- [ ] `src/components/mcp/McpServerTable.ts...

## 🎯 下一步行动

### 立即任务（优先级 P0）

1. ⬜ **实现 useMcp Hook**
   - 文件：`src/hooks/useMcp.ts`
   - 估时：1-2 小时
   - 依赖：API 层（已完成）

2. ⬜ **创建 UnifiedMcpPanel 核心组件**
   - 文件：`src/components/mcp/UnifiedMcpPanel.tsx`
   - 估时：3-4 小时
   - 依赖：useMcp Hook

3. ⬜ **添加国际化文本**
   - 文件：`src/locales/{zh,en}/translation.json`
   - 估时：30 分钟

4. ⬜ **集成到主界面**
   - 文件：`src/App.tsx`
   - 估时：30 分钟
   - 依赖：UnifiedMcpPanel 组件

### 次要任务（优先级 P1）

5. ⬜ **实现子组件**
   - McpServerTable
   - McpServerFormModal
   - McpImportDialog
   - 估时：4-6 小时

6. ⬜ **编写测试用例**
   - 后端单元测试
   - 前端组件测试
   - 集成测试
   - 估时：6-8 小时

7. ⬜ **编写用户文档**
   - 升级指南
   - API 变...

## 💡 技术亮点

### 1. 平滑迁移机制

- ✅ 自动检测旧配置并迁移
- ✅ 新旧结构并存（过渡期）
- ✅ 无需用户手动操作
- ✅ 保留所有历史数据

### 2. 向后兼容

- ✅ 旧命令继续可用（带废弃警告）
- ✅ 前端可增量更新
- ✅ 渐进式重构策略

### 3. 类型安全

- ✅ Rust 强类型保证数据完整性
- ✅ TypeScript 类型定义与后端一致
- ✅ serde 序列化/反序列化自动处理

### 4. 清晰的架构分层

```
Frontend (React)
    ↓ (Tauri IPC)
Commands Layer
    ↓
Services Layer
    ↓
Data Layer (Config + Live Sync)
```

### 5. SSOT 原则

- 单一配置源：`~/.cc-switch/config.json`
- 统一管理：`mcp.servers` 字段
- 按需同步：写入各应用 live 配置

---...

## 📚 参考资源

### 内部文档

- [项目 README](../README.md)
- [CLAUDE.md](../CLAUDE.md) - Claude Code 工作指南
- [架构文档](../CLAUDE.md#架构概述)

### 相关 Issues/PRs

- 无（新功能开发）

### 技术栈文档

- [Tauri 2.0](https://tauri.app/v1/guides/)
- [React 18](https://react.dev/)
- [TanStack Query](https://tanstack.com/query/latest)
- [shadcn/ui](https://ui.shadcn.com/)
- [serde](https://serde.rs/)

---...

## 📝 变更日志

### 2025-11-14

- ✅ 完成后端 Phase 1 & 2（数据结构、服务层、命令层）
- ✅ 修复所有编译错误
- ✅ 完成前端类型定义和 API 层
- ✅ 创建本重构计划文档

### 待更新...

---...

## 👥 团队协作

**开发者**：Claude Code (AI Assistant) + User

**审查者**：User

**测试者**：User

---...

## ⚠️ 风险与对策

### 风险 1：迁移数据丢失

**概率**：低
**影响**：高
**对策**：
- ✅ 迁移前自动备份配置
- ✅ 详细日志记录
- ✅ 测试各种边界情况

### 风险 2：性能问题（大量服务器）

**概率**：中
**影响**：中
**对策**：
- ⬜ 实现虚拟滚动
- ⬜ 分页或懒加载
- ⬜ 性能测试

### 风险 3：兼容性问题

**概率**：中
**影响**：中
**对策**：
- ✅ 保留旧命令兼容层
- ✅ 前端增量更新
- ⬜ 多版本测试

### 风险 4：用户学习成本

**概率**：低
**影响**：低
**对策**：
- ⬜ 清晰的 UI 设计
- ⬜ 详细的升级指南
- ⬜ 操作提示和引导

---...

## 🎉 预期收益

### 用户体验提升

- ⭐ **简化操作**：不再需要在不同应用面板切换
- ⭐ **统一视图**：一目了然看到所有 MCP 配置
- ⭐ **灵活配置**：轻松控制每个 MCP 应用到哪些客户端

### 代码质量提升

- ⭐ **架构优化**：统一数据源，消除冗余
- ⭐ **维护性**：单一面板组件，代码更简洁
- ⭐ **扩展性**：未来添加新应用（如 Cursor）更容易

### 性能提升

- ⭐ **减少重复加载**：统一管理减少配置文件读写
- ⭐ **更快同步**：批量操作更高效

---...

## 📞 联系方式

**问题反馈**：[GitHub Issues](https://github.com/jasonyoungyang/cc-switch/issues)

**功能建议**：[GitHub Discussions](https://github.com/jasonyoungyang/cc-switch/discussions)

---

**文档版本**：v1.0
**最后更新**：2025-11-14
**状态**：🟡 开发中（后端完成 ✅，前端进行中 ⚠️）...

## 关联

- [[hermes-optional-skills-catalog]]
- [[hermes-v0.11.0]]
- [[hermes-bundled-skills-catalog]]
- [[hermes-agent]]
- [[messaging-telegram]]
