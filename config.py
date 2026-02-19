# DailyNews 配置文件
import os
from pathlib import Path

# ================= 项目路径 =================
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
SUMMARIES_DIR = DATA_DIR / "summaries"
OUTPUT_DIR = PROJECT_ROOT / "output"

# 按日期组织的子目录名称
DATE_DIR_ARTICLES = "articles"     # {date}/articles/
DATE_DIR_TRENDING = "trending"     # {date}/trending/
DATE_DIR_PAPERS = "papers"         # {date}/papers/
DATE_DIR_PDF_DOWNLOADS = "pdf_downloads"  # {date}/papers/pdf_downloads/
DATE_DIR_README_FILES = "readme_files"  # {date}/trending/readme_files/

# ================= 微信配置 =================

# 微信管理平台 Token（从环境变量读取）
TOKEN = os.environ.get("WECHAT_TOKEN", "")

# Cookie (lazy load - only validates when accessed)
_COOKIE = None

def get_cookie():
    """Get WeChat cookie, raising error only when actually needed."""
    global _COOKIE
    if _COOKIE is None:
        _COOKIE = os.environ.get("WECHAT_COOKIE", "")
    return _COOKIE

def require_cookie():
    """Get cookie with validation - call this when WeChat task is used."""
    cookie = get_cookie()
    if not cookie:
        raise ValueError("WECHAT_COOKIE 环境变量未设置")
    return cookie

# For backwards compatibility with existing imports
COOKIE = property(get_cookie) if False else ""  # Placeholder, use get_cookie() instead

# 目标公众号列表
TARGET_ACCOUNTS = ["机器之心", "新智元", "量子位"]

# 请求头 (lazy load)
def get_headers():
    """Get WeChat API headers with cookie, only loaded when needed."""
    return {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie": get_cookie(),
        "Referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=10&token=" + TOKEN + "&lang=zh_CN",
        "X-Requested-With": "XMLHttpRequest"
    }

# For backwards compatibility
HEADERS = None

BASE_URL = "https://mp.weixin.qq.com"

# ================= 缓存配置 =================
# True=缓存模式(保存数据到data/), False=无缓存模式(仅内存流转)
ENABLE_CACHE = False
FAKEID_CACHE_FILE = PROJECT_ROOT / "fakeid_cache.json"

# ================= GLM 模型配置 =================
# API Key 从环境变量读取，支持 ZHIPU_API_KEY 或 GLM_API_KEY
GLM_API_KEY = os.environ.get("ZHIPU_API_KEY") or os.environ.get("GLM_API_KEY")
GLM_BASE_URL = "https://open.bigmodel.cn/api/coding/paas/v4"
GLM_MODEL = "glm-4.7"  # 默认模型
GLM_MAX_TOKENS = 65536
GLM_ENABLE_THINKING = True
