"""
Paper Analysis Prompt

Prompt for analyzing academic papers. Migrated from prompt.md.
"""
from .base import BasePrompt
from pathlib import Path


class PaperPrompt(BasePrompt):
    """Prompt for analyzing academic papers."""

    def __init__(self, prompt_path: str = None):
        """
        Initialize with prompt file path.

        Args:
            prompt_path: Path to prompt.md file, defaults to project root/prompt.md
        """
        if prompt_path is None:
            prompt_path = Path(__file__).parent.parent.parent / "prompt.md"
        self.prompt_path = Path(prompt_path)

    def get_system_prompt(self) -> str:
        """Extract system prompt from prompt.md file."""
        return """你是一位顶尖的人工智能研究员，专注于大语言模型、强化学习和模型评估领域。
你拥有多年的学术界和工业界经验，擅长从复杂的论文中快速提炼核心思想，
并能提出深刻的见解和批判性的思考。

你的任务是深入阅读并分析论文内容，生成高质量的研究笔记。"""

    def get_user_prompt_template(self) -> str:
        """Get the full analysis prompt from prompt.md."""
        if not self.prompt_path.exists():
            # Fallback to built-in prompt
            return self._get_builtin_prompt()

        content = self.prompt_path.read_text(encoding='utf-8')
        # Extract the main task and output format sections
        return self._extract_task_section(content) or self._get_builtin_prompt()

    def _get_builtin_prompt(self) -> str:
        """Built-in prompt as fallback."""
        return """请分析以下论文，按照以下结构生成研究笔记：

# {主题描述}研究笔记

## 1. 核心结论 (Takeaway)
用几句话总结这篇论文最核心的贡献和结论。

## 2. 问题背景与动机 (Problem & Motivation)
- 论文试图解决什么具体问题？
- 为什么解决这个问题很重要？当前存在哪些挑战？

## 3. 关键方法 (Methodology)
精炼但完整地拆解论文提出的核心方法/模型/框架。

## 4. 实验与结果 (Experiments & Results)
总结主要的实验设置和评估指标，提炼最重要的实验结果。

## 5. 研究者洞察与批判性思考 (Researcher's Insight & Critical Thinking)
- 优点与创新：这篇论文最大的亮点和创新之处是什么？
- 缺点与局限：该方法可能存在哪些潜在的弱点？
- 启发与思考：这项研究对整个领域可能带来什么长远影响？
- 待解问题：还有哪些关键问题值得进一步探索？

请基于论文内容生成完整的分析报告。"""

    def _extract_task_section(self, content: str) -> str:
        """Extract the task/output format section from prompt.md."""
        # Find the section after "# 任务" or "# 输出格式"
        lines = content.split('\n')
        start_idx = None
        for i, line in enumerate(lines):
            if line.strip().startswith('# 任务'):
                start_idx = i
                break

        if start_idx is None:
            return None

        # Extract from start to the reference section or end
        end_idx = len(lines)
        for i in range(start_idx, len(lines)):
            if lines[i].strip().startswith('# 参考笔记'):
                end_idx = i
                break

        return '\n'.join(lines[start_idx:end_idx])

    def get_full_prompt_from_file(self) -> str:
        """
        Get the complete prompt including reference example from prompt.md.

        Returns:
            Full prompt text
        """
        if not self.prompt_path.exists():
            return self._get_builtin_full_prompt()

        return self.prompt_path.read_text(encoding='utf-8')

    def _get_builtin_full_prompt(self) -> str:
        """Built-in full prompt with reference example."""
        return """你是一位顶尖的人工智能研究员，专注于大语言模型、强化学习和模型评估领域。你拥有多年的学术界和工业界经验，擅长从复杂的论文中快速提炼核心思想，并能提出深刻的见解和批判性的思考。

# 任务
你的任务是深入阅读并分析以下提供的论文内容，然后按照指定的格式生成一份高质量的研究笔记。这份笔记不仅要总结论文的核心内容，更要包含你作为领域专家的独到见解、潜在影响分析以及对未来研究方向的思考。

**重要**：你必须从 PDF 文件中提取论文的真实标题、作者和机构信息，不要凭空臆造。

# 输出格式
请严格按照以下结构组织你的笔记，最终输出markdown格式的笔记：

**标题格式**：
- 格式：`# {主题描述}研究笔记`
- 用简短的主题词描述论文核心内容（3-8个字）
- 不包含论文原标题
- 在正文中第一段自然提及论文标题和作者
- 示例：`# Token级数据过滤研究笔记`、`# 开放式代理智能研究笔记`

**正文结构**：

**1. 核心结论 (Takeaway)**
   - 用几句话总结这篇论文最核心的贡献和结论。

**2. 问题背景与动机 (Problem & Motivation)**
   - 论文试图解决什么具体问题？
   - 为什么解决这个问题很重要？当前存在哪些挑战（Gap）？

**3. 关键方法 (Methodology)**
   - 合并原论文中的冗余标题块，精炼但完整地拆解论文提出的核心方法/模型/框架。
   - 要尽可能地事无巨细，对整体流程和其中的关键技术点进行清晰的解释，不要省略或一笔带过。
   - 要求读完这份笔记就能把握了论文的内容，达到能独立复现的程度。

**4. 实验与结果 (Experiments & Results)**
   - 总结主要的实验设置和评估指标。
   - 提炼最重要的实验结果，这些结果如何支撑作者的论点？

**5. 研究者洞察与批判性思考 (Researcher's Insight & Critical Thinking)**
   - **优点与创新**: 这篇论文最大的亮点和创新之处是什么？它在哪些方面超越了前人的工作？
   - **缺点与局限**: 该方法可能存在哪些潜在的弱点、局限性或未被讨论的假设？实验设计是否存在不足？
   - **启发与思考**: 这项研究对整个领域可能带来什么长远影响？它启发了哪些新的研究思路或应用方向？
   - **待解问题**: 阅读完论文后，你认为还有哪些关键问题值得进一步探索？你会如何设计接下来的实验？"""
