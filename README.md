# DailyNews

全自动 AI 每日资讯聚合系统。从微信公众号、GitHub Trending、ArXiv 论文榜和 Hacker News 爬取内容，使用智谱 AI GLM 模型进行智能总结，生成 Markdown 日报并通过 GitHub Actions 自动发布。

## 功能特性

- **多源数据聚合**：微信公众号文章、GitHub Trending、ArXiv 论文、Hacker News
- **AI 智能总结**：使用智谱 AI GLM-4.7 模型
- **统计数据生成**：自动聚合论文得分、GitHub Stars 等指标
- **前端展示**：Vue.js 驱动的交互式日报浏览页面
- **自动化运行**：GitHub Actions 定时调度，无需本地部署
- **自动提交**：生成的 Markdown 自动推送到仓库

## 架构

```
DailyNews/
├── main.py                 # CLI 入口
├── config.py               # 配置（环境变量驱动）
├── requirements.txt        # Python 依赖
├── index.html              # 前端展示页面
├── viewer.html             # Markdown 查看器
│
├── src/
│   ├── fetchers/           # 数据爬取（微信/GitHub/ArXiv/HackerNews）
│   ├── summarizers/        # AI 总结（GLM 模型）
│   ├── processors/         # 数据处理（去重/格式化）
│   ├── tasks/              # 任务编排
│   └── utils/              # 工具函数（含 stats.py）
│
├── prompts/                # AI 提示词模板
│
├── output/                 # Markdown 输出
│   └── YYYY-MM-DD/
│       ├── daily_report.md
│       ├── github_trending.md
│       ├── hacker_news.md
│       ├── stats.json
│       └── papers/
│           └── papers_summary.md
│
└── .github/workflows/      # GitHub Actions 配置
```

## GitHub Actions 部署

### 1. Fork 本仓库

### 2. 配置 Secrets

在仓库 Settings → Secrets and variables → Actions 添加：

| Secret | 说明 |
|--------|------|
| `WECHAT_COOKIE` | 微信公众号 Cookie（从浏览器导出） |
| `WECHAT_TOKEN` | 微信管理平台 Token |
| `GLM_API_KEY` | 智谱 AI API Key（从 open.bigmodel.cn 获取） |

### 3. 启用 Actions

Fork 后需手动启用 Actions。系统按以下时间自动运行（北京时间）：

| 任务 | 时间 | 归档日期 | 说明 |
|------|------|----------|------|
| Papers | 11:17 | 昨天 | arXiv 当天显示的是前一天提交的论文 |
| Hacker News | 7:53 (次日) | 当天 | 次日早晨汇总前一天的热门 |
| WeChat | 22:13 | 当天 | 晚间汇总当日文章 |
| GitHub Trending | 22:31 | 当天 | 晚间汇总当日 Trending |

也可在 Actions 页面手动触发运行。

## 本地运行（可选）

```bash
# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export WECHAT_COOKIE="your-cookie"
export WECHAT_TOKEN="your-token"
export GLM_API_KEY="your-api-key"

# 运行所有任务
python main.py

# 运行指定任务
python main.py --wechat --github --paper --hackernews

# 指定日期
python main.py --date 2026-02-19
```

## 输出文件

运行后在 `output/YYYY-MM-DD/` 目录生成：

| 文件 | 说明 |
|------|------|
| `daily_report.md` | 微信文章日报 |
| `github_trending.md` | GitHub Trending 报告 |
| `hacker_news.md` | Hacker News 热门故事 |
| `stats.json` | 统计数据（论文得分、GitHub Stars） |
| `papers/papers_summary.md` | 论文汇总 |

## 前端展示

项目提供交互式前端页面浏览日报：

```bash
# 启动本地服务器
python -m http.server 8000

# 访问 http://localhost:8000
```

功能：
- 日历导航，按日期查看报告
- 统计卡片展示论文得分和 GitHub Stars
- Markdown 渲染，支持 LaTeX 公式

## 配置

主要配置项在 `config.py`，通过环境变量控制：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `WECHAT_COOKIE` | 微信 Cookie | 必填 |
| `WECHAT_TOKEN` | 微信 Token | 必填 |
| `GLM_API_KEY` / `ZHIPU_API_KEY` | 智谱 API Key | 必填 |

## 注意事项

- **Cookie 有效期**：微信 Cookie 会过期，需定期更新 Secrets
- **ArXiv 周末**：ArXiv 周末不发布新论文，任务会自动跳过
- **GitHub Trending**：仅支持当天数据，无法获取历史

## License

MIT
