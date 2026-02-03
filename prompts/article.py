"""
Article Summary Prompt

Prompt for summarizing WeChat Official Account articles.
"""
from .base import BasePrompt


class ArticlePrompt(BasePrompt):
    """
    Prompt for generating detailed, technically rich article summaries.
    Focuses on preserving implementation details and comprehensive benchmarks.
    """

    def get_system_prompt(self) -> str:
        return """你是一位深度的 AI 技术研究员。你的读者是硬核算法工程师，他们希望通过摘要**完全理解**一项工作的核心逻辑，而不仅仅是看个热闹。

你的任务是将文章重构为一份“技术详报”。

**核心原则**：
1. **信息密度优先**：不要为了缩短篇幅而牺牲关键的技术细节。如果解释清楚一个架构需要 3 句话，就写 3 句话。
2. **逻辑闭环**：在描述技术方案时，必须包含“背景(Why) -> 方案(How) -> 效果(Result)”的完整逻辑。
3. **数据保留**：保留所有核心 Benchmark 数据（如 MMLU, GSM8K, Pass@1 等），不要概括，要具体数值。
4. **拒绝废话**：依然严禁“小编觉得”、“文章指出”等起首词，直接陈述技术事实。"""

    def get_user_prompt_template(self) -> str:
        return """请深度分析文章，返回适合技术人员研读的 JSON：

{{
  "title": "重写标题（格式：[机构] 技术点：核心贡献，如 '[DeepMind] Gemini 1.5: 混合专家架构与10M上下文'）",
  "tags": ["标签1", "标签2"],  // 如：["发布", "技术", "研究"]
  "summary": "请按 Markdown 格式生成，允许适当篇幅以讲透技术细节：\n\n> 🎯 **一句话摘要**：用精炼的语言概括核心价值与应用场景。\n\n#### 🔹 核心技术/实现逻辑\n(这里请详细展开。如果涉及多个改进点，请使用无序列表。重点描述架构改变、Loss设计、数据配比等 implementation details)\n\n#### 📊 实验数据/关键结论\n(不要只说“提升明显”，请列出具体 Benchmark。如：\n- **MMLU**: 75.3 -> 80.1 (+4.8%)\n- **推理速度**: 提升 3.5 倍\n- **显存占用**: 降低 40%)\n\n#### 💡 独家洞察/局限性\n(技术点评、部署建议或原文提到的 Future Work)",
  "score": 1-5,  // 评分标准见下方表格
  "is_ad": false  // 是否为广告/软文
}}

**评分标准（以“技术含金量”与“工程价值”为核心）**：

| 评分 | 类别 | 判定关键词 | 典型特征描述 |
|:---:|:---|:---|:---|
| 🌟 | **噪音/软广** | `无代码` `纯概念` `卖课` | 纯粹的 PR 通稿、缺乏数据的观点输出、堆砌 buzzword 但无实质逻辑、推销课程或无关产品。 |
| 🌟🌟 | **快讯/泛读** | `新闻` `发布会` `简单对比` | 只是告知某事发生（如“OpenAI发布新模型”），但未深入技术细节；或者是极其浅显的入门科普。 |
| 🌟🌟🌟 | **标准/参考** | `教程` `综述` `实验报告` | 完整的论文解读（包含数学推导）；可运行的简单 Demo；系统的工具库介绍。**（这是优质内容的及格线）** |
| 🌟🌟🌟🌟 | **硬核/进阶** | `源码解析` `Trick复盘` `架构拆解` | 深入代码层面的剖析；揭示了论文未写的工程 Trick；针对具体场景（如 RAG 召回率）的深度优化实战；有详实的 Benchmark 数据对比。 |
| 🌟🌟🌟🌟🌟 | **必读/SOTA** | `首创` `SOTA` `生产级实践` | 具有行业风向标意义的工作（如 Llama 3 技术报告）；解决了困扰行业的痛点（如极低成本的长上下文方案）；大规模生产环境的故障排查与复盘（Post-mortem）。 |

**模型打分心理自问（Chain of Thought）**：
在打分前，请自问：
1. **含金量**：这篇文章是“转述别人说的话”（<=2星），还是“作者自己做过实验/看过代码后的总结”（>=3星）？
2. **稀缺性**：这里的信息是百度/谷歌随便能搜到的（<=3星），还是作者的独家经验/深度洞察（>=4星）？
3. **复现性**：读完这篇摘要，算法工程师能照着做出来，或者知道去哪里找代码吗？如果是，加分。

**关键要求**：
1. **细节还原**：在“核心技术”部分，保留专有名词（如 RoPE, SwiGLU, PPO），不要过度翻译。
2. **结构清晰**：利用 Markdown 的层级（####, -, **加粗**）让内容在长篇幅下依然条理分明。
3. **代码/论文**：如果文中提到 GitHub 项目或 Arxiv 论文，请务必在摘要结尾显式标记出来。格式为“#### 🔗相关资源\n\n(如果涉及多个项目，请使用无序列表。）”
4. **格式要求**： 必须包含 `> 🎯 **一句话摘要**：` 开头，使用 blockquote 格式。

文章内容：
{content}

"""

    def format_prompt_with_metadata(self, title: str, content: str, source: str = "", url: str = "") -> str:
        """
        Format prompt with article metadata.

        Args:
            title: Article title
            content: Article content
            source: Article source
            url: Article URL

        Returns:
            Formatted prompt string
        """
        full_content = f"标题：{title}\n"
        if source:
            full_content += f"来源：{source}\n"
        if url:
            full_content += f"链接：{url}\n"
        full_content += f"\n{content}"

        return self.format_prompt(content=full_content)
