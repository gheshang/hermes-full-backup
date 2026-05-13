---
name: ai-image-consistency
version: 1.0
category: creative
description: 无原生角色参考的AI图像生成器（Nano Banana、Krea、Leonardo等）如何保证多图序列的人物和风格一致性。核心方法：锚点图+img2img编辑链+锁死锚定描述+色调演进轴。
tags: [ai-image, consistency, img2img, character-reference, prompt-engineering]
triggers:
  - 用户要求生成多张同一角色/场景的AI图片
  - 用户使用的图片生成工具没有--cref或等价功能
  - 用户抱怨AI生成的系列图片角色不一致
  - 提到"角色一致性"、"人物锚点"、"img2img链"
---

# AI图片序列一致性方案

## 适用场景

图片生成工具**没有**原生character reference功能（如Midjourney的`--cref`）时，需要生成多张保持同一人物/风格一致的图片序列。

适用工具：Nano Banana、Krea、Leonardo.ai、Playground、Ideogram等。

不适用：Midjourney（有`--cref`）、DALL-E系列（有seed+编辑）、Stable Diffusion（有ControlNet/IP-Adapter）。

## 核心方法论

### 三条铁律

1. **第一张图定脸，后续全部img2img锚定，不许空手生成**
2. **一致性不是"相同"，是"沿固定路径渐变"**——保证渐变路径一致，不是每帧终点一致
3. **底层材质和锚定描述一字不改**——这是硬约束，不是风格建议

### 人物一致性：锚点图 + img2img编辑链

1. 图1纯文字生成（text-to-image），**挑出人物形象最满意的一张作为锚点图**
2. 后续图全部用img2img编辑模式，锚点图作为参考图输入
3. 编辑模式prompt结构：

```
Keep [人物锚定描述 — 一字不改] + Change [本帧变化] + Style + Constraints
```

4. **锚定描述**：从图1提取的最小不变集，包含足以识别角色的特征：
   - 体型/姿态（thin, slightly hunched）
   - 服装（olive-gray linen robe, dark trousers）
   - 发型/年龄特征（short unkempt black hair with gray at the temples）
   - 每张图prompt中锚定描述必须原样复用，不许改写

### 风格一致性：材质锁定 + 色调演进轴

**材质锁定**：全序列声明相同的底层材质关键词，不管画面内容多崩多碎：
- `visible rice paper grain`
- `hand-painted animation cel`
- 或其他项目特定的材质锚点

**色调演进轴**：如果序列有情绪/时间变化，不要求色调一致，但要求色调变化路径一致：

```
图1-3: muted blue-green → gray-white（水墨消融）
图4:   warm amber honey（突然暖）
图5:   harsh blue-white + deep black（突然冷）
图6:   ink-wash gray + white light（崩解）
图7-8: warm amber → clinical white（归白）
图9:   pure overexposed white（绝对白）
```

每张图prompt写死当前色域位置，不允许AI自由发挥。

### 操作流程模板

| 步骤 | 操作 | 参考图 | 模式 |
|------|------|--------|------|
| 1 | 生成图1，挑锚点 | 无 | text-to-image |
| 2 | 用图1做参考 | 图1 | img2img编辑 |
| 3 | 用图2做参考 | 图2 | img2img编辑 |
| ... | 依次链式锚定 | 前一张 | img2img编辑 |
| N | 无人物时用风格参考 | 前一张 | img2img编辑 |

**关键**：每张图用**前一张**做参考（链式锚定），不是全部用图1做参考。链式锚定保证渐变连贯性。

## Prompt模板

### 图1（text-to-image，定锚点）

```
[风格声明]: [主体描述], [场景描述], [材质声明], [色调声明], [构图声明], [约束负面prompt]
```

### 图2-N（img2img编辑模式）

```
Keep [锚定描述 — 一字不改]. Change [本帧变化描述]. [风格声明]. [材质声明 — 同图1]. [色调声明 — 写死当前位置]. [约束负面prompt]
```

## 陷阱

- **不要全部用图1做参考**：如果图5直接锚定图1，跳过了图2-4的渐变，会导致风格断裂。链式锚定才是正解
- **锚定描述不要太笼统**：`a man`不够，`a thin middle-aged Chinese man with short unkempt black hair gray at the temples in olive-gray linen robe slightly hunched`才是锚点
- **情绪硬切时锚定描述不能断**：图4→5虽然情绪翻转，但人物物理特征必须原样保留，只改表情/动作/光线
- **无人物帧也要锚风格**：图7-9没有人物，用前一张做参考保证材质和色调连贯
- **色调演进轴必须提前设计**：不能边生成边定色调，否则AI会"平均化"导致缺乏戏剧性

## 验证方法

生成完9张后，快速翻看检查：
1. 同一人？——脸型、发型、服装、体型是否一致
2. 同一世界？——材质、画风是否连贯
3. 渐变合理？——色调演进是否按设计轴走，没有突兀跳变
4. 每帧独立可读？——单张拿出来是否能理解画面内容（不依赖前后帧）

不通过则重生成该帧，用前一帧重新锚定。
