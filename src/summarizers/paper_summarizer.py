# Paper Summarizer
# Analyze academic papers using GLM
import json
import re
import time
from typing import Dict, Any, List
from pathlib import Path

from .base import BaseSummarizer
from .zhipu_client import ZhipuClient
from prompts.paper import PaperPrompt
from prompts.paper_summary import PaperSummaryPrompt


class PaperSummarizer(BaseSummarizer):
    """Summarizer for academic papers (requires PDF analysis)."""

    def __init__(self, client: ZhipuClient, prompt_path: str = None, load_full_prompt: bool = False):
        """
        Initialize paper summarizer.

        Args:
            client: ZhipuClient instance
            prompt_path: Path to prompt.md file
            load_full_prompt: Whether to load full prompt (for PDF analysis). Default False.
        """
        super().__init__(client)
        # Only initialize PaperPrompt when needed (for PDF analysis)
        # This avoids the abstract method error in --paper lightweight mode
        self.prompt = PaperPrompt() if load_full_prompt else None
        self.full_prompt = None
        # Lightweight prompt for summary-only processing
        self.summary_prompt = PaperSummaryPrompt()
        # Load full prompt if requested
        if load_full_prompt and self.prompt:
            self.full_prompt = self.prompt.get_system_prompt()

    def summarize(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a paper from PDF.

        Args:
            content: PDF file path (not content string)
            metadata: Paper metadata from HuggingFace API

        Returns:
            Analysis result dictionary
        """
        pdf_path = content  # content is actually the PDF path

        if not Path(pdf_path).exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        # Extract metadata
        paper_detail = metadata.get('paper', {})
        arxiv_id = paper_detail.get('id', metadata.get('arxiv_id', ''))
        title = metadata.get('title', 'Unknown')
        org = metadata.get('organization', {}).get('fullname', 'Unknown')
        stars = paper_detail.get('githubStars', 0)
        upvotes = paper_detail.get('upvotes', 0)
        score = metadata.get('rank_score', 0)
        reasons = metadata.get('rank_reasons', '')

        print(f"    📄 分析: {title[:50]}...")

        try:
            # Call Gemini with PDF
            result_text = self.client.analyze_pdf_bytes(pdf_path, self.full_prompt)

            # Parse result - it should be markdown formatted
            return {
                'arxiv_id': arxiv_id,
                'title': title,
                'org': org,
                'stars': stars,
                'upvotes': upvotes,
                'score': score,
                'tags': reasons,
                'analysis': result_text,
                'pdf_path': pdf_path
            }

        except Exception as e:
            print(f"    ❌ 分析失败: {e}")
            return {
                'arxiv_id': arxiv_id,
                'title': title,
                'org': org,
                'error': str(e),
                'analysis': f"# 分析失败\n\n论文：{title}\n\n错误：{str(e)}"
            }

    def summarize_batch(
        self,
        papers: List[Dict],
        pdf_dir: Path = None,
        date: str = None,
        delay: float = 3.0
    ) -> List[Dict]:
        """
        Analyze multiple papers.

        Args:
            papers: List of paper metadata dictionaries
            pdf_dir: Directory containing downloaded PDFs (deprecated, use date instead)
            date: Date string for determining PDF directory path
            delay: Delay between requests

        Returns:
            List of analysis results
        """
        from pathlib import Path
        from datetime import datetime

        results = []
        total = len(papers)

        print(f"  🤖 开始分析 {total} 篇论文...")

        # 确定 PDF 目录
        if pdf_dir is None and date:
            # 新路径: data/{date}/papers/pdf_downloads/
            project_root = Path(__file__).parent.parent.parent
            pdf_dir = project_root / "data" / date / "papers" / "pdf_downloads"

        for i, paper in enumerate(papers, 1):
            paper_detail = paper.get('paper', {})
            arxiv_id = paper_detail.get('id', '')
            title = paper.get('title', 'Unknown')

            print(f"    [{i}/{total}] {title[:40]}...")

            # Find PDF path
            if pdf_dir:
                pdf_path = self._find_pdf(pdf_dir, arxiv_id, title)
                if not pdf_path:
                    print(f"      ⚠️ PDF 未找到，跳过")
                    continue
            else:
                print(f"      ⚠️ 未指定 PDF 目录，跳过")
                continue

            result = self.summarize(str(pdf_path), paper)
            results.append(result)

            if i < total:
                time.sleep(delay)

        print(f"  ✅ 分析完成，{len(results)}/{total} 篇")

        return results

    def _find_pdf(self, pdf_dir: Path, arxiv_id: str, title: str) -> Path:
        """Find PDF file in directory."""
        pdf_dir = Path(pdf_dir)

        # Try exact match with arxiv_id
        for pdf_file in pdf_dir.glob("*.pdf"):
            if arxiv_id and arxiv_id in pdf_file.name:
                return pdf_file

        # Try partial title match
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title).strip()[:50]
        for pdf_file in pdf_dir.glob("*.pdf"):
            if safe_title and safe_title.lower() in pdf_file.name.lower():
                return pdf_file

        return None

    def summarize_batch_from_summary(
        self,
        papers: List[Dict],
        delay: float = 1.0,
        output_path: str = None
    ) -> List[Dict]:
        """
        Generate Chinese summaries from English summary field (lightweight, no PDF needed).

        注意：这是独立于 PDF 分析的另一个功能，不修改现有代码。

        Args:
            papers: List of paper metadata dictionaries (containing paper.summary field)
            delay: Delay between requests
            output_path: If provided, save results incrementally after each paper

        Returns:
            List of papers with Chinese summaries
        """
        results = []
        total = len(papers)

        print(f"  🤖 开始生成论文中文摘要 ({total} 篇)...")

        for i, paper in enumerate(papers, 1):
            paper_detail = paper.get('paper', {})
            title = paper.get('title', 'Unknown')

            # Skip if no summary available
            summary = paper_detail.get('summary', '')
            if not summary or len(summary) < 50:
                print(f"    [{i}/{total}] ⚠️ 无摘要，跳过: {title[:40]}...")
                # Still include with empty summary_zh
                results.append({
                    'arxiv_id': paper_detail.get('id', ''),
                    'title': title,
                    'org': paper.get('organization', {}).get('fullname', ''),
                    'stars': paper_detail.get('githubStars', 0),
                    'upvotes': paper_detail.get('upvotes', 0),
                    'score': paper.get('rank_score', 0),
                    'tags': paper.get('rank_reasons', ''),
                    'summary': summary,
                    'summary_zh': '',
                    'title_zh': '',
                    'highlights': [],
                    'relevance': 'low',
                    'is_golden': paper.get('is_golden', False)
                })

                # 边总结边保存
                if output_path:
                    self.save_json(results, output_path)

                continue

            print(f"    [{i}/{total}] {title[:40]}...")

            try:
                # Format prompt with paper info - include system prompt for format requirements
                system_prompt = self.summary_prompt.get_system_prompt()
                user_prompt = self.summary_prompt.format_prompt_with_paper(paper)
                prompt_text = f"{system_prompt}\n\n{user_prompt}"

                # Call LLM
                response = self.client.generate_content(prompt_text)
                result = self._extract_json_from_response(response.text)

                # 验证必需字段是否存在
                required_fields = ['title_zh', 'summary_zh', 'highlights', 'relevance']
                missing_fields = [f for f in required_fields if f not in result]

                if missing_fields:
                    print(f"      ⚠️ 缺少字段: {missing_fields}，使用默认值")
                    # 添加缺失字段的默认值
                    if 'title_zh' not in result:
                        result['title_zh'] = title
                    if 'summary_zh' not in result:
                        result['summary_zh'] = ''
                    if 'highlights' not in result:
                        result['highlights'] = []
                    if 'relevance' not in result:
                        result['relevance'] = 'medium'

                # Merge with original paper data
                arxiv_id = paper_detail.get('id', '')
                result['arxiv_id'] = arxiv_id
                result['title'] = title
                result['org'] = paper.get('organization', {}).get('fullname', '')
                result['stars'] = paper_detail.get('githubStars', 0)
                result['upvotes'] = paper_detail.get('upvotes', 0)
                result['score'] = paper.get('rank_score', 0)
                result['tags'] = paper.get('rank_reasons', '')
                result['summary'] = summary  # Original English summary
                result['is_golden'] = paper.get('is_golden', False)

                results.append(result)
                print(f"      ✅ Relevance: {result.get('relevance', 'N/A')}")

            except Exception as e:
                print(f"      ❌ 失败: {e}")
                # Return fallback with empty Chinese summary
                results.append({
                    'arxiv_id': paper_detail.get('id', ''),
                    'title': title,
                    'org': paper.get('organization', {}).get('fullname', ''),
                    'stars': paper_detail.get('githubStars', 0),
                    'upvotes': paper_detail.get('upvotes', 0),
                    'score': paper.get('rank_score', 0),
                    'tags': paper.get('rank_reasons', ''),
                    'summary': summary,
                    'summary_zh': '',
                    'title_zh': '',
                    'highlights': [],
                    'relevance': 'low',
                    'is_golden': paper.get('is_golden', False),
                    'error': str(e)
                })

            # 边总结边保存
            if output_path:
                self.save_json(results, output_path)

            if i < total:
                time.sleep(delay)

        print(f"  ✅ 中文摘要生成完成，{len(results)}/{total} 篇")

        return results
