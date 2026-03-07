# 每日论文汇总 - 2026-03-06

**论文数量**: 9

---

###  1. HiFi-Inpaint：面向细节保存人-产品图像的高保真参考式修复 (HiFi-Inpaint: Towards High-Fidelity Reference-Based Inpainting for Generating Detail-Preserving Human-Product Images)

**论文链接**: [https://arxiv.org/abs/2603.02210](https://arxiv.org/abs/2603.02210)
**组织**: ByteDance
**得分**: 86.01
**标签**: Super Lab
**Upvotes**: 24 | **Stars**: 22

**摘要**: 针对人-产品图像生成中产品细节难以保留的问题，该研究提出HiFi-Inpaint框架。该方法引入共享增强注意力（SEA）和细节感知损失（DAL）进行精细化特征提取与像素级监督，并构建了HP-Image-40K数据集。实验表明，该方法在保持高保真细节方面达到SOTA水平。

**亮点**:
  - 提出 HiFi-Inpaint 高保真修复框架
  - 引入 SEA 机制与 DAL 损失函数
  - 构建 HP-Image-40K 新数据集

---

###  2. SkillNet：AI 技能的创建、评估与互联基础设施 (SkillNet: Create, Evaluate, and Connect AI Skills)

**论文链接**: [https://arxiv.org/abs/2603.04448](https://arxiv.org/abs/2603.04448)
**组织**: Zhejiang University
**得分**: 68.43
**标签**: Frontier Lab
**Upvotes**: 47 | **Stars**: 100

**摘要**: 针对 AI 智能体缺乏系统性技能积累与复用机制的问题，本文提出了 SkillNet 开放基础设施。该框架通过统一本体论支持技能的创建、多维评估及连接，并整合了 20 万技能的仓库。实验表明，SkillNet 在多基准测试中将平均奖励提升 40%，执行步骤减少 30%。

**亮点**:
  - 提出统一技能本体论框架
  - 支持多维度的技能评估体系
  - 显著提升智能体任务执行效率

---

###  3. Timer-S1：具有串行扩展能力的十亿级时间序列基础模型 (Timer-S1: A Billion-Scale Time Series Foundation Model with Serial Scaling)

**论文链接**: [https://arxiv.org/abs/2603.04791](https://arxiv.org/abs/2603.04791)
**组织**: ByteDance
**得分**: 61.5
**标签**: Super Lab
**Upvotes**: 7 | **Stars**: 0

**摘要**: 针对现有时间序列模型的可扩展性瓶颈，本文提出 Timer-S1，采用 MoE 架构与串行令牌预测（STP），结合万亿级数据集 TimeBench 进行训练。该方法避免了推理中的误差累积，在 GIFT-Eval 上取得了最佳 MASE 和 CRPS 分数。

**亮点**:
  - 提出 8.3B 参数 MoE 时间序列基础模型
  - 引入串行令牌预测（STP）减少误差累积
  - 在 GIFT-Eval 榜单上取得 SOTA 性能

---

###  4. AgentVista：在极具挑战性的现实视觉场景中评估多模态智能体 (AgentVista: Evaluating Multimodal Agents in Ultra-Challenging Realistic Visual Scenarios)

**论文链接**: [https://arxiv.org/abs/2602.23166](https://arxiv.org/abs/2602.23166)
**组织**: HKUST NLP Group
**得分**: 38.87
**标签**: 
**Upvotes**: 30 | **Stars**: 30

**摘要**: 针对现有基准缺乏真实性和长视界工具使用能力的问题，提出了AgentVista基准，涵盖25个子领域，包含Web搜索、编程等混合工具交互。实验表明，即使是SOTA模型（如Gemini-3-Pro）也仅达27.3%准确率，揭示了多模态智能体在复杂现实任务中的巨大性能鸿沟。

**亮点**:
  - 提出AgentVista基准，专注于长视界多模态工具使用
  - 覆盖25个子领域，集成混合工具交互与真实视觉场景
  - 揭示SOTA模型性能瓶颈，最高准确率仅27.3%

---

###  5. RoboPocket：利用手机即时优化机器人策略 (RoboPocket: Improve Robot Policies Instantly with Your Phone)

**论文链接**: [https://arxiv.org/abs/2603.05504](https://arxiv.org/abs/2603.05504)
**组织**: Shanghai Jiao Tong University
**得分**: 38.62
**标签**: Frontier Lab
**Upvotes**: 29 | **Stars**: 0

**摘要**: 针对模仿学习数据采集效率低及闭环成本高的问题，提出 RoboPocket 系统。该系统利用智能手机结合 AR 视觉预演技术，可视化策略预测轨迹，实现无需物理机器人的即时策略迭代与异步在线微调。实验表明，该方法遵循数据缩放定律，将数据效率提升至离线策略的两倍。

**亮点**:
  - 实现无机器人参与的即时策略迭代
  - 结合 AR 视觉预演可视化预测轨迹
  - 数据效率相比离线策略提升两倍

---

###  6. MOOSE-Star：通过打破复杂性壁垒解锁科学发现的可处理训练 (MOOSE-Star: Unlocking Tractable Training for Scientific Discovery by Breaking the Complexity Barrier)

**论文链接**: [https://arxiv.org/abs/2603.03756](https://arxiv.org/abs/2603.03756)
**组织**: MiroMind AI
**得分**: 36.79
**标签**: 
**Upvotes**: 74 | **Stars**: 9

**摘要**: 针对科学发现中直接建模生成推理过程 P(h|b) 存在的组合复杂性难题，提出 MOOSE-Star 框架。该方法通过分解子任务训练、动机引导分层搜索及有界组合，将复杂度从指数级降至对数级 O(log N)。实验证明，该方法克服了暴力采样的瓶颈，具备连续的测试时扩展能力。

**亮点**:
  - 将计算复杂度从 O(N^k) 显著降低至 O(log N)
  - 提出动机引导的分层搜索与子空间修剪机制
  - 发布包含 10.8 万篇分解论文的 TOMATO-Star 数据集

---

###  7. RealWonder: 实时物理动作条件视频生成 (RealWonder: Real-Time Physical Action-Conditioned Video Generation)

**论文链接**: [https://arxiv.org/abs/2603.05449](https://arxiv.org/abs/2603.05449)
**组织**: Unknown
**得分**: 34.32
**标签**: 
**Upvotes**: 5 | **Stars**: 60

**摘要**: 针对视频生成模型缺乏物理理解的问题，提出首个实时动作条件视频生成系统 RealWonder。该系统利用物理模拟作为桥梁，将动作转化为光流和 RGB，结合 3D 重建与蒸馏视频生成器，在 480x832 分辨率下实现 13.2 FPS 生成，支持力、流体等多种物理效果的交互式模拟。

**亮点**:
  - 首个实时动作条件视频生成系统
  - 利用物理模拟连接动作与视觉表示
  - 支持刚体、流体等多种材质的交互模拟

---

###  8. SageBwd：一种可训练的低比特注意力机制 (SageBwd: A Trainable Low-bit Attention)

**论文链接**: [https://arxiv.org/abs/2603.02170](https://arxiv.org/abs/2603.02170)
**组织**: University of California, Berkeley
**得分**: 33.92
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 0

**摘要**: 针对低比特注意力在预训练中的性能差距，本文通过理论与实验发现主要误差源于反向传播梯度，并指出需引入 QK-norm 和 K-smoothing。优化后的 SageBwd 在预训练中成功匹配全精度注意力性能。

**亮点**:
  - 预训练中匹配全精度性能
  - 定位反向传播梯度误差为性能瓶颈
  - 引入 QK-norm 和 K-smoothing 提升训练稳定性

---

###  9. MASQuant：面向多模态大语言模型的模态感知平滑量化 (MASQuant: Modality-Aware Smoothing Quantization for Multimodal Large Language Models)

**论文链接**: [https://arxiv.org/abs/2603.04800](https://arxiv.org/abs/2603.04800)
**组织**: alibaba-inc
**得分**: 32.93
**标签**: Frontier Lab
**Upvotes**: 8 | **Stars**: 0

**摘要**: 针对大语言模型PTQ方法难以直接迁移至多模态大模型的问题，本文指出SmoothQuant存在平滑错位与跨模态计算不变性缺陷。为此提出MASQuant框架，通过模态感知平滑（MAS）分离模态特定因子，并利用SVD白化进行跨模态补偿。该方法在双模态及三模态模型上实现了稳定量化，性能达到SOTA水平。

**亮点**:
  - 揭示MLLM量化中的平滑错位与跨模态计算不变性问题
  - 提出模态感知平滑（MAS）以学习模态特定的平滑因子
  - 引入基于SVD白化的跨模态补偿（CMC）实现统一量化

---
