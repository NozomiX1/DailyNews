# Stats JSON 生成与展示 实现计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在执行 main.py 时自动生成统计数据 JSON，并在 index.html 首页展示昨日论文得分和 GitHub 新增 Star。

**Architecture:**
1. 创建 `src/utils/stats.py` 工具模块，提供 stats.json 的读写功能
2. 修改 PapersTask 和 GithubTrendingTask，在 format() 阶段收集统计数据并写入 stats.json
3. 修改 index.html，读取 stats.json 并在顶部卡片展示

**Tech Stack:** Python 3.x, JSON, Vue.js 3 (前端已有)

---

### Task 1: 创建 stats 工具模块

**Files:**
- Create: `src/utils/stats.py`

**Step 1: 编写 stats.py 工具函数**

```python
# src/utils/stats.py
"""Statistics JSON utility for daily stats aggregation."""
import json
from pathlib import Path
from typing import Dict, Any, Optional


STATS_FILENAME = "stats.json"


def read_stats(output_dir: Path) -> Dict[str, Any]:
    """
    Read stats.json from output directory.

    Args:
        output_dir: Output directory path (e.g., output/2026-02-19/)

    Returns:
        Existing stats dict or empty dict with date
    """
    stats_path = output_dir / STATS_FILENAME
    if stats_path.exists():
        try:
            with open(stats_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    # Return empty structure with date from directory name
    date_str = output_dir.name
    return {"date": date_str}


def write_stats(output_dir: Path, stats: Dict[str, Any]) -> None:
    """
    Write stats.json to output directory.

    Args:
        output_dir: Output directory path
        stats: Stats dictionary to write
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    stats_path = output_dir / STATS_FILENAME

    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print(f"  📊 Stats saved: {stats_path}")


def update_paper_stats(output_dir: Path, total_score: float, count: int) -> None:
    """
    Update paper statistics in stats.json.

    Args:
        output_dir: Output directory path
        total_score: Sum of all paper scores
        count: Number of papers
    """
    stats = read_stats(output_dir)
    stats["papers"] = {
        "total_score": round(total_score, 2),
        "count": count
    }
    write_stats(output_dir, stats)


def update_github_stats(output_dir: Path, total_stars_today: int, repo_count: int) -> None:
    """
    Update GitHub statistics in stats.json.

    Args:
        output_dir: Output directory path
        total_stars_today: Sum of today's stars for all repos
        repo_count: Number of repositories
    """
    stats = read_stats(output_dir)
    stats["github"] = {
        "total_stars_today": total_stars_today,
        "repo_count": repo_count
    }
    write_stats(output_dir, stats)
```

**Step 2: 验证模块可导入**

Run: `python -c "from src.utils.stats import read_stats, write_stats, update_paper_stats, update_github_stats; print('OK')"`

Expected: `OK`

**Step 3: 提交**

```bash
git add src/utils/stats.py
git commit -m "feat: add stats utility module for JSON aggregation"
```

---

### Task 2: 修改 PapersTask 收集统计数据

**Files:**
- Modify: `src/tasks/papers.py:158-182` (format method)

**Step 1: 添加 stats 导入并修改 format 方法**

在文件顶部添加导入：
```python
from ..utils.stats import update_paper_stats
```

修改 format 方法，在保存文件后收集统计数据：

```python
def format(self, items: List[Dict[str, Any]], date: str) -> str:
    """
    Format papers to Markdown summary.
    """
    if not items:
        return ""

    print(f"\n[3/3] 格式化论文汇总...")

    content = self.formatter.format_papers_summary(items, date)

    # Save to papers subdirectory
    papers_output_dir = self.output_dir / "papers"
    papers_output_dir.mkdir(parents=True, exist_ok=True)
    output_path = papers_output_dir / "papers_summary.md"
    self.formatter.save(content, output_path)

    # Collect and save statistics
    total_score = 0.0
    for paper in items:
        score = paper.get('score', paper.get('rank_score', 0))
        if isinstance(score, (int, float)):
            total_score += score

    update_paper_stats(self.output_dir, total_score, len(items))

    return content
```

**Step 2: 验证语法**

Run: `python -m py_compile src/tasks/papers.py`

Expected: 无输出（语法正确）

**Step 3: 提交**

```bash
git add src/tasks/papers.py
git commit -m "feat(papers): collect and save paper statistics to stats.json"
```

---

### Task 3: 修改 GithubTrendingTask 收集统计数据

**Files:**
- Modify: `src/tasks/github.py:123-144` (format method)

**Step 1: 添加 stats 导入并修改 format 方法**

在文件顶部添加导入：
```python
from ..utils.stats import update_github_stats
```

修改 format 方法：

```python
def format(self, items: List[Dict[str, Any]], date: str) -> str:
    """
    Format summarized repositories to Markdown.
    """
    if not items:
        return ""

    print(f"\n[3/3] 格式化 GitHub Trending 报告...")
    content = self.formatter.format_github(items, date)

    # Save to file
    output_path = self.output_dir / "github_trending.md"
    self.formatter.save(content, output_path)

    # Collect and save statistics
    total_stars_today = 0
    for repo in items:
        today_stars = repo.get('today_stars', repo.get('stars_period', 0))
        if isinstance(today_stars, (int, float)):
            total_stars_today += int(today_stars)
        elif isinstance(today_stars, str):
            # Handle string format like "3384"
            try:
                total_stars_today += int(today_stars.replace(',', ''))
            except ValueError:
                pass

    update_github_stats(self.output_dir, total_stars_today, len(items))

    return content
```

**Step 2: 验证语法**

Run: `python -m py_compile src/tasks/github.py`

Expected: 无输出（语法正确）

**Step 3: 提交**

```bash
git add src/tasks/github.py
git commit -m "feat(github): collect and save trending statistics to stats.json"
```

---

### Task 4: 修改 index.html 展示统计数据

**Files:**
- Modify: `index.html:154-173` (统计卡片区域)
- Modify: `index.html:375` (data reactive 对象)
- Modify: `index.html:468-520` (fetchAllData 函数)

**Step 1: 修改统计卡片标签**

将第 154-173 行的三个卡片修改为：

```html
<div class="grid grid-cols-3 gap-4 md:gap-8 mb-12">
    <div class="p-5 rounded-xl bg-white border border-[var(--line-color)] shadow-sm hover:shadow-md transition-shadow">
        <div class="text-xs text-[var(--secondary-text)] uppercase font-bold tracking-wider mb-1">昨日论文得分</div>
        <div class="text-2xl md:text-3xl font-bold text-gray-900">{{ paperScore }}</div>
    </div>
    <div class="p-5 rounded-xl bg-white border border-[var(--line-color)] shadow-sm hover:shadow-md transition-shadow">
        <div class="text-xs text-[var(--secondary-text)] uppercase font-bold tracking-wider mb-1">昨日新增 Star</div>
        <div class="text-2xl md:text-3xl font-bold text-gray-900">{{ githubStars }}</div>
    </div>
    <div class="p-5 rounded-xl bg-white border border-[var(--line-color)] shadow-sm hover:shadow-md transition-shadow">
        <div class="text-xs text-[var(--secondary-text)] uppercase font-bold tracking-wider mb-1">Status</div>
        <div class="text-lg md:text-xl font-bold text-green-600 flex items-center gap-2">
            <span class="relative flex h-3 w-3">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
            </span>
            UPDATE
        </div>
    </div>
</div>
```

**Step 2: 添加 stats 数据属性和计算属性**

在 setup() 函数中，data reactive 对象后添加：

```javascript
const stats = reactive({ papers: null, github: null });
```

添加格式化计算属性：

```javascript
const paperScore = computed(() => {
    if (stats.papers && typeof stats.papers.total_score === 'number') {
        return stats.papers.total_score.toFixed(2);
    }
    return '--';
});

const githubStars = computed(() => {
    if (stats.github && typeof stats.github.total_stars_today === 'number') {
        return '+' + stats.github.total_stars_today.toLocaleString();
    }
    return '--';
});
```

**Step 3: 添加 stats.json 获取逻辑**

在 fetchAllData 函数中添加 stats 获取：

```javascript
// 在并发请求后添加 stats 获取
const fetchStats = async (pathStr) => {
    try {
        const res = await fetch(`./output/${pathStr}/stats.json?t=${Date.now()}`);
        if (res.ok) {
            return await res.json();
        }
    } catch (e) {}
    return null;
};

// 在 Promise.all 后添加
const statsData = await fetchStats(pathStr);
if (statsData) {
    stats.papers = statsData.papers || null;
    stats.github = statsData.github || null;
} else {
    stats.papers = null;
    stats.github = null;
}
```

**Step 4: 更新 return 对象**

在 return 对象中添加：
```javascript
return {
    // ...existing
    stats, paperScore, githubStars
};
```

**Step 5: 验证**

启动本地服务器：
```bash
python -m http.server 8000
```

访问 http://localhost:8000，检查：
1. 选择有 stats.json 的日期，卡片显示正确数值
2. 选择没有 stats.json 的日期，卡片显示 `--`

**Step 6: 提交**

```bash
git add index.html
git commit -m "feat(ui): display yesterday's paper score and github stars"
```

---

### Task 5: 测试完整流程

**Step 1: 运行 paper 任务生成数据**

Run: `python main.py --paper --date 2026-02-19`

Expected: 生成 `output/2026-02-19/stats.json` 包含 papers 数据

**Step 2: 运行 github 任务生成数据**

Run: `python main.py --github`

Expected: 生成 `output/{today}/stats.json` 包含 github 数据

**Step 3: 验证前端展示**

启动服务器并访问页面，验证统计数据正确显示。

**Step 4: 最终提交（如有修改）**

```bash
git status
# 如有未提交的修改
git add -A && git commit -m "chore: final cleanup for stats feature"
```

---

## 预期成果

1. 每次执行 `python main.py --paper` 或 `--github` 时，自动在 `output/{date}/stats.json` 中记录统计数据
2. index.html 顶部卡片展示：
   - **昨日论文得分**: 如 `346.91` 或 `--`
   - **昨日新增 Star**: 如 `+6,350` 或 `--`
