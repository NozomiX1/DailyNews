# GitHub Summarizer
# Summarize GitHub Trending repositories
import json
import time
from typing import Dict, Any, List
from pathlib import Path

from .base import BaseSummarizer
from prompts.github import GithubPrompt


class GithubSummarizer(BaseSummarizer):
    """Summarizer for GitHub repositories."""

    def __init__(self, client, readme_dir: Path = None, date: str = None):
        """
        Initialize GitHub summarizer.

        Args:
            client: LLM client instance
            readme_dir: Directory containing downloaded README files
            date: Date string for determining readme_dir path
        """
        super().__init__(client)
        self.prompt = GithubPrompt()
        if readme_dir is None:
            project_root = Path(__file__).parent.parent.parent
            # 新路径: data/{date}/trending/readme_files/
            if date is None:
                from datetime import datetime
                date = datetime.now().strftime('%Y-%m-%d')
            readme_dir = project_root / "data" / date / "trending" / "readme_files"
        self.readme_dir = Path(readme_dir)
        self.date = date

    def _load_readme(self, owner: str, repo: str) -> str:
        """Load README content from local cache."""
        # 扁平文件名: owner_repo.md
        filename = f"{owner}_{repo}.md"
        readme_path = self.readme_dir / filename

        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                return f.read()

        return ""

    def summarize(self, content: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Summarize a single repository.

        Args:
            content: README content (or description if no README)
            metadata: Repository metadata

        Returns:
            Summary dictionary
        """
        name = metadata.get('name', '')
        owner = metadata.get('owner', '')
        description = metadata.get('description', '')
        language = metadata.get('language', '')
        stars = metadata.get('total_stars', '0')
        today_stars = metadata.get('stars_period', '0')
        url = metadata.get('url', '')

        # Format prompt
        prompt_text = self.prompt.format_prompt_for_repo(
            name=name,
            description=description,
            language=language,
            stars=stars,
            today_stars=today_stars,
            url=url,
            readme_content=content
        )

        try:
            response = self.client.generate_content(prompt_text)
            result = self._extract_json_from_response(response.text)

            # Merge with metadata
            result.update(metadata)
            result['owner'] = owner
            result['today_stars'] = today_stars

            return result

        except Exception as e:
            print(f"    ❌ 总结失败 ({name}): {e}")
            # Return fallback
            return {
                'name': name,
                'owner': owner,
                'summary': description or "无描述",
                'tech_stack': [language] if language else [],
                'use_cases': [],
                'is_worthy': int(today_stars or 0) > 50,
                'url': url,
                'language': language,
                'stars': stars,
                'today_stars': today_stars,
                'error': str(e)
            }

    def summarize_batch(self, repos: List[Dict], delay: float = 0.5, output_path: str = None) -> List[Dict]:
        """
        Summarize multiple repositories.

        Args:
            repos: List of repository dictionaries
            delay: Delay between requests
            output_path: If provided, save results incrementally after each repo

        Returns:
            List of summary dictionaries
        """
        results = []
        total = len(repos)

        print(f"  🤖 开始总结 {total} 个项目...")

        for i, repo in enumerate(repos, 1):
            name = repo.get('name', '')
            print(f"    [{i}/{total}] {name}")

            # Try to load README
            owner = repo.get('owner', '')
            readme_content = ""
            if owner:
                readme_content = self._load_readme(owner, name.split('/')[-1] if '/' in name else name)

            # Use description if no README
            if not readme_content:
                readme_content = repo.get('description', '')

            result = self.summarize(readme_content, repo)

            results.append(result)

            # 边总结边保存
            if output_path:
                self.save_json(results, output_path)

            if i < total:
                time.sleep(delay)

        print(f"  ✅ 总结完成，{len(results)} 个项目")

        return results
