#!/usr/bin/env python3
"""
发布 GitHub Trending 到微信公众号草稿箱
"""
import requests
import json
import re
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))
import config


class GitHubTrendingPublisher:
    """GitHub Trending 发布器"""

    def __init__(self):
        self.app_id = config.APP_ID
        self.app_secret = config.APP_SECRET
        self.token = self._get_access_token()

    def _get_access_token(self):
        """获取 access_token"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        resp = requests.get(url, proxies=getattr(config, 'PROXIES', None)).json()
        if 'access_token' in resp:
            return resp['access_token']
        else:
            raise Exception(f"获取 access_token 失败: {resp}")

    def _parse_github_trending(self, report_path):
        """解析 github_trending.md 文件"""
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()

        items = []

        # 按文章分割 (每篇以 ### 开头)
        articles = re.split(r'\n###\s+(\d+)\.\s+', content)

        for i in range(1, len(articles), 2):
            if i + 1 >= len(articles):
                break

            idx = articles[i]
            article = articles[i + 1]

            if not article.strip():
                continue

            # 提取项目名 (第一行)
            title_match = re.search(r'^([^\n]+)', article)
            title = title_match.group(1).strip() if title_match else f"项目 {idx}"

            # 提取语言、stars、今日
            lang_match = re.search(r'\*\*语言\*\*: ([^\n|]+)', article)
            language = lang_match.group(1).strip() if lang_match else "未知"

            stars_match = re.search(r'\*\*Stars\*\*: ([\d,]+)', article)
            stars = stars_match.group(1).strip() if stars_match else ""

            today_match = re.search(r'\*\*今日\*\*: \+([\d,]+)', article)
            today_stars = today_match.group(1).strip() if today_match else ""

            # 提取链接
            url_match = re.search(r'\*\*链接\*\*: (.+?)\n', article)
            url = url_match.group(1).strip() if url_match else ""

            # 提取摘要
            summary_match = re.search(r'\*\*摘要\*\*: (.+?)(?:\n---|\n\n###|\Z)', article, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else ""
            summary = re.sub(r'<br>', '\n', summary)

            if title:
                items.append({
                    'title': title,
                    'language': language,
                    'stars': stars,
                    'today_stars': today_stars,
                    'url': url,
                    'summary': summary
                })

        return items

    def generate_html(self, items):
        """生成 HTML 内容"""
        html_parts = ['<section style="font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;">']
        html_parts.append('<section style="margin-top: 20px;"></section>')

        for idx, item in enumerate(items, 1):
            # 标题
            title_html = f'<h3 style="margin-top: 30px; margin-bottom: 5px; font-size: 18px; font-weight: bold; color: #000;">{idx}. {item["title"]}</h3>'

            # 元信息
            meta_parts = []
            if item.get('language'):
                meta_parts.append(f'💻 语言：{item["language"]}')
            if item.get('stars'):
                meta_parts.append(f'⭐ Stars：{item["stars"]}')
            if item.get('today_stars'):
                meta_parts.append(f'🔥 今日：+{item["today_stars"]}')

            meta_first_line = '　'.join(meta_parts)

            meta_html = f'<div style="font-size: 13px; color: #888; margin-bottom: 10px; background: #f9f9f9; padding: 8px; border-radius: 4px;">{meta_first_line}<br><span style="display: inline-block; margin-top: 4px; color: #576b95; word-break: break-all;">🔗 链接：{item["url"]}</span></div>'

            summary_text = item["summary"].replace("\n", "<br>")
            summary_html = f'<p style="font-size: 16px; color: #333; line-height: 1.6; text-align: justify; margin-bottom: 25px;">{summary_text}</p>'

            divider = '<hr style="border: 0; border-top: 1px dashed #ddd; margin: 20px 0;" />' if idx < len(items) else ""
            html_parts.append(title_html + meta_html + summary_html + divider)

        html_parts.append("</section>")
        return "".join(html_parts)

    def publish_to_draft(self, report_path, title=None):
        """发布到草稿箱"""
        items = self._parse_github_trending(report_path)

        if not items:
            raise Exception("❌ 报告中没有找到任何项目")

        print(f"📊 解析到 {len(items)} 个项目")

        # 生成标题
        if not title:
            title = f"GitHub 热门项目 | {datetime.now().strftime('%Y-%m-%d')}"

        # 生成 HTML
        content_html = self.generate_html(items)

        # 创建草稿
        draft_id = self._create_draft(title, content_html, config.COVER_MEDIA_ID)

        return draft_id

    def _create_draft(self, title, content, thumb_id):
        """创建草稿"""
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.token}"
        data = {
            "articles": [{
                "title": title,
                "author": "GitHub Report",
                "digest": "今日 GitHub 热门项目精选...",
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


def main():
    import argparse

    parser = argparse.ArgumentParser(description="将 GitHub Trending 发布到微信公众号草稿箱")
    parser.add_argument("--date", default=None, help="日期 (YYYY-MM-DD)，默认今天")
    args = parser.parse_args()

    # 确定日期
    target_date = args.date or datetime.now().strftime("%Y-%m-%d")

    # 报告路径
    report_path = Path(__file__).parent.parent / "output" / target_date / "github_trending.md"

    if not report_path.exists():
        print(f"❌ 报告文件不存在: {report_path}")
        return

    print("=" * 50)
    print(f"📤 正在发布 GitHub Trending 到草稿箱")
    print(f"📄 报告文件: {report_path}")
    print("=" * 50)

    try:
        publisher = GitHubTrendingPublisher()
        draft_id = publisher.publish_to_draft(report_path)

        print(f"\n✅ 草稿创建成功！")
        print(f"📋 Media ID: {draft_id}")
        print(f"\n👉 请登录微信公众号后台查看草稿箱")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 发布失败: {e}")


if __name__ == "__main__":
    main()
