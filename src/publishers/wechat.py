# DailyNews - WeChat Publisher
# Merged and refactored from wechat_publisher.py, github_publisher.py, paper_publisher.py
import requests
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import config

from .base import BasePublisher


class WechatPublisher(BasePublisher):
    """
    WeChat Official Account publisher.

    Publishes daily reports, GitHub trending, and paper analyses to WeChat drafts.
    """

    def __init__(self, app_id=None, app_secret=None):
        super().__init__()
        self.app_id = app_id or config.APP_ID
        self.app_secret = app_secret or config.APP_SECRET
        self.token = self._get_access_token()

    def _get_access_token(self):
        """获取 access_token"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        try:
            resp = requests.get(url, proxies=getattr(config, 'PROXIES', None)).json()
            if 'access_token' in resp:
                return resp['access_token']
            else:
                raise Exception(f"获取 access_token 失败: {resp}")
        except Exception as e:
            raise Exception(f"获取 access_token 异常: {e}")

    # ================= Text Width Calculation =================

    def _calc_text_width(self, text):
        """计算文本宽度（以 1/3 单位为基准）"""
        width = 0
        for char in text:
            if char in '🌟⭐📍🕒🏷️🔥💻📄🔬📊🔗':
                width += 4
            elif ord(char) > 127:
                width += 3
            else:
                width += 1
        return width

    # ================= HTML Generation =================

    def _generate_meta_row(self, item: Dict, item_type: str = 'article') -> str:
        """Generate metadata HTML row for an item."""
        if item_type == 'article':
            prefix1 = f'📍 来源：{item["source"]}'
            prefix2 = f'⭐ 价值：{item["rating"]}' if item.get("rating") else ''

            width1 = self._calc_text_width(prefix1)
            width2 = self._calc_text_width(prefix2) if prefix2 else 0

            if width1 < width2:
                prefix1 += ' ' * (width2 - width1)
            elif width2 < width1:
                prefix2 += ' ' * (width1 - width2)

            meta_first_line = f'{prefix1}　🕒 {item["time"]}'

            meta_second_parts = []
            if item.get("rating"):
                meta_second_parts.append(prefix2)
            if item.get("tag"):
                meta_second_parts.append(f'　🏷️ 标签：{item["tag"]}')

            meta_second_line = ''
            if meta_second_parts:
                meta_second_line = '<br>' + ''.join(meta_second_parts)

            return f'{meta_first_line}{meta_second_line}<br><span style="display: inline-block; margin-top: 4px; color: #576b95; word-break: break-all;">🔗 链接：{item["url"]}</span>'

        elif item_type == 'github':
            parts = []
            if item.get('language'):
                parts.append(f'💻 语言：{item["language"]}')
            if item.get('stars'):
                parts.append(f'⭐ Stars：{item["stars"]}')
            if item.get('today_stars'):
                parts.append(f'🔥 今日：+{item["today_stars"]}')

            meta_line = f'{"　".join(parts)}<br><span style="display: inline-block; margin-top: 4px; color: #576b95; word-break: break-all;">🔗 链接：{item["url"]}</span>'

            # Add tech stack below the link (without bold)
            if item.get('tech_stack'):
                meta_line += f'<br><span style="display: inline-block; margin-top: 4px; color: #666; font-size: 13px;">技术栈: {item["tech_stack"]}</span>'

            return meta_line

        elif item_type == 'paper':
            parts = []
            if item.get('score'):
                parts.append(f'📊 得分：{item["score"]}')
            if item.get('upvotes'):
                parts.append(f'👍 {item["upvotes"]}')
            if item.get('stars'):
                parts.append(f'⭐ {item["stars"]}')

            meta_line = '　'.join(parts) if parts else ''
            return f'{meta_line}<br><span style="display: inline-block; margin-top: 4px; color: #576b95; word-break: break-all;">🔗 链接：{item["url"]}</span>'

        return ''

    def generate_html(self, items: List[Dict], item_type: str = 'article') -> str:
        """
        从新闻列表生成 HTML

        Args:
            items: News items list
            item_type: Type of items ('article', 'github', 'paper')

        Returns:
            HTML string
        """
        html_parts = ['<section style="font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;">']
        html_parts.append('<section style="margin-top: 20px;"></section>')

        for idx, item in enumerate(items, 1):
            title = item.get('title', item.get('original_title', ''))

            title_html = f'<h3 style="margin-top: 30px; margin-bottom: 5px; font-size: 18px; font-weight: bold; color: #000;">{idx}. {title}</h3>'

            meta_html = f'<div style="font-size: 13px; color: #888; margin-bottom: 10px; background: #f9f9f9; padding: 8px; border-radius: 4px;">{self._generate_meta_row(item, item_type)}</div>'

            summary = item.get('summary', '')
            summary_text = summary.replace("\n", "<br>")
            summary_html = f'<p style="font-size: 16px; color: #333; line-height: 1.6; text-align: justify; margin-bottom: 25px;">{summary_text}</p>'

            # Add highlights section for papers
            highlights_html = ''
            if item_type == 'paper' and item.get('highlights'):
                highlights_html = f'<div style="font-size: 14px; color: #666; background: #f0f7ff; padding: 10px; border-radius: 4px; margin-bottom: 25px; border-left: 3px solid #3498db;"><strong>✨ 亮点:</strong><br>{item["highlights"]}</div>'

            divider = '<hr style="border: 0; border-top: 1px dashed #ddd; margin: 20px 0;" />' if idx < len(items) else ""
            html_parts.append(title_html + meta_html + summary_html + highlights_html + divider)

        html_parts.append("</section>")
        return "".join(html_parts)

    # ================= Parsing =================

    def _parse_daily_report(self, report_path) -> List[Dict]:
        """解析 daily_report.md 文件"""
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()

        news_items = []

        header_end = content.find('### 1.')
        if header_end != -1:
            content = content[header_end + 6:]

        articles = re.split(r'\n###\s+\d+\.\s+', content)

        for article in articles:
            if not article.strip():
                continue

            title_match = re.search(r'^(.+?)\n', article)
            title = title_match.group(1).strip() if title_match else "无标题"

            source_match = re.search(r'\*\*来源\*\*: (.+?) \|', article)
            source = source_match.group(1).strip() if source_match else "未知"

            time_match = re.search(r'\|\s*\*\*时间\*\*: (.+?)\n', article)
            time_str = time_match.group(1).strip() if time_match else ""

            url_match = re.search(r'\*\*链接\*\*: (.+?)\n', article)
            url = url_match.group(1).strip() if url_match else ""

            rating_match = re.search(r'\*\*价值\*\*: (.+?)\n', article)
            rating = rating_match.group(1).strip() if rating_match else ""
            rating = re.sub(r'\s*\*\*标签\*\*:.+', '', rating).strip()

            tag_match = re.search(r'\*\*标签\*\*: (.+?)\n', article)
            tag = tag_match.group(1).strip() if tag_match else ""

            summary_match = re.search(r'\*\*摘要\*\*: (.+?)(?:\n---|\n\n###|\Z)', article, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else ""
            summary = re.sub(r'<br>', '\n', summary)

            if title and source:
                news_items.append({
                    'title': title,
                    'source': source,
                    'time': time_str,
                    'url': url,
                    'rating': rating,
                    'tag': tag,
                    'summary': summary
                })

        return news_items

    def _parse_github_trending(self, report_path) -> List[Dict]:
        """解析 github_trending.md 文件"""
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()

        items = []
        articles = re.split(r'\n###\s+(\d+)\.\s+', content)

        for i in range(1, len(articles), 2):
            if i + 1 >= len(articles):
                break

            article = articles[i + 1]

            if not article.strip():
                continue

            title_match = re.search(r'^([^\n]+)', article)
            title = title_match.group(1).strip() if title_match else f"项目 {articles[i]}"

            lang_match = re.search(r'\*\*语言\*\*: ([^\n|]+)', article)
            language = lang_match.group(1).strip() if lang_match else "未知"

            stars_match = re.search(r'\*\*Stars\*\*: ([\d,]+)', article)
            stars = stars_match.group(1).strip() if stars_match else ""

            today_match = re.search(r'\*\*今日\*\*: \+([\d,]+)', article)
            today_stars = today_match.group(1).strip() if today_match else ""

            url_match = re.search(r'\*\*链接\*\*: (.+?)\n', article)
            url = url_match.group(1).strip() if url_match else ""

            # Extract tech stack (技术栈)
            tech_stack_match = re.search(r'(?:\*\*技术栈\*\*|技术栈):\s*(.+?)(?:\n---|\n\n###|\Z)', article, re.DOTALL)
            tech_stack = tech_stack_match.group(1).strip() if tech_stack_match else ""
            # Clean up tech_stack text
            tech_stack = re.sub(r'\n+', ' ', tech_stack).strip()

            summary_match = re.search(r'\*\*摘要\*\*: (.+?)(?:\n---|\n\n###|\Z|(?:\*\*技术栈\*\*|技术栈):)', article, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else ""

            if title:
                items.append({
                    'title': title,
                    'language': language,
                    'stars': stars,
                    'today_stars': today_stars,
                    'url': url,
                    'tech_stack': tech_stack,
                    'summary': summary
                })

        return items

    # ================= Publishing =================

    def publish(self, content: str, title: str, **kwargs) -> Dict[str, Any]:
        """Base publish method - creates a draft."""
        item_type = kwargs.get('item_type', 'article')
        items = kwargs.get('items', [])

        if items:
            html_content = self.generate_html(items, item_type)
        else:
            html_content = content

        draft_id = self._create_draft(title, html_content, config.COVER_MEDIA_ID)

        return {
            'status': 'success',
            'draft_id': draft_id,
            'title': title
        }

    def publish_daily_report(self, report_path: str, title: str = None, target_date: str = None) -> Dict[str, Any]:
        """
        将 daily_report.md 发布到草稿箱

        Args:
            report_path: 报告文件路径
            title: 草稿标题
            target_date: 报告日期

        Returns:
            Result dictionary
        """
        news_items = self._parse_daily_report(report_path)

        if not news_items:
            raise Exception("❌ 报告中没有找到任何文章")

        print(f"  📊 解析到 {len(news_items)} 篇文章")

        if not title:
            if not target_date:
                target_date = datetime.now().strftime("%Y-%m-%d")
            title = f"AI 每日情报 | {target_date}"

        content_html = self.generate_html(news_items, 'article')
        draft_id = self._create_draft(title, content_html, config.COVER_MEDIA_ID)

        return {
            'status': 'success',
            'draft_id': draft_id,
            'title': title,
            'count': len(news_items)
        }

    def publish_github_trending(self, report_path: str, title: str = None, target_date: str = None) -> Dict[str, Any]:
        """
        将 GitHub Trending 发布到草稿箱

        Args:
            report_path: 报告文件路径
            title: 草稿标题
            target_date: 报告日期 (YYYY-MM-DD)

        Returns:
            Result dictionary
        """
        items = self._parse_github_trending(report_path)

        if not items:
            raise Exception("❌ 报告中没有找到任何项目")

        print(f"  📊 解析到 {len(items)} 个项目")

        if not title:
            if not target_date:
                # 尝试从 markdown 文件中提取日期
                target_date = self._extract_date_from_markdown(report_path)
            title = f"GitHub 热门项目 | {target_date}"

        content_html = self.generate_html(items, 'github')
        draft_id = self._create_draft(title, content_html, config.COVER_MEDIA_ID)

        return {
            'status': 'success',
            'draft_id': draft_id,
            'title': title,
            'count': len(items)
        }

    def publish_paper(self, paper_data: Dict) -> Dict[str, Any]:
        """
        发布单篇论文到草稿箱

        Args:
            paper_data: Paper analysis data (支持两种格式)
                - 简化格式: {'title', 'arxiv_id', 'org', 'tags', 'score', 'upvotes', 'stars', 'analysis'}
                - 完整格式: 从 _parse_analysis_file() 返回的字典

        Returns:
            Result dictionary
        """
        # 判断是简化格式还是完整格式
        if 'body' in paper_data:
            # 完整格式 - 使用精美 HTML
            title = paper_data.get('title', '论文分析')
            if len(title) > 50:
                title = title[:47] + '...'
            content_html = self._generate_paper_html(paper_data)
        else:
            # 简化格式 - 使用简单 HTML
            title = paper_data.get('title', '论文分析')
            if len(title) > 50:
                title = title[:47] + '...'
            content_html = self._generate_simple_paper_html(paper_data)

        draft_id = self._create_draft(title, content_html, config.COVER_MEDIA_ID)

        return {
            'status': 'success',
            'draft_id': draft_id,
            'title': title
        }

    def publish_papers_summary(self, report_path: str, title: str = None, target_date: str = None) -> Dict[str, Any]:
        """
        将论文汇总发布到草稿箱

        Args:
            report_path: 论文汇总报告文件路径
            title: 草稿标题
            target_date: 报告日期 (YYYY-MM-DD)

        Returns:
            Result dictionary
        """
        items = self._parse_papers_summary(report_path)

        if not items:
            raise Exception("❌ 报告中没有找到任何论文")

        print(f"  📊 解析到 {len(items)} 篇论文")

        if not title:
            if not target_date:
                target_date = self._extract_date_from_markdown(report_path)
            title = f"每日论文汇总 | {target_date}"

        content_html = self.generate_html(items, 'paper')
        draft_id = self._create_draft(title, content_html, config.COVER_MEDIA_ID)

        return {
            'status': 'success',
            'draft_id': draft_id,
            'title': title,
            'count': len(items)
        }

    def _parse_papers_summary(self, report_path: str) -> List[Dict]:
        """解析 papers_summary.md 文件"""
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()

        items = []
        # Split by "###" followed by number and dot
        sections = re.split(r'\n###\s+(\d+)\.\s+', content)

        for i in range(1, len(sections), 2):
            if i + 1 >= len(sections):
                break

            section = sections[i + 1]
            if not section.strip():
                continue

            # Extract title (first non-empty line after the header)
            lines = section.split('\n')
            title = ""
            for line in lines:
                line = line.strip()
                if line and not line.startswith('**'):
                    title = line
                    break

            # Extract URL from **论文链接**: [url](url) format
            url_match = re.search(r'\*\*论文链接\*\*:\s*\[([^\]]+)\]\(([^)]+)\)', section)
            url = url_match.group(2).strip() if url_match else ""

            # Extract arXiv ID from URL
            arxiv_id = ""
            if url and 'arxiv.org/abs/' in url:
                arxiv_id = url.split('arxiv.org/abs/')[-1].split('/')[0]
            elif url:
                # Try to extract from URL as fallback
                arxiv_match = re.search(r'(\d+\.\d+)', url)
                arxiv_id = arxiv_match.group(1) if arxiv_match else ""

            # Extract organization
            org_match = re.search(r'\*\*组织\*\*:\s*(.+?)\n', section)
            org = org_match.group(1).strip() if org_match else ""

            # Extract score
            score_match = re.search(r'\*\*得分\*\*:\s*([\d.]+)', section)
            score = score_match.group(1).strip() if score_match else ""

            # Extract tags
            tags_match = re.search(r'\*\*标签\*\*:\s*(.+?)\n', section)
            tags = tags_match.group(1).strip() if tags_match else ""

            # Extract upvotes and stars (format: **Upvotes**: 15 | **Stars**: 42)
            upvotes_match = re.search(r'\*\*Upvotes\*\*:\s*(\d+)', section)
            upvotes = upvotes_match.group(1).strip() if upvotes_match else ""

            stars_match = re.search(r'\|\s*\*\*Stars\*\*:\s*(\d+)', section)
            stars = stars_match.group(1).strip() if stars_match else ""

            # Extract summary (after **摘要** until **亮点** or --- or end)
            summary_match = re.search(r'\*\*摘要\*\*:\s*(.+?)(?:\n\*\*亮点\*\*|\n---|\n\n###|\Z)', section, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else ""
            summary = re.sub(r'\n+', ' ', summary)  # Convert newlines to spaces
            summary = summary[:500] + "..." if len(summary) > 500 else summary  # Limit length

            # Extract highlights (亮点)
            highlights_match = re.search(r'\*\*亮点\*\*:\s*(.+?)(?:\n---|\n\n###|\Z)', section, re.DOTALL)
            highlights = highlights_match.group(1).strip() if highlights_match else ""
            # Convert bullet points to clean text - handle both leading bullets and bullets after newlines
            highlights = re.sub(r'^\s*-\s*', '• ', highlights, count=1)  # First bullet
            highlights = re.sub(r'\n\s*-\s*', '<br>• ', highlights)  # Subsequent bullets
            highlights = highlights[:300] + "..." if len(highlights) > 300 else highlights

            if title or arxiv_id:
                items.append({
                    'title': title or f"Paper {arxiv_id}",
                    'arxiv_id': arxiv_id,
                    'org': org,
                    'score': score,
                    'tags': tags,
                    'upvotes': upvotes,
                    'stars': stars,
                    'url': url,
                    'summary': summary,
                    'highlights': highlights
                })

        return items

    def _parse_analysis_file(self, analysis_path: str) -> Dict[str, Any]:
        """
        解析单篇论文的分析文件

        Args:
            analysis_path: 分析文件路径

        Returns:
            包含论文信息的字典
        """
        with open(analysis_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取标题
        h1_matches = list(re.finditer(r'^#\s+(.+)$', content, re.MULTILINE))
        # 第一个 h1 是英文原标题（用于 HTML 正文）
        if h1_matches:
            english_title = h1_matches[0].group(1).strip()
        else:
            english_title = Path(analysis_path).stem

        # 第二个 h1 是中文标题（用于草稿标题）
        if len(h1_matches) >= 2:
            title = h1_matches[1].group(1).strip()  # 第二个 h1
        elif h1_matches:
            title = english_title  # 只有一个 h1，用第一个
        else:
            title = Path(analysis_path).stem

        # 提取论文原标题 (从第一行的《》中提取)
        paper_title_match = re.search(r'《(.+?)》', content.split('---')[0] if '---' in content else content)
        paper_title = paper_title_match.group(1) if paper_title_match else ''

        # 提取元数据 (arXiv ID, 组织, Stars, Upvotes, 得分, 标签)
        arxiv_id_match = re.search(r'\*\*arXiv ID\*\*:\s*(.+)', content)
        # Extract arXiv ID from markdown link format
        if arxiv_id_match:
            arxiv_id_text = arxiv_id_match.group(1).strip()
            arxiv_id_link = re.search(r'\[([^\]]+)\]\(([^)]+)\)', arxiv_id_text)
            if arxiv_id_link:
                arxiv_id = arxiv_id_link.group(1)  # Use the display text
                arxiv_url = arxiv_id_link.group(2)
            else:
                arxiv_id = arxiv_id_text
                arxiv_url = f"https://arxiv.org/abs/{arxiv_id_text}"
        else:
            arxiv_id = ''
            arxiv_url = ''

        org = re.search(r'\*\*组织\*\*:\s*(.+)', content)
        # Extract stars from format: **Upvotes**: 15 | **Stars**: 42
        upvotes = re.search(r'\*\*Upvotes\*\*:\s*(\d+)', content)
        stars = re.search(r'\|\s*\*\*Stars\*\*:\s*(\d+)', content)
        score = re.search(r'\*\*得分\*\*:\s*([\d.]+)', content)
        tags = re.search(r'\*\*标签\*\*:\s*(.+)', content)

        # 提取正文 (去除 --- 之后的内容)
        parts = content.split('---', 1)
        body = parts[1].strip() if len(parts) > 1 else content

        # 提取第一段作为摘要（去除空行后第一个非标题段落）
        intro_match = re.search(r'^(?!#)(?!<)(.+)$', body, re.MULTILINE)
        intro = intro_match.group(1).strip() if intro_match else ''
        # 去除 intro 中的 markdown 格式
        intro = re.sub(r'\*\*(.+?)\*\*', r'\1', intro)
        intro = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', intro)

        return {
            'title': title,
            'english_title': english_title,
            'paper_title': paper_title,
            'intro': intro,
            'arxiv_id': arxiv_id,
            'arxiv_url': arxiv_url,
            'org': org.group(1).strip() if org else '',
            'stars': stars.group(1).strip() if stars else '',
            'upvotes': upvotes.group(1).strip() if upvotes else '',
            'score': score.group(1).strip() if score else '',
            'tags': tags.group(1).strip() if tags else '',
            'body': body
        }

    def _markdown_to_html(self, markdown_text: str) -> str:
        """
        将 Markdown 转换为微信公众号 HTML - 完整实现
        支持标题、列表、链接、粗体等格式
        """
        lines = markdown_text.split('\n')
        html_lines = []
        skip_first_h1 = True  # 跳过第一个 h1（因为已在标题处显示）

        # 删除第一段（已作为 intro 显示）
        first_para_removed = False

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # 跳过 --- 分隔线
            if stripped == '---':
                i += 1
                continue

            # 跳过第一个 h1 标题
            if skip_first_h1 and re.match(r'^#\s+', line):
                skip_first_h1 = False
                i += 1
                continue

            # 跳过第一段（已作为 intro 显示在卡片中）
            if not first_para_removed and stripped and not re.match(r'^[#\*\-\d\s]', line):
                first_para_removed = True
                i += 1
                continue

            # 处理四级标题
            match = re.match(r'^####\s+(.+)$', line)
            if match:
                content = match.group(1)
                content = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', content)
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                html_lines.append(f'<h4 style="font-size: 16px; font-weight: bold; color: #555; text-align: left; margin: 15px 0 10px;">{content}</h4>')
                i += 1
                continue

            # 处理三级标题
            match = re.match(r'^###\s+(.+)$', line)
            if match:
                content = match.group(1)
                content = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', content)
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                html_lines.append(f'<h3 style="font-size: 18px; font-weight: bold; color: #34495e; text-align: left; margin: 20px 0 12px; padding-left: 10px; border-left: 4px solid #3498db;">{content}</h3>')
                i += 1
                continue

            # 处理二级标题
            match = re.match(r'^##\s+(.+)$', line)
            if match:
                content = match.group(1)
                content = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', content)
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                html_lines.append(f'<h2 style="font-size: 20px; font-weight: bold; color: #2c3e50; text-align: center; margin: 30px 0 15px; padding: 10px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;">{content}</h2>')
                i += 1
                continue

            # 处理一级标题（跳过第一个之后的其他 h1）
            match = re.match(r'^#\s+(.+)$', line)
            if match:
                content = match.group(1)
                content = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', content)
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                html_lines.append(f'<h1 style="font-size: 22px; font-weight: bold; color: #1a1a1a; text-align: center; margin: 25px 0 20px; padding-bottom: 10px;">{content}</h1>')
                i += 1
                continue

            # 处理空行
            if not stripped:
                if html_lines and not html_lines[-1].startswith('</'):
                    html_lines.append('<br>')
                i += 1
                continue

            # 收集列表（多行）- 支持真正的嵌套列表
            list_structure = []  # List of (content, children) tuples
            list_type = None  # 'ul' or 'ol'
            base_indent = None
            current_parents = []  # Track parent items with their indent levels

            while i < len(lines):
                line = lines[i]
                stripped_i = line.strip()

                # 跳过 --- 分隔线
                if stripped_i == '---':
                    i += 1
                    break

                # 空行结束列表
                if not stripped_i:
                    break

                # 检测列表项
                ul_match = re.match(r'^([\s]*)[\*\-]\s+', line)
                ol_match = re.match(r'^([\s]*)\d+\.\s+', line)

                match_obj = ul_match if ul_match else ol_match

                if match_obj:
                    indent = len(match_obj.group(1))

                    # 确定列表类型
                    if list_type is None:
                        list_type = 'ul' if ul_match else 'ol'
                        base_indent = indent

                    # 检测是否是不同类型的列表
                    current_is_ul = ul_match is not None
                    if (current_is_ul and list_type != 'ul') or (not current_is_ul and list_type == 'ul'):
                        if list_structure:
                            break

                    start, end = match_obj.span()
                    content = line[end:].rstrip()

                    # 处理内联格式 - 先处理带中文标点的 bold，把标点包含在 strong 标签内
                    content = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', content)
                    content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3498db;">\1</a>', content)

                    # 判断层级
                    level = 0
                    if indent > base_indent:
                        # 计算嵌套层级 (每4个空格或1个tab为一级)
                        level = (indent - base_indent) // 4 + 1

                    # 添加到结构中
                    item = {'content': content, 'level': level, 'children': []}

                    # 找到正确的父级
                    while current_parents and current_parents[-1]['level'] >= level:
                        current_parents.pop()

                    if current_parents:
                        current_parents[-1]['children'].append(item)
                    else:
                        list_structure.append(item)

                    # 如果这个项可能有自己的子项，加入父级列表
                    # 但只有当内容不为空或者是标题形式时才作为潜在父级
                    if content or True:  # 任何项目都可能有子项
                        current_parents.append(item)

                    i += 1
                else:
                    # 非列表行，检查是否是前一个列表项的续行
                    if list_structure and (line.startswith('    ') or line.startswith('\t')):
                        continuation = line.rstrip()
                        continuation = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', continuation)
                        continuation = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', continuation)
                        continuation = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3498db;">\1</a>', continuation)
                        # 找到最后的列表项并添加续行
                        if current_parents:
                            current_parents[-1]['content'] += f'<br>{continuation}'
                        elif list_structure:
                            list_structure[-1]['content'] += f'<br>{continuation}'
                        i += 1
                    else:
                        break

            # 生成 HTML
            if list_structure:
                def render_item(item, is_root=True):
                    content = item['content']
                    children = item['children']
                    children_html = ''

                    if children:
                        # 递归渲染子列表
                        nested_items = ''.join(render_item(child, False) for child in children)
                        children_html = f'<ul style="margin: 5px 0; padding-left: 20px;">{nested_items}</ul>'

                    style = 'margin: 8px 0; line-height: 1.8; color: #333;' if is_root else 'margin: 4px 0; line-height: 1.8; color: #333;'

                    # 如果内容只有冒号或为空，与子列表合并
                    if not content or content == '：' or content == ':':
                        return f'<li style="{style}">{children_html}</li>'
                    elif children_html:
                        return f'<li style="{style}">{content}{children_html}</li>'
                    else:
                        return f'<li style="{style}">{content}</li>'

                all_items_html = ''.join(render_item(item) for item in list_structure)
                style = 'margin: 15px 0; padding-left: 20px;' if list_type == 'ul' else 'margin: 15px 0; padding-left: 25px;'
                html_lines.append(f'<{list_type} style="{style}">{all_items_html}</{list_type}>')
                continue
                continue

            # 处理普通段落
            if stripped:
                line = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', line)
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', line)
                line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3498db;">\1</a>', line)
                html_lines.append(f'<p style="font-size: 15px; color: #333; line-height: 1.9; margin-bottom: 10px; text-align: justify;">{line}</p>')

            i += 1

        return '\n'.join(html_lines)

    def _generate_paper_html(self, paper_data: Dict) -> str:
        """
        生成单篇论文的精美 HTML

        Args:
            paper_data: 论文数据字典

        Returns:
            HTML 字符串
        """
        container = '<section style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif; max-width: 677px; margin: 0 auto; padding: 20px 0;">'

        # 标题头部 - 使用英文原标题
        english_title = paper_data.get('english_title', paper_data.get('title', ''))
        title_html = f'''
<div style="text-align: center; margin-bottom: 25px;">
    <h1 style="font-size: 24px; font-weight: bold; color: #1a1a1a; margin: 0 0 15px; line-height: 1.4;">{english_title}</h1>
</div>
'''

        # 元信息卡片
        meta_html = '<div style="background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%); padding: 15px; border-radius: 8px; margin-bottom: 25px; font-size: 14px; color: #555;">'

        # 论文链接 - 纯文本格式
        if paper_data.get('arxiv_url'):
            meta_html += f'<div style="margin-bottom: 8px;">📄 论文：<a href="{paper_data["arxiv_url"]}" style="color: #3498db; text-decoration: none;">{paper_data["arxiv_url"]}</a></div>'
        elif paper_data.get('arxiv_id'):
            arxiv_url = f"https://arxiv.org/abs/{paper_data['arxiv_id']}"
            meta_html += f'<div style="margin-bottom: 8px;">📄 论文：<a href="{arxiv_url}" style="color: #3498db; text-decoration: none;">{arxiv_url}</a></div>'

        if paper_data.get('org'):
            meta_html += f'<div style="margin-bottom: 8px;">🔬 <strong>机构：</strong>{paper_data["org"]}</div>'
        if paper_data.get('tags'):
            meta_html += f'<div style="margin-bottom: 8px;">🏷️ <strong>标签：</strong>{paper_data["tags"]}</div>'

        # 得分和互动数据
        stats_row = ''
        if paper_data.get('score'):
            stats_row += f'<span style="display: inline-block; margin-right: 15px;">📊 {paper_data["score"]}</span>'
        if paper_data.get('upvotes'):
            stats_row += f'<span style="display: inline-block; margin-right: 15px;">👍 {paper_data["upvotes"]}</span>'
        if paper_data.get('stars'):
            stats_row += f'<span style="display: inline-block;">🌟 {paper_data["stars"]}</span>'
        if stats_row:
            meta_html += f'<div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #d0d7de;">{stats_row}</div>'

        meta_html += '</div>'

        # 摘要段落
        intro_html = ''
        if paper_data.get('intro'):
            intro_html = f'<p style="font-size: 15px; color: #444; line-height: 1.8; margin-bottom: 20px; text-align: justify; padding: 12px; background: #f9f9f9; border-radius: 6px;">{paper_data["intro"]}</p>'

        # 正文（使用完整 Markdown→HTML 转换）
        body_html = self._markdown_to_html(paper_data['body'])

        return container + title_html + meta_html + intro_html + body_html + '</section>'

    def _generate_simple_paper_html(self, paper: Dict) -> str:
        """
        生成简化版论文 HTML（用于 publish_paper 方法）

        Args:
            paper: 简化论文数据

        Returns:
            HTML 字符串
        """
        container = '<section style="font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif; max-width: 677px; margin: 0 auto; padding: 20px 0;">'

        title_html = f'<h1 style="font-size: 24px; font-weight: bold; color: #1a1a1a; margin: 0 0 15px; text-align: center;">{paper.get("title", "未知")}</h1>'

        meta_html = '<div style="background: #f5f7fa; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-size: 14px; color: #555;">'

        if paper.get('arxiv_id'):
            arxiv_url = f"https://arxiv.org/abs/{paper['arxiv_id']}"
            meta_html += f'<div style="margin-bottom: 8px;">📄 <strong>论文：</strong><a href="{arxiv_url}" style="color: #3498db;">{paper["arxiv_id"]}</a></div>'

        if paper.get('org'):
            meta_html += f'<div style="margin-bottom: 8px;">🔬 <strong>机构：</strong>{paper["org"]}</div>'

        if paper.get('tags'):
            meta_html += f'<div style="margin-bottom: 8px;">🏷️ <strong>标签：</strong>{paper["tags"]}</div>'

        stats_row = ''
        if paper.get('score'):
            stats_row += f'<span style="display: inline-block; margin-right: 15px;">📊 {paper["score"]}</span>'
        if paper.get('upvotes'):
            stats_row += f'<span style="display: inline-block; margin-right: 15px;">👍 {paper["upvotes"]}</span>'
        if paper.get('stars'):
            stats_row += f'<span style="display: inline-block;">⭐ {paper["stars"]}</span>'

        if stats_row:
            meta_html += f'<div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #d0d7de;">{stats_row}</div>'

        meta_html += '</div>'

        # Convert markdown analysis to HTML (simplified)
        analysis = paper.get('analysis', '')
        body_html = f'<div style="font-size: 15px; color: #333; line-height: 1.8;">{analysis.replace("\n", "<br>")}</div>'

        return container + title_html + meta_html + body_html + '</section>'

    def publish_single_paper(self, analysis_path: str) -> Dict[str, Any]:
        """
        发布单篇论文分析到草稿箱

        Args:
            analysis_path: 分析文件路径

        Returns:
            结果字典，包含 draft_id 和 title
        """
        paper_data = self._parse_analysis_file(analysis_path)

        print(f"📄 正在发布: {paper_data['title']}")

        # 生成标题 (去除过长标题)
        title = paper_data['title']
        if len(title) > 50:
            title = title[:47] + '...'

        # 生成 HTML
        content_html = self._generate_paper_html(paper_data)

        # 创建草稿
        draft_id = self._create_draft(title, content_html, config.COVER_MEDIA_ID)

        return {
            'status': 'success',
            'draft_id': draft_id,
            'title': title
        }

    def publish_all_papers(self, date_str: str) -> List[Dict[str, Any]]:
        """
        发布某一天的所有论文分析

        Args:
            date_str: 日期字符串 (YYYY-MM-DD)

        Returns:
            结果列表
        """
        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / "output" / date_str

        if not output_dir.exists():
            raise Exception(f"输出目录不存在: {output_dir}")

        # 找到所有分析文件 (排除 _summary.md)
        analysis_files = [
            f for f in output_dir.glob("papers/papers_note_*.md")
            if not f.name.startswith('_')
        ]

        if not analysis_files:
            print(f"❌ 没有找到分析文件: {output_dir}")
            return []

        print(f"📊 找到 {len(analysis_files)} 篇论文分析")

        results = []
        for i, analysis_file in enumerate(analysis_files, 1):
            print(f"\n[{i}/{len(analysis_files)}] {analysis_file.name}")
            try:
                result = self.publish_single_paper(str(analysis_file))
                result['file'] = analysis_file.name
                results.append(result)
                print(f"  ✅ 成功 - Media ID: {result['draft_id']}")
            except Exception as e:
                results.append({
                    'file': analysis_file.name,
                    'error': str(e),
                    'status': 'failed'
                })
                print(f"  ❌ 失败 - {e}")

        return results

    def _extract_date_from_markdown(self, report_path: str) -> str:
        """从 markdown 文件标题行中提取日期"""
        with open(report_path, "r", encoding="utf-8") as f:
            first_line = f.readline()
        # 匹配格式: # GitHub 热门项目 | 2026-02-01 或 # 每日论文汇总 | 2026-02-01
        match = re.search(r'\| (\d{4}-\d{2}-\d{2})', first_line)
        if match:
            return match.group(1)
        return datetime.now().strftime('%Y-%m-%d')

    def _create_draft(self, title: str, content: str, thumb_id: str) -> str:
        """创建草稿"""
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.token}"
        data = {
            "articles": [{
                "title": title,
                "author": "AI Report",
                "digest": "AI 情报摘要...",
                "content": content,
                "thumb_media_id": thumb_id
            }]
        }

        resp = requests.post(
            url,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json; charset=utf-8'},
            proxies=getattr(config, 'PROXIES', None)
        )

        result = resp.json()

        if 'media_id' not in result:
            raise Exception(f"❌ 草稿创建失败: {result}")

        return result['media_id']
