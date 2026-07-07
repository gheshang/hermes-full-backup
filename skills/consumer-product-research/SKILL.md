---
name: consumer-product-research
category: research
description: Research and compare consumer products (electronics, audio gear, appliances) before purchase decisions. Multi-source review analysis, price comparison, and recommendation synthesis.
---

# Consumer Product Research

Research and compare consumer products (electronics, audio gear, appliances, etc.) before purchase decisions.

## Trigger Conditions

- User asks "what's the best X for Y" or "help me choose X"
- User wants product reviews, comparisons, or price hunting
- User asks for "professional reviews, not ads" or "real user feedback"
- User wants to know "which one to buy" among multiple options

## Workflow

### Step 1: Clarify Requirements (use `clarify` if needed)
Before diving into research, confirm:
- **Primary use case** — What will it actually be used for? (e.g., "K歌 at home" vs "street performance")
- **Budget range** — Hard ceiling or flexible?
- **Must-have features** — Non-negotiable vs nice-to-have
- **Deal-breakers** — What would make them walk away?
- **Where to buy** — Platform preference (淘宝/京东/拼多多/线下)

> ⚠️ Don't skip this. A ¥2000 recommendation for someone who needs a ¥200 solution wastes everyone's time.

### Step 2: Multi-Source Research
Search across these sources in order of credibility:

| Priority | Source | What to Look For |
|----------|--------|-----------------|
| 1 | Official product pages/spec sheets | Baseline specs, official claims |
| 2 | Professional review sites (B站测评, Chiphell, 什么值得买) | In-depth testing, measurements |
| 3 | Video reviews (B站, YouTube) | Real-world sound/usage demos |
| 4 | User reviews (京东评价, 淘宝追评) | Long-term reliability, common issues |
| 5 | Forum discussions (知乎, 吉他中国论坛, Reddit) | Unbiased opinions, comparisons |

> ⚠️ **Filter out ads**: Skip content that reads like marketing copy ("这款神器你一定要买", "性价比之王"). Look for reviews that mention **both pros AND cons**.

### Step 3: Extract Key Data
For each product, collect:
- **Specs** — Power, size, weight, battery, connectivity
- **Price range** — Lowest/mid/high across platforms
- **Pros** — What it does well
- **Cons** — Real weaknesses (not marketing "areas for improvement")
- **Best use case** — Where it shines
- **Worst use case** — Where it fails

### Step 4: Cross-Platform Price Comparison
Search the same product on multiple platforms:

| Platform | Typical Price | Risk Level | Notes |
|----------|-------------|------------|-------|
| 拼多多 | Lowest | ⚠️⚠️⚠️ | Fake/翻新 risk high for branded items |
| 淘宝第三方 | Low-Mid | ⚠️⚠️ | Check store rating ≥4.8, sales volume |
| 京东第三方 | Mid | ⚠️ | Better logistics, decent return policy |
| 京东自营/官方 | Mid-High | ✅ | Safest, best售后 |
| 天猫官方旗舰店 | Highest | ✅ | 100%正品, 发票齐全 |

> ⚠️ **Red flags for fakes**: Price too good to be true (e.g., 森海塞尔XS1 at ¥200), no 7-day return, store rating <4.5, no purchase records.

### Step 5: Synthesize Recommendations
Present as:
1. **Direct answer first** — "Buy X for your scenario"
2. **Why** — 2-3 bullet points tying back to their requirements
3. **Alternatives** — If budget changes or needs shift
4. **Price guide** — Where to buy at what price
5. **Pitfalls** — What to watch out for

## Pitfalls

- **Don't trust single-source reviews** — One B站UP主可能是软广。Cross-reference with at least 2 other sources.
- **Specs ≠ real performance** — 200W power rating doesn't mean better sound than 150W. Look for actual listening tests.
- **New product hype** — "Pro/Max/Plus" versions often have marginal upgrades at significant price premiums. Check if the upgrade matters for the user's use case.
- **Fake review detection**: Reviews that are all 5-star with generic praise ("很好用", "物流快") are suspicious. Look for detailed reviews with specific pros AND cons.
- **Platform price traps**: 拼多多百亿补贴 is usually safe, but regular 拼多多 listings at 30% below market price are often fake.
- **Don't over-research** — After 3-4 solid sources, you have enough. Don't fall into analysis paralysis.

## Quick Reference: Audio Equipment Research

For speakers/amps/microphones specifically:

| Parameter | Why It Matters | Good Range |
|-----------|---------------|-----------|
| Power (RMS) | Real loudness, not marketing peak | Match to room size |
| Frequency response | Bass/treble extension | 60Hz-20kHz is decent for portable |
| Battery life | Real-world usage, not lab conditions | 6h+ for portable |
| Bluetooth latency | K歌同步 | <50ms ideal, <100ms acceptable |
| Input channels | How many devices simultaneously | 2+ for K歌+music playback |
| 幻象电源 | Capacitor mic support | Needed for studio mics |

## Example Output Structure

```
## 直接结论
[One sentence recommendation]

## 为什么选它
- Point 1 tied to user's need
- Point 2 tied to user's need

## 备选方案
| 方案 | 适用场景 | 价格 |
|------|---------|------|
| ... | ... | ... |

## 价格指南
| 平台 | 价格 | 风险 |
|------|------|------|
| ... | ... | ... |

## ⚠️ 避坑
- Thing 1 to watch out for
- Thing 2 to watch out for
```