# DailyNews

全自动 AI 每日资讯聚合与发布系统。从微信公众号、GitHub Trending 和 HuggingFace 论文榜单爬取内容，使用 Gemini AI 进行智能总结和去重，最终生成格式化的 Markdown 日报并发布到微信公众号。

## 功能特性

- **多源数据爬取**：支持微信公众号文章、GitHub Trending、HuggingFace 每日论文
- **AI 智能总结**：使用 Gemini Flash 模型对文章进行摘要生成
- **LLM 去重**：基于语义相似度的智能去重，避免重复内容
- **智能打分**：自动识别广告文章，按来源优先级排序
- **自动发布**：将生成的日报自动发布为微信公众号草稿
- **论文深度分析**：支持下载 PDF 并使用 Gemini 进行深度分析
- **灵活调度**：支持 cron 定时任务或手动指定日期运行

## 目录结构

```
DailyNews/
├── main.py                 # 主入口，命令行接口
├── config.py              # 配置文件
├── requirements.txt       # Python 依赖
├── cookie1.txt            # 微信认证 Cookie（需自行配置）
├── prompt.md              # 论文分析提示词模板
│
├── src/
│   ├── fetchers/          # 数据爬取模块
│   │   ├── __init__.py
│   │   ├── base.py        # 基础爬虫类
│   │   ├── wechat.py      # 微信公众号爬虫
│   │   ├── github_trending.py  # GitHub Trending 爬虫
│   │   └── papers.py      # HuggingFace 论文爬虫
│   │
│   ├── summarizers/       # AI 总结模块
│   │   ├── __init__.py
│   │   ├── base.py        # 基础总结器
│   │   ├── gemini_client.py  # Gemini API 客户端
│   │   ├── article_summarizer.py  # 文章总结器
│   │   ├── github_summarizer.py   # GitHub 项目总结器
│   │   └── paper_summarizer.py    # 论文总结器
│   │
│   ├── processors/        # 数据处理模块
│   │   ├── __init__.py
│   │   ├── llm_deduplicator.py  # LLM 去重
│   │   ├── llm_scorer.py        # 广告识别打分
│   │   └── formatter.py         # Markdown 格式化
│   │
│   ├── publishers/        # 发布模块
│   │   ├── __init__.py
│   │   ├── base.py        # 基础发布器
│   │   └── wechat.py      # 微信公众号发布
│   │
│   └── utils/             # 工具模块
│       ├── __init__.py
│       ├── paper_ranker.py    # 论文排序算法
│       └── markdown_parser.py # Markdown 解析
│
├── prompts/               # AI 提示词模板
│   ├── __init__.py
│   ├── base.py
│   ├── article.py
│   ├── deduplication.py
│   ├── github.py
│   ├── paper.py
│   ├── paper_summary.py
│   └── scoring.py
│
├── scripts/               # 辅助脚本
│   ├── test_paper_summary.py
│   ├── test_paper_note.py
│   └── publish_to_draft.py
│
├── data/                  # 数据存储目录
│   └── summaries/         # AI 总结结果（按日期组织）
│
├── output/                # Markdown 输出目录（按日期组织）
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

### 3. 配置 Cookie

在项目根目录创建 `cookie1.txt` 文件，填入微信公众号管理平台的 Cookie：

1. 登录 [微信公众号管理平台](https://mp.weixin.qq.com)
2. 打开浏览器开发者工具（F12）
3. 复制完整的 Cookie 字符串
4. 粘贴到 `cookie1.txt` 文件中

**注意**：Cookie 会定期过期，需要重新更新。

### 4. 配置 Gemini API

编辑 `src/summarizers/gemini_client.py`，设置你的 Gemini API 配置：

- `api_key`: Gemini API 密钥
- `api_endpoint`: API 端点（支持代理）

## 配置说明

主要配置项位于 `config.py`：

| 配置项 | 说明 |
|--------|------|
| `TARGET_ACCOUNTS` | 目标公众号列表（默认：机器之心、新智元、量子位） |
| `APP_ID` / `APP_SECRET` | 微信公众号凭证 |
| `COVER_MEDIA_ID` | 永久封面图 Media ID |
| `PROXIES` | 代理配置（用于绕过 IP 白名单限制） |
| `AD_KEYWORDS` | 广告识别关键词列表 |

## 使用方法

### 基本用法

```bash
# 运行默认策略（公众号/GitHub 今天，论文昨天）
python main.py

# 指定日期运行
python main.py 2026-02-01

# 只运行到格式化阶段，不发布
python main.py --dry-run
```

### 单独运行各阶段

```bash
# 只爬取数据
python main.py --fetch-only

# 只总结数据（从 JSON 加载已爬取的数据）
python main.py --summarize-only
```

### 论文深度分析

```bash
# 运行论文深度分析流程（下载 PDF + Gemini 分析）
python main.py --analyze-papers

# 指定日期和论文数量
python main.py --analyze-papers --date 2026-01-30 --min-papers 5 --max-papers 15

# 启用兴趣加成
python main.py --analyze-papers --topic-bonus

# 分析完成后发布为草稿
python main.py --analyze-papers --publish-papers
```

### 定时任务配置

使用 cron 每天晚上 11 点自动运行：

```bash
# 编辑 crontab
crontab -e

# 添加以下行
0 23 * * * cd /path/to/DailyNews && /usr/bin/python3 main.py >> logs/cron.log 2>&1
```

## 日志查看

```bash
# 查看最新日志
tail -f logs/cron.log

# 查看今天的输出文件
ls -la output/$(date +%Y-%m-%d)/

# 查看今天的 AI 总结
ls -la data/summaries/$(date +%Y-%m-%d)/
```

## 输出文件

运行完成后，会在 `output/` 目录生成以下文件：

- `daily_report.md` - 公众号文章日报
- `github_trending.md` - GitHub Trending 报告
- `papers_summary.md` - 论文汇总报告

## 注意事项

1. **Cookie 过期**：微信 Cookie 会定期失效，需要重新从浏览器复制
2. **API 限流**：Gemini API 有速率限制，建议在请求间设置适当延迟
3. **代理配置**：如需访问微信公众号 API，可能需要配置代理
4. **日期策略**：论文榜单默认使用"昨天"的日期（因为 HuggingFace 只显示昨天数据）

## License

MIT
