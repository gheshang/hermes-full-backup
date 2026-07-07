# 直接 API 调用方案（Mode D）

当 `image_generate` 工具不可用，但 `config.yaml` 中配置了 OpenAI 兼容的图像 API 时，使用此方案。

## 检测流程

```bash
# 1. 检查 hermes tools 列表
hermes tools 2>/dev/null | grep -i "image"
# 预期：无输出（表示工具不可用）

# 2. 检查 config.yaml 的 image 配置
grep -A5 "image:" ~/.hermes/config.yaml
# 预期输出：
#   image:
#     model: sensenova-u1-fast
#     base_url: https://token.sensenova.cn/v1/images/generations
#     api_key: sk-xxx...

# 3. 检查环境变量
env | grep -iE "OPENAI_IMAGE|SENSENOVA|IMAGE_API"
```

## curl 调用模板

```bash
curl -s -X POST "https://token.sensenova.cn/v1/images/generations" \
  -H "Authorization: Bearer $IMAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sensenova-u1-fast",
    "prompt": "你的提示词",
    "n": 1,
    "size": "2496x1664",
    "response_format": "b64_json"
  }'
```

## Python 调用模板

```python
import requests
import base64
import json

API_KEY = "sk-xxx..."  # 从 config.yaml 或环境变量获取
BASE_URL = "https://token.sensenova.cn/v1/images/generations"

response = requests.post(
    BASE_URL,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "sensenova-u1-fast",
        "prompt": "你的提示词",
        "n": 1,
        "size": "2496x1664",  # 必须使用支持尺寸
        "response_format": "b64_json"
    },
    timeout=120
)

data = response.json()
if "data" in data and len(data["data"]) > 0:
    b64 = data["data"][0].get("b64_json")
    if b64:
        with open("output.png", "wb") as f:
            f.write(base64.b64decode(b64))
        print("✓ 图片已保存")
    else:
        print(f"✗ 无 b64_json: {json.dumps(data, indent=2)[:300]}")
else:
    print(f"✗ 异常响应: {json.dumps(data, indent=2)[:300]}")
```

## 支持尺寸（SenseNova U1 Fast）

| 尺寸 | 用途 |
|------|------|
| `1664x2496` | 竖版海报 |
| `2496x1664` | 横版海报 |
| `1760x2368` | 竖版 |
| `2368x1760` | 横版 |
| `1824x2272` | 竖版 |
| `2272x1824` | 横版 |
| `2048x2048` | 正方形 |
| `2752x1536` | 宽屏横版 |
| `1536x2752` | 宽屏竖版 |
| `3072x1376` | 超宽横版 |
| `1344x3136` | 超宽竖版 |

> ⚠️ **重要**：不要使用 OpenAI 标准尺寸（1024x1024 等），会返回 `field Size invalid` 错误。

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `field Size invalid` | 尺寸不支持 | 使用支持尺寸列表中的尺寸 |
| `401 Unauthorized` | API Key 无效 | 检查 `config.yaml` 中的 `api_key` |
| `429 Too Many Requests` | 速率限制 | 等待后重试，或降低并发 |
| `500 Internal Server Error` | 服务端错误 | 稍后重试 |

## 批量生成

```bash
#!/bin/bash
# 批量生成多张图

PROMPTS=(
  "封面设计：科技感深色背景"
  "架构图：客户端/服务器数据流"
  "代理关系图：多代理协作"
  "工作流程图：任务执行流程"
)

SIZE="2496x1664"
OUTPUT_DIR="./images"
mkdir -p "$OUTPUT_DIR"

for i in "${!PROMPTS[@]}"; do
  echo "生成第 $((i+1)) 张..."
  
  response=$(curl -s -X POST "$BASE_URL" \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"sensenova-u1-fast\",
      \"prompt\": \"${PROMPTS[$i]}\",
      \"n\": 1,
      \"size\": \"$SIZE\",
      \"response_format\": \"b64_json\"
    }")
  
  b64=$(echo "$response" | jq -r '.data[0].b64_json')
  
  if [ "$b64" != "null" ]; then
    echo "$b64" | base64 -d > "$OUTPUT_DIR/image-$((i+1)).png"
    echo "✓ 保存: image-$((i+1)).png"
  else
    echo "✗ 生成失败: $(echo "$response" | jq -r '.error.message')"
  fi
  
  # 速率限制：等待 2 秒
  sleep 2
done
```

## 与 HTML+SVG 的对比

| 维度 | AI 生成 (PNG) | HTML+SVG |
|------|---------------|----------|
| **文字清晰度** | ⚠️ 可能模糊 | ✅ 100% 清晰 |
| **文件大小** | 2-4 MB | 5-15 KB |
| **可编辑性** | ❌ 不可编辑 | ✅ 代码可改 |
| **缩放质量** | ❌ 放大失真 | ✅ 无限缩放 |
| **视觉风格** | ✅ AI 艺术感 | ⚠️ 代码风格 |
| **加载速度** | ⚠️ 较慢 | ✅ 即时 |
| **生成成本** | 💰 API 调用费用 | 💵 零成本 |
| **生成时间** | ⏱️ 10-30 秒/张 | ⏱️ 1-2 秒/张 |

**建议**：
- 文档嵌入 → PNG 版（视觉效果好）
- 网页展示/可编辑 → HTML+SVG 版
- 演示/打印 → PNG 版
- 开发/迭代 → HTML+SVG 版
