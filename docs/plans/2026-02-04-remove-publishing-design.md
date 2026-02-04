# Remove Publishing - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove all publishing-related code from DailyNews, transforming it into a markdown generation system.

**Architecture:** Remove the entire `src/publishers/` module, strip publishing logic from tasks, remove `--publish` and `--dry-run` flags from CLI, and clean up config/dependencies.

**Tech Stack:** Python 3, argparse, file system operations

---

## Task 1: Remove the publishers module

**Files:**
- Delete: `src/publishers/__init__.py`
- Delete: `src/publishers/base.py`
- Delete: `src/publishers/wechat.py`
- Delete: `src/publishers/css_loader.py`

**Step 1: Delete the entire publishers directory**

```bash
rm -rf src/publishers
```

**Step 2: Verify deletion**

```bash
ls src/publishers 2>&1
# Expected: "No such file or directory"
```

**Step 3: Commit**

```bash
git add -A
git commit -m "refactor: remove src/publishers module"
```

---

## Task 2: Remove publish() method from BaseTask

**Files:**
- Modify: `src/tasks/base.py`

**Step 1: Remove the publish() abstract method (lines 91-103)**

Remove this entire section:
```python
    @abstractmethod
    def publish(self, content: str, date: str) -> Dict[str, Any]:
        """
        Publish formatted content to destination.

        Args:
            content: Formatted Markdown content
            date: Date string in YYYY-MM-DD format

        Returns:
            Publish result with status, draft_id, etc.
        """
        pass
```

**Step 2: Remove dry_run parameter from run() method**

Update the `run()` method signature (line 105) from:
```python
    def run(self, date: str, dry_run: bool = False) -> Dict[str, Any]:
```

To:
```python
    def run(self, date: str) -> Dict[str, Any]:
```

**Step 3: Remove publish phase from run() method body**

Remove lines 149-153 (the publish phase):
```python
            # Publish phase
            if not dry_run:
                pub_result = self.publish(content, date)
                result["published"] = pub_result.get("status") == "success"
                result["draft_id"] = pub_result.get("draft_id")
```

**Step 4: Remove published/draft_id from result dict**

Update result dict initialization (lines 116-124) to remove `"published"` and `"draft_id"` keys:
```python
        result = {
            "task": self.name,
            "date": date,
            "skipped": False,
            "fetched": 0,
            "summarized": 0,
            "errors": []
        }
```

**Step 5: Update docstring and print_result()**

Update class docstring (lines 10-19) to remove reference to publish step:
```python
    """
    Task base class, defining the standard lifecycle for all pipeline tasks.

    Each task follows the same workflow:
    1. should_skip() - Check if the task should be skipped
    2. fetch() - Fetch raw data from source
    3. summarize() - Generate summaries using LLM
    4. format() - Format to Markdown
    """
```

Update `print_result()` (lines 160-176) to remove draft_id printing:
```python
    def print_result(self, result: Dict[str, Any]) -> None:
        """
        Print task execution result in a formatted way.

        Args:
            result: Result dictionary from run()
        """
        if result["skipped"]:
            print(f"  ⏭️  跳过")
        elif result["errors"]:
            print(f"  ❌ 错误: {result['errors']}")
        else:
            print(f"  ✅ 完成: 爬取 {result['fetched']} → 总结 {result['summarized']}")
```

**Step 6: Test imports**

```bash
python -c "from src.tasks.base import BaseTask; print('BaseTask imports OK')"
# Expected: "BaseTask imports OK"
```

**Step 7: Commit**

```bash
git add src/tasks/base.py
git commit -m "refactor: remove publish() from BaseTask"
```

---

## Task 3: Remove publisher import and publish() from WechatArticleTask

**Files:**
- Modify: `src/tasks/wechat.py`

**Step 1: Remove WechatPublisher import (line 38)**

Remove:
```python
        from ..publishers import WechatPublisher
```

**Step 2: Remove self.publisher initialization (line 45)**

Remove:
```python
        self.publisher = WechatPublisher()
```

**Step 3: Remove publish() method (lines 142-164)**

Remove entire method:
```python
    def publish(self, content: str, date: str) -> Dict[str, Any]:
        """
        Publish daily report to WeChat drafts.

        Args:
            content: Formatted Markdown content
            date: Date string in YYYY-MM-DD format

        Returns:
            Publish result with draft_id
        """
        print(f"\n📤 发布公众号日报...")
        report_path = self.output_dir / "daily_report.md"

        if not report_path.exists():
            return {"status": "error", "error": "Report file not found"}

        result = self.publisher.publish_daily_report(
            str(report_path),
            target_date=date
        )
        print(f"  ✅ 草稿已创建: {result['draft_id']}")
        return result
```

**Step 4: Update class docstring (lines 11-20)**

Change from:
```python
    """
    Task for WeChat Official Account articles.

    Workflow:
    1. Fetch articles from WeChat (never skips)
    2. Summarize with LLM
    3. Deduplicate with LLM
    4. Format to Markdown
    5. Publish to WeChat drafts
    """
```

To:
```python
    """
    Task for WeChat Official Account articles.

    Workflow:
    1. Fetch articles from WeChat (never skips)
    2. Summarize with LLM
    3. Deduplicate with LLM
    4. Format to Markdown
    """
```

**Step 5: Test imports**

```bash
python -c "from src.tasks.wechat import WechatArticleTask; print('WechatArticleTask imports OK')"
# Expected: "WechatArticleTask imports OK"
```

**Step 6: Commit**

```bash
git add src/tasks/wechat.py
git commit -m "refactor: remove publishing from WechatArticleTask"
```

---

## Task 4: Remove publisher import and publish() from GithubTrendingTask

**Files:**
- Modify: `src/tasks/github.py`

**Step 1: Remove WechatPublisher import (line 38)**

Remove:
```python
        from ..publishers import WechatPublisher
```

**Step 2: Remove self.publisher initialization (line 44)**

Remove:
```python
        self.publisher = WechatPublisher()
```

**Step 3: Remove publish() method (lines 142-164)**

Remove entire method:
```python
    def publish(self, content: str, date: str) -> Dict[str, Any]:
        """
        Publish GitHub Trending report to WeChat drafts.

        Args:
            content: Formatted Markdown content
            date: Date string in YYYY-MM-DD format

        Returns:
            Publish result with draft_id
        """
        print(f"\n📤 发布 GitHub Trending...")
        report_path = self.output_dir / "github_trending.md"

        if not report_path.exists():
            return {"status": "error", "error": "Report file not found"}

        result = self.publisher.publish_github_trending(
            str(report_path),
            target_date=date
        )
        print(f"  ✅ 草稿已创建: {result['draft_id']}")
        return result
```

**Step 4: Update class docstring (lines 11-20)**

Remove reference to publishing.

**Step 5: Test imports**

```bash
python -c "from src.tasks.github import GithubTrendingTask; print('GithubTrendingTask imports OK')"
# Expected: "GithubTrendingTask imports OK"
```

**Step 6: Commit**

```bash
git add src/tasks/github.py
git commit -m "refactor: remove publishing from GithubTrendingTask"
```

---

## Task 5: Remove publisher import and publish() from PapersTask

**Files:**
- Modify: `src/tasks/papers.py`

**Step 1: Remove WechatPublisher import (line 44)**

Remove:
```python
        from ..publishers import WechatPublisher
```

**Step 2: Remove self.publisher initialization (line 50)**

Remove:
```python
        self.publisher = WechatPublisher()
```

**Step 3: Remove publish() method (lines 178-200)**

Remove entire method.

**Step 4: Update class docstring**

Remove reference to publishing.

**Step 5: Test imports**

```bash
python -c "from src.tasks.papers import PapersTask; print('PapersTask imports OK')"
# Expected: "PapersTask imports OK"
```

**Step 6: Commit**

```bash
git add src/tasks/papers.py
git commit -m "refactor: remove publishing from PapersTask"
```

---

## Task 6: Remove publisher import and publish() from PaperAnalysisTask

**Files:**
- Modify: `src/tasks/paper_analysis.py`

**Step 1: Remove WechatPublisher import (line 54)**

Remove:
```python
        from ..publishers import WechatPublisher
```

**Step 2: Remove self.publisher initialization (line 59)**

Remove:
```python
        self.publisher = WechatPublisher()
```

**Step 3: Remove publish() method (lines 314-336)**

Remove entire method:
```python
    def publish(self, content: str, date: str) -> Dict[str, Any]:
        """
        Publish all paper analyses as separate drafts.

        Args:
            content: Summary content (not used, individual papers are published)
            date: Date string in YYYY-MM-DD format

        Returns:
            Publish results for all papers
        """
        print(f"\n📤 发布论文分析...")

        results = self.publisher.publish_all_papers(date)

        success_count = sum(1 for r in results if r.get('status') == 'success')
        print(f"\n✅ 完成: {success_count}/{len(results)} 篇论文发布成功")

        return {
            "status": "success" if success_count > 0 else "error",
            "count": len(results),
            "success_count": success_count
        }
```

**Step 4: Update class docstring (lines 16-25)**

Remove reference to publishing drafts.

**Step 5: Test imports**

```bash
python -c "from src.tasks.paper_analysis import PaperAnalysisTask; print('PaperAnalysisTask imports OK')"
# Expected: "PaperAnalysisTask imports OK"
```

**Step 6: Commit**

```bash
git add src/tasks/paper_analysis.py
git commit -m "refactor: remove publishing from PaperAnalysisTask"
```

---

## Task 7: Remove --publish and --dry-run flags from main.py

**Files:**
- Modify: `main.py`

**Step 1: Remove --publish argument (lines 242-246)**

Remove:
```python
    parser.add_argument(
        '--publish',
        action='store_true',
        help='推送到微信公众号草稿箱（默认不推送）'
    )
```

**Step 2: Remove dry_run parameter from run_pipeline() (line 58)**

Change:
```python
def run_pipeline(date: str, tasks_to_run: list, dry_run: bool = False):
```

To:
```python
def run_pipeline(date: str, tasks_to_run: list):
```

**Step 3: Update run_pipeline() docstring (lines 59-66)**

Change:
```python
    """
    运行完整流程：爬取 → 总结 → 清理 → 格式化 → 发布

    Args:
        date: 目标日期 (YYYY-MM-DD)
        tasks_to_run: 要运行的任务列表，包含 'wechat', 'github', 'paper'
        dry_run: 只运行到格式化，不实际发布
    """
```

To:
```python
    """
    运行完整流程：爬取 → 总结 → 清理 → 格式化

    Args:
        date: 目标日期 (YYYY-MM-DD)
        tasks_to_run: 要运行的任务列表，包含 'wechat', 'github', 'paper'
    """
```

**Step 4: Remove dry_run from task.run() call (line 109)**

Change:
```python
        result = task.run(date, dry_run=dry_run)
```

To:
```python
        result = task.run(date)
```

**Step 5: Remove dry_run print logic (lines 128-129)**

Remove:
```python
    if dry_run:
        print("\n🔍 DRY RUN - 跳过发布阶段")
```

**Step 6: Remove dry_run from run_paper_analysis_pipeline() (line 132)**

Change:
```python
def run_paper_analysis_pipeline(
    target_date: str = None,
    paper_num: int = 5,
    dry_run: bool = False
):
```

To:
```python
def run_paper_analysis_pipeline(
    target_date: str = None,
    paper_num: int = 5
):
```

**Step 7: Update docstring and remove dry_run logic**

Remove `dry_run` parameter from docstring and update the call (line 167):
```python
    result = task.run(target_date)
```

Remove lines 172-174:
```python
    if dry_run:
        print("\n[DRY RUN] 跳过发布阶段")
        return result
```

**Step 8: Remove args.publish references from main() (lines 254, 256, 284)**

Change line 254:
```python
                dry_run=not args.publish
```

To:
```python
```

And update the call to just pass target_date and paper_num:
```python
            run_paper_analysis_pipeline(
                target_date=args.date,
                paper_num=args.paper_num
            )
```

Change line 284:
```python
        run_pipeline(date=target_date, tasks_to_run=tasks_to_run, dry_run=not args.publish)
```

To:
```python
        run_pipeline(date=target_date, tasks_to_run=tasks_to_run)
```

**Step 9: Update file header docstring (lines 1-31)**

Remove references to `--publish` flag and update examples.

**Step 10: Update argparse epilog examples (lines 191-207)**

Remove examples showing `--publish` usage.

**Step 11: Test main.py imports**

```bash
python -c "import main; print('main.py imports OK')"
# Expected: "main.py imports OK"
```

**Step 12: Commit**

```bash
git add main.py
git commit -m "refactor: remove --publish and --dry-run flags"
```

---

## Task 8: Remove WeChat publishing config from config.py

**Files:**
- Modify: `config.py`

**Step 1: Remove WeChat publishing section (lines 53-67)**

Remove entire section:
```python
# ================= 微信发布配置 =================

# 公众号 AppID 和 AppSecret
APP_ID = "wx5cd7b21241569ee4"
APP_SECRET = "28f082df74ed1b78163c8df2e9e8906b"

# 永久封面图 Media ID
COVER_MEDIA_ID = "eczXpKmOOMk1jO1pgqsdcSf22OGzinl4vNpgd_68ZSmv0qrD_aMbB2LdUEByVor_"

# 代理配置（用于微信公众号 API，绕过 IP 白名单限制）
# 设置为 None 则不使用代理
PROXIES = {
    "http": "http://127.0.0.1:1082",
    "https": "http://127.0.0.1:1082",
}
```

**Step 2: Update section header (line 20)**

Change:
```python
# ================= 微信爬取配置 =================
```

To:
```python
# ================= 微信配置 =================
```

**Step 3: Test imports**

```bash
python -c "import config; print('config.py imports OK')"
# Expected: "config.py imports OK"
```

**Step 4: Commit**

```bash
git add config.py
git commit -m "refactor: remove WeChat publishing config"
```

---

## Task 9: Remove publishing dependencies from requirements.txt

**Files:**
- Modify: `requirements.txt`

**Step 1: Remove mistune, premailer, tinycss2 (lines 16-21)**

Remove:
```python
# Markdown 渲染
mistune>=3.0.0

# CSS 处理与内联样式转换
tinycss2
premailer
```

**Step 2: Verify remaining dependencies**

Content should be:
```python
# DailyNews 项目依赖

# HTTP 请求
requests>=2.31.0

# HTML 解析
beautifulsoup4>=4.12.0
lxml>=5.0.0

# HTML 转 Markdown
markdownify>=0.11.6

# Gemini API (LLM 总结与分析)
google-generativeai>=0.3.0
```

**Step 3: Test that core dependencies still install**

```bash
pip install -r requirements.txt --quiet 2>&1 | tail -3
# Expected: No errors
```

**Step 4: Commit**

```bash
git add requirements.txt
git commit -m "chore: remove publishing dependencies"
```

---

## Task 10: Verify all imports work

**Files:**
- Test: Full import test

**Step 1: Test all task imports**

```bash
python -c "
from src.tasks import WechatArticleTask, GithubTrendingTask, PapersTask
from src.tasks.paper_analysis import PaperAnalysisTask
print('All task imports OK')
"
# Expected: "All task imports OK"
```

**Step 2: Test main entry point**

```bash
python main.py --help
# Expected: Help text without --publish or --dry-run flags
```

**Step 3: Verify no orphaned publisher references**

```bash
grep -r "WechatPublisher" src/ 2>/dev/null || echo "No WechatPublisher references found"
# Expected: "No WechatPublisher references found"

grep -r "publishers" src/ 2>/dev/null || echo "No publishers imports found"
# Expected: "No publishers imports found"
```

**Step 4: Verify no dry_run references**

```bash
grep -r "dry_run" src/ main.py 2>/dev/null || echo "No dry_run references found"
# Expected: "No dry_run references found"
```

**Step 5: Commit**

```bash
# If any cleanup was needed
git add -A
git commit -m "test: verify all imports work after publishing removal"
```

---

## Task 11: Update CLAUDE.md documentation

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Update project overview (lines 1-10)**

Change to reflect that the system is now a markdown generation system.

**Step 2: Update running section (lines 14-17)**

Remove references to publishing, update examples to:
```bash
# Generate daily reports to output/
python main.py --wechat --github --paper
```

**Step 3: Remove or update publishing sections**

Remove any sections discussing WeChat publishing APIs, credentials for publishing, etc.

**Step 4: Keep cookie/fetching documentation**

Keep documentation about cookie1.txt for fetching articles.

**Step 5: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: update CLAUDE.md after publishing removal"
```

---

## Verification Task

**Step 1: Run full test**

```bash
# Test that help works
python main.py --help

# Verify the output directory structure would be created correctly
python -c "
from pathlib import Path
from src.tasks import WechatArticleTask
from src.summarizers import GeminiClient

output_dir = Path('output/test')
task = WechatArticleTask(client=None, output_dir=output_dir)
print(f'Task initialized with output_dir: {task.output_dir}')
print('Task creation works correctly')
"
```

**Step 2: Final commit**

```bash
git add -A
git commit -m "feat: complete publishing removal, system now generates markdown only"
```

---

## Summary

After completing all tasks:
- `src/publishers/` directory is completely removed
- All task classes no longer have `publish()` methods
- `--publish` and `--dry-run` flags are gone from CLI
- `config.py` no longer has WeChat API publishing credentials
- `requirements.txt` has minimal dependencies
- System workflow: Fetch → Summarize → Format (output markdown to `output/`)
