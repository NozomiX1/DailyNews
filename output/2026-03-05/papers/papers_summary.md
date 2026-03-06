# 每日论文汇总 - 2026-03-05

**论文数量**: 9

---

### 🏆 1. 异构智能体协同强化学习 (Heterogeneous Agent Collaborative Reinforcement Learning)

**论文链接**: [https://arxiv.org/abs/2603.02604](https://arxiv.org/abs/2603.02604)
**组织**: ByteDance
**得分**: 76.17
**标签**: Super Lab, Must Read
**Upvotes**: 130 | **Stars**: 0

**摘要**: 针对孤立策略优化效率低的问题，提出异构智能体协同强化学习（HACRL）框架。其核心算法HACPO通过训练时共享已验证轨迹实现双向知识互促，推理时保持独立。实验表明，HACPO显著提升异构模型性能，优于GSPO平均3.3%，且轨迹成本减半。

**亮点**:
  - 提出 HACRL 协同优化与独立执行新范式
  - 设计 HACPO 算法实现异构智能体双向互促
  - 优于 GSPO 3.3% 且轨迹成本减半

---

###  2. Helios：真·实时长视频生成模型 (Helios: Real Real-Time Long Video Generation Model)

**论文链接**: [https://arxiv.org/abs/2603.04379](https://arxiv.org/abs/2603.04379)
**组织**: ByteDance
**得分**: 112.39
**标签**: Super Lab
**Upvotes**: 115 | **Stars**: 462

**摘要**: 针对长视频生成中的漂移与效率问题，字节跳动提出Helios 14B自回归扩散模型。通过模拟漂移的训练策略与上下文压缩优化，实现单卡H100 19.5 FPS实时推理与分钟级生成，质量超越现有基线。

**亮点**:
  - 单卡H100实现19.5 FPS实时推理
  - 无需传统反漂移技术即可生成分钟级视频
  - 14B参数模型的高效训练与内存优化架构

---

###  3. CubeComposer：从透视视频生成时空自回归4K 360°视频 (CubeComposer: Spatio-Temporal Autoregressive 4K 360° Video Generation from Perspective Video)

**论文链接**: [https://arxiv.org/abs/2603.04291](https://arxiv.org/abs/2603.04291)
**组织**: ARC Lab, Tencent PCG
**得分**: 55.22
**标签**: Frontier Lab
**Upvotes**: 10 | **Stars**: 39

**摘要**: 针对现有VR视频生成分辨率受限的痛点，本文提出CubeComposer模型。通过立方体图分解和时空自回归策略，有效降低内存消耗，实现原生4K 360°视频生成，并在视觉质量上超越SOTA。

**亮点**:
  - 原生 4K 360° 视频生成
  - 提出时空自回归扩散模型
  - 消除边界缝隙的连续感知技术

---

###  4. Phi-4-reasoning-vision-15B 技术报告 (Phi-4-reasoning-vision-15B Technical Report)

**论文链接**: [https://arxiv.org/abs/2603.03975](https://arxiv.org/abs/2603.03975)
**组织**: Microsoft
**得分**: 52.43
**标签**: Frontier Lab
**Upvotes**: 13 | **Stars**: 21

**摘要**: 针对多模态大模型计算开销大问题，微软发布 Phi-4-reasoning-vision-15B。该模型通过严格的数据筛选、合成增强及高分辨率动态编码器，显著降低了训练与推理成本，并在科学数学推理及UI理解上表现出色，实现了小参数下的高性能。

**亮点**:
  - 采用高分辨率动态编码器提升感知精度
  - 系统性数据清洗与合成增强提升性能
  - 混合推理策略兼顾快速响应与复杂逻辑

---

###  5. V_1：统一生成与自验证的并行推理器 (V_1: Unifying Generation and Self-Verification for Parallel Reasoners)

**论文链接**: [https://arxiv.org/abs/2603.04304](https://arxiv.org/abs/2603.04304)
**组织**: UC Berkeley
**得分**: 45.38
**标签**: Frontier Lab
**Upvotes**: 9 | **Stars**: 7

**摘要**: 针对测试时计算中的验证瓶颈，本文提出了 V_1 框架。该框架利用成对自验证优于标量评分的特性，通过锦标赛式排名（V_1-Infer）和联合强化学习（V_1-PairRL）统一生成与验证。实验显示，V_1 在代码生成和数学推理任务上显著提升了 Pass@1 指标，并优于现有的扩展方法。

**亮点**:
  - 提出基于成对自验证的 V_1 框架
  - 设计 V_1-Infer 算法与 V_1-PairRL 训练策略
  - 在代码与数学基准上显著优于现有方法

---

###  6. Proact-VL：面向实时 AI 伴侣的主动式视频大语言模型 (Proact-VL: A Proactive VideoLLM for Real-Time AI Companions)

**论文链接**: [https://arxiv.org/abs/2603.03447](https://arxiv.org/abs/2603.03447)
**组织**: Microsoft Research
**得分**: 37.48
**标签**: Frontier Lab
**Upvotes**: 24 | **Stars**: 0

**摘要**: 针对实时AI伴侣面临的低延迟推理、自主响应时机及内容控制三大痛点，提出Proact-VL框架，并结合Live Gaming Benchmark数据集进行验证。实验表明，该模型在保持强大视频理解能力的同时，实现了优越的响应速度与生成质量。

**亮点**:
  - 提出 Proact-VL 通用框架
  - 构建 Live Gaming Benchmark 数据集
  - 实现低延迟高质量的实时交互

---

###  7. MemSifter：基于结果驱动代理推理的 LLM 记忆检索卸载框架 (MemSifter: Offloading LLM Memory Retrieval via Outcome-Driven Proxy Reasoning)

**论文链接**: [https://arxiv.org/abs/2603.03379](https://arxiv.org/abs/2603.03379)
**组织**: Unknown
**得分**: 35.54
**标签**: 
**Upvotes**: 23 | **Stars**: 21

**摘要**: 针对LLM长期记忆检索中成本与精度的权衡问题，论文提出MemSifter框架，将检索过程卸载至小型代理模型。该方法引入基于任务结果的强化学习训练范式，通过主模型表现优化检索策略。实验表明，其在八个基准测试中达到SOTA性能，兼具高效性与可扩展性。

**亮点**:
  - 卸载检索至轻量代理模型
  - 提出结果驱动的强化学习训练
  - 多项基准测试达到 SOTA 性能

---

###  8. ArtHOI：基于视频先验进行 4D 重建的关节式人机交互合成 (ArtHOI: Articulated Human-Object Interaction Synthesis by 4D Reconstruction from Video Priors)

**论文链接**: [https://arxiv.org/abs/2603.04338](https://arxiv.org/abs/2603.04338)
**组织**: Unknown
**得分**: 32.61
**标签**: 
**Upvotes**: 19 | **Stars**: 14

**摘要**: 针对无 3D/4D 监督下合成物理合理的关节式人机交互（HOI）的难题，本文提出 ArtHOI 框架。该方法利用视频先验生成的视频作为监督，通过基于光流的部件分割和解耦重建管线，实现零样本 4D 场景重建。实验表明，ArtHOI 在接触精度、抗穿透性及关节保真度上显著优于现有方法，实现了语义对齐且物理落地的交互合成。

**亮点**:
  - 首个基于 4D 重建的关节式人机交互零样本框架
  - 提出基于光流的部件分割与解耦重建管线
  - 显著提升接触精度并减少物体穿透现象

---

###  9. BeamPERL：基于可验证奖励的参数高效强化学习，使紧凑型大语言模型具备结构化梁力学推理能力 (BeamPERL: Parameter-Efficient RL with Verifiable Rewards Specializes Compact LLMs for Structured Beam Mechanics Reasoning)

**论文链接**: [https://arxiv.org/abs/2603.04124](https://arxiv.org/abs/2603.04124)
**组织**: LAMM: MIT Laboratory for Atomistic and Molecular Mechanics
**得分**: 31.16
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 2

**摘要**: 针对强化学习能否教会紧凑大模型物理推理的问题，本文提出 BeamPERL 方法。该方法利用符号求解器的二元奖励，在梁静力学任务上对 1.5B 模型进行参数高效强化学习训练。实验表明模型准确率提升显著，但主要学习了程序化模板而非内化方程，且在拓扑变换下鲁棒性不足，揭示了仅靠精确奖励无法保证可迁移的物理推理能力。

**亮点**:
  - Pass@1 准确率较基线提升 66.7%
  - 揭示模型能力呈各向异性，存在拓扑泛化局限
  - 发现精确奖励诱导模板学习而非物理方程内化

---
