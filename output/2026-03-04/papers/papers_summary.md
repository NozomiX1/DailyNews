# 每日论文汇总 - 2026-03-04

**论文数量**: 13

---

### 🏆 1. Qwen3-Coder-Next 技术报告 (Qwen3-Coder-Next Technical Report)

**论文链接**: [https://arxiv.org/abs/2603.00729](https://arxiv.org/abs/2603.00729)
**组织**: Qwen
**得分**: 125.79
**标签**: Super Lab, Viral
**Upvotes**: 27 | **Stars**: 15866

**摘要**: 针对大模型推理成本高的问题，提出了Qwen3-Coder-Next。该模型拥有800亿参数，推理时仅激活30亿。通过大规模可验证任务合成与可执行环境反馈的智能体训练，结合强化学习，在SWE-Bench等基准上，以极低的激活参数量实现了极具竞争力的性能。

**亮点**:
  - 仅激活30亿参数的高效架构
  - 基于环境反馈的智能体训练
  - SWE-Bench等基准性能优异

---

###  2. Utonia：迈向适用于所有点云的统一编码器 (Utonia: Toward One Encoder for All Point Clouds)

**论文链接**: [https://arxiv.org/abs/2603.03283](https://arxiv.org/abs/2603.03283)
**组织**: Pointcept
**得分**: 58.13
**标签**: 
**Upvotes**: 122 | **Stars**: 231

**摘要**: 针对不同领域点云数据差异巨大的问题，本文提出 Utonia，首个跨多域训练的自监督点云 Transformer 编码器。该模型在遥感、自动驾驶及室内场景等数据上学习到一致的特征表示，提升了感知能力并展现出涌现行为。此外，该特征有效增强了机器人操作及视觉语言模型的空间推理性能。

**亮点**:
  - 首个跨多域通用的点云自监督编码器
  - 实现跨遥感、驾驶及室内场景的一致特征学习
  - 显著提升机器人操作与视觉语言模型的推理能力

---

###  3. Track4World：前馈式世界坐标系下所有像素的密集 3D 跟踪 (Track4World: Feedforward World-centric Dense 3D Tracking of All Pixels)

**论文链接**: [https://arxiv.org/abs/2603.02573](https://arxiv.org/abs/2603.02573)
**组织**: ARC Lab, Tencent PCG
**得分**: 53.63
**标签**: Frontier Lab
**Upvotes**: 7 | **Stars**: 39

**摘要**: 针对现有单目 3D 跟踪局限于稀疏点或基于慢速优化的问题，本文提出前馈模型 Track4World。该模型基于 VGGT-style ViT 和 3D 关联方案，同时估计 2D/3D 密集流，实现世界坐标系下所有像素的高效 3D 跟踪。实验表明其在流估计和跟踪性能上持续优于现有方法。

**亮点**:
  - 提出前馈式模型实现全像素密集 3D 跟踪
  - 采用新颖的 3D 关联方案同时估计 2D/3D 流
  - 在多项基准测试中性能超越现有方法

---

###  4. CFG-Ctrl: 基于控制的无分类器扩散引导 (CFG-Ctrl: Control-Based Classifier-Free Diffusion Guidance)

**论文链接**: [https://arxiv.org/abs/2603.03281](https://arxiv.org/abs/2603.03281)
**组织**: Tsinghua-IVG
**得分**: 49.9
**标签**: Frontier Lab
**Upvotes**: 6 | **Stars**: 23

**摘要**: 针对传统 CFG 在高引导尺度下导致的不稳定性问题，本文提出了基于控制理论的 CFG-Ctrl 框架。核心是引入滑模控制 (SMC-CFG)，通过非线性反馈引导修正速度场。实验证明该方法在 SD3.5 等模型上显著提升了语义对齐性和鲁棒性。

**亮点**:
  - 提出将 CFG 重新诠释为控制问题的统一框架
  - 引入滑模控制 (SMC) 解决线性控制的不稳定性
  - 在 Stable Diffusion 3.5 和 Flux 等模型上验证性能

---

###  5. UniG2U-Bench：统一模型是否推动了多模态理解能力的进步？ (UniG2U-Bench: Do Unified Models Advance Multimodal Understanding?)

**论文链接**: [https://arxiv.org/abs/2603.03241](https://arxiv.org/abs/2603.03241)
**组织**: Unknown
**得分**: 41.08
**标签**: 
**Upvotes**: 76 | **Stars**: 19

**摘要**: 针对生成是否促进理解不明确的问题，提出涵盖7大类30子任务的UniG2U-Bench基准。实验表明统一模型普遍不及基础VLM，但在空间智能和幻觉任务上表现更佳，指出了数据多样性的必要性。

**亮点**:
  - 提出包含7大类30子任务的 G2U 评估基准 UniG2U-Bench
  - 揭示统一模型通常不及基础 VLM，GtA 推理可能降低性能
  - 发现空间智能和多轮推理任务是生成辅助理解的显著提升点

---

###  6. BeyondSWE：当前代码智能体能否胜任超越单仓库Bug修复的任务？ (BeyondSWE: Can Current Code Agent Survive Beyond Single-Repo Bug Fixing?)

**论文链接**: [https://arxiv.org/abs/2603.03194](https://arxiv.org/abs/2603.03194)
**组织**: AweAI Team
**得分**: 39.98
**标签**: 
**Upvotes**: 49 | **Stars**: 22

**摘要**: 针对现有基准忽略跨仓库推理等现实挑战，本文提出包含500个案例的BeyondSWE基准及SearchSWE框架。实验表明，即使前沿模型在复杂任务中成功率也低于45%，且搜索增强效果不稳定，揭示了当前智能体模拟开发者工作流的巨大困难。

**亮点**:
  - 提出BeyondSWE新基准，覆盖跨仓库等真实场景
  - 开发SearchSWE框架，评估外部知识辅助效果
  - 揭示前沿模型成功率不足45%，存在显著能力鸿沟

---

###  7. Kiwi-Edit：基于指令与参考引导的多功能视频编辑 (Kiwi-Edit: Versatile Video Editing via Instruction and Reference Guidance)

**论文链接**: [https://arxiv.org/abs/2603.02175](https://arxiv.org/abs/2603.02175)
**组织**: Show Lab
**得分**: 38.12
**标签**: 
**Upvotes**: 14 | **Stars**: 45

**摘要**: 针对视频编辑中语言描述不精准且高质量参考数据稀缺的问题，提出数据生成管道构建RefVIE数据集，并设计Kiwi-Edit架构融合可学习查询与视觉特征。该方法显著提升了指令遵循与参考保真度，确立了可控视频编辑的SOTA性能。

**亮点**:
  - 提出数据生成管道构建大规模RefVIE数据集
  - 设计Kiwi-Edit统一编辑架构
  - 达到可控视频编辑SOTA性能

---

###  8. 超越长度扩展：协同广度与深度以构建生成式奖励模型 (Beyond Length Scaling: Synergizing Breadth and Depth for Generative Reward Models)

**论文链接**: [https://arxiv.org/abs/2603.01571](https://arxiv.org/abs/2603.01571)
**组织**: Tencent Hunyuan
**得分**: 38.1
**标签**: Frontier Lab
**Upvotes**: 29 | **Stars**: 0

**摘要**: 针对现有生成式奖励模型（GRM）单纯依赖思维链长度扩展而忽略推理机制差异的问题，本文提出了 Mix-GRM 框架。该框架通过模块化合成管线构建结构化的广度与深度 CoT，并利用监督微调（SFT）和可验证奖励强化学习（RLVR）进行优化。实验显示，Mix-GRM 在五个基准上达到 SOTA，平均超越领先开源模型 8.2%，证实了根据任务类型自适应分配推理风格的有效性。

**亮点**:
  - 提出 Mix-GRM 框架，协同广度与深度推理机制
  - 五项基准测试达到 SOTA，平均性能提升 8.2%
  - 验证了 B-CoT 适合主观任务、D-CoT 适合客观任务

---

###  9. 大型语言模型的可控性如何？一种跨行为粒度的统一评估框架 (How Controllable Are Large Language Models? A Unified Evaluation across Behavioral Granularities)

**论文链接**: [https://arxiv.org/abs/2603.02578](https://arxiv.org/abs/2603.02578)
**组织**: alibaba-inc
**得分**: 36.55
**标签**: Frontier Lab
**Upvotes**: 21 | **Stars**: 0

**摘要**: 针对LLM在社会敏感领域的不可预测风险，提出分层基准SteerEval，涵盖语言、情感和性格三个领域及L1-L3三层规范粒度。实验发现现有引导方法在细粒度级别控制力退化，为安全可控的LLM提供了可解释的评估框架。

**亮点**:
  - 提出 SteerEval 统一评估基准
  - 定义 L1-L3 三层行为规范粒度
  - 揭示细粒度控制能力的退化问题

---

###  10. SciDER：以科学数据为核心的端到端研究员 (SciDER: Scientific Data-centric End-to-end Researcher)

**论文链接**: [https://arxiv.org/abs/2603.01421](https://arxiv.org/abs/2603.01421)
**组织**: AI4Research
**得分**: 34.72
**标签**: 
**Upvotes**: 4 | **Stars**: 70

**摘要**: 针对现有智能体难以处理科学实验原始数据的问题，提出了 SciDER 系统。该系统通过专门智能体协作解析数据、生成假设并执行代码，结合自进化记忆与反馈机制。实验表明，其在数据驱动的科学发现中超越通用智能体及 SOTA 模型。

**亮点**:
  - 提出以数据为核心的端到端科研框架 SciDER
  - 集成自进化记忆与批评者反馈循环机制
  - 性能超越通用智能体及现有 SOTA 模型

---

###  11. 学习何时行动或拒绝：面向安全多步工具使用的智能体推理模型防护 (Learning When to Act or Refuse: Guarding Agentic Reasoning Models for Safe Multi-Step Tool Use)

**论文链接**: [https://arxiv.org/abs/2603.03205](https://arxiv.org/abs/2603.03205)
**组织**: Microsoft Research
**得分**: 30.06
**标签**: Frontier Lab
**Upvotes**: 5 | **Stars**: 0

**摘要**: 针对智能体模型在多步工具使用中的安全风险，提出MOSAIC对齐框架，通过显式“计划-检查-行动/拒绝”循环来保障安全。实验显示，该方法零样本下有效减少50%有害行为，并保持良性任务性能。

**亮点**:
  - 提出MOSAIC后训练框架
  - 显式化安全推理与拒绝机制
  - 零样本显著降低有害行为

---

###  12. NOVA：面向无配对视频编辑的稀疏控制与密集合成框架 (NOVA: Sparse Control, Dense Synthesis for Pair-Free Video Editing)

**论文链接**: [https://arxiv.org/abs/2603.02802](https://arxiv.org/abs/2603.02802)
**组织**: Unknown
**得分**: 27.33
**标签**: 
**Upvotes**: 7 | **Stars**: 13

**摘要**: 针对视频编辑依赖配对数据及现有方法一致性差的问题，提出 NOVA 框架。它利用稀疏分支进行关键帧引导，密集分支融合原始视频的运动与纹理，并采用退化模拟训练策略。实验表明，该模型在无需配对数据的情况下，显著提升了编辑保真度和时间连贯性。

**亮点**:
  - 提出稀疏控制与密集合成双分支架构
  - 引入退化模拟训练消除对配对数据的依赖
  - 在编辑保真度和时间连贯性上优于现有方法

---

###  13. AgentConductor：面向多智能体竞赛级代码生成的拓扑演化 (AgentConductor: Topology Evolution for Multi-Agent Competition-Level Code Generation)

**论文链接**: [https://arxiv.org/abs/2602.17100](https://arxiv.org/abs/2602.17100)
**组织**: Shanghai Jiao Tong University
**得分**: 26.59
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 0

**摘要**: 现有代码生成多智能体系统存在通信冗余且难以适应任务难度。AgentConductor 提出基于强化学习和 LLM 编排器的动态拓扑生成架构，能感知任务难度构建有向无环图。实验表明其在多个数据集上达 SOTA，Pass@1 最高提升 14.6%，并显著降低 token 成本和通信密度。

**亮点**:
  - 达到 SOTA 性能表现
  - 提出基于 RL 和 LLM 的动态拓扑演化架构
  - 显著降低 Token 成本与通信冗余

---
