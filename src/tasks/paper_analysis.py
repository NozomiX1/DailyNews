# PaperAnalysisTask
# Task for deep paper analysis with PDF download and Gemini analysis
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime, timedelta as dt
import re
import requests
import time

from .base import BaseTask
from .papers import is_weekend
from prompts import PaperPrompt


class PaperAnalysisTask(BaseTask):
    """
    Task for deep paper analysis with full PDF download and analysis.

    This task:
    - Fetches paper rankings from HuggingFace
    - Downloads full ArXiv PDFs
    - Analyzes each paper with Gemini using PDF upload
    - Generates detailed analysis notes
    - Can publish each paper as a separate draft
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
            client: GeminiClient instance
            output_dir: Output directory for generated files
            project_root: Project root directory
            min_papers: Minimum number of papers to download
            max_papers: Maximum number of papers to download
            enable_topic_bonus: Whether to enable topic interest bonus
        """
        super().__init__(output_dir, project_root)

        from ..summarizers import GeminiClient
        from ..fetchers import PapersFetcher
        from ..utils.paper_ranker import PaperRanker
        from ..publishers import WechatPublisher

        self.client = client or GeminiClient(model="gemini-3-pro-high")
        self.fetcher = PapersFetcher(data_dir=self.project_root / "data")
        self.ranker = PaperRanker(enable_topic_bonus=enable_topic_bonus)
        self.publisher = WechatPublisher()
        self.min_papers = min_papers
        self.max_papers = max_papers

        # Load analysis prompt from PaperPrompt
        paper_prompt = PaperPrompt()
        self.prompt = paper_prompt.get_full_prompt_from_file()

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

        download_dir = self.project_root / "data" / date / "papers" / "pdf_downloads"
        download_dir.mkdir(parents=True, exist_ok=True)

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
            file_path = download_dir / filename

            if file_path.exists():
                print(f"    [已存在] {filename}")
            else:
                try:
                    print(f"    [下载中] {filename}...")
                    r = requests.get(
                        pdf_url,
                        headers={"User-Agent": "Mozilla/5.0"},
                        stream=True,
                        timeout=60
                    )
                    if r.status_code == 200:
                        with open(file_path, 'wb') as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        file_size = file_path.stat().st_size
                        print(f"    [完成] {file_size:,} bytes")
                        time.sleep(3)  # ArXiv rate limit
                    else:
                        print(f"    [失败] HTTP {r.status_code}")
                        continue
                except Exception as e:
                    print(f"    [错误] {e}")
                    continue

            downloaded_files.append({
                "pdf_path": file_path,
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
                result = self.client.upload_and_analyze(
                    str(paper_info["pdf_path"]),
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

    def publish(self, content: str, date: str) -> Dict[str, Any]:
        """
        Publish all paper analyses as separate drafts.

        Args:
            content: Summary content (not used, individual papers are published)
            date: Date string in YYYY-MM-DD format

        Returns:
            Publish results for all papers
        """
        print(f"\n📤 发布论文分析...")

        results = self.publisher.publish_all_papers(date)

        success_count = sum(1 for r in results if r.get('status') == 'success')
        print(f"\n✅ 完成: {success_count}/{len(results)} 篇论文发布成功")

        return {
            "status": "success" if success_count > 0 else "error",
            "count": len(results),
            "success_count": success_count
        }
