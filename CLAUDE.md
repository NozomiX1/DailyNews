# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DailyNews is a Python web scraper for fetching articles from WeChat Official Accounts (公众号). It retrieves published articles via WeChat's internal APIs and converts HTML content to Markdown format.

## Running the Code

```bash
# Fetch yesterday's articles from the target Official Account
python wechat_fetch.py

# Convert a WeChat article URL to Markdown
python conclude.py
```

## Architecture

The project consists of two main Python scripts:

### `wechat_fetch.py` - Article List Fetcher

Orchestrates the scraping workflow:

1. **`get_fakeid(name)`** - Searches for an Official Account by name and returns its `fakeid` (WeChat's internal identifier)
2. **`get_published_articles(fakeid, page)`** - Fetches published articles via `/cgi-bin/appmsgpublish` API. Handles pagination and extracts article metadata (title, link, timestamp, digest, is_headline)
3. **`fetch_yesterday_articles(fakeid)`** - Iterates through pages to collect all articles published yesterday (natural day logic, 00:00-23:59)

Key implementation details:
- Uses a three-strategy approach to extract timestamps from WeChat's complex nested JSON response (sent_info.time, nested publish_info.create_time, or appmsgex[0].create_time)
- Stops pagination when reaching articles older than yesterday to avoid unnecessary API calls
- Results are sorted by timestamp ascending (morning articles first)

### `conclude.py` - HTML to Markdown Converter

**`parse_wechat_to_md(url)`** - Downloads a WeChat article URL and converts it to clean Markdown:

1. Extracts metadata: title (`#activity-name`), account name (`#js_name`), publish time (from script `ct` variable)
2. Extracts article body from `#js_content` div
3. Fixes lazy-loaded images by converting `data-src` to `src`
4. Uses `markdownify` for HTML→Markdown conversion
5. Outputs structured Markdown with YAML-style frontmatter

## Configuration

Both scripts have hardcoded configuration at the top:

- `TOKEN` - WeChat management platform token
- `COOKIE` - Full WeChat authentication cookie (must include `appmsglist_action_*`, `bizuin`, etc.)
- `TARGET_NAME` - The Official Account name to scrape (default: "新智元")
- `HEADERS` - Request headers including User-Agent, Cookie, and Referer

**Important**: WeChat's authentication cookies expire. When the scraper fails with authentication errors, the cookie needs to be updated by copying from browser dev tools.

## Dependencies

The project uses these Python packages (no requirements.txt present):
- `requests` - HTTP client
- `BeautifulSoup` (bs4) - HTML parsing
- `markdownify` - HTML to Markdown conversion

Install via:
```bash
pip install requests beautifulsoup4 markdownify
```

## API Endpoints Used

| Endpoint | Purpose |
|----------|---------|
| `/cgi-bin/searchbiz` | Search Official Accounts by name, get fakeid |
| `/cgi-bin/appmsgpublish` | Fetch published articles list with pagination |

## WeChat API Quirks

- The `publish_page` field in API responses is a JSON string that needs `json.loads()` to parse
- Article timestamps are nested differently depending on publish type (群发 vs 发布)
- Pagination uses `begin` parameter (page * 5) with fixed count of 5
- Referer header is required or newer APIs will return errors
