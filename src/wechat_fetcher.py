# DailyNews - 文章爬取模块
import requests
import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))
import config
import markdown_parser

# ================= fakeid 缓存管理 =================

def load_fakeid_cache():
    """加载 fakeid 缓存"""
    if config.FAKEID_CACHE_FILE.exists():
        try:
            with open(config.FAKEID_CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_fakeid_cache(cache):
    """保存 fakeid 缓存"""
    with open(config.FAKEID_CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_fakeid_with_cache(account_name):
    """
    获取公众号 fakeid，优先使用缓存
    """
    cache = load_fakeid_cache()

    # 检查缓存
    if account_name in cache:
        print(f"✅ 从缓存获取 fakeid: {account_name}")
        return cache[account_name]

    # 缓存未命中，调用 API
    print(f"🔍 正在查询公众号: {account_name}")
    fakeid = get_fakeid(account_name)

    if fakeid:
        # 保存到缓存
        cache[account_name] = fakeid
        save_fakeid_cache(cache)
        print(f"💾 已缓存 fakeid: {account_name}")

    return fakeid

def get_fakeid(name):
    """
    搜索公众号，获取其 fakeid
    API: /cgi-bin/searchbiz
    """
    url = f"{config.BASE_URL}/cgi-bin/searchbiz"
    params = {
        "action": "search_biz",
        "begin": "0",
        "count": "5",
        "query": name,
        "token": config.TOKEN,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }

    try:
        resp = requests.get(url, headers=config.HEADERS, params=params)
        data = resp.json()

        if data.get("base_resp", {}).get("ret") != 0:
            print(f"❌ 搜索失败: {data}")
            return None

        for item in data.get("list", []):
            if item["nickname"] == name:
                print(f"✅ 找到公众号 [{name}], fakeid: {item['fakeid']}")
                return item["fakeid"]

        print(f"❌ 未找到公众号: {name}")
        return None
    except Exception as e:
        print(f"❌ get_fakeid 异常: {e}")
        return None

# ================= 文章爬取 =================

def get_published_articles(fakeid, page=0):
    """
    获取已发布文章列表
    """
    url = f"{config.BASE_URL}/cgi-bin/appmsgpublish"

    params = {
        "sub": "list",
        "search_field": "null",
        "begin": str(page * 5),
        "count": "5",
        "query": "",
        "fakeid": fakeid,
        "type": "101_1",
        "free_publish_type": "1",
        "sub_action": "list_ex",
        "token": config.TOKEN,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1"
    }

    try:
        resp = requests.get(url, headers=config.HEADERS, params=params)
        data = resp.json()

        if data.get("base_resp", {}).get("ret") != 0:
            print(f"❌ 接口报错: {data}")
            return []

        # 解析外层 list
        publish_page = json.loads(data.get("publish_page", "{}"))
        publish_list = publish_page.get("publish_list", [])

        articles_result = []

        for i, item in enumerate(publish_list):
            try:
                # 解包核心数据
                publish_info_str = item.get("publish_info", "{}")
                publish_info = json.loads(publish_info_str)

                # 提取时间 (三级查找策略)
                sent_time = 0

                # 策略 A: type=101 (群发) -> sent_info.time
                if "sent_info" in publish_info and "time" in publish_info["sent_info"]:
                    sent_time = publish_info["sent_info"]["time"]

                # 策略 B: type=1 (发布) -> publish_info.create_time
                elif "publish_info" in publish_info and "create_time" in publish_info["publish_info"]:
                    sent_time = publish_info["publish_info"]["create_time"]

                # 策略 C: 兜底 -> 从第一篇文章拿 create_time
                if sent_time == 0:
                    appmsgex = publish_info.get("appmsgex", [])
                    if appmsgex:
                        sent_time = appmsgex[0].get("create_time", 0)

                if sent_time == 0:
                    sent_time = time.time()

                # 提取文章列表
                appmsg_list = publish_info.get("appmsgex", [])
                if not appmsg_list:
                    appmsg_list = publish_info.get("appmsg_info", [])

                if not appmsg_list:
                    continue

                for index, msg in enumerate(appmsg_list):
                    title = msg.get("title")
                    link = msg.get("link")
                    if not link:
                        link = msg.get("content_url")

                    if title and link:
                        time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(sent_time))

                        articles_result.append({
                            "title": title,
                            "link": link,
                            "timestamp": sent_time,
                            "time_str": time_str,
                            "digest": msg.get("digest", ""),
                            "is_headline": index == 0
                        })

            except Exception as item_err:
                print(f"❌ 解析第 {i+1} 条失败: {item_err}")
                continue

        return articles_result

    except Exception as e:
        print(f"❌ get_published_articles 异常: {e}")
        return []


def fetch_articles_for_date(account_name, target_date):
    """
    爬取指定日期的文章
    """
    fakeid = get_fakeid_with_cache(account_name)
    if not fakeid:
        print(f"❌ 无法获取 {account_name} 的 fakeid，跳过")
        return []

    # 计算时间窗口
    target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    today_0am = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    target_0am = datetime.combine(target_date, datetime.min.time())
    next_day_0am = target_0am + timedelta(days=1)

    start_ts = target_0am.timestamp()
    end_ts = next_day_0am.timestamp()

    print(f"📅 爬取 [{account_name}] 在 {target_date} 的文章")

    target_articles = []
    page = 0
    should_stop = False

    while not should_stop:
        batch = get_published_articles(fakeid, page=page)

        if not batch:
            break

        for art in batch:
            ts = art['timestamp']

            # 还没到目标日期
            if ts >= end_ts:
                continue

            # 已经过目标日期
            if ts < start_ts:
                should_stop = True
                break

            target_articles.append(art)

        if should_stop:
            break

        page += 1
        time.sleep(2)

    target_articles.sort(key=lambda x: x['timestamp'])
    print(f"✅ [{account_name}] 找到 {len(target_articles)} 篇文章")

    return target_articles


def save_article_markdown(account_name, index, article_data, target_date):
    """
    下载文章并保存为 Markdown
    """
    url = article_data['link']
    title = article_data['title']

    print(f"  📥 [{index+1}] {title}")

    # 使用 markdown_parser 下载并转换
    md_content = markdown_parser.parse_wechat_to_md(url)

    if md_content:
        # 保存文件
        date_dir = config.DATA_DIR / target_date
        date_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{account_name}_{index+1:03d}.md"
        filepath = date_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"    💾 已保存: {filename}")
        return True
    else:
        print(f"    ❌ 下载失败: {title}")
        return False


# ================= 主函数 =================

def main():
    """
    主函数：爬取所有公众号今天的文章
    """
    # 默认爬取今天的文章
    today = datetime.now().strftime("%Y-%m-%d")

    print("=" * 50)
    print(f"🚀 开始爬取文章，目标日期: {today}")
    print("=" * 50)

    all_articles = []

    for account_name in config.TARGET_ACCOUNTS:
        print(f"\n{'=' * 20} {account_name} {'=' * 20}")

        # 爬取文章列表
        articles = fetch_articles_for_date(account_name, today)

        # 下载并保存每篇文章
        for idx, article in enumerate(articles):
            save_article_markdown(account_name, idx, article, today)
            all_articles.append({
                "account": account_name,
                "index": idx + 1,
                "article": article
            })
            time.sleep(1)  # 避免请求过快

    print("\n" + "=" * 50)
    print(f"✅ 爬取完成！共保存 {len(all_articles)} 篇文章")
    print(f"📁 保存位置: {config.DATA_DIR / today}")
    print("=" * 50)


if __name__ == "__main__":
    main()
