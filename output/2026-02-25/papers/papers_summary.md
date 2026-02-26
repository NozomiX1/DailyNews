# 每日论文汇总 - 2026-02-25

**论文数量**: 13

---

###  1. 探究提升大语言模型终端能力的数据工程方法 (On Data Engineering for Scaling LLM Terminal Capabilities)

**论文链接**: [https://arxiv.org/abs/2602.21193](https://arxiv.org/abs/2602.21193)
**组织**: NVIDIA
**得分**: 42.97
**标签**: Frontier Lab
**Upvotes**: 74 | **Stars**: 0

**摘要**: 针对LLM终端代理训练策略不透明的痛点，本文提出了Terminal-Task-Gen流水线构建Terminal-Corpus数据集，并训练了Nemotron-Terminal模型。通过课程学习和长上下文训练，该模型在Terminal-Bench 2.0上性能显著提升（最高至27.4%），匹配更大模型水平。

**亮点**:
  - 提出Terminal-Task-Gen合成任务生成流水线
  - 开源大规模Terminal-Corpus数据集
  - Nemotron-Terminal模型在终端任务上性能大幅提升

---

###  2. 通用LLM智能体测试时扩展基准测试 (Benchmark Test-Time Scaling of General LLM Agents)

**论文链接**: [https://arxiv.org/abs/2602.18998](https://arxiv.org/abs/2602.18998)
**组织**: CMU-LTI
**得分**: 41.73
**标签**: Frontier Lab
**Upvotes**: 5 | **Stars**: 6

**摘要**: 针对现有基准缺乏对通用智能体多技能协作评估的问题，提出General AgentBench统一框架，涵盖搜索、编码等领域并系统研究测试时扩展策略。实验发现，主流智能体在此设置下性能大幅下降，且因上下文上限和验证缺口，扩展策略难以有效提升表现。

**亮点**:
  - 提出General AgentBench通用智能体基准
  - 揭示测试时扩展的局限性（上下文上限与验证缺口）
  - 发现通用场景下智能体性能显著下降

---

###  3. 面向长上下文处理的查询聚焦与记忆感知重排序模型 (Query-focused and Memory-aware Reranker for Long Context Processing)

**论文链接**: [https://arxiv.org/abs/2602.12192](https://arxiv.org/abs/2602.12192)
**组织**: Tencent
**得分**: 39.93
**标签**: Frontier Lab
**Upvotes**: 38 | **Stars**: 0

**摘要**: 针对现有重排序方法对监督数据依赖强的问题，本文提出利用大模型检索头的注意力分数估计相关性的重排序框架。该方法无需Likert量表监督，支持Listwise排序，且仅需4B参数即可在多个领域及LoCoMo基准上超越SOTA性能。

**亮点**:
  - 利用注意力分数估计相关性
  - 无需Likert量表监督的Listwise排序
  - 在LoCoMo基准上刷新SOTA

---

###  4. PyVision-RL：通过强化学习构建开放权重的智能体视觉模型 (PyVision-RL: Forging Open Agentic Vision Models via RL)

**论文链接**: [https://arxiv.org/abs/2602.20739](https://arxiv.org/abs/2602.20739)
**组织**: Unknown
**得分**: 39.9
**标签**: 
**Upvotes**: 24 | **Stars**: 43

**摘要**: 针对智能体多模态模型的交互坍缩问题，提出PyVision-RL框架。该方法结合过采样策略与累积工具奖励，并开发了支持按需上下文构建的PyVision模型。实验表明其显著提升了性能与推理效率。

**亮点**:
  - 解决强化学习中的交互坍缩问题
  - 提出过采样-过滤-排序训练策略
  - 实现视频推理的按需上下文构建

---

###  5. 基于 KV 绑定的测试时训练实质上是隐式线性注意力机制 (Test-Time Training with KV Binding Is Secretly Linear Attention)

**论文链接**: [https://arxiv.org/abs/2602.21204](https://arxiv.org/abs/2602.21204)
**组织**: NVIDIA
**得分**: 36.78
**标签**: Frontier Lab
**Upvotes**: 22 | **Stars**: 0

**摘要**: 针对测试时训练（TTT）常被误认为测试时记忆化的问题，该研究将其重新表述为习得的线性注意力算子。这一视角不仅解释了模型行为，还实现了架构简化和全并行化，在保持性能的同时提升效率，证明 TTT 本质上是具有增强表征能力的线性注意力机制。

**亮点**:
  - 重新定义 TTT 为习得线性注意力算子
  - 实现全并行化以提升计算效率
  - 系统性简化 TTT 架构

---

###  6. DREAM：基于智能体指标的深度研究评估 (DREAM: Deep Research Evaluation with Agentic Metrics)

**论文链接**: [https://arxiv.org/abs/2602.18940](https://arxiv.org/abs/2602.18940)
**组织**: Amazon Web Services
**得分**: 33.09
**标签**: Frontier Lab
**Upvotes**: 10 | **Stars**: 0

**摘要**: 针对深度研究 Agent 因缺乏单一真值及“合成幻象”导致的评估难题，本文提出 DREAM 框架。该框架利用工具调用 Agent 实现评估代理化，通过自适应指标验证时间有效性与事实正确性。实验表明，DREAM 对事实和时间衰减的检测灵敏度显著优于现有基准。

**亮点**:
  - 揭示深度研究评估中的“合成幻象”及能力不匹配问题
  - 提出基于能力对等原则的 DREAM 代理评估框架
  - 显著提升对事实错误和时间衰减的检测灵敏度

---

###  7. LongCLI-Bench：命令行界面中长时程智能体编程的初步基准与研究 (LongCLI-Bench: A Preliminary Benchmark and Study for Long-horizon Agentic Programming in Command-Line Interfaces)

**论文链接**: [https://arxiv.org/abs/2602.14337](https://arxiv.org/abs/2602.14337)
**组织**: Unknown
**得分**: 32.19
**标签**: 
**Upvotes**: 10 | **Stars**: 22

**摘要**: 针对现有基准在长时程任务评估上的不足，该研究推出了包含20项真实任务的LongCLI-Bench基准，并设计了双集测试协议与步骤级评分机制。实验发现即使最先进的智能体通过率也低于20%，且人机协作显著优于纯智能体执行。

**亮点**:
  - 提出长时程命令行编程基准 LongCLI-Bench
  - 引入双集测试协议与步骤级评分
  - 揭示 SOTA 智能体表现不足，强调人机协作重要性

---

###  8. 基于连续去噪的单步语言建模 (One-step Language Modeling via Continuous Denoising)

**论文链接**: [https://arxiv.org/abs/2602.16813](https://arxiv.org/abs/2602.16813)
**组织**: Unknown
**得分**: 30.74
**标签**: 
**Upvotes**: 3 | **Stars**: 43

**摘要**: 针对离散扩散模型少步生成质量下降的问题，提出基于流的连续去噪语言模型(FLM)。该方法在独热编码上进行欧几里得去噪，并利用时间重参数化提升稳定性。通过蒸馏得到的FMLM，其单步生成质量显著优于现有少步模型，实现了高效生成。

**亮点**:
  - 提出基于流的连续去噪模型 FLM 与 FMLM
  - 单步生成质量超越现有少步语言模型
  - 挑战离散扩散对离散模态生成的必要性

---

###  9. 高效推理的艺术：数据、奖励与优化 (The Art of Efficient Reasoning: Data, Reward, and Optimization)

**论文链接**: [https://arxiv.org/abs/2602.20945](https://arxiv.org/abs/2602.20945)
**组织**: Tencent Hunyuan
**得分**: 28.74
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 0

**摘要**: 针对LLM思维链推理计算成本高昂的问题，本文系统性调研了高效推理的数据、奖励与优化机制。通过大规模实验，揭示了“长度适应与推理优化”两阶段范式，并提出在简单提示词上训练以避免长度崩溃。该方法在Qwen3系列模型上验证了鲁棒性。

**亮点**:
  - 揭示高效推理两阶段训练范式
  - 发现简单提示词训练可避免长度崩溃
  - 在Qwen3全系列模型验证有效性

---

###  10. Aletheia 自主应对 FirstProof 挑战 (Aletheia tackles FirstProof autonomously)

**论文链接**: [https://arxiv.org/abs/2602.21201](https://arxiv.org/abs/2602.21201)
**组织**: Google
**得分**: 27.62
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 本文评估了基于 Gemini 3 Deep Think 的数学研究智能体 Aletheia 在首届 FirstProof 挑战赛中的表现。该智能体通过自主推理，在规定时间内成功解决了 10 道数学证明题中的 6 道。实验结果验证了其在自主解决复杂数学问题方面的能力。

**亮点**:
  - 基于 Gemini 3 Deep Think 的数学智能体
  - 自主解决 FirstProof 挑战赛 6/10 问题
  - 公开完整实验数据与提示词

---

###  11. 任意模态下的多向量索引压缩 (Multi-Vector Index Compression in Any Modality)

**论文链接**: [https://arxiv.org/abs/2602.21202](https://arxiv.org/abs/2602.21202)
**组织**: JHU Human Language Technology Center of Excellence
**得分**: 25.73
**标签**: 
**Upvotes**: 19 | **Stars**: 4

**摘要**: 针对后期交互检索随文档长度增加导致存储和计算成本高昂的问题，本文提出了四种查询无关的压缩方法，重点介绍了注意力引导聚类（AGC）。AGC 利用注意力机制识别语义显著区域进行聚合。实验显示，AGC 在多模态检索任务上优于其他参数化方法，且能在大幅压缩索引后保持甚至超越未压缩模型的性能。

**亮点**:
  - 跨模态多向量压缩方案
  - 提出注意力引导聚类（AGC）方法
  - 压缩后性能超越未压缩索引

---

###  12. 从感知到行动：用于视觉推理的交互式基准 (From Perception to Action: An Interactive Benchmark for Vision Reasoning)

**论文链接**: [https://arxiv.org/abs/2602.21015](https://arxiv.org/abs/2602.21015)
**组织**: Unknown
**得分**: 25.16
**标签**: 
**Upvotes**: 21 | **Stars**: 3

**摘要**: 现有 VLM 评估侧重于被动感知，缺乏对动态环境物理结构推理的评估。为此，提出交互式 3D 物理基准 CHAIN，测试模型在物理约束下规划并执行动作序列的能力。研究发现，SOTA 模型仍难以内化物理因果约束，在长时序规划和动作转化上表现不佳。

**亮点**:
  - 提出交互式 3D 物理基准 CHAIN
  - 从被动感知转向主动问题解决
  - 揭示 SOTA 模型难以内化物理约束

---

###  13. 通过主动重构检测语言模型训练数据 (Learning to Detect Language Model Training Data via Active Reconstruction)

**论文链接**: [https://arxiv.org/abs/2602.19020](https://arxiv.org/abs/2602.19020)
**组织**: University of Washington NLP
**得分**: 24.56
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 0

**摘要**: 针对传统成员推断攻击（MIA）被动且受限的问题，本文提出主动数据重构攻击（ADRA）。该方法利用强化学习主动诱导模型重构文本，通过分析训练数据与非成员的可重构性差异进行推断。实验表明，ADRA 在预训练和后训练数据检测上显著优于现有方法，平均性能提升 10.7%。

**亮点**:
  - 提出主动数据重构攻击（ADRA）框架
  - 利用强化学习（RL）主动诱导模型重构以提升检测精度
  - 在预训练与后训练数据检测中显著超越现有 SOTA

---
