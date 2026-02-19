# DailyNews 配置文件
import os
from pathlib import Path

# ================= 项目路径 =================
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
SUMMARIES_DIR = DATA_DIR / "summaries"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOGS_DIR = PROJECT_ROOT / "logs"
CACHE_DIR = PROJECT_ROOT

# 按日期组织的子目录名称
DATE_DIR_ARTICLES = "articles"     # {date}/articles/
DATE_DIR_TRENDING = "trending"     # {date}/trending/
DATE_DIR_PAPERS = "papers"         # {date}/papers/
DATE_DIR_PDF_DOWNLOADS = "pdf_downloads"  # {date}/papers/pdf_downloads/
DATE_DIR_README_FILES = "readme_files"  # {date}/trending/readme_files/

# ================= 微信配置 =================

# 从 cookie1.txt 读取 Cookie
def load_cookie():
    cookie_path = PROJECT_ROOT / "cookie1.txt"
    try:
        with open(cookie_path, "r", encoding="utf-8") as f:
            cookie = f.read().strip()
            if not cookie:
                raise ValueError("cookie1.txt is empty")
            return cookie
    except FileNotFoundError:
        raise FileNotFoundError("❌ 找不到 cookie1.txt 文件")

# 微信管理平台 Token
TOKEN = "1428445068"

# Cookie
COOKIE = load_cookie()

# 目标公众号列表
TARGET_ACCOUNTS = ["机器之心", "新智元", "量子位"]

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Cookie": COOKIE,
    "Referer": "https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&createType=10&token=" + TOKEN + "&lang=zh_CN",
    "X-Requested-With": "XMLHttpRequest"
}

BASE_URL = "https://mp.weixin.qq.com"

# ================= 缓存配置 =================
# True=缓存模式(保存数据到data/), False=无缓存模式(仅内存流转)
ENABLE_CACHE = False
FAKEID_CACHE_FILE = PROJECT_ROOT / "fakeid_cache.json"

# ================= GLM 模型配置 =================
# API Key 从环境变量读取，请设置 ZHIPU_API_KEY 环境变量
GLM_API_KEY = os.environ.get("ZHIPU_API_KEY")
GLM_BASE_URL = "https://open.bigmodel.cn/api/coding/paas/v4"
GLM_MODEL = "glm-4.7"  # 默认模型
GLM_MAX_TOKENS = 65536
GLM_ENABLE_THINKING = True
GLM_TEMPERATURE = 1.0
