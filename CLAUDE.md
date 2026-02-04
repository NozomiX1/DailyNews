# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DailyNews is a Markdown generation system that aggregates content from multiple sources:
- **WeChat Official Accounts** - Fetches and converts articles to Markdown
- **GitHub Trending** - Generates daily trending repositories summaries
- **ArXiv Papers** - Summarizes recent research papers from arXiv

All generated Markdown files are output to the `output/` directory.

## Running the Code

```bash
# Generate daily reports to output/
python main.py --wechat --github --paper

# Generate only WeChat articles
python main.py --wechat

# Generate only GitHub trending
python main.py --github

# Generate only arXiv papers summary
python main.py --paper
```

## Architecture

The project uses a modular generator pattern with source-specific implementations:

### Generators

All generators implement a common interface and output Markdown to `output/`:

1. **`WeChatGenerator`** - Fetches articles from WeChat Official Accounts
   - Uses `cookie1.txt` for authentication (browser export format)
   - Converts WeChat HTML to clean Markdown
   - Handles pagination and date filtering

2. **`GitHubTrendingGenerator`** - Generates trending repository summaries
   - Scrapes GitHub trending page
   - Extracts repository metadata and descriptions

3. **`ArXivPaperGenerator`** - Summarizes research papers
   - Fetches recent papers from arXiv
   - Generates paper summaries in Markdown

### Configuration

Configuration is loaded from `.env` file:

- `WECHAT_COOKIE_PATH` - Path to cookie file (default: `cookie1.txt`)
- `WECHAT_TARGET_NAME` - Target Official Account name (default: "新智元")
- `OUTPUT_DIR` - Output directory for generated Markdown (default: `output/`)

**Cookie Format**: The `cookie1.txt` file should be exported from your browser in Netscape cookie format. WeChat's authentication cookies expire periodically and need to be refreshed.

## Dependencies

Install Python dependencies via:
```bash
pip install -r requirements.txt
```

The project uses these Python packages:
- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing
- `markdownify` - HTML to Markdown conversion
- `python-dotenv` - Environment configuration
- `httpx` - Async HTTP client

## Output Format

All generators output Markdown files with YAML frontmatter:

```markdown
---
title: Article Title
source: wechat/github/arxiv
date: 2025-01-15
url: https://...
---

# Article Title

Content here...
```

Files are organized in `output/` by source and date:
- `output/wechat/YYYY-MM-DD-title.md`
- `output/github/trending-YYYY-MM-DD.md`
- `output/arxiv/papers-YYYY-MM-DD.md`
