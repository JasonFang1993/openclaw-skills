---
name: ai-image-generation
description: AI图像生成指南
---

# AI图像生成

## 主流模型

| 模型 | 特点 | API |
|-----|------|-----|
| DALL-E 3 | 文字理解强 | OpenAI |
| Midjourney | 艺术感强 | Discord |
| Stable Diffusion | 本地可跑 | Stability AI |
| Imagen | Google | Google |

## 提示词结构

### 正面
```
[主体] + [场景] + [动作] + [风格] + [光线] + [色彩] + [构图]
```

### 负面
```
ugly, deformed, low quality, blurry, watermark, text
```

## 常用参数

- aspect-ratio: 16:9 / 4:3 / 1:1 / 9:16
- quality: standard / hd
- style: natural / vivid / art

## 生成技巧

1. **主体明确**：具体描述主体
2. **风格指定**：photorealistic / anime / 3D render
3. **光照描述**：soft lighting / cinematic lighting
4. **细节补充**：highly detailed, 8k

## 输出格式

支持：PNG / JPEG / WebP

## 使用场景

- 封面图
- 产品图
- 概念图
- 插画
- UI mockup
