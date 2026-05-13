# 第三方图像生成 API 提供商 quirks

本文件记录各 OpenAI 兼容图像生成 API 的特殊限制和注意事项。

---

## SenseNova (商汤大模型)

**文档**：https://platform.sensenova.cn/docs

### 基本信息

| 项目 | 值 |
|------|-----|
| Base URL | `https://token.sensenova.cn/v1` |
| 图像端点 | `POST /v1/images/generations` |
| 模型 ID | `sensenova-u1-fast` |
| 调用限制 | 每5小时1500次 |

### 支持尺寸

```
1664x2496, 2496x1664, 1760x2368, 2368x1760,
1824x2272, 2272x1824, 2048x2048,
2752x1536, 1536x2752, 3072x1376, 1344x3136
```

⚠️ **不支持** OpenAI 标准尺寸（`1024x1024`, `1024x1792` 等）。

### 关键注意事项

1. **必须使用 `response_format: "b64_json"`**
   - URL 响应签名 1 小时后过期
   - 使用 b64_json 可立即保存，无过期问题

2. **模型名固定**
   - 必须使用 `sensenova-u1-fast`
   - 不支持 `dall-e-3` 或 `gpt-image-2`

3. **Prompt 格式**
   - 完全兼容 OpenAI 格式
   - 支持多模态输入（图像理解）

### 配置示例

```yaml
# ~/.hermes/config.yaml
model:
  image:
    model: sensenova-u1-fast
    base_url: https://token.sensenova.cn/v1/images/generations
    api_key: sk-xxx

# 或使用环境变量
OPENAI_IMAGE_BASE_URL=https://token.sensenova.cn/v1/images/generations
OPENAI_IMAGE_API_KEY=sk-xxx
OPENAI_IMAGE_MODEL=sensenova-u1-fast
```

### 调用示例

```bash
curl https://token.sensenova.cn/v1/images/generations \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sensenova-u1-fast",
    "prompt": "A beautiful landscape",
    "n": 1,
    "size": "1344x3136",
    "response_format": "b64_json"
  }'
```

### 响应处理

```python
import json, base64

data = json.loads(response)
b64 = data['data'][0]['b64_json']
with open('output.png', 'wb') as f:
    f.write(base64.b64decode(b64))
```

---

## DeepSeek

**文档**：https://api-docs.deepseek.com/

### 基本信息

| 项目 | 值 |
|------|-----|
| Base URL | `https://api.deepseek.com/v1` |
| 图像端点 | `POST /v1/images/generations` |
| 模型 ID | `deepseek-image` (需查最新文档) |

### 注意事项

- 图像生成能力可能有限，需查最新文档
- 尺寸支持类似 OpenAI

---

## Moonshot (月之暗面)

**文档**：https://platform.moonshot.cn/docs/

### 基本信息

| 项目 | 值 |
|------|-----|
| Base URL | `https://api.moonshot.cn/v1` |
| 图像端点 | `POST /v1/images/generations` |
| 模型 ID | 需查文档 |

### 注意事项

- 以文档为准
- 尺寸可能有限制

---

## 通用建议

### 探测支持尺寸

```bash
# 尝试常用尺寸，记录哪些返回 400
for size in "1024x1024" "1024x1792" "1792x1024" "1344x3136" "1536x2752"; do
  echo "Testing $size..."
  curl -s https://TOKEN.sensenova.cn/v1/images/generations \
    -H "Authorization: Bearer $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"sensenova-u1-fast\",\"prompt\":\"test\",\"size\":\"$size\"}" | \
    python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if 'data' in d else d.get('error',{}).get('message',''))"
done
```

### 检查响应格式

```bash
# 测试 b64_json 是否可用
curl -s https://TOKEN.sensenova.cn/v1/images/generations \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"sensenova-u1-fast","prompt":"test","response_format":"b64_json"}' | \
  python3 -c "import sys,json; d=json.load(sys.stdin); print('Has b64_json' if 'b64_json' in d.get('data',[{}])[0] else 'No b64_json')"
```

---

## 更新日志

| 日期 | 变更 |
|------|------|
| 2026-05-07 | 新增 SenseNova U1 Fast 完整文档 |
