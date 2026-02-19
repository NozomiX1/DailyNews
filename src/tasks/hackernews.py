# src/tasks/hackernews.py
"""
Hacker News Task

Orchestrates HN story fetching, article crawling, and summarization.

Note: Output is organized by yesterday's date since the 8am (Beijing) crawl
captures stories from the previous day.
"""
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta

from .base import BaseTask
import config


class HackerNewsTask(BaseTask):
    """
    Task for Hacker News daily summary.

    Workflow:
    1. Fetch top stories from HN API
    2. Crawl article content with Crawl4AI
    3. Summarize with LLM
    4. Format to categorized Markdown
    """

    name = "hacker_news"

    def __init__(self, client=None, output_dir: Path = None, project_root: Path = None, limit: int = 30):
        super().__init__(output_dir, project_root)

        from ..summarizers import ZhipuClient, HackerNewsSummarizer
        from ..fetchers import HackerNewsFetcher
        from ..fetchers.article_crawler import ArticleCrawler
        from ..processors import MarkdownFormatter

        self.client = client or ZhipuClient(
            model=config.GLM_MODEL,
            api_key=config.GLM_API_KEY,
            base_url=config.GLM_BASE_URL,
            max_tokens=config.GLM_MAX_TOKENS,
            enable_thinking=config.GLM_ENABLE_THINKING,
        )
        self.fetcher = HackerNewsFetcher(data_dir=self.project_root / "data")
        self.crawler = ArticleCrawler()
        self.summarizer = HackerNewsSummarizer(self.client)
        self.formatter = MarkdownFormatter()
        self.limit = limit

    def run(self, date: str) -> Dict[str, Any]:
        """
        Execute the complete task workflow using yesterday's date.

        HN task runs at 8am Beijing time, so output is organized by
        the previous day's date (the stories being crawled).

        Args:
            date: Current date string (will be adjusted to yesterday)

        Returns:
            Result dictionary with task status
        """
        # Use yesterday's date for output
        current_date = datetime.strptime(date, '%Y-%m-%d')
        yesterday = (current_date - timedelta(days=1)).strftime('%Y-%m-%d')

        # Update output_dir to use yesterday's date
        self.output_dir = self.project_root / "output" / yesterday

        # Call parent run with yesterday's date
        return super().run(yesterday)

    def fetch(self, date: str) -> List[Dict[str, Any]]:
        """
        Fetch HN stories, comments, and article content.

        Args:
            date: Date string (YYYY-MM-DD)

        Returns:
            List of story dictionaries with content
        """
        print(f"\n[1/3] 获取 Hacker News ({date})...")

        # Fetch stories with comments
        stories = self.fetcher.fetch(date, limit=self.limit, comments_per_story=10)

        if not stories:
            return []

        # Save raw data
        self.fetcher.save_raw_data(stories, date)

        # Crawl article content for stories with URLs
        print(f"\n  📦 抓取文章正文...")
        urls_to_crawl = []
        url_to_story_id = {}

        for story in stories:
            url = story.get('url', '')
            if url:
                urls_to_crawl.append(url)
                url_to_story_id[url] = story.get('id')

        if urls_to_crawl:
            print(f"    需要抓取 {len(urls_to_crawl)} 个 URL...")
            crawl_results = self.crawler.crawl_batch(urls_to_crawl, concurrency=5)

            # Map crawl results to story IDs
            article_contents = {}
            success_count = 0
            for i, result in enumerate(crawl_results):
                url = urls_to_crawl[i]
                story_id = url_to_story_id[url]
                if result.get('success'):
                    article_contents[story_id] = result.get('content', '')
                    success_count += 1
                else:
                    article_contents[story_id] = ""
                    print(f"    ⚠️ 抓取失败: {url[:50]}... - {result.get('error', 'Unknown')}")

            print(f"    ✅ 正文抓取完成: {success_count}/{len(urls_to_crawl)} 成功")
        else:
            article_contents = {}

        # Store article contents with stories
        for story in stories:
            story['article_content'] = article_contents.get(story.get('id'), '')

        return stories

    def summarize(self, items: List[Dict[str, Any]], date: str) -> List[Dict[str, Any]]:
        """
        Summarize stories using LLM.

        Args:
            items: List of story dictionaries with article content
            date: Date string

        Returns:
            List of summarized story dictionaries
        """
        if not items:
            return []

        print(f"\n[2/3] Hacker News 故事总结...")

        # Build article contents dict
        article_contents = {}
        for story in items:
            story_id = story.get('id')
            content = story.get('article_content', '')
            if content:
                article_contents[story_id] = content

        # Summarize
        summaries = self.summarizer.summarize_batch(
            items,
            article_contents=article_contents,
            delay=0.5
        )

        self.print_json_preview(summaries, preview_count=3)

        return summaries

    def format(self, items: List[Dict[str, Any]], date: str) -> str:
        """
        Format summaries to categorized Markdown.

        Args:
            items: List of summarized story dictionaries
            date: Date string

        Returns:
            Formatted Markdown content
        """
        if not items:
            return ""

        print(f"\n[3/3] 格式化 Hacker News 报告...")

        # Group by category
        categories = {
            'story': {'emoji': '📰', 'name': 'News', 'items': []},
            'ask_hn': {'emoji': '💬', 'name': 'Ask HN', 'items': []},
            'show_hn': {'emoji': '🚀', 'name': 'Show HN', 'items': []},
            'job': {'emoji': '💼', 'name': 'Jobs', 'items': []},
            'other': {'emoji': '📌', 'name': 'Other', 'items': []},
        }

        for item in items:
            cat = item.get('category', 'other')
            if cat in categories:
                categories[cat]['items'].append(item)

        # Build markdown
        lines = [
            f"# Hacker News Top {len(items)} | {date}",
            "",
            "## 📊 今日概览",
            "",
        ]

        # Category summary
        for cat_key, cat_data in categories.items():
            count = len(cat_data['items'])
            if count > 0:
                lines.append(f"- {cat_data['emoji']} **{cat_data['name']}**: {count} 条")

        lines.extend(["", "---", ""])

        # Each category
        for cat_key, cat_data in categories.items():
            items_in_cat = cat_data['items']
            if not items_in_cat:
                continue

            # Sort by score descending
            items_in_cat.sort(key=lambda x: x.get('score', 0), reverse=True)

            lines.append(f"## {cat_data['emoji']} {cat_data['name']} ({len(items_in_cat)})")
            lines.append("")

            for i, item in enumerate(items_in_cat, 1):
                title = item.get('title', 'Unknown')
                score = item.get('score', 0)
                comments_count = item.get('descendants', 0)
                url = item.get('url', '')
                story_id = item.get('id', '')

                lines.append(f"### {i}. {title}")
                lines.append(f"> Score: {score} | Comments: {comments_count}")

                # Summary (if available)
                summary = item.get('summary', '')
                if summary:
                    lines.append(f"")
                    lines.append(f"**摘要**: {summary}")

                # Key points as bullet list
                key_points = item.get('key_points', [])
                if key_points:
                    lines.append(f"")
                    lines.append(f"**关键点**:")
                    for point in key_points[:3]:
                        lines.append(f"- {point}")

                # Community sentiment
                sentiment = item.get('community_sentiment', '')
                if sentiment:
                    lines.append(f"")
                    lines.append(f"**社区观点**: {sentiment}")

                # Links
                lines.append(f"")
                if url:
                    lines.append(f"🔗 [原文]({url})")
                if story_id:
                    hn_url = f"https://news.ycombinator.com/item?id={story_id}"
                    lines.append(f"💬 [评论区]({hn_url})")

                # Article fetch status
                if not item.get('article_fetched'):
                    lines.append(f"")
                    lines.append(f"⚠️ *正文获取失败*")

                # Comments preview
                comments = item.get('comments', [])
                if comments:
                    lines.append(f"")
                    lines.append(f"💬 *精选评论*:")
                    for comment in comments[:2]:
                        by = comment.get('by', 'unknown')
                        text = comment.get('text', '')[:100]
                        # Clean HTML
                        import re
                        text = re.sub(r'<[^>]+>', '', text)
                        lines.append(f"> \"{text}...\" — @{by}")

                lines.append("")
                lines.append("---")
                lines.append("")

        content = "\n".join(lines)

        # Save to file
        output_path = self.output_dir / "hacker_news.md"
        self.formatter.save(content, output_path)

        return content
