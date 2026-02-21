# 每日论文汇总 - 2026-02-20

**论文数量**: 6

---

###  1. SpargeAttention2: 基于混合 Top-k+Top-p 掩码与蒸馏微调的可训练稀疏注意力 (SpargeAttention2: Trainable Sparse Attention via Hybrid Top-k+Top-p Masking and Distillation Fine-Tuning)

**论文链接**: [https://arxiv.org/abs/2602.13515](https://arxiv.org/abs/2602.13515)
**组织**: Tsinghua University
**得分**: 38.45
**标签**: Frontier Lab
**Upvotes**: 27 | **Stars**: 0

**摘要**: 针对现有稀疏注意力方法在扩散模型中稀疏度受限的问题，本文提出 SpargeAttention2。该方法结合 Top-k 与 Top-p 混合掩码，引入高效的可训练实现及蒸馏微调目标。实验表明，其在视频扩散模型上实现 95% 稀疏度和 16.2 倍加速，且无损生成质量。

**亮点**:
  - 提出 Top-k 与 Top-p 混合掩码策略
  - 引入蒸馏微调目标保持生成质量
  - 在视频扩散模型上实现 95% 稀疏度

---

###  2. Mobile-Agent-v3.5：多平台基础 GUI 智能体 (Mobile-Agent-v3.5: Multi-platform Fundamental GUI Agents)

**论文链接**: [https://arxiv.org/abs/2602.16855](https://arxiv.org/abs/2602.16855)
**组织**: TongyiLab
**得分**: 37.28
**标签**: Frontier Lab
**Upvotes**: 23 | **Stars**: 0

**摘要**: 针对多平台 GUI 自动化难题，提出 GUI-Owl-1.5 模型。通过混合数据飞轮、统一思维合成及 MRPO 算法优化数据与训练，实现了桌面、移动端及浏览器的云边协作。在 20+ 项基准测试中达到开源模型 SOTA 性能。

**亮点**:
  - 在 20+ 项 GUI 基准测试中取得开源模型 SOTA 性能
  - 提出混合数据飞轮与 MRPO 多平台强化学习算法
  - 支持多平台（桌面/移动/浏览器）及多种模型尺寸

---

###  3. 统一潜变量 (UL)：潜变量训练指南 (Unified Latents (UL): How to train your latents)

**论文链接**: [https://arxiv.org/abs/2602.17270](https://arxiv.org/abs/2602.17270)
**组织**: Google
**得分**: 36.84
**标签**: Frontier Lab
**Upvotes**: 21 | **Stars**: 0

**摘要**: 该研究提出统一潜变量(UL)框架，利用扩散先验和模型联合正则化学习潜变量表示。该方法在Kinetics-600取得SOTA，在ImageNet-512上以更低计算开销实现极具竞争力的FID。

**亮点**:
  - 提出扩散先验与模型联合正则化框架
  - 在Kinetics-600上刷新FVD SOTA记录
  - 训练计算成本优于Stable Diffusion潜变量

---

###  4. DDiT：用于高效扩散 Transformer 的动态 Patch 调度 (DDiT: Dynamic Patch Scheduling for Efficient Diffusion Transformers)

**论文链接**: [https://arxiv.org/abs/2602.16968](https://arxiv.org/abs/2602.16968)
**组织**: Amazon
**得分**: 33.38
**标签**: Frontier Lab
**Upvotes**: 10 | **Stars**: 0

**摘要**: 针对 Diffusion Transformers 计算开销大的痛点，提出动态 tokenization 策略。该方法根据去噪时间步和内容复杂度自适应调整 patch 大小，平衡全局结构与局部细节的建模。实验表明，该方法在不牺牲生成质量的前提下，在 FLUX-1.Dev 等模型上实现了最高 3.52 倍的推理加速。

**亮点**:
  - 提出基于时间步的动态 tokenization 策略
  - 自适应调整 patch 大小以平衡计算效率与质量
  - 在保持质量不变的情况下实现最高 3.52 倍加速

---

###  5. StereoAdapter-2：全局结构一致的水下立体深度估计 (StereoAdapter-2: Globally Structure-Consistent Underwater Stereo Depth Estimation)

**论文链接**: [https://arxiv.org/abs/2602.16915](https://arxiv.org/abs/2602.16915)
**组织**: Peking University
**得分**: 29.42
**标签**: Frontier Lab
**Upvotes**: 0 | **Stars**: 3

**摘要**: 针对水下深度估计中的域偏移与长程视差传播难题，提出StereoAdapter-2框架，利用基于选择性状态空间模型的ConvSS2D算子替代传统ConvGRU，实现高效的全局结构建模。结合新构建的大规模合成数据集UW-StereoDepth-80K，该方法在主流水下基准上取得了SOTA零样本性能。

**亮点**:
  - 提出基于选择性状态空间模型的 ConvSS2D 算子
  - 构建大规模合成数据集 UW-StereoDepth-80K
  - 水下基准测试实现 SOTA 零样本性能

---

###  6. 利用大语言模型发现多智能体学习算法 (Discovering Multiagent Learning Algorithms with Large Language Models)

**论文链接**: [https://arxiv.org/abs/2602.16928](https://arxiv.org/abs/2602.16928)
**组织**: Google
**得分**: 29.15
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 0

**摘要**: 针对多智能体强化学习算法设计依赖人工迭代的问题，本文提出基于大语言模型的进化编码代理AlphaEvolve，用于自动发现新算法。该方法演化出VAD-CFR和SHOR-PSRO两种新变体，实验显示其在非完备信息游戏中超越了包括Discounted Predictive CFR+在内的SOTA基准，具有更优的收敛性能。

**亮点**:
  - 提出 AlphaEvolve 进化编码代理
  - 发现超越 SOTA 的 VAD-CFR 算法
  - 提出收敛性更佳的 SHOR-PSRO 变体

---
