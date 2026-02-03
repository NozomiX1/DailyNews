# GithubTrendingTask
# Task for fetching, summarizing, and publishing GitHub Trending repositories
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime

from .base import BaseTask


class GithubTrendingTask(BaseTask):
    """
    Task for GitHub Trending repositories.

    Workflow:
    1. Fetch trending repos (only for current date)
    2. Download README files
    3. Summarize with LLM
    4. Format to Markdown
    5. Publish to WeChat drafts
    """

    name = "github_trending"

    def __init__(self, client=None, output_dir: Path = None, project_root: Path = None):
        """
        Initialize GitHub Trending task.

        Args:
            client: GeminiClient instance
            output_dir: Output directory for generated files
            project_root: Project root directory
        """
        super().__init__(output_dir, project_root)

        from ..summarizers import GeminiClient, GithubSummarizer
        from ..fetchers import GithubTrendingFetcher
        from ..processors import MarkdownFormatter
        from ..publishers import WechatPublisher

        self.client = client or GeminiClient()
        self.fetcher = GithubTrendingFetcher(data_dir=self.project_root / "data")
        self.summarizer = None  # Created with date in summarize()
        self.formatter = MarkdownFormatter()
        self.publisher = WechatPublisher()

    def should_skip(self, date: str) -> bool:
        """
        Skip if date is not today (GitHub Trending only works for current date).

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            True if should skip, False otherwise
        """
        today = datetime.now().strftime('%Y-%m-%d')
        return date != today

    def fetch(self, date: str) -> List[Dict[str, Any]]:
        """
        Fetch GitHub Trending repos for the given date.

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            List of repository dictionaries
        """
        print(f"\n[1/3] 爬取 GitHub Trending ({date})...")
        try:
            repos = self.fetcher.fetch(date)
            # Save raw data
            if repos:
                self.fetcher.save_raw_data(repos, date)
                # Download README files
                self.fetcher.download_readmes(repos, date=date)
            print(f"  ✅ 爬取完成: {len(repos)} 个项目")
            return repos
        except Exception as e:
            print(f"  ❌ 爬取失败: {e}")
            return []

    def summarize(self, items: List[Dict[str, Any]], date: str) -> List[Dict[str, Any]]:
        """
        Summarize repositories using LLM.

        Args:
            items: List of repository dictionaries
            date: Date string in YYYY-MM-DD format

        Returns:
            List of summarized repository dictionaries
        """
        if not items:
            return []

        print(f"\n[2/3] GitHub 项目总结...")
        from ..summarizers import GithubSummarizer
        import config

        # Create summarizer with date for README path
        self.summarizer = GithubSummarizer(self.client, date=date)

        summaries_dir = self.project_root / "data" / "summaries" / date
        if config.ENABLE_CACHE:
            summaries_dir.mkdir(parents=True, exist_ok=True)

        summaries = self.summarizer.summarize_batch(
            items,
            delay=0.5,
            output_path=str(summaries_dir / "trending.json")
        )

        # Print JSON preview
        self.print_json_preview(summaries, preview_count=3)

        return summaries

    def format(self, items: List[Dict[str, Any]], date: str) -> str:
        """
        Format summarized repositories to Markdown.

        Args:
            items: List of summarized repository dictionaries
            date: Date string in YYYY-MM-DD format

        Returns:
            Formatted Markdown content
        """
        if not items:
            return ""

        print(f"\n[3/3] 格式化 GitHub Trending 报告...")
        content = self.formatter.format_github(items, date)

        # Save to file
        output_path = self.output_dir / "github_trending.md"
        self.formatter.save(content, output_path)

        return content

    def publish(self, content: str, date: str) -> Dict[str, Any]:
        """
        Publish GitHub Trending report to WeChat drafts.

        Args:
            content: Formatted Markdown content
            date: Date string in YYYY-MM-DD format

        Returns:
            Publish result with draft_id
        """
        print(f"\n📤 发布 GitHub Trending...")
        report_path = self.output_dir / "github_trending.md"

        if not report_path.exists():
            return {"status": "error", "error": "Report file not found"}

        result = self.publisher.publish_github_trending(
            str(report_path),
            target_date=date
        )
        print(f"  ✅ 草稿已创建: {result['draft_id']}")
        return result
