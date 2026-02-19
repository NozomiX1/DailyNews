# Hacker News Daily Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add Hacker News daily summarization feature to DailyNews project.

**Architecture:** Uses HN Firebase API for story/comment data, Crawl4AI for article extraction, GLM-4.7 for summarization. Follows existing BaseTask pattern (fetch → summarize → format).

**Tech Stack:** Python 3.11, Crawl4AI, Playwright, ZhipuClient (GLM-4.7), asyncio

---

## Task 1: Update Dependencies

**Files:**
- Modify: `requirements.txt`

**Step 1: Add crawl4ai dependency**

```diff
# DailyNews 项目依赖

# HTTP 请求
requests>=2.31.0

# HTML 解析
beautifulsoup4>=4.12.0
lxml>=5.0.0

# HTML 转 Markdown
markdownify>=0.11.6

# OpenAI SDK (zhipu_client 使用 OpenAI 兼容 API)
openai>=1.0.0

+# Web Crawling (for Hacker News article extraction)
+crawl4ai>=0.4.0
```

**Step 2: Commit**

```bash
git add requirements.txt
git commit -m "chore: add crawl4ai dependency for Hacker News feature"
```

---

## Task 2: Create HackerNewsPrompt

**Files:**
- Create: `prompts/hackernews.py`
- Modify: `prompts/__init__.py`

**Step 1: Create the prompt class**

```python
# prompts/hackernews.py
"""
Hacker News Summary Prompt

Prompt for summarizing HN stories with article content and comments.
"""
from .base import BasePrompt


class HackerNewsPrompt(BasePrompt):
    """Prompt for summarizing Hacker News stories with structured analysis."""

    def get_system_prompt(self) -> str:
        return """你是一位资深的技术趋势分析师和 HN 社区观察者。你的专长是从 Hacker News 的文章和讨论中提炼核心洞察。

你的任务是将文章内容和社区讨论转化为**简洁、高价值**的中文摘要。

**核心原则**：
1. **客观准确**：基于提供的内容，严禁幻觉
2. **洞察优先**：突出文章价值 + 社区热议点
3. **格式严格**：仅返回纯 JSON，无 markdown 代码块"""

    def get_user_prompt_template(self) -> str:
        return """### 故事信息
- 标题：{title}
- 分类：{category}
- 得分：{score}
- 评论数：{comment_count}
- 链接：{url}

### 文章正文
{article_content}

### 精选评论
{comments}

---

请生成 JSON 摘要（Key 必须保持不变）：
{{
  "summary": "80-120字的中文摘要：核心内容是什么 + 社区在讨论什么",
  "key_points": ["关键点1", "关键点2"],
  "community_sentiment": "正面/中性/负面/混合",
  "worth_reading": true,
  "comment_excerpt": "最能代表社区观点的评论片段（50字以内，中文翻译）"
}}

**只返回纯 JSON 字符串，不要包含 Markdown 格式标记。**"""

    def format_prompt_for_story(
        self,
        title: str,
        category: str,
        score: int,
        comment_count: int,
        url: str,
        article_content: str,
        comments: str
    ) -> str:
        """
        Format prompt for a specific HN story.

        Args:
            title: Story title
            category: Story category (story, ask_hn, show_hn, job, other)
            score: Story score/upvotes
            comment_count: Number of comments
            url: Story URL (or HN link if no external URL)
            article_content: Extracted article content (or "正文获取失败")
            comments: Formatted comments string

        Returns:
            Formatted prompt string
        """
        return self.get_user_prompt_template().format(
            title=title,
            category=category,
            score=score,
            comment_count=comment_count,
            url=url or "无外部链接",
            article_content=article_content or "（无正文内容）",
            comments=comments or "（无评论）"
        )
```

**Step 2: Update prompts/__init__.py**

```diff
 """
 DailyNews Prompts Module

 Centralized prompt management for all summarization tasks.
 """

 from .base import BasePrompt
 from .article import ArticlePrompt
 from .github import GithubPrompt
 from .paper import PaperPrompt
 from .paper_summary import PaperSummaryPrompt
 from .deduplication import DeduplicationPrompt
+from .hackernews import HackerNewsPrompt
```

**Step 3: Commit**

```bash
git add prompts/hackernews.py prompts/__init__.py
git commit -m "feat: add HackerNewsPrompt for story summarization"
```

---

## Task 3: Create HackerNewsFetcher

**Files:**
- Create: `src/fetchers/hackernews.py`
- Modify: `src/fetchers/__init__.py`

**Step 1: Create the fetcher class**

```python
# src/fetchers/hackernews.py
"""
Hacker News Fetcher

Fetches top stories and comments using HN Firebase API.
"""
import httpx
from typing import List, Dict, Any, Optional
from pathlib import Path
import asyncio

from .base import BaseFetcher


class HackerNewsFetcher(BaseFetcher):
    """
    Fetches data from Hacker News using the official Firebase API.

    API endpoints:
    - https://hacker-news.firebaseio.com/v0/topstories.json
    - https://hacker-news.firebaseio.com/v0/item/{id}.json
    """

    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    HN_URL = "https://news.ycombinator.com"

    def __init__(self, data_dir: Path = None, timeout: int = 30):
        super().__init__(data_dir)
        self.timeout = timeout

    def fetch(self, date: str) -> List[Dict[str, Any]]:
        """
        Fetch top 30 stories with comments (sync wrapper).

        Args:
            date: Date string (not used for HN, but required by base class)

        Returns:
            List of story dictionaries with comments
        """
        return asyncio.run(self.fetch_async())

    async def fetch_async(self, limit: int = 30) -> List[Dict[str, Any]]:
        """
        Async fetch top stories with comments.

        Args:
            limit: Number of stories to fetch (default 30)

        Returns:
            List of story dictionaries
        """
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Get top story IDs
            story_ids = await self._fetch_top_story_ids(client, limit)

            # Fetch all stories concurrently
            tasks = [self._fetch_story_with_comments(client, sid) for sid in story_ids]
            stories = await asyncio.gather(*tasks)

            # Filter out None results
            return [s for s in stories if s is not None]

    async def _fetch_top_story_ids(self, client: httpx.AsyncClient, limit: int) -> List[int]:
        """Fetch top story IDs."""
        response = await client.get(f"{self.BASE_URL}/topstories.json")
        response.raise_for_status()
        all_ids = response.json()
        return all_ids[:limit]

    async def _fetch_story_with_comments(
        self,
        client: httpx.AsyncClient,
        story_id: int
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch a single story with its top comments.

        Args:
            client: HTTP client
            story_id: Story ID

        Returns:
            Story dictionary with comments, or None if fetch fails
        """
        try:
            # Fetch story details
            story = await self._fetch_item(client, story_id)
            if not story:
                return None

            # Fetch top comments
            kids = story.get("kids", [])[:10]  # Top 10 comments
            comments = []
            for kid_id in kids:
                comment = await self._fetch_item(client, kid_id)
                if comment and not comment.get("deleted") and not comment.get("dead"):
                    comments.append({
                        "id": comment.get("id"),
                        "by": comment.get("by", "unknown"),
                        "text": self._clean_html(comment.get("text", "")),
                    })

            # Categorize story
            category = self._categorize_story(story)

            return {
                "id": story_id,
                "title": story.get("title", "No title"),
                "url": story.get("url", ""),
                "by": story.get("by", "unknown"),
                "score": story.get("score", 0),
                "descendants": story.get("descendants", 0),
                "category": category,
                "hn_url": f"{self.HN_URL}/item?id={story_id}",
                "comments": comments,
            }
        except Exception as e:
            print(f"  ⚠️ Failed to fetch story {story_id}: {e}")
            return None

    async def _fetch_item(self, client: httpx.AsyncClient, item_id: int) -> Optional[Dict]:
        """Fetch a single item (story or comment) by ID."""
        try:
            response = await client.get(f"{self.BASE_URL}/item/{item_id}.json")
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def _categorize_story(self, story: Dict) -> str:
        """Categorize story by title patterns."""
        title = story.get("title", "").lower()

        if title.startswith("ask hn:"):
            return "ask_hn"
        elif title.startswith("show hn:"):
            return "show_hn"
        elif story.get("url", "") == "":
            return "ask_hn"  # No URL usually means Ask HN style
        else:
            # Check for job posts
            if "hiring" in title or "is hiring" in title:
                return "job"
            return "story"

    def _clean_html(self, text: str) -> str:
        """Remove HTML tags from comment text."""
        import re
        # Basic HTML tag removal
        text = re.sub(r'<[^>]+>', '', text)
        # Decode HTML entities
        import html
        text = html.unescape(text)
        return text.strip()

    def save_raw_data(self, items: List[Dict[str, Any]], date: str) -> Path:
        """Save raw fetched data (optional, for caching)."""
        import json
        import config

        if not config.ENABLE_CACHE:
            return None

        output_path = self._get_date_path("hackernews", date, "stories.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        return output_path
```

**Step 2: Update src/fetchers/__init__.py**

```diff
 """
 DailyNews Fetchers Module

 Data fetching from various sources (WeChat, GitHub, HuggingFace, etc.).
 """

 from .base import BaseFetcher
 from .wechat import WechatFetcher
 from .github_trending import GithubTrendingFetcher
 from .papers import PapersFetcher
+from .hackernews import HackerNewsFetcher

 __all__ = [
     "BaseFetcher",
     "WechatFetcher",
     "GithubTrendingFetcher",
     "PapersFetcher",
+    "HackerNewsFetcher",
 ]
```

**Step 3: Commit**

```bash
git add src/fetchers/hackernews.py src/fetchers/__init__.py
git commit -m "feat: add HackerNewsFetcher using Firebase API"
```

---

## Task 4: Create ArticleCrawler

**Files:**
- Create: `src/fetchers/article_crawler.py`

**Step 1: Create the crawler class**

```python
# src/fetchers/article_crawler.py
"""
Article Crawler

Uses Crawl4AI to extract article content from URLs.
"""
import asyncio
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class CrawlResult:
    """Result of a single crawl operation."""
    url: str
    success: bool
    content: str = ""
    error: str = ""


class ArticleCrawler:
    """
    Async article content extractor using Crawl4AI.

    Features:
    - Concurrent crawling
    - Automatic content extraction
    - Timeout and error handling
    """

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 2,
        concurrency: int = 5
    ):
        """
        Initialize the crawler.

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            concurrency: Maximum concurrent requests
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.concurrency = concurrency

    async def crawl(self, url: str) -> CrawlResult:
        """
        Crawl a single URL and extract content.

        Args:
            url: URL to crawl

        Returns:
            CrawlResult with success status and content
        """
        if not url:
            return CrawlResult(url=url, success=False, error="No URL provided")

        try:
            from crawl4ai import AsyncWebCrawler
            from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig

            browser_config = BrowserConfig(
                headless=True,
                verbose=False,
            )
            run_config = CrawlerRunConfig(
                word_count_threshold=50,
                excluded_tags=['nav', 'footer', 'header', 'aside'],
            )

            async with AsyncWebCrawler(config=browser_config) as crawler:
                result = await crawler.arun(
                    url=url,
                    config=run_config,
                )

                if result.success:
                    # Use markdown content if available, otherwise use extracted content
                    content = result.markdown or result.extracted_content or ""
                    return CrawlResult(
                        url=url,
                        success=True,
                        content=content[:10000]  # Limit content length
                    )
                else:
                    return CrawlResult(
                        url=url,
                        success=False,
                        error=result.error_message or "Unknown error"
                    )

        except Exception as e:
            return CrawlResult(
                url=url,
                success=False,
                error=str(e)[:200]
            )

    async def crawl_batch(self, urls: List[str]) -> List[CrawlResult]:
        """
        Crawl multiple URLs concurrently with rate limiting.

        Args:
            urls: List of URLs to crawl

        Returns:
            List of CrawlResults
        """
        semaphore = asyncio.Semaphore(self.concurrency)

        async def crawl_with_limit(url: str) -> CrawlResult:
            async with semaphore:
                result = await self.crawl(url)
                await asyncio.sleep(0.5)  # Rate limiting
                return result

        tasks = [crawl_with_limit(url) for url in urls]
        results = await asyncio.gather(*tasks)
        return list(results)

    def crawl_batch_sync(self, urls: List[str]) -> List[CrawlResult]:
        """
        Synchronous wrapper for batch crawling.

        Args:
            urls: List of URLs to crawl

        Returns:
            List of CrawlResults
        """
        return asyncio.run(self.crawl_batch(urls))
```

**Step 2: Commit**

```bash
git add src/fetchers/article_crawler.py
git commit -m "feat: add ArticleCrawler using Crawl4AI"
```

---

## Task 5: Create HackerNewsSummarizer

**Files:**
- Create: `src/summarizers/hackernews_summarizer.py`
- Modify: `src/summarizers/__init__.py`

**Step 1: Create the summarizer class**

```python
# src/summarizers/hackernews_summarizer.py
"""
Hacker News Summarizer

Summarizes HN stories using LLM.
"""
import time
from typing import List, Dict, Any
from pathlib import Path

from .base import BaseSummarizer
from prompts.hackernews import HackerNewsPrompt


class HackerNewsSummarizer(BaseSummarizer):
    """Summarizer for Hacker News stories."""

    def __init__(self, client):
        """
        Initialize the summarizer.

        Args:
            client: ZhipuClient instance
        """
        super().__init__(client)
        self.prompt = HackerNewsPrompt()

    def summarize(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize a single HN story.

        Args:
            content: Not used directly, data comes from metadata
            metadata: Story data with title, comments, article_content, etc.

        Returns:
            Summary dictionary
        """
        # Format comments for prompt
        comments_text = self._format_comments(metadata.get("comments", []))

        # Format article content
        article_content = metadata.get("article_content", "（正文获取失败）")

        # Build prompt
        prompt = self.prompt.format_prompt_for_story(
            title=metadata.get("title", ""),
            category=metadata.get("category", "story"),
            score=metadata.get("score", 0),
            comment_count=metadata.get("descendants", 0),
            url=metadata.get("url") or metadata.get("hn_url", ""),
            article_content=article_content,
            comments=comments_text,
        )

        # Call LLM
        try:
            response = self.client.generate_content(prompt)
            result = self._extract_json_from_response(response.text)

            # Merge with original metadata
            return {
                **metadata,
                "summary": result.get("summary", ""),
                "key_points": result.get("key_points", []),
                "community_sentiment": result.get("community_sentiment", "未知"),
                "worth_reading": result.get("worth_reading", True),
                "comment_excerpt": result.get("comment_excerpt", ""),
            }
        except Exception as e:
            print(f"      ⚠️ Summarization failed: {e}")
            return {
                **metadata,
                "summary": "",
                "key_points": [],
                "community_sentiment": "未知",
                "worth_reading": False,
                "comment_excerpt": "",
                "error": str(e),
            }

    def summarize_batch(
        self,
        items: List[Dict],
        delay: float = 0.5,
        output_path: str = None
    ) -> List[Dict]:
        """
        Summarize multiple stories with rate limiting.

        Args:
            items: List of story dictionaries
            delay: Delay between requests (seconds)
            output_path: Optional path to save JSON results

        Returns:
            List of summarized story dictionaries
        """
        results = []
        total = len(items)

        for i, item in enumerate(items, 1):
            print(f"      [{i}/{total}] 总结: {item.get('title', 'Unknown')[:40]}...")

            result = self.summarize("", item)
            results.append(result)

            if i < total:
                time.sleep(delay)

        # Save to JSON if path provided
        if output_path:
            self.save_json(results, output_path)

        return results

    def _format_comments(self, comments: List[Dict]) -> str:
        """Format comments for the prompt."""
        if not comments:
            return "（无评论）"

        lines = []
        for i, comment in enumerate(comments[:5], 1):  # Top 5 comments
            by = comment.get("by", "anonymous")
            text = comment.get("text", "")[:300]  # Limit comment length
            lines.append(f"{i}. @{by}: {text}")

        return "\n".join(lines)
```

**Step 2: Update src/summarizers/__init__.py**

```diff
 """
 DailyNews Summarizers Module

 Content summarization using LLM (Zhipu GLM).
 """

 from .base import BaseSummarizer
 from .zhipu_client import ZhipuClient
 from .article_summarizer import ArticleSummarizer
 from .github_summarizer import GithubSummarizer
 from .paper_summarizer import PaperSummarizer
+from .hackernews_summarizer import HackerNewsSummarizer

 __all__ = [
     "BaseSummarizer",
     "ZhipuClient",
     "ArticleSummarizer",
     "GithubSummarizer",
     "PaperSummarizer",
+    "HackerNewsSummarizer",
 ]
```

**Step 3: Commit**

```bash
git add src/summarizers/hackernews_summarizer.py src/summarizers/__init__.py
git commit -m "feat: add HackerNewsSummarizer for LLM-based summarization"
```

---

## Task 6: Create HackerNewsFormatter

**Files:**
- Modify: `src/processors/formatter.py`

**Step 1: Add format_hackernews method to MarkdownFormatter**

Add this method to the `MarkdownFormatter` class in `src/processors/formatter.py`:

```python
    def format_hackernews(self, stories: List[Dict], date: str = None) -> str:
        """
        Generate Hacker News daily summary Markdown.

        Args:
            stories: List of story summary dictionaries
            date: Report date

        Returns:
            Formatted Markdown string
        """
        if not stories:
            return "# Hacker News 每日精选\n\n今日无内容。"

        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        # Group stories by category
        categories = {
            "story": {"name": "📰 News", "stories": []},
            "ask_hn": {"name": "💬 Ask HN", "stories": []},
            "show_hn": {"name": "🚀 Show HN", "stories": []},
            "job": {"name": "💼 Jobs", "stories": []},
            "other": {"name": "📌 Other", "stories": []},
        }

        for story in stories:
            cat = story.get("category", "other")
            if cat in categories:
                categories[cat]["stories"].append(story)
            else:
                categories["other"]["stories"].append(story)

        lines = [
            f"# Hacker News 每日精选 | {date}",
            "",
            f"**精选故事**: {len(stories)} 条",
            "",
            "---",
            "",
        ]

        # Output each category
        for cat_key, cat_data in categories.items():
            cat_stories = cat_data["stories"]
            if not cat_stories:
                continue

            lines.append(f"## {cat_data['name']} ({len(cat_stories)})")
            lines.append("")

            for i, story in enumerate(cat_stories, 1):
                title = story.get("title", "No title")
                score = story.get("score", 0)
                comments = story.get("descendants", 0)
                url = story.get("url") or story.get("hn_url", "")

                lines.append(f"### {i}. {title}")
                lines.append(f"> Score: {score} | Comments: {comments}")
                lines.append(f"> 链接: {url}")
                lines.append("")

                # Summary
                summary = story.get("summary", "")
                article_failed = story.get("article_content") == "（正文获取失败）" or not story.get("article_content")

                if article_failed and not summary:
                    lines.append("⚠️ *正文获取失败*")
                    lines.append("")
                elif summary:
                    lines.append(f"**摘要**: {summary}")
                    lines.append("")

                # Key points
                key_points = story.get("key_points", [])
                if key_points:
                    lines.append(f"**关键点**: {' | '.join(key_points)}")
                    lines.append("")

                # Community sentiment
                sentiment = story.get("community_sentiment", "")
                if sentiment:
                    lines.append(f"**社区观点**: {sentiment}")
                    lines.append("")

                # Comment excerpt
                comment_excerpt = story.get("comment_excerpt", "")
                if comment_excerpt:
                    lines.append("💬 *精选评论*:")
                    lines.append(f"> {comment_excerpt}")
                    lines.append("")

                lines.append("---")
                lines.append("")

        return "\n".join(lines)
```

**Step 2: Commit**

```bash
git add src/processors/formatter.py
git commit -m "feat: add format_hackernews method to MarkdownFormatter"
```

---

## Task 7: Create HackerNewsTask

**Files:**
- Create: `src/tasks/hackernews.py`
- Modify: `src/tasks/__init__.py`

**Step 1: Create the task class**

```python
# src/tasks/hackernews.py
"""
Hacker News Task

Task for fetching, summarizing, and formatting HN stories.
"""
from typing import List, Dict, Any
from pathlib import Path

from .base import BaseTask
from ..fetchers.hackernews import HackerNewsFetcher
from ..fetchers.article_crawler import ArticleCrawler
from ..summarizers.hackernews_summarizer import HackerNewsSummarizer
from ..processors.formatter import MarkdownFormatter
import config


class HackerNewsTask(BaseTask):
    """
    Task for Hacker News daily summary.

    Workflow:
    1. Fetch top 30 stories + comments via Firebase API
    2. Crawl article content via Crawl4AI
    3. Summarize with LLM
    4. Format to Markdown by category
    """

    name = "hacker_news"

    def __init__(
        self,
        client=None,
        output_dir: Path = None,
        project_root: Path = None,
        limit: int = 30
    ):
        """
        Initialize Hacker News task.

        Args:
            client: ZhipuClient instance
            output_dir: Output directory for generated files
            project_root: Project root directory
            limit: Number of stories to fetch
        """
        super().__init__(output_dir, project_root)

        from ..summarizers import ZhipuClient

        self.client = client or ZhipuClient(
            model=config.GLM_MODEL,
            api_key=config.GLM_API_KEY,
            base_url=config.GLM_BASE_URL,
            max_tokens=config.GLM_MAX_TOKENS,
            enable_thinking=config.GLM_ENABLE_THINKING,
        )
        self.limit = limit
        self.fetcher = HackerNewsFetcher()
        self.crawler = ArticleCrawler()
        self.summarizer = HackerNewsSummarizer(self.client)
        self.formatter = MarkdownFormatter()

    def fetch(self, date: str) -> List[Dict[str, Any]]:
        """
        Fetch HN stories, comments, and article content.

        Args:
            date: Date string (used for output organization)

        Returns:
            List of story dictionaries with content
        """
        print(f"\n[1/3] 爬取 Hacker News Top {self.limit}...")

        # Fetch stories with comments
        stories = self.fetcher.fetch(date)
        print(f"  ✅ 获取 {len(stories)} 条故事")

        if not stories:
            return []

        # Crawl article content for stories with URLs
        print(f"\n[1.5/3] 抓取文章正文...")
        urls_to_crawl = []
        url_to_story_idx = {}

        for idx, story in enumerate(stories):
            url = story.get("url", "")
            if url:  # Only crawl stories with external URLs
                urls_to_crawl.append(url)
                url_to_story_idx[url] = idx

        if urls_to_crawl:
            print(f"  📄 需要抓取 {len(urls_to_crawl)} 篇文章...")
            crawl_results = self.crawler.crawl_batch_sync(urls_to_crawl)

            # Attach content to stories
            success_count = 0
            for result in crawl_results:
                idx = url_to_story_idx.get(result.url)
                if idx is not None:
                    if result.success:
                        stories[idx]["article_content"] = result.content
                        success_count += 1
                    else:
                        stories[idx]["article_content"] = "（正文获取失败）"
                        stories[idx]["crawl_error"] = result.error

            print(f"  ✅ 正文抓取完成: {success_count}/{len(urls_to_crawl)} 成功")

        # Mark stories without URLs
        for story in stories:
            if "article_content" not in story:
                story["article_content"] = "（无外部链接）"

        return stories

    def summarize(self, items: List[Dict[str, Any]], date: str) -> List[Dict[str, Any]]:
        """
        Summarize stories using LLM.

        Args:
            items: List of story dictionaries
            date: Date string

        Returns:
            List of summarized story dictionaries
        """
        if not items:
            return []

        print(f"\n[2/3] 总结 Hacker News 故事...")

        summaries = self.summarizer.summarize_batch(
            items,
            delay=0.5,
        )

        # Print preview
        self.print_json_preview(summaries, preview_count=2)

        return summaries

    def format(self, items: List[Dict[str, Any]], date: str) -> str:
        """
        Format summarized stories to Markdown.

        Args:
            items: List of summarized story dictionaries
            date: Date string

        Returns:
            Formatted Markdown content
        """
        if not items:
            return ""

        print(f"\n[3/3] 格式化 Hacker News 报告...")
        content = self.formatter.format_hackernews(items, date)

        # Save to file
        output_path = self.output_dir / "hacker_news.md"
        self.formatter.save(content, output_path)

        return content
```

**Step 2: Update src/tasks/__init__.py**

```diff
 """
 DailyNews Tasks Module

 Orchestrates the complete pipeline for different content types:
 - WeChat articles
 - GitHub Trending
 - Papers summary
 - Paper analysis
+- Hacker News
 """

 from .base import BaseTask
 from .wechat import WechatArticleTask
 from .github import GithubTrendingTask
 from .papers import PapersTask
 from .paper_analysis import PaperAnalysisTask
+from .hackernews import HackerNewsTask

 __all__ = [
     "BaseTask",
     "WechatArticleTask",
     "GithubTrendingTask",
     "PapersTask",
     "PaperAnalysisTask",
+    "HackerNewsTask",
 ]
```

**Step 3: Commit**

```bash
git add src/tasks/hackernews.py src/tasks/__init__.py
git commit -m "feat: add HackerNewsTask following BaseTask pattern"
```

---

## Task 8: Update main.py

**Files:**
- Modify: `main.py`

**Step 1: Add --hackernews argument and task integration**

Find the argument parser section and add the new argument:

```diff
     parser.add_argument(
         '--paper',
         action='store_true',
         help='运行 Papers 轻量汇总任务'
     )
+    parser.add_argument(
+        '--hackernews',
+        action='store_true',
+        help='运行 Hacker News 任务'
+    )
     parser.add_argument(
```

Update the imports:

```diff
-from src.tasks import WechatArticleTask, GithubTrendingTask, PapersTask
+from src.tasks import WechatArticleTask, GithubTrendingTask, PapersTask, HackerNewsTask
```

Update the run_pipeline function to include hackernews:

```diff
     print(f"   公众号: {'Y' if 'wechat' in tasks_to_run else 'N'}")
     print(f"   Trending: {'Y' if 'github' in tasks_to_run else 'N'}")
     print(f"   论文轻量汇总: {'Y' if 'paper' in tasks_to_run else 'N'}")
+    print(f"   Hacker News: {'Y' if 'hackernews' in tasks_to_run else 'N'}")
     print(f"   输出目录: output/{date}/")
```

```diff
     if 'paper' in tasks_to_run and not skip_papers:
         tasks.append(PapersTask(client=client, output_dir=output_dir))
+    if 'hackernews' in tasks_to_run:
+        tasks.append(HackerNewsTask(client=client, output_dir=output_dir))
```

Update the main function to handle hackernews argument:

```diff
         if args.paper:
             tasks_to_run.append('paper')
+        if args.hackernews:
+            tasks_to_run.append('hackernews')
```

**Step 2: Commit**

```bash
git add main.py
git commit -m "feat: add --hackernews argument to main.py"
```

---

## Task 9: Create GitHub Actions Workflow

**Files:**
- Create: `.github/workflows/hacker_news.yml`

**Step 1: Create the workflow file**

```yaml
name: Hacker News Daily

on:
  schedule:
    # UTC 0:00 = 北京时间 8:00
    - cron: '0 0 * * *'
  workflow_dispatch:

env:
  GLM_API_KEY: ${{ secrets.GLM_API_KEY }}

jobs:
  generate:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        cache: 'pip'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Cache Playwright browsers
      uses: actions/cache@v4
      id: playwright-cache
      with:
        path: ~/.cache/ms-playwright
        key: ${{ runner.os }}-playwright-${{ hashFiles('**/requirements.txt') }}
        restore-keys: |
          ${{ runner.os }}-playwright-

    - name: Install Playwright
      if: steps.playwright-cache.outputs.cache-hit != 'true'
      run: python -m playwright install chromium --with-deps

    - name: Run Hacker News task
      run: python main.py --hackernews

    - name: Commit and push changes
      run: |
        git config user.name "github-actions[bot]"
        git config user.email "github-actions[bot]@users.noreply.github.com"
        git add output/
        git diff --quiet && git diff --staged --quiet || \
          (git commit -m "chore: update hacker news $(date +%Y-%m-%d)" && \
           git pull --rebase && \
           git push)
```

**Step 2: Commit**

```bash
git add .github/workflows/hacker_news.yml
git commit -m "feat: add GitHub Actions workflow for Hacker News (UTC 0:00)"
```

---

## Task 10: Integration Test

**Step 1: Run local test**

```bash
# Test with limited stories (modify limit temporarily or run as-is)
python main.py --hackernews
```

**Step 2: Verify output**

Check that:
- `output/{date}/hacker_news.md` is created
- Stories are categorized correctly
- Summaries are generated
- Comment excerpts appear

**Step 3: Commit any fixes**

```bash
git add -A
git commit -m "fix: resolve integration test issues"
```

---

## Summary

**Files Created:**
- `prompts/hackernews.py`
- `src/fetchers/hackernews.py`
- `src/fetchers/article_crawler.py`
- `src/summarizers/hackernews_summarizer.py`
- `src/tasks/hackernews.py`
- `.github/workflows/hacker_news.yml`

**Files Modified:**
- `requirements.txt`
- `prompts/__init__.py`
- `src/fetchers/__init__.py`
- `src/summarizers/__init__.py`
- `src/tasks/__init__.py`
- `src/processors/formatter.py`
- `main.py`

**Total: 6 new files, 6 modified files**
