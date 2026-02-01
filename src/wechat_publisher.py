# DailyNews - 微信公众号发布模块
# 将生成的日报发布到草稿箱
import requests
import json
from pathlib import Path
import sys
import re
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))
import config


class WeChatPublisher:
    """微信公众号发布器"""

    def __init__(self, app_id=None, app_secret=None):
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

    def _calc_text_width(self, text):
        """计算文本宽度（以 1/3 单位为基准）"""
        width = 0
        for char in text:
            if char in '🌟⭐📍🕒🏷️':
                width += 4  # emoji = 4/3单位
            elif ord(char) > 127:  # 中文字符
                width += 3  # 中文字符 = 1单位
            else:  # 英文空格等
                width += 1  # 英文空格 = 1/3单位
        return width

    def generate_html(self, news_items):
        """
        从新闻列表生成 HTML（紧凑格式，无多余缩进）

        Args:
            news_items: 新闻列表，每个元素包含 {title, source, time, url, rating, tag, summary}

        Returns:
            HTML 字符串
        """
        html_parts = ['<section style="font-family: -apple-system, BlinkMacSystemFont, Arial, sans-serif;">']
        html_parts.append('<section style="margin-top: 20px;"></section>')

        for idx, item in enumerate(news_items, 1):
            # 紧凑的HTML，无多余缩进和换行
            title_html = f'<h3 style="margin-top: 30px; margin-bottom: 5px; font-size: 18px; font-weight: bold; color: #000;">{idx}. {item["title"]}</h3>'

            # 动态计算填充空格，让两行的emoji对齐
            prefix1 = f'📍 来源：{item["source"]}'
            prefix2 = f'⭐ 价值：{item["rating"]}' if item.get("rating") else ''

            width1 = self._calc_text_width(prefix1)
            width2 = self._calc_text_width(prefix2) if prefix2 else 0

            # 用英文空格补齐短的
            if width1 < width2:
                prefix1 += ' ' * (width2 - width1)
            elif width2 < width1:
                prefix2 += ' ' * (width1 - width2)

            # 拼接（各加一个中文空格分隔下一个emoji）
            meta_first_line = f'{prefix1}　🕒 {item["time"]}'

            meta_second_parts = []
            if item.get("rating"):
                meta_second_parts.append(prefix2)
            if item.get("tag"):
                meta_second_parts.append(f'　🏷️ 标签：{item["tag"]}')

            meta_second_line = ''
            if meta_second_parts:
                meta_second_line = '<br>' + ''.join(meta_second_parts)

            # 合并：第一行 + 第二行 + 链接
            meta_html = f'<div style="font-size: 13px; color: #888; margin-bottom: 10px; background: #f9f9f9; padding: 8px; border-radius: 4px;">{meta_first_line}{meta_second_line}<br><span style="display: inline-block; margin-top: 4px; color: #576b95; word-break: break-all;">🔗 链接：{item["url"]}</span></div>'

            summary_text = item["summary"].replace("\n", "<br>")
            summary_html = f'<p style="font-size: 16px; color: #333; line-height: 1.6; text-align: justify; margin-bottom: 25px;">{summary_text}</p>'

            divider = '<hr style="border: 0; border-top: 1px dashed #ddd; margin: 20px 0;" />' if idx < len(news_items) else ""
            html_parts.append(title_html + meta_html + summary_html + divider)

        html_parts.append("</section>")
        return "".join(html_parts)

    def _parse_daily_report(self, report_path):
        """
        解析 daily_report.md 文件

        Args:
            report_path: 报告文件路径

        Returns:
            解析后的新闻列表
        """
        with open(report_path, "r", encoding="utf-8") as f:
            content = f.read()

        news_items = []

        # 去掉开头的 header 部分，找到 "### 1." 开始的位置
        header_end = content.find('### 1.')
        if header_end != -1:
            content = content[header_end + 6:]  # +6 跳过 "### 1."

        # 按文章分割 (每篇以 ### 开头)
        articles = re.split(r'\n###\s+\d+\.\s+', content)

        for article in articles:
            if not article.strip():
                continue

            # 提取标题
            title_match = re.search(r'^(.+?)\n', article)
            title = title_match.group(1).strip() if title_match else "无标题"

            # 提取来源
            source_match = re.search(r'\*\*来源\*\*: (.+?) \|', article)
            source = source_match.group(1).strip() if source_match else "未知"

            # 提取时间
            time_match = re.search(r'\|\s*\*\*时间\*\*: (.+?)\n', article)
            time_str = time_match.group(1).strip() if time_match else ""

            # 提取链接
            url_match = re.search(r'\*\*链接\*\*: (.+?)\n', article)
            url = url_match.group(1).strip() if url_match else ""

            # 提取价值评分（清理可能包含的标签部分）
            rating_match = re.search(r'\*\*价值\*\*: (.+?)\n', article)
            rating = rating_match.group(1).strip() if rating_match else ""
            # 移除后面可能包含的 "**标签**: xxx" 部分
            rating = re.sub(r'\s*\*\*标签\*\*:.+', '', rating).strip()

            # 提取标签
            tag_match = re.search(r'\*\*标签\*\*: (.+?)\n', article)
            tag = tag_match.group(1).strip() if tag_match else ""

            # 提取摘要
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

    def publish_to_draft(self, report_path, title=None, target_date=None):
        """
        将 daily_report.md 发布到草稿箱

        Args:
            report_path: 报告文件路径
            title: 草稿标题，默认为 "AI 每日情报 | YYYY-MM-DD"
            target_date: 报告日期 (YYYY-MM-DD)，默认今天

        Returns:
            draft_id: 草稿 ID
        """
        # 解析报告
        news_items = self._parse_daily_report(report_path)

        if not news_items:
            raise Exception("❌ 报告中没有找到任何文章")

        print(f"📊 解析到 {len(news_items)} 篇文章")

        # 生成标题
        if not title:
            if not target_date:
                target_date = datetime.now().strftime("%Y-%m-%d")
            title = f"AI 每日情报 | {target_date}"

        # 生成 HTML
        content_html = self.generate_html(news_items)

        # 创建草稿
        draft_id = self._create_draft(title, content_html, config.COVER_MEDIA_ID)

        return draft_id

    def _create_draft(self, title, content, thumb_id):
        """
        创建草稿

        Args:
            title: 文章标题
            content: 文章内容 (HTML)
            thumb_id: 封面图 media_id

        Returns:
            media_id: 草稿 ID
        """
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.token}"
        data = {
            "articles": [{
                "title": title,
                "author": "AI Report",
                "digest": "今日AI热点摘要...",
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


# ================= 命令行入口 =================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="将日报发布到微信公众号草稿箱")
    parser.add_argument("--date", default=None, help="报告日期 (YYYY-MM-DD)，默认今天")
    args = parser.parse_args()

    # 确定日期
    target_date = args.date or datetime.now().strftime("%Y-%m-%d")

    # 报告路径
    report_path = config.OUTPUT_DIR / target_date / "daily_report.md"

    if not report_path.exists():
        print(f"❌ 报告文件不存在: {report_path}")
        print(f"   请先运行任务执行指南中的步骤 2-3 生成报告")
        return

    print("=" * 50)
    print(f"📤 正在发布报告到草稿箱")
    print(f"📄 报告文件: {report_path}")
    print("=" * 50)

    try:
        publisher = WeChatPublisher()
        draft_id = publisher.publish_to_draft(report_path, target_date=target_date)

        print(f"\n✅ 草稿创建成功！")
        print(f"📋 Media ID: {draft_id}")
        print(f"\n👉 请登录微信公众号后台查看草稿箱")
        print("=" * 50)

    except Exception as e:
        print(f"\n❌ 发布失败: {e}")
        print("\n可能的原因:")
        print("  1. APP_ID 或 APP_SECRET 配置错误")
        print("  2. COVER_MEDIA_ID 无效")
        print("  3. 网络连接问题")


if __name__ == "__main__":
    main()
