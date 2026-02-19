# PaperAnalysisTask
# Task for deep paper analysis with PDF download and GLM analysis
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta as dt
import re
import requests
import time

from .base import BaseTask
from .papers import is_weekend
from prompts import PaperPrompt
import config


class PaperAnalysisTask(BaseTask):
    """
    Task for deep paper analysis with full PDF download and analysis.

    This task:
    - Fetches paper rankings from HuggingFace
    - Downloads full ArXiv PDFs
    - Analyzes each paper with GLM
    - Generates detailed analysis notes
    """

    name = "paper_analysis"

    def __init__(
        self,
        client=None,
        output_dir: Path = None,
        project_root: Path = None,
        min_papers: int = 3,
        max_papers: int = 20,
        enable_topic_bonus: bool = False
    ):
        """
        Initialize paper analysis task.

        Args:
            client: ZhipuClient instance
            output_dir: Output directory for generated files
            project_root: Project root directory
            min_papers: Minimum number of papers to download
            max_papers: Maximum number of papers to download
            enable_topic_bonus: Whether to enable topic interest bonus
        """
        super().__init__(output_dir, project_root)

        from ..summarizers import ZhipuClient
        from ..fetchers import PapersFetcher
        from ..utils.paper_ranker import PaperRanker

        self.client = client or ZhipuClient(
            model=config.GLM_MODEL,
            api_key=config.GLM_API_KEY,
            base_url=config.GLM_BASE_URL,
            max_tokens=config.GLM_MAX_TOKENS,
            enable_thinking=config.GLM_ENABLE_THINKING,
        )
        self.fetcher = PapersFetcher(data_dir=self.project_root / "data")
        self.ranker = PaperRanker(enable_topic_bonus=enable_topic_bonus)
        self.min_papers = min_papers
        self.max_papers = max_papers

        # Load analysis prompt from PaperPrompt
        self.prompt = PaperPrompt().get_system_prompt()

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
        Fetch and rank papers, then download PDFs.

        Args:
            date: Date string in YYYY-MM-DD format

        Returns:
            List of downloaded paper info dictionaries
        """
        print(f"\n[1/4] 获取并排序论文列表...")

        # Fetch papers from HuggingFace
        url = f"https://huggingface.co/api/daily_papers?date={date}"
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

        if resp.status_code != 200:
            print(f"  ❌ API 请求失败 ({resp.status_code})")
            return []

        papers = resp.json()
        if not papers:
            print(f"  ⚠️ 无数据: {date}")
            return []

        print(f"  获取到 {len(papers)} 篇论文")

        # Rank papers
        ranked = self.ranker.rank_papers(papers)

        # Find last Frontier Lab paper
        last_frontier_idx = 0
        for i, p in enumerate(ranked):
            reasons = p.get("rank_reasons", "")
            if "Super Lab" in reasons or "Frontier Lab" in reasons:
                last_frontier_idx = i

        # Determine download count
        download_count = max(self.min_papers, last_frontier_idx + 1)
        download_count = min(download_count, self.max_papers)

        papers_to_download = ranked[:download_count]

        frontier_count = sum(1 for p in papers_to_download
                           if "Super Lab" in p.get("rank_reasons", "")
                           or "Frontier Lab" in p.get("rank_reasons", ""))

        print(f"  将下载: 第1篇 → 第{last_frontier_idx+1}篇 (共 {download_count} 篇)")
        print(f"  其中 Frontier Labs: {frontier_count} 篇")

        # Show papers to be downloaded
        print(f"\n  将分析的论文:")
        for i, p in enumerate(papers_to_download, 1):
            title = p.get("title", "")[:55]
            score = p.get("rank_score", 0)
            reasons = p.get("rank_reasons", "")
            marker = "🔥" if ("Super Lab" in reasons or "Frontier Lab" in reasons) else "  "
            print(f"    {i:2d}. [{marker}] {score:6.2f} | {title}... | {reasons}")

        # Download PDFs
        return self._download_pdfs(papers_to_download, date)

    def _download_pdfs(self, papers: List[Dict], date: str) -> List[Dict[str, Any]]:
        """
        Download PDF files for papers.

        Args:
            papers: List of paper metadata dictionaries
            date: Date string for directory organization

        Returns:
            List of downloaded paper info dictionaries
        """
        print(f"\n[2/4] 下载 PDF...")

        import config
        if config.ENABLE_CACHE:
            download_dir = self.project_root / "data" / date / "papers" / "pdf_downloads"
            download_dir.mkdir(parents=True, exist_ok=True)
        else:
            download_dir = None  # Not used in non-cache mode

        downloaded_files = []

        for i, p in enumerate(papers, 1):
            paper = p.get("paper", {})
            arxiv_id = paper.get("id", "")
            title = p.get("title", "")
            score = p.get("rank_score", 0)
            reasons = p.get("rank_reasons", "")

            print(f"\n  [{i}/{len(papers)}] Score: {score} | {title[:60]}...")
            print(f"     Tags: {reasons}")

            # Download PDF
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            safe_title = re.sub(r'[\\/*?:"<>|]', "", title).strip()
            filename = f"{arxiv_id}_{safe_title[:80]}.pdf"

            # Determine file path and check for existing cache
            file_path = None
            pdf_data = None
            from_cache = False

            if config.ENABLE_CACHE:
                file_path = download_dir / filename
                if file_path.exists():
                    print(f"    [已缓存] {filename}")
                    from_cache = True

            # Download if not cached
            if not from_cache:
                try:
                    print(f"    [下载中] {filename}...")
                    r = requests.get(
                        pdf_url,
                        headers={"User-Agent": "Mozilla/5.0"},
                        stream=True,
                        timeout=60
                    )
                    if r.status_code == 200:
                        # Read PDF data into memory
                        pdf_data = r.content
                        print(f"    [完成] {len(pdf_data):,} bytes")

                        # Save to cache if enabled
                        if config.ENABLE_CACHE and file_path:
                            with open(file_path, 'wb') as f:
                                f.write(pdf_data)
                            time.sleep(3)  # ArXiv rate limit
                    else:
                        print(f"    [失败] HTTP {r.status_code}")
                        continue
                except Exception as e:
                    print(f"    [错误] {e}")
                    continue

            downloaded_files.append({
                "pdf_path": str(file_path) if file_path else filename,
                "pdf_data": pdf_data,  # Has data if newly downloaded, None if from cache
                "arxiv_id": arxiv_id,
                "title": title,
                "org": p.get("organization", {}).get("fullname", ""),
                "stars": paper.get("githubStars", 0),
                "upvotes": paper.get("upvotes", 0),
                "score": score,
                "reasons": reasons
            })

        return downloaded_files

    def summarize(self, items: List[Dict[str, Any]], date: str) -> List[Dict[str, Any]]:
        """
        Analyze downloaded PDFs using Gemini.

        Args:
            items: List of downloaded paper info dictionaries
            date: Date string in YYYY-MM-DD format

        Returns:
            List of analysis results with output paths
        """
        if not items:
            return []

        print(f"\n[3/4] 分析论文...")

        output_dir = self.output_dir / "papers"
        output_dir.mkdir(parents=True, exist_ok=True)

        analysis_files = []

        for i, paper_info in enumerate(items, 1):
            print(f"\n  论文 {i}/{len(items)}")

            try:
                # Use pdf_data if available (non-cache mode), otherwise read from file
                pdf_data = paper_info.get("pdf_data")
                if pdf_data:
                    result = self.client.analyze_pdf_bytes(
                        paper_info["pdf_path"],
                        self.prompt,
                        pdf_data=pdf_data
                    )
                else:
                    result = self.client.upload_and_analyze(
                        paper_info["pdf_path"],
                        self.prompt
                    )

                # Save analysis result
                arxiv_id = paper_info.get("arxiv_id", "unknown")
                filename = f"papers_note_{arxiv_id}.md"
                output_path = output_dir / filename

                # Build full output
                content = f"# {paper_info.get('title', 'Unknown')}\n\n"
                content += f"**arXiv ID**: {arxiv_id}\n"
                content += f"**组织**: {paper_info.get('org', 'Unknown')}\n"
                content += f"**GitHub Stars**: {paper_info.get('stars', 0)}\n"
                content += f"**Upvotes**: {paper_info.get('upvotes', 0)}\n"
                content += f"**得分**: {paper_info.get('score', 0)}\n"
                content += f"**标签**: {paper_info.get('reasons', 'N/A')}\n\n"
                content += "---\n\n"
                content += result

                # Always save paper notes for user reference
                output_path.write_text(content, encoding='utf-8')
                print(f"  [保存] {filename}")

                analysis_files.append({
                    **paper_info,
                    "output_path": output_path,
                    "analysis": result
                })

            except Exception as e:
                print(f"  [错误] 分析失败: {e}")

        return analysis_files

    def format(self, items: List[Dict[str, Any]], date: str) -> str:
        """
        Format stage - not needed for paper analysis.
        Individual papers are already formatted in summarize().

        Args:
            items: List of analysis result dictionaries (not used)
            date: Date string in YYYY-MM-DD format (not used)

        Returns:
            Empty string (no-op)
        """
        # No-op: papers are already formatted in summarize()
        return ""
