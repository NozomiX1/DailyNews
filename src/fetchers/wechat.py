# DailyNews - WeChat Article Fetcher
# Migrated from src/wechat_fetcher.py
import requests
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import sys

from .base import BaseFetcher
from ..utils import parse_wechat_to_md, retry_on_request_error
import config


class WechatFetcher(BaseFetcher):
    """WeChat Official Account article fetcher."""

    def __init__(self, data_dir: Path = None):
        super().__init__(data_dir)
        self.target_accounts = config.TARGET_ACCOUNTS
        self.fakeid_cache_file = config.FAKEID_CACHE_FILE

    # ================= fakeid 缓存管理 =================

    def _load_fakeid_cache(self):
        """加载 fakeid 缓存"""
        if self.fakeid_cache_file.exists():
            try:
                with open(self.fakeid_cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_fakeid_cache(self, cache):
        """保存 fakeid 缓存"""
        with open(self.fakeid_cache_file, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)

    def _get_fakeid_with_cache(self, account_name):
        """获取公众号 fakeid，优先使用缓存"""
        cache = self._load_fakeid_cache()

        if account_name in cache:
            print(f"  ✅ 从缓存获取 fakeid: {account_name}")
            return cache[account_name]

        print(f"  🔍 正在查询公众号: {account_name}")
        fakeid = self._get_fakeid(account_name)

        if fakeid:
            cache[account_name] = fakeid
            self._save_fakeid_cache(cache)
            print(f"  💾 已缓存 fakeid: {account_name}")

        return fakeid

    @retry_on_request_error(max_retries=3)
    def _get_fakeid(self, name):
        """搜索公众号，获取其 fakeid"""
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
                print(f"  ❌ 搜索失败: {data}")
                return None

            for item in data.get("list", []):
                if item["nickname"] == name:
                    print(f"  ✅ 找到公众号 [{name}], fakeid: {item['fakeid']}")
                    return item["fakeid"]

            print(f"  ❌ 未找到公众号: {name}")
            return None
        except Exception as e:
            print(f"  ❌ get_fakeid 异常: {e}")
            return None

    # ================= 文章爬取 =================

    @retry_on_request_error(max_retries=3)
    def _get_published_articles(self, fakeid, page=0):
        """获取已发布文章列表"""
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
                print(f"  ❌ 接口报错: {data}")
                return []

            publish_page = json.loads(data.get("publish_page", "{}"))
            publish_list = publish_page.get("publish_list", [])
            articles_result = []

            for i, item in enumerate(publish_list):
                try:
                    publish_info_str = item.get("publish_info", "{}")
                    publish_info = json.loads(publish_info_str)

                    sent_time = 0

                    if "sent_info" in publish_info and "time" in publish_info["sent_info"]:
                        sent_time = publish_info["sent_info"]["time"]
                    elif "publish_info" in publish_info and "create_time" in publish_info["publish_info"]:
                        sent_time = publish_info["publish_info"]["create_time"]

                    if sent_time == 0:
                        appmsgex = publish_info.get("appmsgex", [])
                        if appmsgex:
                            sent_time = appmsgex[0].get("create_time", 0)

                    if sent_time == 0:
                        sent_time = time.time()

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
                    print(f"  ❌ 解析第 {i+1} 条失败: {item_err}")
                    continue

            return articles_result

        except Exception as e:
            print(f"  ❌ get_published_articles 异常: {e}")
            return []

    def _fetch_articles_for_date(self, account_name, target_date):
        """爬取指定日期的文章"""
        fakeid = self._get_fakeid_with_cache(account_name)
        if not fakeid:
            print(f"  ❌ 无法获取 {account_name} 的 fakeid，跳过")
            return []

        target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
        target_0am = datetime.combine(target_date, datetime.min.time())
        next_day_0am = target_0am + timedelta(days=1)

        start_ts = target_0am.timestamp()
        end_ts = next_day_0am.timestamp()

        print(f"  📅 爬取 [{account_name}] 在 {target_date} 的文章")

        target_articles = []
        page = 0
        should_stop = False

        while not should_stop:
            batch = self._get_published_articles(fakeid, page=page)

            if not batch:
                break

            for art in batch:
                ts = art['timestamp']

                if ts >= end_ts:
                    continue

                if ts < start_ts:
                    should_stop = True
                    break

                target_articles.append(art)

            if should_stop:
                break

            page += 1
            time.sleep(2)

        target_articles.sort(key=lambda x: x['timestamp'])
        print(f"  ✅ [{account_name}] 找到 {len(target_articles)} 篇文章")

        return target_articles

    def _save_article_markdown(self, account_name, index, article_data, target_date):
        """下载文章并保存为 Markdown"""
        url = article_data['link']
        title = article_data['title']

        print(f"    📥 [{index+1}] {title}")

        md_content = parse_wechat_to_md(url)

        if md_content:
            # 新路径: data/{date}/articles/
            date_dir = self.data_dir / target_date / "articles"
            date_dir.mkdir(parents=True, exist_ok=True)

            filename = f"{account_name}_{index+1:03d}.md"
            filepath = date_dir / filename

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(md_content)

            print(f"      💾 已保存: {filename}")
            return {
                "account": account_name,
                "index": index + 1,
                "filepath": str(filepath),
                "title": title,
                "url": url,
                "time_str": article_data.get('time_str', ''),
                "timestamp": article_data.get('timestamp', 0)
            }
        else:
            print(f"      ❌ 下载失败: {title}")
            return None

    # ================= 主接口 =================

    def fetch(self, date: str = None) -> list:
        """
        Fetch articles for a specific date.

        Args:
            date: Date string in YYYY-MM-DD format, defaults to today

        Returns:
            List of article dictionaries with content and metadata
        """
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        print(f"📡 开始爬取公众号文章，目标日期: {date}")

        all_articles = []

        for account_name in self.target_accounts:
            print(f"\n{'=' * 20} {account_name} {'=' * 20}")

            articles = self._fetch_articles_for_date(account_name, date)

            for idx, article in enumerate(articles):
                result = self._save_article_markdown(account_name, idx, article, date)
                if result:
                    # Read the saved content
                    try:
                        with open(result['filepath'], 'r', encoding='utf-8') as f:
                            result['content'] = f.read()
                    except:
                        result['content'] = ''
                    all_articles.append(result)
                time.sleep(1)

        print(f"\n✅ 爬取完成！共保存 {len(all_articles)} 篇文章")

        return all_articles

    def save_raw_data(self, items: list, date: str) -> Path:
        """Save raw article data (metadata only, content is saved separately)."""
        # 新路径: data/{date}/articles/
        date_dir = self.data_dir / date / "articles"
        date_dir.mkdir(parents=True, exist_ok=True)
        output_path = date_dir / f"{date}_metadata.json"
        import json
        with open(output_path, 'w', encoding='utf-8') as f:
            # Don't save content in metadata
            metadata = [{k: v for k, v in item.items() if k != 'content'} for item in items]
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        return output_path

    def load_from_json(self, date: str) -> list:
        """
        从本地 JSON 加载文章 metadata 并读取内容

        Args:
            date: 日期字符串 (YYYY-MM-DD)

        Returns:
            包含 content 的文章列表
        """
        import json

        json_path = self.data_dir / date / "articles" / f"{date}_metadata.json"
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    metadata_list = json.load(f)

                # 读取每篇文章的 Markdown 内容
                for meta in metadata_list:
                    filepath = Path(meta.get('filepath', ''))
                    if filepath.exists():
                        with open(filepath, 'r', encoding='utf-8') as f:
                            meta['content'] = f.read()
                    else:
                        meta['content'] = ''

                print(f"  ✅ 从 JSON 加载 {len(metadata_list)} 篇文章")
                return metadata_list
            except Exception as e:
                print(f"  ⚠️ 加载 JSON 失败: {e}")
        return []
