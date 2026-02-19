# 每日论文汇总 - 2026-02-19

**论文数量**: 8

---

### 🏆 1. SAM 3D Body：鲁棒的全人体网格恢复 (SAM 3D Body: Robust Full-Body Human Mesh Recovery)

**论文链接**: [https://arxiv.org/abs/2602.15989](https://arxiv.org/abs/2602.15989)
**组织**: Unknown
**得分**: 57.63
**标签**: Viral
**Upvotes**: 7 | **Stars**: 2622

**摘要**: 针对单张图像全人体 3D 网格恢复问题，提出 SAM 3D Body (3DB) 模型。该模型采用编码器-解码器架构，引入 Momentum Human Rig (MHR) 新参数化表示以解耦骨骼与形状，并支持 2D 关键点和掩码等提示输入。实验表明，3DB 在泛化能力和精度上达到 SOTA，显著优于现有方法，并已开源。

**亮点**:
  - 提出 Momentum Human Rig (MHR) 新参数化表示
  - 实现全人体网格恢复 SOTA 性能
  - 支持类似 SAM 的可提示交互式推断

---

###  2. 世界动作模型即零样本策略 (World Action Models are Zero-shot Policies)

**论文链接**: [https://arxiv.org/abs/2602.15922](https://arxiv.org/abs/2602.15922)
**组织**: NVIDIA Deep Imagination Research
**得分**: 68.55
**标签**: Frontier Lab
**Upvotes**: 5 | **Stars**: 733

**摘要**: 针对VLA模型难以泛化未见物理动作的问题，提出DreamZero世界动作模型。该方法基于视频扩散主干预测未来状态和动作以学习动力学。实验表明，其在新任务泛化性能较SOTA提升超2倍，并能实现7Hz实时闭环控制及跨具身迁移。

**亮点**:
  - 提出DreamZero世界动作模型架构
  - 实现14B模型7Hz实时闭环控制
  - 零样本与跨具身泛化性能优异

---

###  3. RynnBrain：开放具身基础模型 (RynnBrain: Open Embodied Foundation Models)

**论文链接**: [https://arxiv.org/abs/2602.14979](https://arxiv.org/abs/2602.14979)
**组织**: DAMO Academy
**得分**: 51.97
**标签**: 
**Upvotes**: 19 | **Stars**: 395

**摘要**: 针对缺乏统一物理感知模型的痛点，提出RynnBrain开源时空基础模型。该模型在统一框架内集成了感知、推理与规划能力，在20个具身基准测试中显著超越现有模型，有效支持物理接地推理及下游任务适应。

**亮点**:
  - 统一感知、推理与规划的开源时空基础模型
  - 在20个具身基准测试中显著超越现有模型
  - 提供多尺寸模型及多样化下游任务适配

---

###  4. SLA2：带有可学习路由和量化感知训练的稀疏线性注意力 (SLA2: Sparse-Linear Attention with Learnable Routing and QAT)

**论文链接**: [https://arxiv.org/abs/2602.12675](https://arxiv.org/abs/2602.12675)
**组织**: UC Berkeley
**得分**: 38.73
**标签**: Frontier Lab
**Upvotes**: 33 | **Stars**: 0

**摘要**: 针对SLA在视频生成中启发式计算分配次优及误差不匹配的问题，提出SLA2架构。该架构引入可学习路由动态选择分支，结合更忠实的公式化和低比特量化，在保持生成质量的同时实现了97%稀疏度和18.6倍加速。

**亮点**:
  - 引入可学习路由动态选择稀疏或线性注意力分支
  - 修正注意力误差不匹配，提出更直接的稀疏-线性注意力公式
  - 在视频扩散模型上实现97%稀疏度与18.6倍加速

---

###  5. MMA：多模态记忆智能体 (MMA: Multimodal Memory Agent)

**论文链接**: [https://arxiv.org/abs/2602.16493](https://arxiv.org/abs/2602.16493)
**组织**: Peking University
**得分**: 37.06
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 3

**摘要**: 针对长视距多模态智能体因外部记忆检索不可靠导致过度自信错误的问题，提出多模态记忆智能体(MMA)。该方法通过整合来源可信度、时间衰减及冲突感知共识计算动态可靠性评分，用于重加权证据或拒答。实验表明MMA在降低方差的同时保持准确率，并发现了RAG智能体的视觉安慰剂效应。

**亮点**:
  - 提出动态可靠性评分机制
  - 引入 MMA-Bench 评测基准
  - 揭示“视觉安慰剂效应”

---

###  6. 空书架还是丢失的钥匙？回忆是参数事实性的瓶颈 (Empty Shelves or Lost Keys? Recall Is the Bottleneck for Parametric Factuality)

**论文链接**: [https://arxiv.org/abs/2602.14080](https://arxiv.org/abs/2602.14080)
**组织**: Google
**得分**: 34.23
**标签**: Frontier Lab
**Upvotes**: 14 | **Stars**: 0

**摘要**: 针对LLM事实性评估未能区分“知识缺失”与“记忆失效”的问题，研究提出基于事实层面的行为框架并构建WikiProfile基准。实验发现前沿模型知识编码率极高（95-98%），但回忆能力是主要瓶颈。研究表明推理计算可显著改善回忆，未来提升应更关注如何利用已有知识。

**亮点**:
  - 提出区分知识编码与回忆的行为评估框架
  - 构建 WikiProfile 基准测试涵盖 13 个模型
  - 揭示回忆而非编码是当前参数事实性的主要瓶颈

---

###  7. 基于上下文协玩家推理的多智能体合作 (Multi-agent cooperation through in-context co-player inference)

**论文链接**: [https://arxiv.org/abs/2602.16301](https://arxiv.org/abs/2602.16301)
**组织**: Google
**得分**: 30.42
**标签**: Frontier Lab
**Upvotes**: 6 | **Stars**: 0

**摘要**: 针对自私智能体难以合作的问题，本文提出利用序列模型的上下文学习能力，无需硬编码假设即可推断协玩家策略。实验发现，对抗多样化的协玩家自然诱导了最佳响应策略，且受勒索的脆弱性机制促使了合作行为的涌现。

**亮点**:
  - 利用序列模型的上下文学习能力
  - 无需硬编码假设或时间尺度分离
  - 揭示了受勒索脆弱性驱动合作涌现的机制

---

###  8. BiManiBench：评估多模态大语言模型双臂协调能力的分层基准 (BiManiBench: A Hierarchical Benchmark for Evaluating Bimanual Coordination of Multimodal Large Language Models)

**论文链接**: [https://arxiv.org/abs/2602.08392](https://arxiv.org/abs/2602.08392)
**组织**: Tsinghua University
**得分**: 28.32
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 1

**摘要**: 针对现有评估仅限于单臂操作的痛点，本文提出 BiManiBench 分层基准，包含空间推理、动作规划及末端控制三个层级。实验评估了 30 多个 SOTA 模型，结果表明虽然其具备高层推理能力，但在双臂空间定位和互为运动学约束的理解上存在严重不足。

**亮点**:
  - 提出首个评估 MLLMs 双臂协调能力的分层基准
  - 涵盖从空间推理到末端控制的完整评估体系
  - 揭示现有 SOTA 模型在双臂运动约束理解上的短板

---
