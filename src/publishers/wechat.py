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

import mistune
from premailer import transform as premailer_transform

from .base import BasePublisher
from .css_loader import get_inline_styles_css


# ==================== Markdown Renderer ====================

class WeChatRenderer(mistune.HTMLRenderer):
    """
    微信公众号渲染器 - 输出带 class 的 HTML
    样式由 CSS 文件定义，最后通过 premailer 转换为内联样式
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.footnotes = []
        self.footnote_index = 0

    def reset_footnotes(self):
        self.footnotes = []
        self.footnote_index = 0

    def build_footnotes(self):
        if not self.footnotes:
            return ''

        html = '<h4>引用链接</h4>\n<p class="footnotes">'
        for idx, title, url in self.footnotes:
            html += f'<code>[{idx}]</code>: <i>{url}</i><br/>'
        html += '</p>'
        return html

    def heading(self, text, level, **attrs):
        return f'<h{level}>{text}</h{level}>\n'

    def paragraph(self, text):
        return f'<p>{text}</p>\n'

    def strong(self, text):
        return f'<strong>{text}</strong>'

    def emphasis(self, text):
        return f'<em>{text}</em>'

    def link(self, text, url, title=None):
        # 微信内部链接直接渲染
        if url.startswith('https://mp.weixin.qq.com'):
            return f'<a href="{url}">{text}</a>'

        # 外部链接转换为脚注
        self.footnote_index += 1
        self.footnotes.append((self.footnote_index, text, url))
        return f'{text}<sup>[{self.footnote_index}]</sup>'

    def codespan(self, text):
        return f'<code>{text}</code>'

    def block_code(self, code, info=None):
        escaped = mistune.escape(code)
        return f'<pre class="code__pre"><code>{escaped}</code></pre>\n'

    def list(self, text, ordered, **attrs):
        tag = 'ol' if ordered else 'ul'
        return f'<{tag}>{text}</{tag}>\n'

    def list_item(self, text, **attrs):
        return f'<li>{text}</li>\n'

    def block_quote(self, text):
        return f'<blockquote>{text}</blockquote>\n'

    def thematic_break(self):
        return '<hr>\n'

    def image(self, alt, url, title=None):
        title_attr = f' title="{title}"' if title else ''
        return f'<img src="{url}" alt="{alt}"{title_attr}>'

    def table(self, header, body):
        return f'<table><thead>{header}</thead><tbody>{body}</tbody></table>\n'

    def table_head(self, text):
        return f'<tr>{text}</tr>\n'

    def table_body(self, text):
        return text

    def table_row(self, text):
        return f'<tr>{text}</tr>\n'

    def table_cell(self, text, **attrs):
        tag = 'th' if attrs.get('is_head') else 'td'
        return f'<{tag}>{text}</{tag}>'


def _preprocess_latex(text: str) -> str:
    """
    预处理 LaTeX 公式
    转换 $$...$$ 为 [formula]...[/formula]
    """
    # 块级公式
    text = re.sub(r'\$\$([^$]+)\$\$', r'[formula]\1[/formula]', text)
    # 行内公式
    text = re.sub(r'\$([^$]+)\$', r'[inline_formula]\1[/inline_formula]', text)
    return text


def _apply_inline_styles(html: str) -> str:
    """
    将 class-based HTML 转换为内联样式 HTML

    Args:
        html: 带 class 的 HTML

    Returns:
        带内联样式的 HTML（微信兼容）
    """
    css = get_inline_styles_css()

    # 包装为完整 HTML 文档供 premailer 处理
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>{css}</style>
    </head>
    <body>
        <section>{html}</section>
    </body>
    </html>
    """

    # premailer 转换
    result = premailer_transform(
        full_html,
        remove_classes=True,
        strip_important=True,
        keep_style_tags=False,
        cssutils_logging_level='CRITICAL'
    )

    # 提取 <section> 内容
    match = re.search(r'<section[^>]*>(.*?)</section>', result, re.DOTALL)
    if match:
        return match.group(1).strip()
    return html


def _create_wechat_markdown_parser():
    """创建配置好的 mistune Markdown 解析器"""
    renderer = WeChatRenderer(escape=False)
    md = mistune.create_markdown(renderer=renderer)

    def parse_with_styles(text):
        # 重置脚注
        renderer.reset_footnotes()
        # 预处理 LaTeX 公式
        preprocessed = _preprocess_latex(text)
        # 渲染为 class-based HTML
        html = md(preprocessed)
        # 添加脚注
        footnotes = renderer.build_footnotes()
        full_html = html + footnotes
        # 转换为内联样式
        return _apply_inline_styles(full_html)

    return parse_with_styles


# ==================== Publisher ====================


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
            # Use markdown conversion instead of simple newline replacement
            summary_html = self._simple_markdown_to_html(summary)
            summary_html = f'<div style="font-size: 16px; color: #333; line-height: 1.6; margin-bottom: 25px;">{summary_html}</div>'

            # Add highlights section for papers and use_cases/highlights for github
            highlights_html = ''
            if item_type == 'paper' and item.get('highlights'):
                highlights_html = f'<div style="font-size: 14px; color: #666; background: #f0f7ff; padding: 10px; border-radius: 4px; margin-bottom: 25px; border-left: 3px solid #3498db;"><strong>✨ 亮点:</strong><br>{item["highlights"]}</div>'
            elif item_type == 'github':
                # Use cases section
                if item.get('use_cases'):
                    highlights_html += f'<div style="font-size: 14px; color: #666; background: #f0f7ff; padding: 10px; border-radius: 4px; margin-bottom: 10px; border-left: 3px solid #3498db;"><strong>🎯 使用场景:</strong><br>{item["use_cases"]}</div>'
                # Highlights section
                if item.get('highlights'):
                    highlights_html += f'<div style="font-size: 14px; color: #666; background: #fff8e1; padding: 10px; border-radius: 4px; margin-bottom: 25px; border-left: 3px solid #f39c12;"><strong>✨ 亮点:</strong><br>{item["highlights"]}</div>'

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

            # Extract one-line summary from quote block format - preserve the label
            summary_match = re.search(r'> 🎯 \*\*一句话摘要\*\*：(.+?)(?=\n|$)', article)
            one_line_summary = summary_match.group(1).strip() if summary_match else ""

            # Extract all content after the link (from quote block to separator)
            # This captures: 一句话摘要 + 核心技术 + 实验数据 + 独家洞察 + 相关资源
            # Use greedy match to capture all sections until --- or next ###
            full_content_match = re.search(
                r'> 🎯 \*\*一句话摘要\*\*：\s*(.+)(?=\n---|\n\n###)',
                article,
                re.DOTALL
            )

            # Build the full summary with all sections
            full_summary = ""
            if full_content_match and full_content_match.group(1):
                full_content = full_content_match.group(1).strip()
                # Convert markdown headers to readable text
                # Note: The actual headers include the text after emoji, so we need to replace the entire header line
                # Handle both with and without space after emoji
                full_summary = re.sub(r'####\s+🔹\s*核心技术/实现逻辑', '\n\n#### **核心技术**', full_content, count=1)
                full_summary = re.sub(r'####\s+📊\s*实验数据/关键结论', '\n\n#### **实验数据**', full_summary, count=1)
                full_summary = re.sub(r'####\s+💡\s*独家洞察/局限性', '\n\n#### **独家洞察**', full_summary, count=1)
                full_summary = re.sub(r'####\s+🔗\s*相关资源', '\n\n#### **相关资源**', full_summary, count=1)
                # Clean up list items - convert markdown lists to proper markdown format with hyphens
                full_summary = re.sub(r'^\u2022\s+', '- ', full_summary, flags=re.MULTILINE)  # bullet character
                full_summary = re.sub(r'\n\u2022\s+', '\n- ', full_summary)  # bullet character after newline
                full_summary = re.sub(r'^-\s+\*\*', '- **', full_summary, flags=re.MULTILINE)
                full_summary = re.sub(r'\n-\s+\*\*', '\n- **', full_summary)
                # Also handle items with * instead of -
                full_summary = re.sub(r'\n\*\s+\*\*', '\n* **', full_summary)
                full_summary = full_summary.strip()
                # Preserve the "一句话摘要：" label (full_content already has the one-line summary, so just add label)
                full_summary = f'**一句话摘要：**{full_summary}'

            # If no detailed content, still preserve the label
            if not full_summary and one_line_summary:
                full_summary = f'**一句话摘要：**{one_line_summary}'

            summary = full_summary if full_summary else (f'**一句话摘要：**{one_line_summary}' if one_line_summary else "")

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

            # Extract tech stack (技术栈) - stop at next section (next **)
            tech_stack_match = re.search(r'(?:\*\*技术栈\*\*|技术栈):\s*(.+?)(?:\n\*\*|\n---|\n\n###|\Z)', article, re.DOTALL)
            tech_stack = tech_stack_match.group(1).strip() if tech_stack_match else ""
            # Clean up tech_stack text
            tech_stack = re.sub(r'\n+', ' ', tech_stack).strip()

            # Extract use cases (使用场景)
            use_cases_match = re.search(r'\*\*使用场景\*\*:\s*(.+?)(?:\n\*\*亮点\*\*|\n---|\n\n###|\Z)', article, re.DOTALL)
            use_cases = use_cases_match.group(1).strip() if use_cases_match else ""
            # Convert bullet points to clean text
            use_cases = re.sub(r'^\s*-\s*', '• ', use_cases, count=1)
            use_cases = re.sub(r'\n\s*-\s*', '<br>• ', use_cases)

            # Extract highlights (亮点)
            highlights_match = re.search(r'\*\*亮点\*\*:\s*(.+?)(?:\n---|\n\n###|\Z)', article, re.DOTALL)
            highlights = highlights_match.group(1).strip() if highlights_match else ""
            # Convert bullet points to clean text
            highlights = re.sub(r'^\s*-\s*', '• ', highlights, count=1)
            highlights = re.sub(r'\n\s*-\s*', '<br>• ', highlights)

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
                    'summary': summary,
                    'use_cases': use_cases,
                    'highlights': highlights
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
        # Split by "###" followed by optional emoji/chars, then number and dot
        sections = re.split(r'\n###\s*[^0-9]*?(\d+)\.\s+', content)

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

    def _simple_markdown_to_html(self, text: str) -> str:
        """
        轻量级 Markdown 转 HTML，用于 summary 格式化

        处理:
        - 四级标题 (####)
        - 加粗 (**text**)
        - 链接 ([text](url))
        - 嵌套列表项 (- 或 * 开头, 根据缩进判断层级)
        - 段落间距
        """
        if not text:
            return ""

        lines = text.split('\n')
        result = []

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            # 跳过空行
            if not stripped:
                result.append('<br>')
                i += 1
                continue

            # 处理四级标题
            if stripped.startswith('#### '):
                content = stripped[5:].strip()
                # 处理标题中的加粗
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                result.append(f'<h4 style="font-size: 16px; font-weight: bold; color: #555; text-align: center; margin: 20px 0 12px; padding: 8px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;">{content}</h4>')
                i += 1
                continue

            # 检测列表项 (支持 markdown 格式和 bullet 字符)
            list_match = re.match(r'^(\s*)([-*]|\u2022)\s+', line)
            if list_match:
                # 收集连续的列表项并构建嵌套结构
                list_items = []
                base_indent = None

                while i < len(lines):
                    line = lines[i]
                    list_match = re.match(r'^(\s*)([-*]|\u2022)\s+', line)

                    if not list_match:
                        break

                    indent_str = list_match.group(1)
                    content_start = list_match.end()
                    content = line[content_start:].rstrip()

                    # 计算缩进层级 (每4个空格为一级)
                    indent = len(indent_str)
                    if base_indent is None:
                        base_indent = indent

                    # 计算相对层级 (0-based)
                    level = 0
                    if indent > base_indent:
                        level = (indent - base_indent) // 4 + 1

                    # 处理内联格式
                    content = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', content)
                    content = re.sub(r'\*\*([^*]+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3498db;">\1</a>', content)

                    list_items.append({'level': level, 'content': content})
                    i += 1

                    # 检查下一行是否是列表的续行（缩进更多且不是新的列表项）
                    if i < len(lines):
                        next_line = lines[i]
                        if next_line.strip() and not re.match(r'^\s*[-*]|\u2020\s+', next_line):
                            next_indent = len(next_line) - len(next_line.lstrip())
                            if next_indent > indent:
                                # 这是续行，添加到当前项
                                continuation = next_line.rstrip()
                                continuation = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', continuation)
                                continuation = re.sub(r'\*\*([^*]+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', continuation)
                                continuation = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3498db;">\1</a>', continuation)
                                list_items[-1]['content'] += f' {continuation}'
                                i += 1

                # 生成嵌套列表 HTML
                result.append(self._render_nested_list(list_items))
                continue

            # 处理普通段落
            processed = re.sub(r'\*\*(.+?)\*\*([：:、,，.。；;])', r'<strong style="color: #2c3e50; font-weight: 600;">\1\2</strong>', stripped)
            processed = re.sub(r'\*\*([^*]+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', processed)
            processed = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3498db;">\1</a>', processed)
            result.append(f'<p style="margin: 8px 0; line-height: 1.6;">{processed}</p>')
            i += 1

        return ''.join(result)

    def _render_nested_list(self, items: List[Dict]) -> str:
        """
        渲染嵌套列表结构为 HTML

        Args:
            items: 列表项字典列表，每个包含 'level' 和 'content'

        Returns:
            HTML 字符串
        """
        if not items:
            return ''

        def build_tree(items):
            """将扁平列表项树结构"""
            if not items:
                return []

            root = []
            stack = [(root, -1)]  # (parent_list, level)

            for item in items:
                level = item['level']
                content = item['content']

                node = {'content': content, 'children': []}

                # 找到正确的父级
                while stack and stack[-1][1] >= level:
                    stack.pop()

                if stack:
                    stack[-1][0].append(node)
                else:
                    root.append(node)

                # 将此节点作为可能的父级
                stack.append((node['children'], level))

            return root

        def render_items(nodes, is_root=True):
            """递归渲染列表项"""
            html = []
            for node in nodes:
                content = node['content']
                children = node['children']

                if children:
                    children_html = render_items(children, is_root=False)
                    # 如果内容只有冒号或为空，只渲染子列表
                    if not content or content in [':', '：']:
                        html.append(f'<li style="margin: 5px 0; line-height: 1.6;">{children_html}</li>')
                    else:
                        html.append(f'<li style="margin: 5px 0; line-height: 1.6;">{content}<ul style="margin: 5px 0; padding-left: 20px;">{children_html}</ul></li>')
                else:
                    html.append(f'<li style="margin: 5px 0; line-height: 1.6;">{content}</li>')
            return ''.join(html)

        tree = build_tree(items)
        items_html = render_items(tree)
        return f'<ul style="margin: 5px 0; padding-left: 20px;">{items_html}</ul>'

    def _markdown_to_html(self, markdown_text: str) -> str:
        """
        将 Markdown 转换为微信公众号 HTML - CSS 驱动版本
        使用 mistune 渲染，通过 premailer 将 CSS 转为内联样式
        """
        # 获取解析器（带缓存）
        if not hasattr(self, '_markdown_parser'):
            self._markdown_parser = _create_wechat_markdown_parser()

        # 预处理：跳过第一个 h1（因为已在标题处显示）
        lines = markdown_text.split('\n')
        first_h1_skipped = False
        processed_lines = []

        for line in lines:
            # 跳过 --- 分隔线
            if line.strip() == '---':
                continue
            # 跳过第一个 h1
            if not first_h1_skipped and re.match(r'^#\s+', line):
                first_h1_skipped = True
                continue
            processed_lines.append(line)

        processed_text = '\n'.join(processed_lines)
        return self._markdown_parser(processed_text)

    def _generate_paper_html(self, paper_data: Dict) -> str:
        """
        生成单篇论文的精美 HTML（CSS 驱动）

        Args:
            paper_data: 论文数据字典

        Returns:
            HTML 字符串
        """
        english_title = paper_data.get('english_title', paper_data.get('title', ''))

        html_parts = []
        html_parts.append(f'<h1>{english_title}</h1>')

        # 元信息
        meta_parts = []
        if paper_data.get('arxiv_url'):
            meta_parts.append(f'📄 论文：<a href="{paper_data["arxiv_url"]}">{paper_data["arxiv_url"]}</a>')
        elif paper_data.get('arxiv_id'):
            url = f"https://arxiv.org/abs/{paper_data['arxiv_id']}"
            meta_parts.append(f'📄 论文：<a href="{url}">{url}</a>')
        if paper_data.get('org'):
            meta_parts.append(f'🔬 <strong>机构：</strong>{paper_data["org"]}')
        if paper_data.get('tags'):
            meta_parts.append(f'🏷️ <strong>标签：</strong>{paper_data["tags"]}')

        stats = []
        if paper_data.get('score'):
            stats.append(f'📊 {paper_data["score"]}')
        if paper_data.get('upvotes'):
            stats.append(f'👍 {paper_data["upvotes"]}')
        if paper_data.get('stars'):
            stats.append(f'🌟 {paper_data["stars"]}')

        if meta_parts or stats:
            html_parts.append('<blockquote>')
            html_parts.append('<p>' + '<br>'.join(meta_parts) + '</p>')
            if stats:
                html_parts.append('<p>' + ' | '.join(stats) + '</p>')
            html_parts.append('</blockquote>')

        if paper_data.get('intro'):
            html_parts.append(f'<p><em>{paper_data["intro"]}</em></p>')

        # 正文
        body_html = self._markdown_to_html(paper_data['body'])
        html_parts.append(body_html)

        full_html = '<section>' + '\n'.join(html_parts) + '</section>'
        return _apply_inline_styles(full_html)

    def _generate_simple_paper_html(self, paper: Dict) -> str:
        """
        生成简化版论文 HTML（CSS 驱动）

        Args:
            paper: 简化论文数据

        Returns:
            HTML 字符串
        """
        html_parts = []
        html_parts.append(f'<h1>{paper.get("title", "未知")}</h1>')

        meta_parts = []
        if paper.get('arxiv_id'):
            url = f"https://arxiv.org/abs/{paper['arxiv_id']}"
            meta_parts.append(f'📄 <strong>论文：</strong><a href="{url}">{paper["arxiv_id"]}</a>')
        if paper.get('org'):
            meta_parts.append(f'🔬 <strong>机构：</strong>{paper["org"]}')
        if paper.get('tags'):
            meta_parts.append(f'🏷️ <strong>标签：</strong>{paper["tags"]}')

        if meta_parts:
            html_parts.append('<blockquote><p>' + '<br>'.join(meta_parts) + '</p></blockquote>')

        analysis = paper.get('analysis', '')
        if analysis:
            html_parts.append(f'<p>{analysis}</p>')

        full_html = '<section>' + '\n'.join(html_parts) + '</section>'
        return _apply_inline_styles(full_html)

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
