# Markdown Formatter
# Convert JSON summaries to formatted Markdown
from typing import List, Dict
from pathlib import Path
from datetime import datetime


class MarkdownFormatter:
    """
    Convert JSON format summaries to Markdown documents.
    """

    def format_articles(self, articles: List[Dict], date: str = None) -> str:
        """
        生成公众号日报 Markdown

        Args:
            articles: List of article summary dictionaries
            date: Report date

        Returns:
            Formatted Markdown string
        """
        if not articles:
            return "# AI 每日情报\n\n今日无内容。"

        if date is None:
            date = articles[0].get('date', datetime.now().strftime('%Y-%m-%d'))

        lines = [
            f"# AI 每日情报 | {date}",
            "",
            "## 📊 今日情报",
            ""
        ]

        # Sort by score descending
        sorted_articles = sorted(
            articles,
            key=lambda x: x.get('score', 0),
            reverse=True
        )

        for i, article in enumerate(sorted_articles, 1):
            stars = "🌟" * article.get('score', 3)
            tags = " ".join([f"[{t}]" for t in article.get('tags', [])])

            title = article.get('title', article.get('original_title', '无标题'))

            lines.extend([
                f"### {i}. {title}",
                f"**来源**: {article.get('source', '未知')} | **时间**: {article.get('time', '')}",
                f"**价值**: {stars} **标签**: {tags}",
                f"**链接**: {article.get('url', '')}",
                "",
                article.get('summary', ''),  # 直接显示摘要内容，不加前缀
                "",
                "---",
                ""
            ])

        return "\n".join(lines)

    def format_github(self, repos: List[Dict], date: str = None) -> str:
        """
        生成 GitHub Trending Markdown

        Args:
            repos: List of repository summary dictionaries
            date: Report date

        Returns:
            Formatted Markdown string
        """
        if not repos:
            return "# GitHub 热门项目\n\n今日无内容。"

        if date is None:
            date = repos[0].get('date', datetime.now().strftime('%Y-%m-%d'))

        lines = [
            f"# GitHub 热门项目 | {date}",
            "",
            "## 📊 今日榜单",
            ""
        ]

        for i, repo in enumerate(repos, 1):
            name = repo.get('name', repo.get('name', 'unknown'))
            category = repo.get('category', '')
            language = repo.get('language', 'N/A')
            stars = repo.get('total_stars', repo.get('stars', '0'))
            today_stars = repo.get('today_stars', repo.get('stars_period', '0'))
            url = repo.get('url', '')

            # Title line with category
            if category:
                title_line = f"**分类**: {category} | **语言**: {language} | **Stars**: {stars} | **今日**: +{today_stars}"
            else:
                title_line = f"**语言**: {language} | **Stars**: {stars} | **今日**: +{today_stars}"

            lines.extend([
                f"### {i}. {name}",
                title_line,
                f"**链接**: {url}",
                "",
            ])

            # Add summary if available
            summary = repo.get('summary', '')
            if summary:
                lines.append(f"**摘要**: {summary}")
                lines.append("")

            # Add tech stack if available
            tech_stack = repo.get('tech_stack', [])
            if tech_stack:
                lines.append(f"**技术栈**: {', '.join(tech_stack)}")
                lines.append("")

            # Add use cases if available
            use_cases = repo.get('use_cases', [])
            if use_cases:
                lines.append("**使用场景**:")
                for case in use_cases:
                    lines.append(f"- {case}")
                lines.append("")

            # Add highlights if available
            highlights = repo.get('highlights', [])
            if highlights:
                lines.append("**亮点**:")
                for highlight in highlights:
                    lines.append(f"- {highlight}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def format_papers_summary(self, papers: List[Dict], date: str = None) -> str:
        """
        生成论文汇总 Markdown

        Args:
            papers: List of paper dictionaries
            date: Report date

        Returns:
            Formatted Markdown string
        """
        if not papers:
            return "# 每日论文汇总\n\n今日无内容。"

        if date is None:
            date = papers[0].get('date', datetime.now().strftime('%Y-%m-%d'))

        lines = [
            f"# 每日论文汇总 - {date}",
            "",
            f"**论文数量**: {len(papers)}",
            "",
            "---",
            ""
        ]

        for i, paper in enumerate(papers, 1):
            title = paper.get('title', 'Unknown')
            title_zh = paper.get('title_zh', '')
            # Handle both string and dict formats for organization
            org_val = paper.get('org', paper.get('organization'))
            if isinstance(org_val, dict):
                org = org_val.get('fullname', 'Unknown')
            else:
                org = org_val or 'Unknown'
            score = paper.get('score', paper.get('rank_score', 0))
            reasons = paper.get('reasons', paper.get('tags', paper.get('rank_reasons', '')))
            is_golden = paper.get('is_golden', False)

            paper_detail = paper.get('paper', {})
            arxiv_id = paper.get('arxiv_id', paper_detail.get('id', ''))
            arxiv_url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else ''
            upvotes = paper.get('upvotes', paper_detail.get('upvotes', 0))
            stars = paper.get('stars', paper_detail.get('githubStars', 0))

            golden_mark = "🏆" if is_golden else ""

            # 标题行：中文标题 (英文标题)
            if title_zh and title_zh != title:
                title_line = f"{title_zh} ({title})"
            else:
                title_line = title

            lines.extend([
                f"### {golden_mark} {i}. {title_line}",
                "",
                f"**论文链接**: [{arxiv_url}]({arxiv_url})" if arxiv_url else f"**arXiv ID**: {arxiv_id}",
                f"**组织**: {org}",
                f"**得分**: {score}",
                f"**标签**: {reasons}",
                f"**Upvotes**: {upvotes} | **Stars**: {stars}",
                ""
            ])

            # 使用中文摘要
            summary_zh = paper.get('summary_zh', '')
            if summary_zh:
                lines.append(f"**摘要**: {summary_zh}")
                lines.append("")

            # 亮点多级列表
            highlights = paper.get('highlights', [])
            if highlights:
                lines.append("**亮点**:")
                for highlight in highlights:
                    lines.append(f"  - {highlight}")
                lines.append("")

            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def save(self, content: str, output_path: str) -> None:
        """
        Save formatted content to file (always saves, even in no-cache mode).

        Args:
            content: Formatted Markdown content
            output_path: Path to output file

        Note:
            Output files are always saved for user reference.
            Only data/summaries JSON files are skipped in no-cache mode.
        """

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  💾 已保存: {output_path}")
