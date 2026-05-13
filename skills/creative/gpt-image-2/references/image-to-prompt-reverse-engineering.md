# Image-to-Prompt Reverse Engineering

## 概述

从 AI 生成的图像反推其提示词（prompt）的技术。适用于：
- 分析参考图以复用风格
- 学习优秀作品的 prompt 结构
- 调试为何某张图生成效果不符合预期

## 核心分析方法

### 1. 视觉元素拆解

| 维度 | 分析要点 |
|------|----------|
| **媒介/风格** | 水墨、油画、3D渲染、像素艺术、照片等 |
| **主体** | 人物/物体/场景的核心描述 |
| **文化/美学意象** | 敦煌飞天、赛博朋克、浮世绘等特定风格来源 |
| **姿态/构图** | S型曲线、对称、三分法、动态/静态 |
| **技法特征** | 飞白、厚涂、线稿、景深等 |
| **材质/纹理** | 宣纸、画布、金属、玻璃等 |
| **色彩方案** | 单色、互补色、渐变、点缀色 |
| **背景/氛围** | 朦胧、清晰、光影、季节感 |
| **细节元素** | 印章、签名、装饰物、文字 |
| **质量修饰词** | masterpiece, detailed, 8k 等 |

### 2. Prompt 结构模板

```
[风格声明]: [主体描述], [场景描述], [材质声明], [色调声明], [构图声明], [质量修饰词]
```

**示例（水墨飞天舞女）：**

```
Chinese ink wash painting, a graceful female dancer in traditional Hanfu,
敦煌飞天 style, dynamic dancing pose with S-curve body composition,
flowing wide sleeves and ribbons, flying white brush technique,
ink and watercolor on textured rice paper,
monochrome with pale teal accents, misty background,
serene expression, traditional hair bun with loose strands,
red seal stamp in upper left corner,
elegant, ethereal, classical Chinese aesthetics,
masterpiece, detailed brushwork, vertical composition
```

### 3. 负面 Prompt 模式

常见负面词分类：

| 类别 | 负面词 |
|------|--------|
| **风格冲突** | photorealistic, 3d, cgi, western art |
| **质量低劣** | low quality, blurry, sketch, ugly |
| **元素冲突** | western clothing, modern elements |
| **类型冲突** | anime, cartoon（当目标是写实时） |

### 4. 工具参数映射

| 工具 | 关键参数 | 说明 |
|------|----------|------|
| Midjourney | `--ar 9:16` | 竖版构图 |
| Midjourney | `--stylize 250` | 中低风格化（保留原质感） |
| Midjourney | `--v 6.0` | 模型版本 |
| SD | 模型选择 | Anything V5 + 水墨 LoRA |
| SD | Negative prompt | 风格冲突词 |

## 实践技巧

### 技巧 1：锚定关键特征词

不要试图反推完整 prompt，而是提取**足以复现风格的核心词**：
- ✅ `flying white brush technique`（飞白笔法）
- ✅ `textured rice paper`（宣纸纹理）
- ✅ `pale teal accents`（青绿点缀）

### 技巧 2：区分"生成特征"和"后期特征"

- **生成特征**：AI 直接生成的（人物姿态、色彩、构图）
- **后期特征**：PS/手绘添加的（印章、签名、特定文字）

印章、签名通常不是 AI 生成的，需要后期添加。

### 技巧 3：验证 prompt 有效性

反推后，用以下方法验证：
1. 用相同 prompt 生成新图，对比风格一致性
2. 逐步移除/添加关键词，观察变化
3. 对比不同工具的生成结果

## 常见陷阱

| 陷阱 | 避免方法 |
|------|----------|
| 过度反推 | 只提取核心风格词，不追求 100% 还原 |
| 忽略负面 prompt | 负面词对风格控制同样重要 |
| 混淆后期元素 | 印章、签名等需单独处理 |
| 忽略工具差异 | 同一 prompt 在不同工具效果不同 |

## 工作流程

```
1. 视觉分析 → 拆解各维度特征
2. 提取核心词 → 筛选最关键的风格描述
3. 构建 prompt → 按结构模板组织
4. 添加负面词 → 排除风格冲突
5. 映射参数 → 根据目标工具添加参数
6. 验证迭代 → 生成测试图，对比调整
```
