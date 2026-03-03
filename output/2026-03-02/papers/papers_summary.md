# 每日论文汇总 - 2026-03-02

**论文数量**: 13

---

### 🏆 1. CUDA Agent: 用于高性能 CUDA 内核生成的大规模智能体强化学习系统 (CUDA Agent: Large-Scale Agentic RL for High-Performance CUDA Kernel Generation)

**论文链接**: [https://arxiv.org/abs/2602.24286](https://arxiv.org/abs/2602.24286)
**组织**: ByteDance Seed
**得分**: 70.35
**标签**: Super Lab, Must Read
**Upvotes**: 46 | **Stars**: 0

**摘要**: 针对现有方法难以提升 LLM 内核优化能力的问题，提出 CUDA Agent 系统。该系统通过数据合成管道、自动化验证环境及强化学习技术增强模型性能。实验表明其在 KernelBench 达到 SOTA，速度显著超越 torch.compile 和 Claude 等顶级模型。

**亮点**:
  - KernelBench 达到 SOTA 性能
  - 提出大规模智能体强化学习系统
  - 性能显著超越 torch.compile 及 Claude 等模型

---

###  2. dLLM：简易扩散语言建模 (dLLM: Simple Diffusion Language Modeling)

**论文链接**: [https://arxiv.org/abs/2602.22661](https://arxiv.org/abs/2602.22661)
**组织**: UC Berkeley
**得分**: 89.02
**标签**: Frontier Lab
**Upvotes**: 81 | **Stars**: 1924

**摘要**: 针对现有扩散语言模型组件分散、难以复现的问题，该研究提出开源框架 dLLM。该框架统一了训练、推理和评估流程，支持将 BERT 或自回归模型转换为扩散模型。dLLM 提供了标准化的复现与微调管线，并开源了小型模型权重，显著降低了研究门槛。

**亮点**:
  - 统一扩散语言模型核心组件
  - 支持 BERT/ARLM 转 DLM
  - 开源小型 DLM 构建方案及权重

---

###  3. 通过奖励建模增强图像生成的空间理解 (Enhancing Spatial Understanding in Image Generation via Reward Modeling)

**论文链接**: [https://arxiv.org/abs/2602.24233](https://arxiv.org/abs/2602.24233)
**组织**: Peking University
**得分**: 62.85
**标签**: Frontier Lab
**Upvotes**: 44 | **Stars**: 41

**摘要**: 针对文生图模型处理复杂空间关系难的问题，本文构建了8万偏好对数据集SpatialReward-Dataset并提出SpatialScore奖励模型。该模型在空间评估上超越领先私有模型，并通过强化学习显著提升了生成的空间准确性。

**亮点**:
  - 构建包含8万偏好对的SpatialReward-Dataset
  - 提出SpatialScore评估空间关系准确性
  - 通过在线强化学习显著提升空间理解

---

###  4. 融合众数寻优与均值寻优的快速长视频生成 (Mode Seeking meets Mean Seeking for Fast Long Video Generation)

**论文链接**: [https://arxiv.org/abs/2602.24289](https://arxiv.org/abs/2602.24289)
**组织**: NVIDIA
**得分**: 38.39
**标签**: Frontier Lab
**Upvotes**: 29 | **Stars**: 0

**摘要**: 针对长视频数据稀缺的瓶颈，提出基于解耦扩散Transformer的训练范式。该方法利用全局流匹配头学习长程叙事，并使用众数寻优反向KL将局部窗口对齐冻结的短视频教师，实现了兼具局部清晰度与长程连贯性的分钟级视频快速生成。

**亮点**:
  - 提出解耦扩散Transformer架构
  - 融合众数寻优与均值寻优训练策略
  - 实现分钟级长视频少步快速生成

---

###  5. 翻译复原：自动化基准和数据集翻译的高效流水线 (Recovered in Translation: Efficient Pipeline for Automated Translation of Benchmarks and Datasets)

**论文链接**: [https://arxiv.org/abs/2602.22207](https://arxiv.org/abs/2602.22207)
**组织**: Institute for Computer Science, Artificial intelligence and Technology 
**得分**: 35.69
**标签**: 
**Upvotes**: 36 | **Stars**: 14

**摘要**: 针对多语种 LLM 评估基准翻译质量差的问题，本文提出一种自动化翻译框架。该方法采用测试时算力扩展策略 USI 及多轮排序法 T-RANK，显著提升了翻译质量，有效保留了任务结构与语言细节。实验表明，其翻译效果优于现有资源，提升了下游模型评估的准确性。

**亮点**:
  - 提出包含 T-RANK 的自动化翻译流水线
  - 利用测试时算力扩展策略提升翻译质量
  - 显著改善东欧与南欧语言基准评估可靠性

---

###  6. LongVideo-R1：面向低成本长视频理解的智能导航 (LongVideo-R1: Smart Navigation for Low-cost Long Video Understanding)

**论文链接**: [https://arxiv.org/abs/2602.20913](https://arxiv.org/abs/2602.20913)
**组织**: ucas
**得分**: 30.04
**标签**: 
**Upvotes**: 8 | **Stars**: 18

**摘要**: 针对低算力成本下的长视频理解难题，本文提出了LongVideo-R1智能代理。该模型利用推理模块从高层视觉摘要自顶向下导航，动态选择关键片段并适时停止，通过SFT和RL两阶段训练，在QA准确率与效率间实现了更优平衡。

**亮点**:
  - 提出具备推理能力的主动式视频理解代理
  - 实现自顶向下的层级式导航与智能早停
  - 采用SFT与强化学习相结合的两阶段训练范式

---

###  7. Ref-Adv：探索指代表达任务中的MLLM视觉推理能力 (Ref-Adv: Exploring MLLM Visual Reasoning in Referring Expression Tasks)

**论文链接**: [https://arxiv.org/abs/2602.23898](https://arxiv.org/abs/2602.23898)
**组织**: Northeastern University 
**得分**: 28.13
**标签**: 
**Upvotes**: 7 | **Stars**: 15

**摘要**: 针对现有指代表达理解基准存在表述简单、干扰项少及易受捷径解法影响的问题，本文提出了Ref-Adv数据集。该数据集通过引入语言非平凡表达和困难干扰项，迫使模型进行真正的视觉推理。实验表明，尽管当前MLLM在标准基准上表现优异，但在Ref-Adv上性能显著下降，揭示了模型过度依赖捷径及缺乏深层视觉推理能力的短板。

**亮点**:
  - 提出Ref-Adv基准以抑制捷径解法，测试深层推理
  - 构建包含复杂语言表达、困难干扰项及否定推理的数据集
  - 揭示了当前SOTA MLLM在真实视觉推理场景下的性能崩塌

---

###  8. 面向 LLM 推理的强化感知知识蒸馏 (Reinforcement-aware Knowledge Distillation for LLM Reasoning)

**论文链接**: [https://arxiv.org/abs/2602.22495](https://arxiv.org/abs/2602.22495)
**组织**: Amazon Web Services (AWS)
**得分**: 24.56
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 0

**摘要**: 针对 RL 训练中传统 KD 方法存在的分布不匹配和目标干扰问题，提出强化感知蒸馏（RLAD）。该方法利用信任域比率蒸馏（TRRD）替代 KL 正则化，在学生模型的更新中进行选择性模仿。实验表明，RLAD 在逻辑推理和数学基准上超越了离线蒸馏、标准 GRPO 等方法。

**亮点**:
  - 提出 RLAD 解决 RL 训练中的分布不匹配
  - 引入 TRRD 模块平衡探索与模仿
  - 在多项基准测试中超越现有蒸馏方法

---

###  9. DUET-VLM：面向 VLM 训练与推理的双阶段统一高效 Token 压缩 (DUET-VLM: Dual stage Unified Efficient Token reduction for VLM Training and Inference)

**论文链接**: [https://arxiv.org/abs/2602.18846](https://arxiv.org/abs/2602.18846)
**组织**: AMD
**得分**: 23.86
**标签**: 
**Upvotes**: 3 | **Stars**: 13

**摘要**: 针对 VLM 因密集视觉 Token 导致计算昂贵的问题，提出 DUET-VLM 框架。该方法通过视觉端的冗余感知压缩与语言端基于文本显著性的分层 Token 丢弃，实现双重压缩。在 LLaVA-1.5-7B 上，Token 减少 67% 时保持 99% 以上精度，并在 Video-LLaVA 上超越基线性能。

**亮点**:
  - 提出双阶段统一高效压缩框架
  - 89% Token 减少率下仍保持 >97% 精度
  - 端到端训练实现 SOTA 性能

---

###  10. 通过学习潜在控制动力学加速掩码图像生成 (Accelerating Masked Image Generation by Learning Latent Controlled Dynamics)

**论文链接**: [https://arxiv.org/abs/2602.23996](https://arxiv.org/abs/2602.23996)
**组织**: Unknown
**得分**: 22.84
**标签**: 
**Upvotes**: 8 | **Stars**: 5

**摘要**: 针对掩码图像生成模型（MIGM）计算冗余且效率低的问题，提出 MIGM-Shortcut 方法。该方法通过学习融合历史特征与采样 token 的轻量级模型，回归特征演化速度场。实验显示，在 SOTA 模型 Lumina-DiMOO 上实现 4 倍加速且保持质量。

**亮点**:
  - 提出 MIGM-Shortcut 轻量级架构
  - 在 SOTA 模型上实现 4 倍生成加速
  - 显著推进掩码图像生成的帕累托前沿

---

###  11. SenCache：基于感知敏感度的扩散模型推理加速缓存方案 (SenCache: Accelerating Diffusion Model Inference via Sensitivity-Aware Caching)

**论文链接**: [https://arxiv.org/abs/2602.24208](https://arxiv.org/abs/2602.24208)
**组织**: Unknown
**得分**: 22.1
**标签**: 
**Upvotes**: 6 | **Stars**: 6

**摘要**: 针对现有扩散模型推理缓存方法依赖启发式且需大量调优的痛点，本文提出SenCache框架。通过分析模型对输入扰动的敏感性，理论推导出缓存误差预测模型，实现动态按样本自适应的缓存策略。实验显示，在同等算力下，SenCache在多个视频生成模型上视觉质量优于现有方法。

**亮点**:
  - 提出感知敏感度缓存框架
  - 建立缓存误差与敏感度的理论联系
  - 实现动态按样本自适应缓存策略

---

###  12. 视觉嵌入模型实现组合泛化需具备线性正交表征 (Compositional Generalization Requires Linear, Orthogonal Representations in Vision Embedding Models)

**论文链接**: [https://arxiv.org/abs/2602.24264](https://arxiv.org/abs/2602.24264)
**组织**: Unknown
**得分**: 21.52
**标签**: 
**Upvotes**: 14 | **Stars**: 2

**摘要**: 针对模型在未见组合输入上的泛化难题，研究形式化了三个期望条件，从理论上证明支持组合泛化的表征必须具备线性分解且概念间正交的几何结构。通过对 CLIP 等视觉模型的实证分析，发现表征确实存在部分线性分解，且该结构程度与未见组合上的泛化能力正相关。

**亮点**:
  - 提出支持组合泛化的线性正交表征理论约束
  - 为“线性表征假说”提供理论依据
  - 验证了视觉模型表征结构与泛化能力的关联

---

###  13. 认知模型与 AI 算法为语言智能体设计提供模板 (Cognitive Models and AI Algorithms Provide Templates for Designing Language Agents)

**论文链接**: [https://arxiv.org/abs/2602.22523](https://arxiv.org/abs/2602.22523)
**组织**: Princeton University
**得分**: 21.1
**标签**: Frontier Lab
**Upvotes**: 0 | **Stars**: 0

**摘要**: 针对单一 LLM 难以处理复杂任务及组合方式不明确的痛点，论文提出借鉴认知模型和 AI 算法设计“智能体模板”。通过形式化定义 LLM 角色与组合方式，并调研现有工作，旨在指导构建有效且可解释的模块化语言智能体。

**亮点**:
  - 提出智能体模板形式化概念
  - 结合认知科学与 AI 算法设计
  - 解决多 LLM 系统组合难题

---
