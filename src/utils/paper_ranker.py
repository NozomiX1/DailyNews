"""
PaperRanker - 为 HuggingFace Daily Papers API 设计的评分系统

数据来源: https://huggingface.co/api/daily_papers?date=YYYY-MM-DD
"""
import math
import re
from typing import Dict, List, Any, Optional


class PaperRanker:
    """HuggingFace 论文评分器"""

    # 超级实验室 (持续发布模型、刷榜的顶级实验室) - +50 分
    SUPER_LABS = [
        r"\bOpenAI\b",           # GPT系列
        r"\bAnthropic\b",         # Claude系列
        r"Google DeepMind|DeepMind",  # Gemini, AlphaFold
        r"\bDeepSeek\b",          # V3, R1...
        r"\bQwen\b",              # 通义千问
        r"\bMoonshot\b",          # Kimi (月之暗面)
        r"\bMistral\b",           # Mistral AI
        r"\bMeta AI\b",           # LLaMA系列
        r"01\.AI|零一万物|Zhipu",  # 智谱 AI / Zhipu AI
        r"\bByteDance\b",         # 豆包
        r"\bBaichuan\b",          # 百川智能
    ]

    # Frontier 实验室 (顶级研究机构) - +20 分
    FRONTIER_LABS = [
        r"DeepMind|Google", r"Meta AI|FAIR|Facebook",
        r"Anthropic", r"NVIDIA", r"Microsoft", r"Alibaba", r"Tencent",
        r"DeepSeek", r"Qwen", r"Mistral", r"Moonshot",
        r"01\.AI|Zhipu", r"ByteDance", r"Baichuan",
        r"Stanford", r"Berkeley", r"MIT", r"CMU",
        r"OpenAI", r"Tsinghua", r"Peking University",
        r"Huawei", r"Baidu", r"SenseTime"
    ]

    # 兴趣关键词 (命中 +10 分)
    INTEREST_KEYWORDS = [
        r"LLM", r"Large Language Model", r"Reasoning", r"Chain of Thought",
        r"Agent", r"RAG", r"Retrieval", r"Efficient", r"Quantization",
        r"Post-training", r"RLHF", r"Alignment", r"World Model",
        r"Multimodal", r"Vision", r"Diffusion"
    ]

    def __init__(
        self,
        *,
        upvotes_weight: float = 1.0,
        stars_weight: float = 1.5,
        comments_weight: float = 0.5,
        super_lab_bonus: float = 50.0,
        lab_bonus: float = 20.0,
        topic_bonus: float = 10.0,
        enable_topic_bonus: bool = False
    ):
        """
        初始化评分器

        Args:
            upvotes_weight: upvotes 权重
            stars_weight: stars 权重
            comments_weight: comments 权重
            super_lab_bonus: 超级实验室加成 (OpenAI/Anthropic/DeepMind/DeepSeek)
            lab_bonus: 普通 Frontier Lab 加成
            topic_bonus: 兴趣匹配加成
            enable_topic_bonus: 是否启用兴趣加成
        """
        self.upvotes_weight = upvotes_weight
        self.stars_weight = stars_weight
        self.comments_weight = comments_weight
        self.super_lab_bonus = super_lab_bonus
        self.lab_bonus = lab_bonus
        self.topic_bonus = topic_bonus if enable_topic_bonus else 0

    def _check_regex_list(self, text: str, regex_list: List[str]) -> bool:
        """检查文本是否匹配正则列表中的任一模式"""
        if not text:
            return False
        for pattern in regex_list:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False

    def _extract_fields(self, api_item: Dict[str, Any]) -> Dict[str, Any]:
        """从 API 响应中提取评分所需的字段"""
        paper = api_item.get("paper", {})

        return {
            "title": api_item.get("title", ""),
            "org": api_item.get("organization", {}).get("fullname", ""),
            "upvotes": paper.get("upvotes", 0),
            "stars": paper.get("githubStars", 0),
            "comments": api_item.get("numComments", 0),
            "github_repo": paper.get("githubRepo", ""),
            "arxiv_id": paper.get("id", ""),
            "summary": paper.get("summary", "") or api_item.get("summary", ""),
            "ai_keywords": paper.get("ai_keywords", []),
            "ai_summary": paper.get("ai_summary", ""),
        }

    def calculate_score(self, api_item: Dict[str, Any]) -> Dict[str, Any]:
        """
        计算单篇论文的得分

        Args:
            api_item: HuggingFace API 返回的单篇论文数据

        Returns:
            包含 score, is_golden, reasons 等字段的字典
        """
        fields = self._extract_fields(api_item)

        score = 0.0
        reasons = []

        # --- 基础数值指标 (Log 归一化) ---
        upvotes = fields["upvotes"]
        stars = fields["stars"]
        comments = fields["comments"]

        # Upvotes
        u_score = math.log1p(upvotes) * 5 * self.upvotes_weight
        score += u_score

        # Stars
        s_score = math.log1p(stars) * 4 * self.stars_weight
        score += s_score

        # Comments
        c_score = math.log1p(comments) * 2 * self.comments_weight
        score += c_score

        # --- 实验室加成 ---
        org = fields["org"]
        is_super = self._check_regex_list(org, self.SUPER_LABS)
        is_frontier = self._check_regex_list(org, self.FRONTIER_LABS)

        if is_super:
            score += self.super_lab_bonus
            reasons.append("Super Lab")
        elif is_frontier:
            score += self.lab_bonus
            reasons.append("Frontier Lab")

        # --- 兴趣匹配加成 ---
        if self.topic_bonus > 0:
            title_match = self._check_regex_list(fields["title"], self.INTEREST_KEYWORDS)
            summary_match = self._check_regex_list(fields["summary"], self.INTEREST_KEYWORDS)

            if title_match or summary_match:
                score += self.topic_bonus
                reasons.append("Relevant")

        # --- 金牌直通车规则 ---
        is_golden = False

        # 爆款直通
        if stars > 2000 or upvotes > 500:
            is_golden = True
            reasons.append("Viral")

        # 超级实验室 + 相关领域
        if is_super:
            title_match = self._check_regex_list(fields["title"], self.INTEREST_KEYWORDS)
            if title_match:
                is_golden = True
                reasons.append("Must Read")

        return {
            "score": round(score, 2),
            "is_golden": is_golden,
            "reasons": ", ".join(reasons),
            "fields": fields,
        }

    def rank_papers(self, api_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        对论文列表进行评分和排序

        Args:
            api_items: HuggingFace API 返回的论文列表

        Returns:
            评分并排序后的论文列表，每个元素包含原数据 + score, is_golden, reasons
        """
        results = []

        for item in api_items:
            result = self.calculate_score(item)
            # 保留原始数据
            item["rank_score"] = result["score"]
            item["is_golden"] = result["is_golden"]
            item["rank_reasons"] = result["reasons"]
            results.append(item)

        # 排序: Golden 优先，然后按分数降序
        results.sort(key=lambda x: (x["is_golden"], x["rank_score"]), reverse=True)

        return results


# --- 便捷函数 ---

def fetch_and_rank(date: str, max_papers: int = 10, enable_topic_bonus: bool = False) -> List[Dict]:
    """
    获取指定日期的论文并排名

    Args:
        date: 日期字符串 (YYYY-MM-DD)
        max_papers: 最多返回论文数
        enable_topic_bonus: 是否启用兴趣加成

    Returns:
        排名后的论文列表
    """
    import requests

    url = f"https://huggingface.co/api/daily_papers?date={date}"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if resp.status_code != 200:
        raise Exception(f"API 请求失败: {resp.status_code}")

    papers = resp.json()

    if not papers:
        return []

    ranker = PaperRanker(enable_topic_bonus=enable_topic_bonus)
    ranked = ranker.rank_papers(papers)

    return ranked[:max_papers]


def print_ranking(ranked_papers: List[Dict], show_details: bool = True):
    """
    打印排名结果

    Args:
        ranked_papers: 排名后的论文列表
        show_details: 是否显示详细信息
    """
    print("=" * 100)
    print("论文排名")
    print("=" * 100)

    for i, p in enumerate(ranked_papers, 1):
        golden = "🏆" if p.get("is_golden") else "  "
        title = p.get("title", "")[:55]
        score = p.get("rank_score", 0)
        reasons = p.get("rank_reasons", "")

        print(f'{i:2d}. [{golden}] {score:6.2f} | {title}...')

        if show_details:
            paper = p.get("paper", {})
            org = p.get("organization", {}).get("fullname", "")
            upvotes = paper.get("upvotes", 0)
            stars = paper.get("githubStars", 0)
            comments = p.get("numComments", 0)

            print(f"     Org: {org} | upvotes:{upvotes:3d} stars:{stars:4d} comments:{comments:2d}")
            if reasons:
                print(f"     Tags: {reasons}")
            print()


if __name__ == "__main__":
    import argparse
    from datetime import date, timedelta

    parser = argparse.ArgumentParser(description="获取并排名 HuggingFace 每日论文")
    parser.add_argument("--date", default=None, help="日期 (YYYY-MM-DD)，默认昨天")
    parser.add_argument("--max-papers", type=int, default=10, help="最多返回论文数")
    parser.add_argument("--topic-bonus", action="store_true", help="启用兴趣加成")

    args = parser.parse_args()

    # 默认昨天
    target_date = args.date or (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"获取 {target_date} 的论文...")

    ranked = fetch_and_rank(target_date, max_papers=args.max_papers, enable_topic_bonus=args.topic_bonus)
    print_ranking(ranked)
