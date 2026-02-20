# 统计数据生成与展示设计

## 概述

在执行 `main.py` 时，自动生成每日统计数据（JSON 格式），并在 `index.html` 首页展示，用于衡量每日「信息密度」。

## 需求

- **论文指标**：展示昨日选取论文的总得分
- **GitHub 指标**：展示昨日 trending 项目的新增 star 数
- **用途**：快速判断当天是否有高质量内容

## 数据结构

### 存储位置

```
output/{YYYY-MM-DD}/stats.json
```

### JSON 格式

```json
{
  "date": "2026-02-19",
  "papers": {
    "total_score": 346.91,
    "count": 8
  },
  "github": {
    "total_stars_today": 6350,
    "repo_count": 7
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| date | string | 数据日期 |
| papers.total_score | number | 所有选取论文的 score 之和 |
| papers.count | number | 选取论文数量 |
| github.total_stars_today | number | 所有 trending 项目的今日新增 star 之和 |
| github.repo_count | number | trending 项目数量 |

## 实现方案

### 数据收集

在任务执行过程中维护变量，实时累加统计数据：

1. **PapersTask**
   - 时机：筛选论文时
   - 操作：累加每篇论文的 `score` 字段
   - 任务完成后写入 `stats.json`

2. **GithubTrendingTask**
   - 时机：生成 markdown 时
   - 操作：累加每个项目的 `stars_today` 值
   - 任务完成后写入 `stats.json`

### 文件写入策略

- 每个任务完成后，读取现有 `stats.json`（如存在），合并新数据后写回
- 确保 paper 和 github 任务的数据不会互相覆盖

## 前端展示

### index.html 修改

修改顶部两个统计卡片：

| 位置 | 原标签 | 新标签 | 数值格式 | 示例 |
|------|--------|--------|----------|------|
| 第一个卡片 | Total Papers | 昨日论文得分 | `346.91` | 保留两位小数 |
| 第二个卡片 | Github Repos | 昨日新增 Star | `+6,350` | 带加号、千位分隔符 |

### 前端读取逻辑

1. 监听日历日期变化
2. 读取 `output/{selected_date}/stats.json`
3. 如果文件不存在或字段缺失，显示 `--` 占位符
4. 格式化数值显示

### 数值格式化规则

```javascript
// 论文得分：保留两位小数
const formatPaperScore = (score) => score?.toFixed(2) ?? '--';

// GitHub Stars：带加号和千位分隔符
const formatStars = (stars) => stars ? `+${stars.toLocaleString()}` : '--';
```

## 注意事项

- paper 任务在每天 11 点左右执行，但归档日期为昨天
- 所有统计数据统一使用归档日期，确保与 markdown 文件日期一致
- stats.json 与 markdown 文件存储在同一目录下
