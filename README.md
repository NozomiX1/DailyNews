# DailyNews

全自动 AI 每日资讯聚合与发布系统。从微信公众号、GitHub Trending 和 HuggingFace 论文榜单爬取内容，使用 Gemini AI 进行智能总结和去重，最终生成格式化的 Markdown 日报并发布到微信公众号。

## 功能特性

- **多源数据爬取**：支持微信公众号文章、GitHub Trending、HuggingFace 每日论文
- **AI 智能总结**：使用 Gemini Flash 模型对文章进行摘要生成
- **LLM 去重**：基于语义相似度的智能去重，避免重复内容
- **智能打分**：自动识别广告文章，按来源优先级排序
- **自动发布**：将生成的日报自动发布为微信公众号草稿
- **论文深度分析**：支持下载 PDF 并使用 Gemini Pro High 进行深度分析
- **灵活调度**：支持 cron 定时任务或手动指定日期运行
- **缓存模式**：可选是否缓存 PDF 文件到本地

## 目录结构

```
DailyNews/
├── main.py                 # 主入口，命令行接口
├── config.py              # 配置文件
├── requirements.txt       # Python 依赖
│
├── src/
│   ├── fetchers/          # 数据爬取模块
│   │   ├── base.py        # 基础爬虫类
│   │   ├── wechat.py      # 微信公众号爬虫
│   │   ├── github_trending.py  # GitHub Trending 爬虫
│   │   └── papers.py      # HuggingFace 论文爬虫
│   │
│   ├── summarizers/       # AI 总结模块
│   │   ├── base.py        # 基础总结器
│   │   ├── gemini_client.py  # Gemini API 客户端
│   │   ├── article_summarizer.py  # 文章总结器
│   │   ├── github_summarizer.py   # GitHub 项目总结器
│   │   └── paper_summarizer.py    # 论文总结器
│   │
│   ├── processors/        # 数据处理模块
│   │   ├── llm_deduplicator.py  # LLM 去重
│   │   ├── llm_scorer.py        # 广告识别打分
│   │   └── formatter.py         # Markdown 格式化
│   │
│   ├── publishers/        # 发布模块
│   │   ├── base.py        # 基础发布器
│   │   └── wechat.py      # 微信公众号发布
│   │
│   ├── tasks/             # 任务编排模块
│   │   ├── base.py        # 基础任务类
│   │   ├── wechat.py      # 微信文章任务
│   │   ├── github.py      # GitHub Trending 任务
│   │   ├── papers.py      # 论文汇总任务
│   │   └── paper_analysis.py  # 论文深度分析任务
│   │
│   └── utils/             # 工具模块
│       ├── paper_ranker.py    # 论文排序算法
│       └── markdown_parser.py # Markdown 解析
│
├── prompts/               # AI 提示词模板
│   ├── base.py            # 抽象基类
│   ├── article.py         # 文章总结提示词
│   ├── deduplication.py   # 去重提示词
│   ├── github.py          # GitHub 项目提示词
│   ├── paper.py           # 论文深度分析提示词
│   ├── paper_summary.py   # 论文汇总提示词
│   └── scoring.py         # 打分提示词
│
├── scripts/               # 辅助脚本
│   ├── test_paper_summary.py
│   ├── test_paper_note.py
│   └── publish_to_draft.py
│
├── data/                  # 数据缓存目录
│   └── YYYY-MM-DD/        # 按日期组织
│       ├── articles/      # 微信文章缓存
│       ├── trending/      # GitHub Trending 缓存
│       └── papers/        # 论文元数据和 PDF 缓存
│           └── pdf_downloads/  # PDF 文件（缓存模式下）
│
├── output/                # Markdown 输出目录
│   └── YYYY-MM-DD/        # 按日期组织
│       ├── daily_report.md
│       ├── github_trending.md
│       ├── papers_summary.md
│       └── papers/        # 论文详细笔记
│           └── papers_note_*.md
│
└── logs/                  # 日志文件目录
```

## 安装步骤

### 1. 克隆项目

```bash
git clone <repository-url>
cd DailyNews
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 Gemini API

编辑 `src/summarizers/gemini_client.py`，设置你的 Gemini API 配置：

```python
api_key = 'your-api-key'
api_endpoint = 'http://127.0.0.1:8045'  # 或官方端点
```

## 配置说明

主要配置项位于 `config.py`：

| 配置项 | 说明 |
|--------|------|
| `ENABLE_CACHE` | 是否缓存 PDF 文件到本地（默认 False） |
| `TARGET_ACCOUNTS` | 目标公众号列表 |
| `APP_ID` / `APP_SECRET` | 微信公众号凭证 |
| `COVER_MEDIA_ID` | 永久封面图 Media ID |
| `PROXIES` | 代理配置 |
| `AD_KEYWORDS` | 广告识别关键词列表 |

## 使用方法

### 基本用法

```bash
# 运行所有任务（今天的数据）
python main.py

# 指定日期运行
python main.py --date 2026-02-01

# 只运行指定任务
python main.py --wechat --github --paper
```

### 论文深度分析

```bash
# 运行论文深度分析（下载 PDF + Gemini Pro High 分析）
python main.py --analyze

# 指定论文数量
python main.py --analyze --paper-num 10

# 分析完成后发布为草稿
python main.py --analyze --paper-num 5 --publish
```

**缓存模式说明**：
- `ENABLE_CACHE = False`（默认）：PDF 不保存到本地，直接从内存分析
- `ENABLE_CACHE = True`：PDF 保存到 `data/{date}/papers/pdf_downloads/`，下次复用

### 定时任务配置

使用 cron 每天晚上 11 点自动运行：

```bash
crontab -e

# 添加以下行
0 23 * * * cd /path/to/DailyNews && /usr/bin/python3 main.py >> logs/cron.log 2>&1
```

## 输出文件

运行完成后，会在 `output/` 目录生成以下文件：

- `daily_report.md` - 公众号文章日报
- `github_trending.md` - GitHub Trending 报告
- `papers_summary.md` - 论文汇总报告
- `papers/papers_note_*.md` - 论文详细笔记（--analyze 模式）

## 注意事项

1. **API 限流**：Gemini API 有速率限制，建议在请求间设置适当延迟
2. **代理配置**：如需访问微信公众号 API，可能需要配置代理
3. **日期策略**：论文榜单默认使用"今天"的日期
4. **周末跳过**：ArXiv 周末不发布新论文，analyze 模式会自动跳过

## License

MIT
