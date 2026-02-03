# PapersTask
# Task for lightweight paper summary generation (no PDF download)
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime

from .base import BaseTask


def is_weekend(date_str: str) -> bool:
    """Check if the given date is a weekend."""
    weekday = datetime.strptime(date_str, '%Y-%m-%d').weekday()
    return weekday == 5 or weekday == 6  # 5=Saturday, 6=Sunday


class PapersTask(BaseTask):
    """
    Task for lightweight paper summary generation.

    This task:
    - Fetches paper metadata from HuggingFace (NO PDF download)
    - Generates Chinese summaries from English abstracts
    - Formats and publishes a summary report

    Use PaperAnalysisTask for deep PDF analysis.
    """

    name = "papers_summary"

    def __init__(self, client=None, output_dir: Path = None, project_root: Path = None):
        """
        Initialize papers task.

        Args:
            client: GeminiClient instance
            output_dir: Output directory for generated files
            project_root: Project root directory
        """
        super().__init__(output_dir, project_root)

        from ..summarizers import GeminiClient, PaperSummarizer
        from ..fetchers import PapersFetcher
        from ..processors import MarkdownFormatter
        from ..publishers import WechatPublisher

        self.client = client or GeminiClient()
        self.fetcher = PapersFetcher(data_dir=self.project_root / "data")
        self.summarizer = PaperSummarizer(self.client)
        self.formatter = MarkdownFormatter()
        self.publisher = WechatPublisher()

    def should_skip(self, date: str) -> bool:
        """
        Skip on weekends (arXiv doesn't publish new papers on weekends).

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            True if should skip, False otherwise
        """
        return is_weekend(date)

    def fetch(self, date: str) -> List[Dict[str, Any]]:
        """
        Fetch paper metadata from HuggingFace (NO PDF download).

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            List of paper metadata dictionaries (from 1st to last Frontier Lab)
        """
        print(f"\n[1/3] 获取 HuggingFace 论文 ({date})...")
        try:
            # Fetch more papers initially to find Frontier Labs
            all_papers = self.fetcher.fetch(date, max_papers=50)

            if not all_papers:
                print(f"  ⚠️ 无数据")
                return []

            # Find last Frontier Lab paper
            last_frontier_idx = 0
            for i, p in enumerate(all_papers):
                reasons = p.get("rank_reasons", "")
                if "Super Lab" in reasons or "Frontier Lab" in reasons:
                    last_frontier_idx = i

            # Only return papers from 1st to last Frontier Lab
            papers = all_papers[:last_frontier_idx + 1]

            frontier_count = sum(1 for p in papers
                               if "Super Lab" in p.get("rank_reasons", "")
                               or "Frontier Lab" in p.get("rank_reasons", ""))

            print(f"  将处理: 第1篇 → 第{last_frontier_idx+1}篇 (共 {len(papers)} 篇)")
            print(f"  其中 Frontier Labs: {frontier_count} 篇")

            # Save raw metadata (all fetched papers)
            self.fetcher.save_raw_data(all_papers, date)
            print(f"  ✅ 获取完成: {len(papers)} 篇")
            return papers
        except Exception as e:
            print(f"  ❌ 获取失败: {e}")
            return []

    def summarize(self, items: List[Dict[str, Any]], date: str) -> List[Dict[str, Any]]:
        """
        Generate Chinese summaries from English abstracts (no PDF needed).

        Args:
            items: List of paper metadata dictionaries
            date: Date string in YYYY-MM-DD format

        Returns:
            List of papers with Chinese summaries
        """
        if not items:
            return []

        # Try to load from JSON if in-memory items are incomplete
        paper_detail = items[0].get("paper", {})
        if not paper_detail.get("summary"):
            loaded = self.fetcher.load_from_json(date)
            if loaded:
                items = loaded

        if not items:
            return []

        print(f"\n[2/3] 生成论文中文摘要...")
        import config

        summaries_dir = self.project_root / "data" / "summaries" / date / "papers"
        if config.ENABLE_CACHE:
            summaries_dir.mkdir(parents=True, exist_ok=True)

        # Use summarize_batch_from_summary (lightweight, no PDF)
        summaries = self.summarizer.summarize_batch_from_summary(
            items,
            delay=1.0,
            output_path=str(summaries_dir / "papers.json")
        )

        # Print JSON preview
        self.print_json_preview(summaries, preview_count=3)

        print(f"  ✅ 论文数据已保存 ({len(summaries)} 篇)")
        return summaries

    def format(self, items: List[Dict[str, Any]], date: str) -> str:
        """
        Format papers to Markdown summary.

        Args:
            items: List of paper dictionaries with Chinese summaries
            date: Date string in YYYY-MM-DD format

        Returns:
            Formatted Markdown content
        """
        if not items:
            return ""

        print(f"\n[3/3] 格式化论文汇总...")

        content = self.formatter.format_papers_summary(items, date)

        # Save to papers subdirectory
        papers_output_dir = self.output_dir / "papers"
        papers_output_dir.mkdir(parents=True, exist_ok=True)
        output_path = papers_output_dir / "papers_summary.md"
        self.formatter.save(content, output_path)

        return content

    def publish(self, content: str, date: str) -> Dict[str, Any]:
        """
        Publish papers summary to WeChat drafts.

        Args:
            content: Formatted Markdown content
            date: Date string in YYYY-MM-DD format

        Returns:
            Publish result with draft_id
        """
        print(f"\n📤 发布论文汇总...")
        report_path = self.output_dir / "papers" / "papers_summary.md"

        if not report_path.exists():
            return {"status": "error", "error": "Report file not found"}

        result = self.publisher.publish_papers_summary(
            str(report_path),
            target_date=date
        )
        print(f"  ✅ 草稿已创建: {result['draft_id']}")
        return result
