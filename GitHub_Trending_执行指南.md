# GitHub Trending 执行指南

> 本文档是给未来的 Claude (AI) 看的操作手册，用于完成每日 GitHub 热门项目的抓取、总结和发布。

---

## 任务概述

每天执行以下流程：
1. 爬取 GitHub Trending 榜单（全部语言，今日）
2. 下载每个项目的 README.md
3. 逐个阅读 README 并生成项目总结
4. 发布到微信公众号草稿箱

---

## 步骤 1: 爬取 GitHub Trending

### 执行命令

在工作目录 `/Users/nozomi/Desktop/projects/DailyNews` 下执行：

```bash
python -m src.github_trending --since daily
```

### 预期结果

- 程序会自动爬取今日的 GitHub Trending（全部语言）
- 文章保存到 `data/github_trending/YYYY-MM-DD.md`
- 文件格式：Markdown 格式的项目榜单

### 确认文件已生成

使用 Bash 检查：

```bash
ls -la data/github_trending/$(date +%Y-%m-%d).md
```

或 Glob 工具：

```
glob pattern: data/github_trending/*.md
```

---

## 步骤 2: 下载项目 README

### 执行命令

```bash
python -m src.readme_downloader --date today
```

### 预期结果

```
🔍 正在处理 2026-01-30 的 GitHub Trending...
📦 找到 14 个仓库，开始下载 README...
  ✓ openclaw/openclaw - 下载成功 (85533 字节)
  ✓ asgeirtj/system_prompts_leaks - 下载成功 (674 字节)
  ...

📊 下载完成:
  ✓ 成功: 13
  ⊙ 跳过: 0
  ✗ 未找到 README: 1
```

### 存储位置

README 文件保存在：
```
data/readme_files/{owner}/{repo}/README.md
```

---

## 步骤 3: 逐个总结项目

### ⚠️ 重要：边读边写

**为防止上下文爆炸，必须采用"边读边写"策略：**

1. 读取一个项目的 README
2. 立即生成该项目的总结
3. 将总结**追加写入**到 `output/YYYY-MM-DD/github_trending.md`

**不要**把所有 README 都读完后才开始写总结。

### 3.1 初始化报告文件

首先创建报告文件头部：

```markdown
# GitHub 热门项目 | YYYY-MM-DD

## 📊 今日榜单

```

保存到 `output/YYYY-MM-DD/github_trending.md`

### 3.2 逐篇处理项目

1. **使用 Read 工具读取单个 README**（按 150 行分批读取）

2. **分析项目并生成总结**，要求：
   - **核心功能**：这个项目是做什么的？
   - **技术特点**：使用了什么技术栈？有什么特色功能？
   - **适用场景**：适合什么场景使用？
   - **生成摘要**：
     - 100-200 字中文描述
     - 突出项目价值和特点
     - 避免简单翻译，用中文自然表达
   - **无 README 处理**：如果没有 README，使用原始的简短描述或标记"该项目未提供 README 描述"

3. **输出格式**（严格遵循）：

```markdown
### N. owner/repo
**语言**: TypeScript | **Stars**: 108,821 | **今日**: +16,338
**链接**: https://github.com/owner/repo

**摘要**: 项目描述...

---
```

### 3.3 保存报告

使用 Write 工具保存到：
```
output/YYYY-MM-DD/github_trending.md
```

---

## 步骤 4: 发布到草稿箱

### 执行命令

```bash
python -m src.github_publisher --date YYYY-MM-DD
```

如果不指定日期，默认处理今天。

### 预期结果

```
==================================================
📤 正在发布 GitHub Trending 到草稿箱
📄 报告文件: output/2026-01-30/github_trending.md
==================================================
📊 解析到 14 个项目

✅ 草稿创建成功！
📋 Media ID: eczXpKmOOMk1jO1pgqsdcR0sVManGpLIA4Na1T6LMqmazBg19skSnZY0OXIIEeDR

👉 请登录微信公众号后台查看草稿箱
==================================================
```

---

## 完整工作流示例

```bash
# 1. 爬取 GitHub Trending
python -m src.github_trending --since daily

# 2. 下载 README
python -m src.readme_downloader --date today

# 3. Claude 处理：读取 README → 生成总结 → 保存到 output/YYYY-MM-DD/github_trending.md
# [Claude 手动完成]

# 4. 发布到草稿箱
python -m src.github_publisher --date 2026-01-30
```

---

## 注意事项

1. **README 文件过大**：有些 README 超过 token 限制，使用 offset 和 limit 参数分段读取
2. **无 README 的项目**：使用 trending.md 中的原始描述，或标记"未提供 README"
3. **去重处理**：readme_downloader 会自动跳过已下载的 README
4. **日期格式**：统一使用 YYYY-MM-DD 格式

---

## 文件路径速查

| 用途 | 路径 |
|------|------|
| Trending 榜单 | `data/github_trending/YYYY-MM-DD.md` |
| 项目 README | `data/readme_files/{owner}/{repo}/README.md` |
| 生成的报告 | `output/YYYY-MM-DD/github_trending.md` |
| 配置文件 | `config.py` |

---

## 命令速查

| 任务 | 命令 |
|------|------|
| 爬取 Trending | `python -m src.github_trending --since daily` |
| 指定语言爬取 | `python -m src.github_trending --since daily --language python` |
| 下载 README | `python -m src.readme_downloader --date today` |
| 强制重新下载 | `python -m src.readme_downloader --date today --force` |
| 查看已下载列表 | `python -m src.readme_downloader --list` |
| 发布到草稿箱 | `python -m src.github_publisher --date 2026-01-30` |
