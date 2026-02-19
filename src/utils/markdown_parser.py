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


class WeChatContentError(requests.exceptions.RequestException):
    """微信文章内容获取失败异常（触发重试）"""
    pass

# 沿用配置中的 Headers (lazy load)
def _get_headers():
    """Get headers with cookie, only loaded when needed."""
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": config.get_cookie()
    }

# For backwards compatibility
HEADERS = None


@retry_on_request_error(max_retries=3, delay=2.0, backoff=2.0)
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
        resp = requests.get(url, headers=_get_headers(), timeout=30)
        if resp.status_code != 200:
            raise WeChatContentError(f"HTTP {resp.status_code}")

        # 检查是否获取到有效内容
        if 'js_content' not in resp.text:
            # 检查是否是速率限制（需要重试）
            rate_limit_indicators = ['访问过于频繁', '请在微信客户端', 'anti-spider', 'antispider']
            is_rate_limit = any(indicator in resp.text for indicator in rate_limit_indicators)

            if is_rate_limit:
                raise WeChatContentError("可能遇到速率限制，稍后重试")
            else:
                # 内容确实不存在（文章删除/违规等），不重试
                print(f"      ⚠️ 文章内容不可用（可能已删除或需特殊权限）")
                return None

        soup = BeautifulSoup(resp.text, 'html.parser')

        # ================= 提取正文 =================
        # 元数据（title, account, date_str, url）由调用方从 article dict 或 JSON 获取

        content_div = soup.find('div', {'id': 'js_content'})
        if not content_div:
            content_div = soup.find('div', {'class': 'rich_media_content'})

        if not content_div:
            raise WeChatContentError("未找到文章内容区域")

        # 修复图片：data-src -> src
        for img in content_div.find_all('img'):
            if 'data-src' in img.attrs:
                img['src'] = img['data-src']
            if 'style' in img.attrs:
                del img['style']

        # 移除重复的 logo 图片
        from collections import Counter
        all_imgs = content_div.find_all('img')

        # 先收集所有图片 URL（在修改 DOM 之前）
        img_urls = []
        for img in all_imgs:
            if img.attrs:  # 检查 attrs 不是 None
                src = img.get('src') or img.get('data-src', '')
                if src:
                    img_urls.append(src)

        url_counts = Counter(img_urls)

        # 先收集要删除的图片元素（避免迭代时修改 DOM）
        imgs_to_remove = []
        for img in all_imgs:
            if img.attrs:  # 检查 attrs 不是 None
                img_url = img.get('src') or img.get('data-src', '')
                if img_url and url_counts.get(img_url, 0) > 2:
                    imgs_to_remove.append(img)

        # 统一删除
        for img in imgs_to_remove:
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
