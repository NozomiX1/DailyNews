# DailyNews - Papers Fetcher
# Migrated from src/paper_fetch.py
import os
import requests
from datetime import date, timedelta
from pathlib import Path
from typing import List, Dict, Any
import json

from .base import BaseFetcher
from ..utils import PaperRanker, retry_on_request_error, retry_on_http_error
import config


class PapersFetcher(BaseFetcher):
    """HuggingFace Daily Papers fetcher."""

    def __init__(self, data_dir: Path = None):
        super().__init__(data_dir)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def _sanitize_filename(self, name: str) -> str:
        """清理文件名中的非法字符"""
        import re
        return re.sub(r'[\\/*?:"<>|]', "", name).strip()

    @retry_on_http_error(max_retries=3)
    def _download_pdf(self, pdf_url: str, file_path: Path) -> bool:
        """下载单个PDF文件"""
        if not config.ENABLE_CACHE:
            return True  # Skip download but return success

        resp = requests.get(
            pdf_url,
            headers={"User-Agent": "Mozilla/5.0"},
            stream=True,
            timeout=60
        )
        resp.raise_for_status()

        with open(file_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return True

    @retry_on_request_error(max_retries=3)
    def fetch_papers_from_huggingface(self, target_date: str) -> List[Dict]:
        """
        从 HuggingFace API 获取论文列表

        Args:
            target_date: 目标日期 (YYYY-MM-DD)

        Returns:
            论文列表
        """
        url = f"https://huggingface.co/api/daily_papers?date={target_date}"

        print(f"  📡 获取论文列表: {target_date}")
        resp = requests.get(url, headers=self.headers, timeout=30)
        resp.raise_for_status()

        papers = resp.json()
        if not papers:
            raise ValueError(f"当日无数据: {target_date}")

        print(f"  ✅ 获取到 {len(papers)} 篇论文")

        return papers

    def fetch(
        self,
        date: str = None,
        max_papers: int = 20,
        enable_topic_bonus: bool = False
    ) -> List[Dict]:
        """
        获取并排名论文

        Args:
            date: 目标日期 (YYYY-MM-DD)，默认昨天
            max_papers: 最多返回论文数
            enable_topic_bonus: 是否启用兴趣加成

        Returns:
            排名后的论文列表
        """
        if date is None:
            date = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        print(f"📡 获取 HuggingFace 每日论文: {date}")

        papers = self.fetch_papers_from_huggingface(date)

        # 排序
        print(f"  📊 论文排序...")
        ranker = PaperRanker(enable_topic_bonus=enable_topic_bonus)
        ranked = ranker.rank_papers(papers)

        for paper in ranked:
            paper['date'] = date

        print(f"  ✅ 完成，共 {len(ranked)} 篇")

        result = ranked[:max_papers]

        # Print data preview
        self._print_data_preview(result, "HuggingFace Papers")

        return result

    def _print_data_preview(self, items: List[Dict], title: str):
        """打印第一条数据预览"""
        if not items:
            return

        print(f"\n📋 {title} - 数据预览 (第1条):")
        print("-" * 50)

        # 打印 JSON 预览
        first_item = items[0]
        preview_json = json.dumps(
            first_item,
            ensure_ascii=False,
            indent=2
        )
        preview_lines = preview_json.split('\n')
        for line in preview_lines[:15]:  # 前15行
            print(line)
        if len(preview_lines) > 15:
            print("... (省略)")
        print("-" * 50)

    def save_raw_data(self, items: List[Dict], date: str) -> Path:
        """
        保存论文榜单为 JSON

        Args:
            items: 论文列表
            date: 日期字符串

        Returns:
            保存的文件路径
        """
        if not config.ENABLE_CACHE:
            print(f"      📋 无缓存模式，跳过保存 papers JSON")
            return None

        # 新路径: data/{date}/papers/
        papers_dir = self.data_dir / date / "papers"
        papers_dir.mkdir(parents=True, exist_ok=True)

        output_path = papers_dir / f"{date}.json"

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False, indent=2)

        print(f"  💾 已保存: {output_path}")
        return output_path

    def load_from_json(self, date: str, max_papers: int = None) -> List[Dict]:
        """
        从本地 JSON 文件加载论文数据（用于总结阶段）

        Args:
            date: 日期字符串
            max_papers: 最多加载论文数（默认 None，加载全部）

        Returns:
            论文列表，如果文件不存在或加载失败则返回 None
        """
        import json

        json_path = self.data_dir / date / "papers" / f"{date}.json"
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    papers = json.load(f)
                if max_papers:
                    papers = papers[:max_papers]
                    print(f"  ✅ 从 JSON 加载 {len(papers)} 篇论文 (限制 {max_papers} 篇)")
                else:
                    print(f"  ✅ 从 JSON 加载 {len(papers)} 篇论文")
                return papers
            except Exception as e:
                print(f"  ⚠️ 加载 JSON 失败: {e}")
        return None

    def download_pdfs(self, items: List[Dict], date: str = None, min_papers: int = 3, max_papers: int = 12) -> Dict[str, int]:
        """
        下载论文 PDF

        Args:
            items: 论文列表
            date: 日期字符串，用于确定保存路径
            min_papers: 最少下载数（默认3）
            max_papers: 最多下载数（默认12）

        Returns:
            下载统计字典 {'success': 成功数, 'skipped': 跳过数, 'failed': 失败数}
        """
        if not config.ENABLE_CACHE:
            print(f"      📋 无缓存模式，跳过下载 PDF")
            return {'success': 0, 'skipped': len(items), 'failed': 0}

        import time
        import re

        # 新路径: data/{date}/papers/pdf_downloads/
        if date is None:
            date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        pdf_dir = self.data_dir / date / "papers" / "pdf_downloads"
        pdf_dir.mkdir(parents=True, exist_ok=True)

        # 找到最后一篇 Frontier Lab 论文的位置
        last_frontier_idx = 0
        for i, paper in enumerate(items):
            reasons = paper.get("rank_reasons", "")
            if "Super Lab" in reasons or "Frontier Lab" in reasons:
                last_frontier_idx = i

        # 确定下载数量: 从第1篇到最后一篇 Frontier Lab
        download_count = max(min_papers, last_frontier_idx + 1)
        download_count = min(download_count, max_papers)

        items_to_download = items[:download_count]

        # 统计 Frontier Lab 数量
        frontier_count = sum(1 for p in items_to_download
                              if "Super Lab" in p.get("rank_reasons", "") or "Frontier Lab" in p.get("rank_reasons", ""))

        print(f"  📦 开始下载 PDF (第1篇 → 第{last_frontier_idx+1}篇, 共 {download_count} 篇, Frontier Labs: {frontier_count})...")

        stats = {'success': 0, 'skipped': 0, 'failed': 0}

        for i, paper in enumerate(items_to_download, 1):
            paper_detail = paper.get("paper", {})
            arxiv_id = paper_detail.get("id", "")
            title = paper.get("title", "")

            if not arxiv_id:
                continue

            # 清理文件名
            safe_title = re.sub(r'[\\/*?:"<>|]', "", title).strip()
            filename = f"{arxiv_id}_{safe_title[:80]}.pdf"
            file_path = pdf_dir / filename

            # 检查是否已存在
            if file_path.exists():
                stats['skipped'] += 1
                print(f"    [{i}/{len(items_to_download)}] ⊙ {arxiv_id} - 已存在")
                continue

            # 下载 PDF
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            try:
                print(f"    [{i}/{len(items_to_download)}] ⬇️ {arxiv_id}...")
                self._download_pdf(pdf_url, file_path)
                file_size = file_path.stat().st_size
                stats['success'] += 1
                print(f"       ✓ {file_size:,} bytes")
                time.sleep(3)  # ArXiv 限制
            except Exception as e:
                stats['failed'] += 1
                print(f"       ✗ 错误: {e}")

        print(f"    PDF 下载完成: ✓{stats['success']} ⊙{stats['skipped']} ✗{stats['failed']}")
        return stats
