# WechatArticleTask
# Task for fetching, summarizing, and publishing WeChat Official Account articles
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime

from .base import BaseTask


class WechatArticleTask(BaseTask):
    """
    Task for WeChat Official Account articles.

    Workflow:
    1. Fetch articles from WeChat (never skips)
    2. Summarize with LLM
    3. Deduplicate with LLM
    4. Format to Markdown
    """

    name = "wechat_articles"

    def __init__(self, client=None, output_dir: Path = None, project_root: Path = None):
        """
        Initialize WeChat article task.

        Args:
            client: GeminiClient instance
            output_dir: Output directory for generated files
            project_root: Project root directory
        """
        super().__init__(output_dir, project_root)

        from ..summarizers import GeminiClient, ArticleSummarizer
        from ..fetchers import WechatFetcher
        from ..processors import LLMDeduplicator, MarkdownFormatter

        self.client = client or GeminiClient()
        self.fetcher = WechatFetcher(data_dir=self.project_root / "data")
        self.summarizer = ArticleSummarizer(self.client)
        self.deduplicator = LLMDeduplicator(self.client)
        self.formatter = MarkdownFormatter()

    def should_skip(self, date: str) -> bool:
        """WeChat articles never skip."""
        return False

    def fetch(self, date: str) -> List[Dict[str, Any]]:
        """
        Fetch WeChat articles for the given date.

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            List of article dictionaries with content
        """
        print(f"\n[1/4] 爬取公众号文章 ({date})...")
        try:
            articles = self.fetcher.fetch(date)
            print(f"  ✅ 爬取完成: {len(articles)} 篇")
            return articles
        except Exception as e:
            print(f"  ❌ 爬取失败: {e}")
            return []

    def summarize(self, items: List[Dict[str, Any]], date: str) -> List[Dict[str, Any]]:
        """
        Summarize articles using LLM and deduplicate.

        Args:
            items: List of article dictionaries
            date: Date string in YYYY-MM-DD format

        Returns:
            List of deduplicated summarized articles
        """
        if not items:
            return []

        # Try to load from JSON if items don't have content
        if not items[0].get('content'):
            items = self.fetcher.load_from_json(date)

        if not items:
            return []

        # Summarize
        print(f"\n[2/4] 公众号文章总结...")
        import config
        summaries_dir = self.project_root / "data" / "summaries" / date
        if config.ENABLE_CACHE:
            summaries_dir.mkdir(parents=True, exist_ok=True)

        summaries = self.summarizer.summarize_batch(
            items,
            delay=1.0,
            output_path=str(summaries_dir / "articles.json")
        )

        # Deduplicate
        print(f"\n[3/4] LLM 去重...")
        before_count = len(summaries)
        cleaned = self.deduplicator.deduplicate(
            summaries,
            output_path=str(summaries_dir / "articles.json")
        )
        after_count = len(cleaned)
        print(f"  ✅ 去重完成: {before_count} → {after_count}")

        # Print JSON preview
        self.print_json_preview(cleaned, preview_count=3)

        return cleaned

    def format(self, items: List[Dict[str, Any]], date: str) -> str:
        """
        Format summarized articles to Markdown.

        Args:
            items: List of summarized article dictionaries
            date: Date string in YYYY-MM-DD format

        Returns:
            Formatted Markdown content
        """
        if not items:
            return ""

        print(f"\n[4/4] 格式化公众号日报...")
        content = self.formatter.format_articles(items, date)

        # Save to file
        output_path = self.output_dir / "daily_report.md"
        self.formatter.save(content, output_path)

        return content
