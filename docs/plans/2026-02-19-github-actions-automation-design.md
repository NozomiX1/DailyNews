# GitHub Actions 自动化设计文档

## 概述

将 DailyNews 项目改造为支持 GitHub Actions 自动化运行，每天自动爬取数据、生成报告并部署到 GitHub Pages。

## 目标

- 每天自动运行爬取任务（WeChat + GitHub Trending + ArXiv）
- 生成 Markdown 报告并 commit 到仓库
- GitHub Pages 自动同步更新

## 架构

```
GitHub Actions (UTC 00:00 = 北京 08:00)
       │
       ▼
┌─────────────────────────────────────┐
│  1. Checkout 代码                    │
│  2. 安装 Python 依赖                 │
│  3. 运行 python main.py              │
│  4. Commit output/ 到 main 分支      │
└─────────────────────────────────────┘
       │
       ▼
  GitHub Pages 自动更新
  (https://user.github.io/DailyNews/output/...)
```

## 改动清单

### 1. config.py 重构

**目标**：敏感配置优先从环境变量读取

**改动内容**：
```python
# TOKEN: 硬编码 → 环境变量
TOKEN = os.environ.get("WECHAT_TOKEN", "")

# COOKIE: 文件优先 → 环境变量优先
def load_cookie():
    env_cookie = os.environ.get("WECHAT_COOKIE", "")
    if env_cookie:
        return env_cookie
    # fallback 到本地文件
    cookie_path = PROJECT_ROOT / "cookie1.txt"
    ...

# GLM_API_KEY: 保持不变（已经是环境变量）
GLM_API_KEY = os.environ.get("ZHIPU_API_KEY") or os.environ.get("GLM_API_KEY")
```

### 2. .github/workflows/daily_news.yml 重写

```yaml
name: Daily News Generator

on:
  schedule:
    - cron: '0 0 * * *'  # UTC 00:00 = 北京 08:00
  workflow_dispatch:

env:
  WECHAT_COOKIE: ${{ secrets.WECHAT_COOKIE }}
  WECHAT_TOKEN: ${{ secrets.WECHAT_TOKEN }}
  GLM_API_KEY: ${{ secrets.GLM_API_KEY }}

jobs:
  generate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - uses: actions/setup-python@v5
      with:
        python-version: '3.11'

    - name: Install dependencies
      run: pip install -r requirements.txt

    - name: Run DailyNews
      run: python main.py

    - name: Commit changes
      run: |
        git config user.name "github-actions[bot]"
        git config user.email "github-actions[bot]@users.noreply.github.com"
        git add output/
        git diff --quiet && git diff --staged --quiet || \
          (git commit -m "chore: update daily news $(date +%Y-%m-%d)" && git push)
```

### 3. requirements.txt 补充

确保包含所有依赖：
```
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=5.0.0
markdownify>=0.11.6
python-dotenv>=1.0.0
zhipuai>=2.0.0
```

### 4. .env.example 新增

```env
# WeChat 配置
WECHAT_COOKIE=your_cookie_here
WECHAT_TOKEN=your_token_here

# 智谱 AI 配置
ZHIPU_API_KEY=your_api_key_here
# 或
GLM_API_KEY=your_api_key_here
```

### 5. .gitignore 更新

```
# 本地环境配置
.env
cookie1.txt
fakeid_cache.json
```

## GitHub Secrets 配置

用户需要在 GitHub 仓库设置中添加以下 Secrets：

| Secret | 说明 | 获取方式 |
|--------|------|----------|
| `WECHAT_COOKIE` | 微信公众号 Cookie | 浏览器开发者工具导出 |
| `WECHAT_TOKEN` | 微信 Token | URL 参数中的 token 值 |
| `GLM_API_KEY` | 智谱 AI API Key | https://open.bigmodel.cn |

## 文件变更总结

| 文件 | 操作 |
|------|------|
| `config.py` | 修改：环境变量优先 |
| `.github/workflows/daily_news.yml` | 重写：完整 workflow |
| `requirements.txt` | 修改：补充依赖 |
| `.env.example` | 新增：示例配置 |
| `.gitignore` | 修改：忽略敏感文件 |

## 验证步骤

1. 本地测试：`python main.py` 确认正常运行
2. 配置 Secrets：在 GitHub 仓库设置中添加 3 个 Secrets
3. 手动触发：Actions 页面点击 "Run workflow" 测试
4. 检查结果：确认 output/ 目录有新文件，Pages 可访问
