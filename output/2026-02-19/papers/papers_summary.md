# 每日论文汇总 - 2026-02-19

**论文数量**: 11

---

### 🏆 1. SAM 3D Body: 鲁棒的全身人体网格恢复 (SAM 3D Body: Robust Full-Body Human Mesh Recovery)

**论文链接**: [https://arxiv.org/abs/2602.15989](https://arxiv.org/abs/2602.15989)
**组织**: Unknown
**得分**: 58.92
**标签**: Viral
**Upvotes**: 8 | **Stars**: 2627

**摘要**: 针对单图像3D人体网格恢复在野外条件下的挑战，提出了可提示模型SAM 3D Body。该模型采用编码器-解码器架构，引入解耦骨骼与表面形状的新参数化表示MHR，并支持关键点与掩码等辅助提示。实验表明，该模型实现了SOTA性能，在泛化能力和准确性上显著优于现有方法。

**亮点**:
  - 达到SOTA性能，具有强泛化能力
  - 提出Momentum Human Rig (MHR) 新参数化表示
  - 支持用户引导推理的可提示模型

---

###  2. 世界动作模型即零样本策略 (World Action Models are Zero-shot Policies)

**论文链接**: [https://arxiv.org/abs/2602.15922](https://arxiv.org/abs/2602.15922)
**组织**: NVIDIA Deep Imagination Research
**得分**: 71.87
**标签**: Frontier Lab
**Upvotes**: 9 | **Stars**: 742

**摘要**: 针对现有VLA模型难以泛化未见物理动作的问题，提出基于视频扩散的世界动作模型DreamZero。该模型通过联合预测视频和动作学习物理动力学，实现了异构数据的有效利用。实验表明，其泛化性能较SOTA VLA提升两倍，支持14B模型7Hz实时控制，并具备高效的跨具身迁移能力。

**亮点**:
  - 泛化性能超越SOTA VLA两倍
  - 提出基于视频扩散的世界动作模型
  - 实现14B模型7Hz实时闭环控制

---

###  3. RynnBrain：开放具身基础模型 (RynnBrain: Open Embodied Foundation Models)

**论文链接**: [https://arxiv.org/abs/2602.14979](https://arxiv.org/abs/2602.14979)
**组织**: DAMO Academy
**得分**: 54.26
**标签**: 
**Upvotes**: 27 | **Stars**: 402

**摘要**: 针对具身智能缺乏统一物理基础模型的痛点，提出RynnBrain时空基础模型。该架构集成了感知、推理与规划，提供多尺寸及下游任务变体，在20余项具身基准测试中大幅超越现有模型。

**亮点**:
  - 提出统一时空基础模型架构
  - 20余项基准测试大幅超越现有模型
  - 开源包含MoE架构的多尺寸模型家族

---

###  4. MMA：多模态记忆智能体 (MMA: Multimodal Memory Agent)

**论文链接**: [https://arxiv.org/abs/2602.16493](https://arxiv.org/abs/2602.16493)
**组织**: Peking University
**得分**: 40.81
**标签**: Frontier Lab
**Upvotes**: 5 | **Stars**: 5

**摘要**: 针对长视距多模态智能体记忆检索易出现陈旧或冲突信息的问题，提出MMA架构，通过结合来源可信度与冲突感知共识的动态可靠性评分机制重加权证据。该架构在FEVER上降低方差35.2%，揭示了“视觉安慰剂效应”，并在MMA-Bench上显著优于基线。

**亮点**:
  - 提出具有动态可靠性评分机制的MMA架构
  - 推出MMA-Bench基准测试集
  - 揭示了RAG中的视觉安慰剂效应

---

###  5. SLA2：具有可学习路由与量化感知训练的稀疏-线性注意力 (SLA2: Sparse-Linear Attention with Learnable Routing and QAT)

**论文链接**: [https://arxiv.org/abs/2602.12675](https://arxiv.org/abs/2602.12675)
**组织**: UC Berkeley
**得分**: 40.64
**标签**: Frontier Lab
**Upvotes**: 44 | **Stars**: 0

**摘要**: 针对SLA依赖启发式分割及存在数学误差的痛点，提出SLA2。该方法引入可学习路由器动态分配计算分支，优化了稀疏-线性注意力的结合公式，并引入低比特量化设计。实验显示，在视频扩散模型上实现了97%的稀疏度和18.6倍加速，且保持生成质量。

**亮点**:
  - 引入可学习路由器动态选择注意力分支
  - 提出更准确的稀疏-线性注意力结合公式
  - 视频扩散模型上实现18.6倍加速与97%稀疏度

---

###  6. 面向开集词汇视觉移动操作的类人机器人末端执行器控制学习 (Learning Humanoid End-Effector Control for Open-Vocabulary Visual Loco-Manipulation)

**论文链接**: [https://arxiv.org/abs/2602.16705](https://arxiv.org/abs/2602.16705)
**组织**: University of Illinois at Urbana-Champaign
**得分**: 37.68
**标签**: Frontier Lab
**Upvotes**: 25 | **Stars**: 0

**摘要**: 针对现有基于现实模仿学习泛化能力差的问题，提出HERO系统。该系统结合大视觉模型与仿真训练，设计了残差感知末端执行器追踪策略，融合逆运动学与神经前向模型。实验表明，该方法将追踪误差降低3.2倍，实现了从办公室到咖啡店等多样化环境下的开集物体操作。

**亮点**:
  - 提出HERO开集词汇操作新范式
  - 设计残差感知末端执行器追踪策略
  - 追踪误差降低3.2倍，实现多场景落地

---

###  7. 基于下一序列预测的强化快速权重模型 (Reinforced Fast Weights with Next-Sequence Prediction)

**论文链接**: [https://arxiv.org/abs/2602.16704](https://arxiv.org/abs/2602.16704)
**组织**: Princeton University
**得分**: 36.77
**标签**: Frontier Lab
**Upvotes**: 9 | **Stars**: 1

**摘要**: 针对快速权重架构因 Next-Token Prediction 训练范式限制导致长程依赖捕捉不足的问题，提出 REFINE 框架。该框架利用强化学习进行 Next-Sequence Prediction，通过 GRPO 优化模型。实验表明 REFINE 在长上下文检索与问答任务上优于监督微调。

**亮点**:
  - 提出 REFINE 强化学习框架
  - 采用 Next-Sequence Prediction 优化目标
  - 在长上下文基准测试中超越 SFT

---

###  8. 空书架还是弄丢钥匙？回忆是参数化事实性的瓶颈 (Empty Shelves or Lost Keys? Recall Is the Bottleneck for Parametric Factuality)

**论文链接**: [https://arxiv.org/abs/2602.14080](https://arxiv.org/abs/2602.14080)
**组织**: Google
**得分**: 35.55
**标签**: Frontier Lab
**Upvotes**: 16 | **Stars**: 0

**摘要**: LLM事实性评估常混淆知识缺失与提取失败。本文提出行为框架和WikiProfile基准，将事实细分为已编码但不可回忆、直接回忆和推理回忆三类。实验显示，前沿模型知识编码已饱和，但提取失败（回忆瓶颈）是主要错误来源。通过推理时间计算可恢复大量失效事实，表明提升知识利用率比模型扩参更重要。

**亮点**:
  - 提出WikiProfile评测基准
  - 发现回忆而非编码是事实性瓶颈
  - 推理计算显著提升事实回忆

---

###  9. BiManiBench：多模态大语言模型双臂协调能力的分层基准 (BiManiBench: A Hierarchical Benchmark for Evaluating Bimanual Coordination of Multimodal Large Language Models)

**论文链接**: [https://arxiv.org/abs/2602.08392](https://arxiv.org/abs/2602.08392)
**组织**: Tsinghua University
**得分**: 33.18
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 2

**摘要**: 针对现有 MLLM 机器人基准局限于单臂操作的问题，本文提出了分层基准 BiManiBench，涵盖空间推理、高层规划和低层控制。评估 30 余种 SOTA 模型发现，尽管具备高层推理能力，MLLMs 在双臂空间定位与控制上仍存在显著短板，常导致相互干扰。

**亮点**:
  - 提出 BiManiBench 分层基准
  - 涵盖推理到控制全流程评估
  - 揭示 SOTA 模型双臂协调缺陷

---

###  10. 迈向 AI Agent 可靠性科学 (Towards a Science of AI Agent Reliability)

**论文链接**: [https://arxiv.org/abs/2602.16666](https://arxiv.org/abs/2602.16666)
**组织**: Princeton University
**得分**: 33.12
**标签**: Frontier Lab
**Upvotes**: 11 | **Stars**: 0

**摘要**: 针对现有评测指标掩盖 Agent 实际失效的问题，本文提出包含一致性、鲁棒性、可预测性和安全性四个维度的12项可靠性指标。评估14个模型发现，近期模型的能力提升仅带来微小可靠性改善，该框架为理解 Agent 失效模式提供了新工具。

**亮点**:
  - 提出12项可靠性评估指标
  - 覆盖一致性与鲁棒性等四个维度
  - 揭示能力提升未显著改善可靠性

---

###  11. 基于上下文内队友推断的多智能体合作 (Multi-agent cooperation through in-context co-player inference)

**论文链接**: [https://arxiv.org/abs/2602.16301](https://arxiv.org/abs/2602.16301)
**组织**: Google
**得分**: 33.09
**标签**: Frontier Lab
**Upvotes**: 10 | **Stars**: 0

**摘要**: 针对现有方法依赖硬编码假设的痛点，本文利用序列模型的上下文学习能力，使智能体从多样化队友中推断策略。实验表明，该方法无需显式假设即可涌现出合作行为，实现了可扩展的自利智能体协作。

**亮点**:
  - 利用序列模型实现多智能体上下文学习
  - 无需硬编码假设或时间尺度分离
  - 通过敲诈脆弱性机制涌现合作行为

---
