# DailyNews

全自动 AI 每日资讯聚合系统。从微信公众号、GitHub Trending 和 ArXiv 论文榜爬取内容，使用智谱 AI GLM 模型进行智能总结，生成 Markdown 日报并通过 GitHub Actions 自动发布。

## 功能特性

- **多源数据聚合**：微信公众号文章、GitHub Trending、ArXiv 论文
- **AI 智能总结**：使用智谱 AI GLM-4.7 模型
- **自动化运行**：GitHub Actions 定时调度，无需本地部署
- **自动提交**：生成的 Markdown 自动推送到仓库

## 架构

```
DailyNews/
├── main.py                 # CLI 入口
├── config.py               # 配置（环境变量驱动）
├── requirements.txt        # Python 依赖
│
├── src/
│   ├── fetchers/           # 数据爬取（微信/GitHub/ArXiv）
│   ├── summarizers/        # AI 总结（GLM 模型）
│   ├── processors/         # 数据处理（去重/格式化）
│   ├── tasks/              # 任务编排
│   └── utils/              # 工具函数
│
├── prompts/                # AI 提示词模板
│
├── output/                 # Markdown 输出
│   └── YYYY-MM-DD/
│       ├── daily_report.md
│       ├── github_trending.md
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

Fork 后需手动启用 Actions。系统将在每天北京时间 23:00（UTC 15:00）自动运行。

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
python main.py --wechat --github --paper

# 指定日期
python main.py --date 2026-02-19
```

## 输出文件

运行后在 `output/YYYY-MM-DD/` 目录生成：

- `daily_report.md` - 微信文章日报
- `github_trending.md` - GitHub Trending 报告
- `papers/papers_summary.md` - 论文汇总

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
