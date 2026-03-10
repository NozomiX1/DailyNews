# 每日论文汇总 - 2026-03-09

**论文数量**: 7

---

### 🏆 1. 推理模型在控制思维链方面存在困难 (Reasoning Models Struggle to Control their Chains of Thought)

**论文链接**: [https://arxiv.org/abs/2603.05706](https://arxiv.org/abs/2603.05706)
**组织**: OpenAI
**得分**: 66.55
**标签**: Super Lab, Must Read
**Upvotes**: 21 | **Stars**: 0

**摘要**: 本研究探讨了现代推理模型的思维链(CoT)可控性问题。研究团队开发了CoT-Control评估套件，包含需要模型在遵守CoT指令的同时解决问题的任务。实验表明，推理模型的CoT可控性显著低于输出可控性，例如Claude Sonnet 4.5的CoT可控性仅为2.7%，但输出可控性达61.9%。研究发现更大模型具有更高CoT可控性，但随着RL训练、测试时计算和问题难度增加，CoT可控性反而下降。研究结果认为当前CoT可控性不太可能成为CoT监控的失败模式，但建议前沿实验室在未来模型中跟踪CoT可控性。

**亮点**:
  - 推理模型CoT可控性显著低于输出可控性
  - CoT可控性随RL训练和难度增加而降低
  - 当前CoT可控性不太可能破坏监控有效性

---

###  2. 企鹅-VL：基于LLM视觉编码器的VLM效率极限探索 (Penguin-VL: Exploring the Efficiency Limits of VLM with LLM-based Vision Encoders)

**论文链接**: [https://arxiv.org/abs/2603.06569](https://arxiv.org/abs/2603.06569)
**组织**: Tencent
**得分**: 68.9
**标签**: Frontier Lab
**Upvotes**: 76 | **Stars**: 70

**摘要**: 本论文针对VLM依赖模型规模扩展导致难以在移动端部署的问题，探索了紧凑型（2B和8B）VLM的性能极限。研究提出Penguin-VL架构，其核心创新在于使用纯文本LLM初始化视觉编码器，而非传统的CLIP/SigLIP对比预训练方法。实验表明，该方法解决了对比学习导致的细粒度视觉信息丢失问题，在文档理解、视觉知识推理和多视角视频理解等任务上超越Qwen3-VL等领先模型，同时仅需轻量级架构，证明了改进视觉表征而非增加模型规模是提升性能的关键。

**亮点**:
  - 提出基于纯文本LLM初始化的视觉编码器，替代传统对比预训练
  - 轻量级架构在文档理解和视频理解任务上超越Qwen3-VL
  - 验证视觉表征改进而非模型扩展是VLM性能提升的关键

---

###  3. PixARMesh：自回归网格原生的单视角场景重建 (PixARMesh: Autoregressive Mesh-Native Single-View Scene Reconstruction)

**论文链接**: [https://arxiv.org/abs/2603.05888](https://arxiv.org/abs/2603.05888)
**组织**: mlpc-ucsd
**得分**: 43.93
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 17

**摘要**: 本论文提出PixARMesh方法，实现从单张RGB图像自回归重建完整的3D室内场景网格。不同于以往依赖隐式符号距离场的方法，该方法在一个统一模型中联合预测物体布局和几何，直接生成连贯且可用于下游任务的艺术家友好网格。技术上基于点云编码器，通过交叉注意力机制融合像素对齐的图像特征与全局场景上下文，实现准确的单图像空间推理。实验在合成和真实数据集上表明，该方法达到了最先进的重建质量，同时生成轻量化、高保真几何的网格。

**亮点**:
  - 提出统一自回归框架联合预测场景布局与几何
  - 实现单次前向传递生成艺术家友好的完整3D网格
  - 在合成与真实数据集上达到SOTA重建质量

---

###  4. BandPO：通过概率感知边界弥合信任域与比率裁剪的大语言模型强化学习 (BandPO: Bridging Trust Regions and Ratio Clipping via Probability-Aware Bounds for LLM Reinforcement Learning)

**论文链接**: [https://arxiv.org/abs/2603.04918](https://arxiv.org/abs/2603.04918)
**组织**: OpenMOSS
**得分**: 43.76
**标签**: 
**Upvotes**: 52 | **Stars**: 37

**摘要**: 本论文针对大语言模型强化学习中PPO裁剪机制的固有问题进行研究。传统裁剪边界固定，严格限制低概率动作的上行更新，导致高优势尾部策略被过度抑制，并引发快速熵崩溃。为此，论文提出Band-constrained Policy Optimization (BandPO)，将f-散度定义的信任域投射到动态的、概率感知的裁剪区间。理论分析将映射表述为凸优化问题，保证全局最优解并推导出特定散度的闭式解。在多种模型和数据集上的实验表明，BandPO始终优于传统裁剪和Clip-Higher方法，同时有效缓解了熵崩溃问题。

**亮点**:
  - 提出BandPO新方法，解决PPO固定裁剪边界导致的探索瓶颈问题
  - 将信任域映射转化为凸优化问题，保证全局最优数值解
  - 实验表明BandPO在多种模型和数据集上显著优于传统裁剪方法，并有效缓解熵崩溃

---

###  5. Mario：基于大型语言模型的多模态图推理 (Mario: Multimodal Graph Reasoning with Large Language Models)

**论文链接**: [https://arxiv.org/abs/2603.05181](https://arxiv.org/abs/2603.05181)
**组织**: New York University
**得分**: 39.9
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 5

**摘要**: 本研究针对现有视觉语言模型忽略多模态数据关联结构的问题，提出名为Mario的统一框架。框架包含两个创新阶段：图条件VLM设计通过细粒度跨模态对比学习联合优化文本和视觉特征；模态自适应图指令调整机制利用可学习路由器为每个节点选择最优模态配置。在多种多模态图基准测试中，Mario在监督和零样本场景下的节点分类和链接预测任务中均优于现有SOTA图模型。

**亮点**:
  - 提出统一的多模态图推理框架Mario
  - 图条件VLM设计解决跨模态一致性问题
  - 模态自适应机制实现异构模态偏好处理

---

###  6. 基于8个Token的紧凑离散分词器：构建高效潜在世界模型 (Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model)

**论文链接**: [https://arxiv.org/abs/2603.05438](https://arxiv.org/abs/2603.05438)
**组织**: Unknown
**得分**: 35.79
**标签**: 
**Upvotes**: 28 | **Stars**: 17

**摘要**: 世界模型为模拟环境动态并支持动作规划提供了强大框架，但传统方法将每帧观测编码为数百个token，导致实时规划计算成本过高。针对这一痛点，本文提出CompACT离散分词器，将每帧观测压缩至仅8个token，在大幅降低计算开销的同时保留规划所需的关键信息。实验表明，基于该tokenizer的动作条件世界模型实现了具有竞争力的规划性能，规划速度提升数个数量级，为世界模型在实际机器人控制中的部署提供了可行路径。

**亮点**:
  - 将观测压缩至仅8个token，大幅降低规划计算成本
  - 保留关键规划信息，实现competitive规划性能
  - 推理速度提升数个数量级，接近实时控制要求

---

###  7. IF-RewardBench：指令遵循评估的法官模型基准测试 (IF-RewardBench: Benchmarking Judge Models for Instruction-Following Evaluation)

**论文链接**: [https://arxiv.org/abs/2603.04738](https://arxiv.org/abs/2603.04738)
**组织**: Tsinghua University
**得分**: 32.88
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 3

**摘要**: 指令遵循是大型语言模型的基础能力，其改进依赖于可扩展且准确的法官模型反馈。然而，现有元评估基准存在数据覆盖不足、成对评估范式过于简化等问题，导致法官模型在指令遵循方面的可靠性尚未被充分探索。本文提出IF-RewardBench，一个覆盖多种指令和约束类型的综合元评估基准，通过为每个指令构建包含多个响应间所有成对偏好的偏好图，实现列表式评估范式。实验揭示了当前法官模型的显著缺陷，并证明该基准与下游任务性能具有更强的正相关关系。

**亮点**:
  - 提出IF-RewardBench基准，覆盖多样指令和约束类型
  - 构建偏好图实现列表式评估，更契合模型对齐场景
  - 实验证明该基准与下游任务性能有更强正相关性

---
