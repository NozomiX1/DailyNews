# 智谱 GLM 4.7 Flash 集成设计

## 概述

将智谱 GLM 4.7 Flash 模型集成到 DailyNews 项目中，用于测试公众号文章摘要效果。

## 背景

- 当前使用 Gemini 3 Flash 进行文章摘要
- `zhipu.py` 演示了智谱 API 的调用方式（OpenAI 兼容格式）
- 需要测试 GLM 4.7 Flash 的摘要质量

## 设计决策

1. **新建 ZhipuClient 类** - 与 GeminiClient 保持相同的接口，便于切换和测试
2. **独立测试脚本** - 不修改现有代码，方便 A/B 对比
3. **聚焦公众号文章摘要** - 本次测试仅覆盖 ArticleSummarizer 功能

## 组件设计

### 1. ZhipuClient 类

**位置**: `src/summarizers/zhipu_client.py`

**接口**:
```python
class ZhipuClient:
    def __init__(self, model: str = "glm-4-flash", api_key: str = None)
    def generate_content(self, prompt: str, max_retries: int = 3) -> str
```

**特性**:
- 使用 OpenAI 兼容 API 格式
- 端点: `https://open.bigmodel.cn/api/paas/v4/chat/completions`
- 包含重试逻辑（与 GeminiClient 类似）
- API Key 从环境变量 `ZHIPU_API_KEY` 读取

### 2. 测试脚本

**位置**: `scripts/test_zhipu_summarizer.py`

**功能**:
- 读取昨天的公众号文章数据
- 使用 ZhipuClient + ArticleSummarizer 进行摘要
- 输出结果到 `test_output/` 目录
- 打印摘要结果便于查看

### 3. 测试数据

使用 `output/2026-02-18-backup/daily_report.md` 中的文章。

## 文件变更

| 文件 | 操作 |
|------|------|
| `src/summarizers/zhipu_client.py` | 新增 |
| `scripts/test_zhipu_summarizer.py` | 新增 |
| `.env` | 可选：添加 `ZHIPU_API_KEY` |

## 不涉及

- 不修改 GeminiClient
- 不修改 config.py
- 不修改 main.py
- 不影响现有生产流程
