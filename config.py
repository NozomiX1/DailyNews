# DailyNews 配置文件
import os
from pathlib import Path

# ================= 项目路径 =================
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data" / "articles"
OUTPUT_DIR = PROJECT_ROOT / "output"
CACHE_DIR = PROJECT_ROOT

# ================= 微信爬取配置 =================

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
TOKEN = "1987896076"

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

# ================= 微信发布配置 =================

# 公众号 AppID 和 AppSecret
APP_ID = "wx5cd7b21241569ee4"
APP_SECRET = "28f082df74ed1b78163c8df2e9e8906b"

# 永久封面图 Media ID
COVER_MEDIA_ID = "eczXpKmOOMk1jO1pgqsdcSf22OGzinl4vNpgd_68ZSmv0qrD_aMbB2LdUEByVor_"

# 代理配置（用于微信公众号 API，绕过 IP 白名单限制）
# 设置为 None 则不使用代理，设置为 "http://127.0.0.1:1082" 使用本地代理
PROXIES = {
    "http": "http://127.0.0.1:1082",
    "https": "http://127.0.0.1:1082",
}

# ================= 缓存配置 =================

FAKEID_CACHE_FILE = PROJECT_ROOT / "fakeid_cache.json"

# ================= 广告关键词 =================
AD_KEYWORDS = [
    "广告", "推广", "赞助", "合作", "招商",
    "课程", "限时优惠", "立即购买", "扫码报名",
    "广告位", "商务合作", "诚招代理"
]
