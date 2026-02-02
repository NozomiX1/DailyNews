# DailyNews - Markdown 解析模块
# 将微信公众号文章 HTML 转换为 Markdown
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import re
from pathlib import Path
import sys
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))
import config

from .retry import retry_on_request_error

# 沿用配置中的 Headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": config.COOKIE
}


@retry_on_request_error(max_retries=3)
def parse_wechat_to_md(url: str) -> Optional[str]:
    """
    下载微信文章并转换为 Markdown

    Args:
        url: 微信文章链接

    Returns:
        Markdown 格式的文章内容，失败返回 None
    """
    print(f"    📥 正在下载: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            print(f"    ❌ 下载失败: {resp.status_code}")
            return None

        # 检查是否获取到有效内容
        if 'js_content' not in resp.text:
            print(f"    ❌ Cookie 可能已过期或无效")
            return None

        soup = BeautifulSoup(resp.text, 'html.parser')

        # ================= 提取正文 =================
        # 元数据（title, account, date_str, url）由调用方从 article dict 或 JSON 获取

        content_div = soup.find('div', {'id': 'js_content'})
        if not content_div:
            content_div = soup.find('div', {'class': 'rich_media_content'})

        if not content_div:
            return None

        # 修复图片：data-src -> src
        for img in content_div.find_all('img'):
            if 'data-src' in img.attrs:
                img['src'] = img['data-src']
            if 'style' in img.attrs:
                del img['style']

        # 移除重复的 logo 图片
        from collections import Counter
        img_urls = [img.get('src') or img.get('data-src', '')
                    for img in content_div.find_all('img')
                    if img.get('src') or img.get('data-src')]
        url_counts = Counter(img_urls)

        for img in content_div.find_all('img'):
            img_url = img.get('src') or img.get('data-src', '')
            if img_url and url_counts.get(img_url, 0) > 2:
                img.decompose()

        # 移除干扰标签
        for tag in content_div(['script', 'style', 'iframe']):
            tag.decompose()

        # 处理微信代码块格式
        for pre in content_div.find_all('pre', class_=re.compile(r'code-snippet__\w+')):
            for code in pre.find_all('code', recursive=False):
                code.insert_before('\n')

        # 转 Markdown
        body_md = md(str(content_div), heading_style="ATX", strip=['a', 'span'])

        # ================= 格式清理 =================
        # 清理多余空行
        body_md = re.sub(r'\n{3,}', '\n\n', body_md)

        # 移除空标题
        body_md = re.sub(r'^###\s*\n', '', body_md, flags=re.MULTILINE)
        body_md = re.sub(r'^###\s*$', '', body_md, flags=re.MULTILINE)

        # 修复图片被错误包裹加粗
        body_md = re.sub(r'\*\*(!\[.*?\]\([^)]+\))\*\*', r'\1', body_md)

        # 修复双重加粗
        body_md = re.sub(r'\*\*(.+?)\*\*\*\*(.+?)\*\*', r'**\1\2**', body_md)

        # 清理连续的反引号块标记
        body_md = re.sub(r'```\s*```\n', '```\n', body_md)
        body_md = re.sub(r'```\s*```\s*```', '```', body_md)

        # 移除代码块周围多余的反引号行
        body_md = re.sub(r'\n```\n```\n', '\n```\n', body_md)

        # 再次清理多余空行
        body_md = re.sub(r'\n{3,}', '\n\n', body_md)

        # 元数据（title, account, date_str, url）由调用方从 article dict 或 JSON 获取
        # 此处只返回文章正文内容，避免与 JSON metadata 和 LLM prompt 重复
        return body_md

    except Exception as e:
        print(f"    ❌ 解析异常: {e}")
        return None


# 测试入口
if __name__ == "__main__":
    # 测试单篇文章转换
    test_url = "https://mp.weixin.qq.com/s/acMM1zgxUmzlrFk6O7p7iw"
    result = parse_wechat_to_md(test_url)

    if result:
        print(result[:2000])
        print("\n✅ 转换成功！")
