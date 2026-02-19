# 智谱 GLM 4.7 Flash 集成实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 创建 ZhipuClient 类和测试脚本，测试 GLM 4.7 Flash 对公众号文章的摘要效果。

**Architecture:** 新建 ZhipuClient 类模仿 GeminiClient 的接口，通过独立测试脚本验证摘要效果，不修改现有代码。

**Tech Stack:** Python 3.x, requests, OpenAI-compatible API

---

## Task 1: 创建 ZhipuClient 类

**Files:**
- Create: `src/summarizers/zhipu_client.py`

**Step 1: 创建 ZhipuClient 类文件**

创建文件 `src/summarizers/zhipu_client.py`，包含：

```python
# Zhipu AI Client Wrapper
# OpenAI-compatible API client for GLM models
import os
import time
import requests
from typing import Optional


class ZhipuClient:
    """Zhipu AI API client with OpenAI-compatible interface."""

    API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    def __init__(
        self,
        model: str = "glm-4-flash",
        api_key: str = None,
    ):
        """
        Initialize Zhipu client.

        Args:
            model: Model name (default: glm-4-flash)
            api_key: API key for authentication (reads from ZHIPU_API_KEY env var if not provided)
        """
        self.model = model
        self.api_key = api_key or os.environ.get("ZHIPU_API_KEY")

        if not self.api_key:
            raise ValueError(
                "Zhipu API key is required. "
                "Set ZHIPU_API_KEY environment variable or pass api_key parameter."
            )

    def generate_content(
        self,
        prompt: str,
        max_retries: int = 3,
        initial_delay: float = 2.0,
        backoff: float = 2.0,
        temperature: float = 0.7,
    ) -> "ZhipuResponse":
        """
        Generate content from text prompt with retry logic.

        Args:
            prompt: Text prompt
            max_retries: Maximum retry attempts (default: 3)
            initial_delay: Initial delay in seconds before first retry (default: 2.0)
            backoff: Exponential backoff multiplier (default: 2.0)
            temperature: Sampling temperature (default: 0.7)

        Returns:
            ZhipuResponse object with .text attribute
        """
        current_delay = initial_delay
        last_exception = None

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "temperature": temperature,
        }

        for attempt in range(max_retries + 1):
            try:
                response = requests.post(
                    self.API_URL,
                    json=payload,
                    headers=headers,
                    timeout=60,
                )

                if response.status_code == 200:
                    data = response.json()
                    return ZhipuResponse(data)

                # Handle retryable status codes
                if response.status_code in [429, 500, 502, 503, 504]:
                    raise requests.HTTPError(f"HTTP {response.status_code}: {response.text}")

                # Non-retryable error
                raise requests.HTTPError(f"HTTP {response.status_code}: {response.text}")

            except Exception as e:
                last_exception = e
                error_str = str(e)

                # Check if error is retryable
                is_retryable = self._is_retryable_error(error_str)

                if not is_retryable or attempt >= max_retries:
                    if attempt >= max_retries and is_retryable:
                        print(f"      ⚠️ LLM请求失败，达到最大重试次数 ({max_retries})")
                    raise

                print(f"      ⚠️ LLM请求失败，{current_delay:.1f}秒后重试 ({attempt + 1}/{max_retries}): {error_str[:60]}...")
                time.sleep(current_delay)
                current_delay *= backoff

        raise last_exception

    def _is_retryable_error(self, error_str: str) -> bool:
        """Check if an error is retryable."""
        retryable_keywords = [
            "429",
            "500",
            "502",
            "503",
            "504",
            "Resource has been exhausted",
            "RESOURCE_EXHAUSTED",
            "quota",
            "rate limit",
            "ConnectionError",
            "Timeout",
            "network",
        ]

        error_str_lower = error_str.lower()
        for keyword in retryable_keywords:
            if keyword.lower() in error_str_lower:
                return True

        return False


class ZhipuResponse:
    """Response wrapper that mimics Gemini's response interface."""

    def __init__(self, data: dict):
        """
        Initialize response from API data.

        Args:
            data: Raw API response dictionary
        """
        self._data = data
        self._text = None

    @property
    def text(self) -> str:
        """Get the generated text content."""
        if self._text is None:
            try:
                self._text = self._data["choices"][0]["message"]["content"]
            except (KeyError, IndexError) as e:
                raise ValueError(f"Invalid API response format: {e}")
        return self._text
```

**Step 2: 验证文件创建成功**

Run: `ls -la src/summarizers/zhipu_client.py`
Expected: File exists with correct permissions

**Step 3: Commit**

```bash
git add src/summarizers/zhipu_client.py
git commit -m "feat: add ZhipuClient for GLM 4.7 Flash integration

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 2: 创建测试脚本

**Files:**
- Create: `scripts/test_zhipu_summarizer.py`

**Step 1: 创建测试脚本**

创建文件 `scripts/test_zhipu_summarizer.py`，包含：

```python
#!/usr/bin/env python3
"""
Test script for Zhipu GLM 4.7 Flash article summarization.

Usage:
    python scripts/test_zhipu_summarizer.py

This script reads yesterday's WeChat articles and summarizes them
using the ZhipuClient to test GLM 4.7 Flash's performance.
"""
import sys
import os
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.summarizers.zhipu_client import ZhipuClient
from src.summarizers.article_summarizer import ArticleSummarizer


def get_test_articles():
    """Get test articles from yesterday's daily report."""
    # Use yesterday's backup report
    report_path = PROJECT_ROOT / "output" / "2026-02-18-backup" / "daily_report.md"

    if not report_path.exists():
        print(f"❌ 找不到测试文件: {report_path}")
        return []

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Parse articles from the report
    articles = []
    sections = content.split("---")

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split("\n")
        if not lines:
            continue

        # Find title line (starts with ###)
        title_line = None
        for line in lines:
            if line.startswith("### "):
                title_line = line[4:].strip()
                break

        if not title_line:
            continue

        # Extract metadata
        source = ""
        url = ""
        for line in lines:
            if line.startswith("**来源**:"):
                source = line.replace("**来源**:", "").strip()
            elif line.startswith("**链接**:"):
                url = line.replace("**链接**:", "").strip()

        # Get summary content (skip metadata lines)
        summary_start = False
        summary_lines = []
        for line in lines:
            if line.startswith("> "):
                summary_start = True
            if summary_start:
                summary_lines.append(line)

        summary_content = "\n".join(summary_lines)

        articles.append({
            "title": title_line,
            "source": source,
            "url": url,
            "content": summary_content,
        })

    return articles


def main():
    """Main test function."""
    print("=" * 60)
    print("🧪 Zhipu GLM 4.7 Flash 文章摘要测试")
    print("=" * 60)

    # Initialize Zhipu client
    print("\n📦 初始化 ZhipuClient...")
    try:
        client = ZhipuClient(model="glm-4-flash")
        print("✅ ZhipuClient 初始化成功")
    except ValueError as e:
        print(f"❌ 初始化失败: {e}")
        print("💡 请设置 ZHIPU_API_KEY 环境变量")
        return

    # Get test articles
    print("\n📄 加载测试文章...")
    articles = get_test_articles()

    if not articles:
        print("❌ 没有找到测试文章")
        return

    print(f"✅ 找到 {len(articles)} 篇文章")

    # Test with first article only for quick validation
    print("\n" + "=" * 60)
    print("📝 测试第一篇文章摘要...")
    print("=" * 60)

    test_article = articles[0]
    print(f"\n文章标题: {test_article['title']}")
    print(f"来源: {test_article['source']}")

    # Create summarizer with Zhipu client
    summarizer = ArticleSummarizer(client)

    print("\n🤖 正在生成摘要...")

    try:
        result = summarizer.summarize(
            content=test_article["content"],
            metadata={
                "title": test_article["title"],
                "account": test_article["source"],
                "url": test_article["url"],
            }
        )

        print("\n" + "=" * 60)
        print("✅ 摘要生成成功")
        print("=" * 60)

        print(f"\n标题: {result.get('title', 'N/A')}")
        print(f"标签: {result.get('tags', [])}")
        print(f"评分: {'🌟' * result.get('score', 0)}")
        print(f"广告: {'是' if result.get('is_ad') else '否'}")
        print(f"\n摘要:\n{result.get('summary', 'N/A')}")

        # Save result
        output_dir = PROJECT_ROOT / "test_output" / "2026-02-18-zhipu"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "summary_result.json"

        import json
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n💾 结果已保存到: {output_file}")

    except Exception as e:
        print(f"\n❌ 摘要生成失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
```

**Step 2: 创建 scripts 目录（如果不存在）**

Run: `mkdir -p scripts`
Expected: Directory created or already exists

**Step 3: 验证测试脚本创建成功**

Run: `ls -la scripts/test_zhipu_summarizer.py`
Expected: File exists with correct permissions

**Step 4: Commit**

```bash
git add scripts/test_zhipu_summarizer.py
git commit -m "feat: add test script for Zhipu GLM summarization

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

---

## Task 3: 配置 API Key 并运行测试

**Step 1: 设置 API Key 环境变量**

从 `zhipu.py` 中提取 API key 并设置为环境变量：

```bash
export ZHIPU_API_KEY="b4b828f419a3459ba59851305f60e6ae.y6xZA73SMAQp9cln"
```

**Step 2: 运行测试脚本**

Run: `python scripts/test_zhipu_summarizer.py`
Expected: Script runs successfully and generates summary

**Step 3: 检查输出结果**

Run: `cat test_output/2026-02-18-zhipu/summary_result.json`
Expected: JSON file with summary result

---

## Task 4: 对比测试（可选）

如果需要与 Gemini 结果对比：

**Step 1: 查看原始 Gemini 结果**

Run: `head -100 output/2026-02-18-backup/daily_report.md`
Expected: Original summary with Gemini formatting

**Step 2: 对比两个版本的差异**

手动对比 Zhipu 输出和 Gemini 输出的：
- 标题质量
- 摘要完整性
- 评分合理性
- 格式规范度

---

## 验收标准

- [ ] ZhipuClient 类创建完成，接口与 GeminiClient 兼容
- [ ] 测试脚本可以成功调用 GLM 4.7 Flash API
- [ ] 生成的摘要格式正确（JSON 格式）
- [ ] 不影响现有生产代码
