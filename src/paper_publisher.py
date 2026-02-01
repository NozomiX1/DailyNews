#!/usr/bin/env python3
"""
发布每日论文到微信公众号草稿箱
每篇论文发布为一个独立的草稿
"""
import requests
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))
import config


class PaperPublisher:
    """论文发布器 - 每篇论文一个草稿"""

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

    def _parse_analysis_file(self, analysis_path):
        """解析单篇论文的分析文件"""
        with open(analysis_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取标题 (第一个 # 后面的内容)
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else Path(analysis_path).stem

        # 提取论文原标题 (从第一行的《》中提取)
        paper_title_match = re.search(r'《(.+?)》', content.split('---')[0] if '---' in content else content)
        paper_title = paper_title_match.group(1) if paper_title_match else ''

        # 提取元数据 (arXiv ID, 组织, Stars, Upvotes, 得分, 标签)
        arxiv_id = re.search(r'\*\*arXiv ID\*\*:\s*(.+)', content)
        org = re.search(r'\*\*组织\*\*:\s*(.+)', content)
        stars = re.search(r'\*\*GitHub Stars\*\*:\s*(.+)', content)
        upvotes = re.search(r'\*\*Upvotes\*\*:\s*(.+)', content)
        score = re.search(r'\*\*得分\*\*:\s*(.+)', content)
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
            'paper_title': paper_title,
            'intro': intro,
            'arxiv_id': arxiv_id.group(1).strip() if arxiv_id else '',
            'org': org.group(1).strip() if org else '',
            'stars': stars.group(1).strip() if stars else '',
            'upvotes': upvotes.group(1).strip() if upvotes else '',
            'score': score.group(1).strip() if score else '',
            'tags': tags.group(1).strip() if tags else '',
            'body': body
        }

    def _markdown_to_html(self, markdown_text):
        """将 Markdown 转换为微信公众号 HTML - 直接解析并生成带样式的 HTML"""
        lines = markdown_text.split('\n')
        html_lines = []
        skip_first_h1 = True  # 跳过第一个 h1（因为已在标题处显示）

        # 删除第一段（已作为 intro 显示）
        first_para_removed = False

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

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
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                html_lines.append(f'<h4 style="font-size: 16px; font-weight: bold; color: #555; text-align: left; margin: 15px 0 10px;">{content}</h4>')
                i += 1
                continue

            # 处理三级标题
            match = re.match(r'^###\s+(.+)$', line)
            if match:
                content = match.group(1)
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                html_lines.append(f'<h3 style="font-size: 18px; font-weight: bold; color: #34495e; text-align: left; margin: 20px 0 12px; padding-left: 10px; border-left: 4px solid #3498db;">{content}</h3>')
                i += 1
                continue

            # 处理二级标题
            match = re.match(r'^##\s+(.+)$', line)
            if match:
                content = match.group(1)
                content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                html_lines.append(f'<h2 style="font-size: 20px; font-weight: bold; color: #2c3e50; text-align: center; margin: 30px 0 15px; padding: 10px 0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0;">{content}</h2>')
                i += 1
                continue

            # 处理一级标题（跳过第一个之后的其他 h1）
            match = re.match(r'^#\s+(.+)$', line)
            if match:
                content = match.group(1)
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

            # 收集列表（多行）
            list_items = []
            list_start_idx = i
            list_type = None  # 'ul' or 'ol'
            base_indent = None

            while i < len(lines):
                line = lines[i]
                stripped_i = line.strip()

                # 空行结束列表
                if not stripped_i:
                    break

                # 检测列表项
                ul_match = re.match(r'^([\s]*)[\*\-]\s+', line)
                ol_match = re.match(r'^([\s]*)\d+\.\s+', line)

                # 确定使用哪个匹配对象
                match_obj = None
                if ul_match:
                    match_obj = ul_match
                elif ol_match:
                    match_obj = ol_match

                if match_obj:
                    indent = len(match_obj.group(1))

                    # 确定列表类型
                    if list_type is None:
                        list_type = 'ul' if ul_match else 'ol'
                        base_indent = indent

                    # 检测是否是不同类型的列表（需要重新开始）
                    current_is_ul = ul_match is not None
                    if (current_is_ul and list_type != 'ul') or (not current_is_ul and list_type == 'ul'):
                        if list_items:
                            break  # 切换列表类型

                    # 使用 match 对象的 span 来截取字符串
                    start, end = match_obj.span()
                    content = line[end:].strip()

                    # 跳过空内容
                    if not content:
                        i += 1
                        continue

                    # 处理内联格式
                    content = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', content)
                    content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3498db;">\1</a>', content)

                    # 根据缩进判断是否嵌套
                    is_nested = indent > base_indent
                    style = 'margin: 6px 0; line-height: 1.8; color: #333;' if is_nested else 'margin: 8px 0; line-height: 1.8; color: #333;'

                    if is_nested:
                        # 嵌套列表项（使用不同样式）
                        list_items.append(f'<li style="{style} padding-left: 10px;">{content}</li>')
                    else:
                        list_items.append(f'<li style="{style}">{content}</li>')

                    i += 1
                else:
                    # 非列表行，检查是否是前一个列表项的续行
                    if list_items and (line.startswith('    ') or line.startswith('\t')):
                        # 续行，追加到上一个列表项
                        continuation = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', stripped)
                        continuation = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3498db;">\1</a>', continuation)
                        # 移除最后一个 </li> 并添加续行
                        last_item = list_items[-1]
                        list_items[-1] = last_item.replace('</li>', f' {continuation}</li>')
                        i += 1
                    else:
                        break

            # 输出列表
            if list_items:
                if list_type == 'ul':
                    style = 'margin: 15px 0; padding-left: 20px;'
                else:
                    style = 'margin: 15px 0; padding-left: 25px;'
                html_lines.append(f'<{list_type} style="{style}">')
                html_lines.extend(list_items)
                html_lines.append(f'</{list_type}>')
                continue  # i 已经在列表处理中更新了

            # 处理普通段落
            if stripped:
                # 处理粗体
                line = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color: #2c3e50; font-weight: 600;">\1</strong>', line)
                # 处理链接
                line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" style="color: #3498db;">\1</a>', line)
                html_lines.append(f'<p style="font-size: 15px; color: #333; line-height: 1.9; margin-bottom: 10px; text-align: justify;">{line}</p>')

            i += 1

        return '\n'.join(html_lines)

    def generate_html(self, paper_data):
        """生成单篇论文的 HTML"""
        # 容器样式
        container = '<section style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, Helvetica, Arial, sans-serif; max-width: 677px; margin: 0 auto; padding: 20px 0;">'

        # 标题头部
        title_html = f'''
<div style="text-align: center; margin-bottom: 25px;">
    <h1 style="font-size: 24px; font-weight: bold; color: #1a1a1a; margin: 0 0 15px; line-height: 1.4;">{paper_data['title']}</h1>
    {f'<p style="font-size: 14px; color: #666; margin: 5px 0 0;">《{paper_data["paper_title"]}》</p>' if paper_data.get('paper_title') else ''}
</div>
'''

        # 元信息卡片
        meta_html = '<div style="background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%); padding: 15px; border-radius: 8px; margin-bottom: 25px; font-size: 14px; color: #555;">'

        if paper_data.get('arxiv_id'):
            arxiv_url = f"https://arxiv.org/abs/{paper_data['arxiv_id']}"
            meta_html += f'<div style="margin-bottom: 8px;">📄 <strong>论文：</strong><a href="{arxiv_url}" style="color: #3498db; text-decoration: none;">{paper_data["arxiv_id"]}</a></div>'
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
            stats_row += f'<span style="display: inline-block;">⭐ {paper_data["stars"]}</span>'
        if stats_row:
            meta_html += f'<div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #d0d7de;">{stats_row}</div>'

        meta_html += '</div>'

        # 摘要段落
        intro_html = ''
        if paper_data.get('intro'):
            intro_html = f'<p style="font-size: 15px; color: #444; line-height: 1.8; margin-bottom: 20px; text-align: justify; padding: 12px; background: #f9f9f9; border-radius: 6px;">{paper_data["intro"]}</p>'

        # 分隔线
        divider = '<hr style="border: none; border-top: 1px solid #e0e0e0; margin: 25px 0;">'

        # 正文
        body_html = self._markdown_to_html(paper_data['body'])

        # 结尾
        footer = '''
<div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #e0e0e0; text-align: center; color: #888; font-size: 13px;">
    <p style="margin: 0;">📝 由 AI 精读整理 | 仅供学习交流</p>
</div>
</section>
'''

        return container + title_html + meta_html + intro_html + divider + body_html + footer

    def publish_single_paper(self, analysis_path):
        """发布单篇论文到草稿箱"""
        paper_data = self._parse_analysis_file(analysis_path)

        print(f"📄 正在发布: {paper_data['title']}")

        # 生成标题 (去除过长标题)
        title = paper_data['title']
        if len(title) > 50:
            title = title[:47] + '...'

        # 生成 HTML
        content_html = self.generate_html(paper_data)

        # 创建草稿
        draft_id = self._create_draft(title, content_html, config.COVER_MEDIA_ID)

        return draft_id, paper_data['title']

    def publish_all_papers(self, date_str):
        """发布某一天的所有论文"""
        project_root = Path(__file__).parent.parent
        output_dir = project_root / "output" / date_str

        if not output_dir.exists():
            raise Exception(f"输出目录不存在: {output_dir}")

        # 找到所有分析文件 (排除 _summary.md)
        analysis_files = [
            f for f in output_dir.glob("*_analysis.md")
            if not f.name.startswith('_')
        ]

        if not analysis_files:
            print(f"❌ 没有找到分析文件: {output_dir}")
            return

        print(f"📊 找到 {len(analysis_files)} 篇论文分析")

        results = []
        for i, analysis_file in enumerate(analysis_files, 1):
            print(f"\n[{i}/{len(analysis_files)}] {analysis_file.name}")
            try:
                draft_id, title = self.publish_single_paper(analysis_file)
                results.append({'file': analysis_file.name, 'draft_id': draft_id, 'title': title, 'status': 'success'})
                print(f"  ✅ 成功 - Media ID: {draft_id}")
            except Exception as e:
                results.append({'file': analysis_file.name, 'error': str(e), 'status': 'failed'})
                print(f"  ❌ 失败 - {e}")

        return results

    def _create_draft(self, title, content, thumb_id):
        """创建草稿"""
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.token}"
        data = {
            "articles": [{
                "title": title,
                "author": "Paper Analysis",
                "digest": f"{title[:50]}...",
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
            raise Exception(f"草稿创建失败: {result}")

        return result['media_id']


def main():
    import argparse

    parser = argparse.ArgumentParser(description="将论文精读发布到微信公众号草稿箱")
    parser.add_argument("--date", default=None, help="日期 (YYYY-MM-DD)，默认昨天")
    parser.add_argument("--file", default=None, help="单个分析文件路径")
    args = parser.parse_args()

    # 确定日期
    if args.file:
        # 单个文件模式
        target_date = None
    else:
        if args.date:
            target_date = args.date
        else:
            # 默认昨天
            target_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    publisher = PaperPublisher()

    print("=" * 60)
    print("📤 每日论文精读发布到草稿箱")
    if target_date:
        print(f"📅 日期: {target_date}")
    if args.file:
        print(f"📄 文件: {args.file}")
    print("=" * 60)

    try:
        if args.file:
            # 发布单个文件
            draft_id, title = publisher.publish_single_paper(args.file)
            print(f"\n✅ 草稿创建成功！")
            print(f"📋 Media ID: {draft_id}")
            print(f"📄 标题: {title}")
        else:
            # 发布所有论文
            results = publisher.publish_all_papers(target_date)

            success_count = sum(1 for r in results if r['status'] == 'success')
            print(f"\n{'=' * 60}")
            print(f"✅ 完成: {success_count}/{len(results)} 篇论文发布成功")
            print(f"👉 请登录微信公众号后台查看草稿箱")
            print("=" * 60)

    except Exception as e:
        print(f"\n❌ 发布失败: {e}")


if __name__ == "__main__":
    main()
