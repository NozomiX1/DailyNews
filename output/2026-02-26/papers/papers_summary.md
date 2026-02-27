# 每日论文汇总 - 2026-02-26

**论文数量**: 11

---

### 🏆 1. DualPath：打破 Agent LLM 推理中的存储带宽瓶颈 (DualPath: Breaking the Storage Bandwidth Bottleneck in Agentic LLM Inference)

**论文链接**: [https://arxiv.org/abs/2602.21548](https://arxiv.org/abs/2602.21548)
**组织**: DeepSeek
**得分**: 64.29
**标签**: Super Lab, Must Read
**Upvotes**: 13 | **Stars**: 0

**摘要**: 针对Agent LLM推理中KV-Cache存储IO瓶颈，本文提出DualPath系统。它引入双路径加载机制，新增存储到解码引擎路径，利用RDMA传输至预填充引擎，并配合全局调度器。实验显示，该系统使离线推理吞吐量最高提升1.87倍，在线服务吞吐量平均提升1.96倍。

**亮点**:
  - 提出双路径KV-Cache加载架构
  - 利用RDMA优化存储到Prefill的数据传输
  - 在线推理吞吐量平均提升1.96倍

---

### 🏆 2. 世界引导：基于条件空间世界建模的动作生成方法 (World Guidance: World Modeling in Condition Space for Action Generation)

**论文链接**: [https://arxiv.org/abs/2602.22010](https://arxiv.org/abs/2602.22010)
**组织**: ByteDance Seed
**得分**: 61.09
**标签**: Super Lab, Must Read
**Upvotes**: 7 | **Stars**: 0

**摘要**: 针对 VLA 模型难以平衡未来表示效率与细粒度指导的问题，提出 WoG 框架。该方法将未来观测映射为紧凑条件空间，引导 VLA 联合预测条件与动作。实验表明，该方法在模拟和真实环境中显著优于现有方法，具备优越的泛化能力与细粒度动作生成能力。

**亮点**:
  - 提出 WoG (World Guidance) 新框架
  - 在条件空间实现高效世界建模
  - 显著优于现有基于未来预测的方法

---

###  3. DreamID-Omni：可控以人为中心的音视频生成统一框架 (DreamID-Omni: Unified Framework for Controllable Human-Centric Audio-Video Generation)

**论文链接**: [https://arxiv.org/abs/2602.12160](https://arxiv.org/abs/2602.12160)
**组织**: ByteDance
**得分**: 92.77
**标签**: Super Lab
**Upvotes**: 33 | **Stars**: 54

**摘要**: 针对现有方法将音视频生成任务视为孤立目标且难以精确控制多身份与音色的问题，本文提出了DreamID-Omni统一框架。该框架设计了对称条件扩散Transformer，并引入双层解耦策略解决身份-音色绑定失败，利用多任务渐进训练协调目标。实验表明，该方法在视频、音频及音画一致性上取得全面SOTA性能，超越顶级商业模型。

**亮点**:
  - 提出统一的可控以人为中心音视频生成框架
  - 设计双层解耦策略解决身份音色绑定失败
  - 取得全面SOTA性能并超越领先商业模型

---

###  4. 面向稀疏视图高斯泼溅的锚点与球谐系数丢弃方法 (Dropping Anchor and Spherical Harmonics for Sparse-view Gaussian Splatting)

**论文链接**: [https://arxiv.org/abs/2602.20933](https://arxiv.org/abs/2602.20933)
**组织**: StepFun
**得分**: 57.62
**标签**: Super Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 针对稀疏视图3DGS的过拟合及邻域补偿效应问题，提出DropAnSH-GS。该方法采用基于锚点的邻居移除策略打破冗余，并丢弃高阶球谐系数以集中外观信息，有效抑制过拟合并支持模型压缩，性能优于现有Dropout方法。

**亮点**:
  - 识别并解决邻域补偿效应
  - 提出基于锚点的Dropout策略
  - 引入球谐系数丢弃机制

---

###  5. GUI-Libra：利用动作感知监督和部分可验证强化学习训练原生 GUI 智能体 (GUI-Libra: Training Native GUI Agents to Reason and Act with Action-aware Supervision and Partially Verifiable RL)

**论文链接**: [https://arxiv.org/abs/2602.22190](https://arxiv.org/abs/2602.22190)
**组织**: UIUC ScaleML Lab
**得分**: 48.83
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 11

**摘要**: 针对开源 GUI 智能体在长程任务中表现欠佳及推理与定位脱节的问题，本文提出 GUI-Libra 训练框架。该方法发布了 81K 高质量数据集，设计了动作感知监督技术，并利用 KL 正则化和成功自适应缩放解决了部分可验证性下的 RL 训练难题。实验显示，该框架显著提升了 Web 和移动端的任务完成率。

**亮点**:
  - 发布 81K 高质量 GUI 推理数据集
  - 提出动作感知 SFT 协调推理与执行
  - 引入 KL 信任区域稳定部分可验证 RL

---

###  6. JavisDiT++：联合音视频生成的统一建模与优化 (JavisDiT++: Unified Modeling and Optimization for Joint Audio-Video Generation)

**论文链接**: [https://arxiv.org/abs/2602.19163](https://arxiv.org/abs/2602.19163)
**组织**: JavisVerse
**得分**: 47.75
**标签**: 
**Upvotes**: 10 | **Stars**: 322

**摘要**: 针对现有开源音视频联合生成（JAVG）模型在质量、同步性和对齐方面的不足，本文提出了 JavisDiT++ 框架。该框架通过模态特定的混合专家（MS-MoE）设计增强跨模态交互，利用时间对齐 RoPE（TA-RoPE）实现显式帧级同步，并引入音视频直接偏好优化（AV-DPO）对齐人类偏好。实验表明，该模型在仅使用约 100 万条公共数据的情况下达到了 SOTA 性能。

**亮点**:
  - 提出 MS-MoE 设计以增强单模态及跨模态生成质量
  - 引入 TA-RoPE 策略实现显式帧级音视频同步
  - 开发 AV-DPO 方法并基于少量数据达成 SOTA 性能

---

###  7. Solaris：在 Minecraft 中构建多人视频世界模型 (Solaris: Building a Multiplayer Video World Model in Minecraft)

**论文链接**: [https://arxiv.org/abs/2602.22208](https://arxiv.org/abs/2602.22208)
**组织**: Unknown
**得分**: 39.81
**标签**: 
**Upvotes**: 17 | **Stars**: 56

**摘要**: 针对现有视频世界模型局限于单智能体视角的痛点，提出 Solaris 多人视频世界模型。通过构建自动化多人数据系统收集海量数据，并采用分阶段训练及 Checkpointed Self Forcing 技术，实现了对多智能体交互和一致多视角观察的模拟。实验表明，该架构在多项评估中优于现有基线。

**亮点**:
  - 提出多人视频世界模型 Solaris
  - 构建专用多人数据收集与评估系统
  - 提出 Checkpointed Self Forcing 训练技术

---

###  8. ARLArena：稳定智能体强化学习的统一框架 (ARLArena: A Unified Framework for Stable Agentic Reinforcement Learning)

**论文链接**: [https://arxiv.org/abs/2602.21534](https://arxiv.org/abs/2602.21534)
**组织**: University of California, Los Angeles
**得分**: 33.16
**标签**: 
**Upvotes**: 18 | **Stars**: 17

**摘要**: 针对智能体强化学习（ARL）训练易崩溃的痛点，本文提出统一框架ARLArena。该框架通过构建标准化测试环境并解构策略梯度，提出了SAMPO优化算法。实验表明，SAMPO在多种任务中实现了稳定训练与优异性能，为构建可复现的LLM智能体训练管道提供了实用指导。

**亮点**:
  - 提出ARLArena统一框架与标准化测试床
  - 解构策略梯度为四个核心设计维度
  - 提出稳定智能体策略优化方法SAMPO

---

###  9. 真实性谱系假说 (The Truthfulness Spectrum Hypothesis)

**论文链接**: [https://arxiv.org/abs/2602.20273](https://arxiv.org/abs/2602.20273)
**组织**: Columbia University
**得分**: 28.72
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 1

**摘要**: 针对LLM是否线性编码真实性的争议，本文提出“真实性谱系假说”。通过跨领域探测和几何分析，证实表征空间中存在泛化程度不一的真实性方向，且特定领域方向干预更有效，后训练重塑了该结构。

**亮点**:
  - 提出“真实性谱系假说”统一通用与特定领域的真实性编码观点
  - 发现探针方向几何特征可极高精度预测跨领域泛化（R²=0.98）
  - 揭示特定领域方向干预效果优于通用方向，解释模型阿谀倾向的表征基础

---

###  10. 三模态掩码扩散模型的设计空间 (The Design Space of Tri-Modal Masked Diffusion Models)

**论文链接**: [https://arxiv.org/abs/2602.21472](https://arxiv.org/abs/2602.21472)
**组织**: Apple
**得分**: 27.62
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 针对多模态生成，本文提出首个从头预训练的三模态掩码扩散模型。通过分析缩放定律并引入基于随机微分方程的参数化技术，解耦了批次大小限制。30亿参数模型在文本、文生图及文生音任务中表现优异。

**亮点**:
  - 首个从零预训练的三模态掩码扩散模型
  - 提出SDE重参数化解耦批次大小
  - 30亿参数模型展现多模态强性能

---

###  11. JAEGER：模拟物理环境中的联合 3D 音视频定位与推理 (JAEGER: Joint 3D Audio-Visual Grounding and Reasoning in Simulated Physical Environments)

**论文链接**: [https://arxiv.org/abs/2602.18527](https://arxiv.org/abs/2602.18527)
**组织**: Tsinghua University
**得分**: 24.56
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 0

**摘要**: 针对现有 AV-LLMs 缺乏 3D 空间感知的问题，本文提出 JAEGER 框架。该框架通过融合 RGB-D 图像和多通道音频，结合神经强度向量表示，实现了 3D 空间的联合定位与推理。基于 SpatialSceneQA 基准的实验表明，该方法在空间感知任务上显著优于 2D 基准，验证了显式 3D 建模的重要性。

**亮点**:
  - 提出 JAEGER 3D 音视频大模型框架
  - 提出神经强度向量增强音频方向感知
  - 构建 SpatialSceneQA 3D 空间推理基准

---
