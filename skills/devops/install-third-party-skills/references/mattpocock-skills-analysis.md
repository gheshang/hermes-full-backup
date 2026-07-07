# mattpocock/skills 案例分析

## 仓库概览

- **来源**: https://github.com/mattpocock/skills
- **规模**: ~40+ 个已发布 SKILL.md
- **分类**: `engineering/` (~20个), `productivity/` (~5个), `misc/` (~5个), `in-progress/`, `deprecated/`

## 技能清单

### engineering/ (核心)

| 技能 | 用途 | 优先级 |
|------|------|--------|
| `diagnose` | 诊断问题/错误 | ⭐⭐⭐ 必装 |
| `tdd` | 测试驱动开发 | ⭐⭐⭐ 必装 |
| `review` | 代码审查 | ⭐⭐⭐ 必装 |
| `grill-with-docs` | 基于文档质询 | ⭐⭐ 按需 |
| `zoom-out` | 全局审视 | ⭐⭐ 按需 |
| `improve-codebase-architecture` | 架构重构 | ⭐⭐ 按需 |
| `to-prd` | 转PRD | ⭐ 按需 |
| `to-issues` | 转Issue | ⭐ 按需 |
| `triage` | Issue分诊 | ⭐ 按需 |
| `prototype` | 原型设计 | ⭐ 按需 |
| `qa` | 质量保障 | ⭐ 按需 |
| `request-refactor-plan` | 重构计划 | ⭐ 按需 |
| `ubiquitous-language` | 通用语言建模 | ⭐ 按需 |
| `write-a-prd` | 写PRD | ⭐ 按需 |
| `prd-to-plan` | PRD转计划 | ⭐ 按需 |
| `prd-to-issues` | PRD转Issue | ⭐ 按需 |
| `design-an-interface` | 界面设计 | ⭐ 按需 |

### productivity/

| 技能 | 用途 |
|------|------|
| `grill-me` | 被质询 |
| `caveman` | 极简模式 |
| `handoff` | 任务交接 |

### misc/

| 技能 | 用途 |
|------|------|
| `git-guardrails` | Git防护 |
| `scaffold-exercises` | 练习脚手架 |
| `write-a-skill` | 写技能 |
| `migrate-to-shoehorn` | 迁移工具 |
| `setup-pre-commit` | pre-commit配置 |

## 功能重叠警告

以下技能功能相近但触发条件不同，容易让Agent困惑：

| 重叠组 | 技能 |
|--------|------|
| PRD相关 | `to-prd`, `write-a-prd`, `prd-to-plan`, `prd-to-issues` |
| Issue相关 | `to-issues`, `triage` |
| 架构相关 | `zoom-out`, `improve-codebase-architecture`, `request-refactor-plan` |

**建议**: 每组只选1个，根据实际工作流决定。

## 安装建议

### 最小可行安装 (3个)
```bash
cp /tmp/mp-skills/skills/engineering/diagnose/SKILL.md ~/.hermes/skills/engineering/diagnose.md
cp /tmp/mp-skills/skills/engineering/tdd/SKILL.md ~/.hermes/skills/engineering/tdd.md
cp /tmp/mp-skills/skills/engineering/review/SKILL.md ~/.hermes/skills/engineering/review.md
```

### 按需扩展
根据项目阶段动态添加，不要一次性全装。

## 关键教训

1. **技能是工具，不是收藏品** — 每个技能安装前问自己：我最近一周有没有用过类似功能？
2. **Agent不会自动推荐技能** — 只会更混乱。你决定何时调用哪个技能
3. **定期审计** — 超过3个月未调用的技能直接删除