# 每日论文汇总 - 2026-02-03

**论文数量**: 11

---

### 🏆 1. Kimi K2.5：视觉自主智能体 (Kimi K2.5: Visual Agentic Intelligence)

**论文链接**: [https://arxiv.org/abs/2602.02276](https://arxiv.org/abs/2602.02276)
**组织**: Moonshot AI
**得分**: 72.08
**标签**: Super Lab, Must Read
**Upvotes**: 71 | **Stars**: 0

**摘要**: Moonshot AI 推出 Kimi K2.5 开源多模态智能体模型。该模型通过文本与视觉模态的联合预训练、零视觉 SFT 及联合强化学习实现双模态协同增强。同时引入 Agent Swarm 并行编排框架，实现复杂任务的动态分解与并发执行。实验显示其在编程、视觉及推理任务中均达 SOTA 性能，且任务延迟最高降低 4.5 倍。

**亮点**:
  - 实现文本与视觉模态的深度联合优化
  - 提出 Agent Swarm 并行智能体编排框架
  - 多领域性能达 SOTA 且显著降低执行延迟

---

### 🏆 2. FSVideo：高压缩潜空间下的极速视频扩散模型 (FSVideo: Fast Speed Video Diffusion Model in a Highly-Compressed Latent Space)

**论文链接**: [https://arxiv.org/abs/2602.02092](https://arxiv.org/abs/2602.02092)
**组织**: ByteDance
**得分**: 61.51
**标签**: Super Lab, Must Read
**Upvotes**: 9 | **Stars**: 0

**摘要**: 针对视频生成计算成本高的挑战，字节跳动推出 FSVideo 框架。核心创新包括：1. 具备 64×64×4 极高时空压缩比的视频自编码器；2. 引入层记忆（Layer Memory）设计的 DiT 架构，增强层间信息流与上下文复用；3. 结合 14B 参数基座与上采样模型的多分辨率生成策略。实验表明，该模型在保持竞争力的同时，推理速度比主流开源模型快一个数量级。

**亮点**:
  - 采用 64x64x4 极高压缩比的视频自编码器
  - 创新层记忆（Layer Memory）机制增强 DiT 处理效率
  - 推理速度实现 10 倍跨越式提升

---

###  3. 世界模型量化的经验性研究 (An Empirical Study of World Model Quantization)

**论文链接**: [https://arxiv.org/abs/2602.02110](https://arxiv.org/abs/2602.02110)
**组织**: HUAWEI Noah's Ark Lab
**得分**: 67.2
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 929

**摘要**: 针对世界模型计算开销大、内存占用高的问题，本文以 DINO-WM 为例，对世界模型的后训练量化（PTQ）进行了系统性经验研究。通过在多种视觉规划任务中测试不同比特位宽和粒度，发现分组权重量化能稳定低位宽预测，且编码器与预测器的量化敏感性呈高度不对称性。此外，激进的低比特量化会严重破坏规划目标与任务成功率的对齐，为受限资源下的模型部署提供了实战指导。

**亮点**:
  - 首次系统性评估 PTQ 对世界模型规划任务的影响
  - 揭示了编码器与预测器模块间高度不对称的量化敏感性
  - 发现激进量化会导致规划目标与任务成功率的严重失配

---

###  4. SWE-Universe：将真实世界可验证软件工程环境扩展至百万级 (SWE-Universe: Scale Real-World Verifiable Environments to Millions)

**论文链接**: [https://arxiv.org/abs/2602.02361](https://arxiv.org/abs/2602.02361)
**组织**: Qwen
**得分**: 64.56
**标签**: Super Lab
**Upvotes**: 15 | **Stars**: 0

**摘要**: 针对真实世界软件工程（SWE）环境构建中良率低、验证弱及成本高昂等痛点，本研究提出 SWE-Universe 框架。该框架利用定制模型驱动的构建智能体，通过迭代自验证和环路黑客检测，从 GitHub PR 中自动生成高保真任务。目前已构建超 80 万个跨语言环境，并助力 Qwen3-Max-Thinking 在 SWE-bench Verified 基准测试中取得 75.3% 的 SOTA 成绩。

**亮点**:
  - 提出可扩展的自动化 SWE 环境构建框架
  - 成功构建包含 80 万个真实任务的跨语言数据集
  - 助力 Qwen3 系列模型在 SWE-bench 取得突破性进展

---

###  5. SPARKLING：在宽度渐进式学习中平衡信号保持与对称性打破 (SPARKLING: Balancing Signal Preservation and Symmetry Breaking for Width-Progressive Learning)

**论文链接**: [https://arxiv.org/abs/2602.02472](https://arxiv.org/abs/2602.02472)
**组织**: ByteDance Seed
**得分**: 61.68
**标签**: Super Lab
**Upvotes**: 8 | **Stars**: 0

**摘要**: 针对宽度渐进式学习在训练中期扩展时面临的训练不稳定（Loss 激增）和梯度对称性（特征多样性受损）痛点，本文提出 SPARKLING 框架。该方法利用 RMS 尺度一致性维持信号稳定，并通过非对称优化器状态重置与学习率再预热打破对称性。实验表明，在 MoE 模型上该方案较从头训练可节省达 35% 的计算成本。

**亮点**:
  - 提出首个针对训练中期宽度扩展的 SPARKLING 框架
  - 结合 RMS 尺度一致性与非对称优化器重置解决训练失稳
  - 在 MoE 模型上实现高达 35% 的预训练计算成本缩减

---

###  6. Causal Forcing：用于高质量实时交互式视频生成的自回归扩散蒸馏优化方案 (Causal Forcing: Autoregressive Diffusion Distillation Done Right for High-Quality Real-Time Interactive Video Generation)

**论文链接**: [https://arxiv.org/abs/2602.02214](https://arxiv.org/abs/2602.02214)
**组织**: Tsinghua Machine Learning Group
**得分**: 54.85
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 34

**摘要**: 针对实时交互式视频生成，现有方法在将双向视频扩散模型蒸馏为自回归（AR）模型时，因注意力机制差异导致 ODE 初始化违反帧级单射性，进而产生均值解并降低生成质量。本文提出 Causal Forcing，通过引入 AR 教师模型进行 ODE 初始化，从理论上弥补了双向与自回归架构间的鸿沟。实验表明，该方法在动态度、视觉奖励和指令遵循等指标上显著超越 SOTA 模型 Self Forcing。

**亮点**:
  - 理论上解决了自回归蒸馏中的架构不匹配与单射性失效问题
  - 提出 Causal Forcing 框架实现高质量实时交互式视频生成
  - 性能显著超越 SOTA，其中动态度指标提升达 19.3%

---

###  7. RLAnything：在完全动态强化学习系统中构建环境、策略与奖励模型 (RLAnything: Forge Environment, Policy, and Reward Model in Completely Dynamic RL System)

**论文链接**: [https://arxiv.org/abs/2602.02488](https://arxiv.org/abs/2602.02488)
**组织**: Princeton AI Lab
**得分**: 46.85
**标签**: 
**Upvotes**: 20 | **Stars**: 161

**摘要**: 针对大语言模型和智能体场景中学习信号不足的挑战，普林斯顿大学提出 RLAnything 框架。该系统通过闭环优化动态构建环境、策略和奖励模型：策略层结合步进式与结果信号，奖励模型通过一致性反馈进行协同优化，且环境能根据反馈自动适配。实验表明，该方案显著提升了 Qwen 系列模型在 OSWorld 和 LiveBench 等任务上的性能，且优化后的奖励信号优于人工标注。

**亮点**:
  - 提出环境、策略与奖励模型协同进化的闭环 RL 框架
  - 利用一致性反馈和自动环境适配增强学习信号
  - 在多项智能体基准测试中实现显著的性能增益

---

###  8. PixelGen：基于感知损失超越潜空间扩散的像素扩散模型 (PixelGen: Pixel Diffusion Beats Latent Diffusion with Perceptual Loss)

**论文链接**: [https://arxiv.org/abs/2602.02493](https://arxiv.org/abs/2602.02493)
**组织**: Peking University
**得分**: 44.36
**标签**: Frontier Lab
**Upvotes**: 10 | **Stars**: 6

**摘要**: 针对潜空间扩散模型中 VAE 带来的伪影与性能瓶颈，本文提出 PixelGen 框架，直接在像素空间进行端到端生成。通过引入 LPIPS 局部感知损失和基于 DINO 的全局语义感知损失，PixelGen 有效解决了高维像素流形优化难题。实验证明，该方法在 ImageNet-256 上达到了 5.11 的 FID 评分，且在大规模文生图任务中表现优异，提供了一种无需 VAE 的更简便且强大的生成范式。

**亮点**:
  - 提出受感知监督的端到端像素扩散框架
  - 无需 VAE 即可超越强力潜空间扩散模型基线
  - 引入 LPIPS 与 DINO 双重损失优化高维像素流形

---

###  9. PISCES: 基于最优传输对齐奖励的无标注文本生成视频后训练方法 (PISCES: Annotation-free Text-to-Video Post-Training via Optimal Transport-Aligned Rewards)

**论文链接**: [https://arxiv.org/abs/2602.01624](https://arxiv.org/abs/2602.01624)
**组织**: Microsoft
**得分**: 35.42
**标签**: Frontier Lab
**Upvotes**: 18 | **Stars**: 0

**摘要**: 针对文本生成视频（T2V）后训练中依赖大规模人工标注或嵌入对齐不足的问题，微软提出 PISCES 框架。该框架引入双重最优传输（OT）奖励模块，在分布层级提升视频质量与时空相干性，并在离散 Token 层级强化文本与视频的语义对应。实验证明，PISCES 在 VBench 评分上优于多种有标注及无标注方法，且兼容反向传播与强化学习等多种优化范式。

**亮点**:
  - 提出首个利用最优传输（OT）实现无标注奖励监督的视频生成后训练算法
  - 设计双重 OT 奖励机制，兼顾全局视觉质量与细粒度语义时空对齐
  - 在 VBench 短视频和长视频生成任务中性能全面超越现有基准方法

---

###  10. Vision-DeepResearch：激发多模态大语言模型的深度研究能力 (Vision-DeepResearch: Incentivizing DeepResearch Capability in Multimodal Large Language Models)

**论文链接**: [https://arxiv.org/abs/2601.22060](https://arxiv.org/abs/2601.22060)
**组织**: Unknown
**得分**: 34.22
**标签**: 
**Upvotes**: 21 | **Stars**: 18

**摘要**: 针对现有多模态模型在复杂搜索中推理深度不足及难以应对视觉噪声的问题，本文提出 Vision-DeepResearch 范式。该方法采用多轮、多实体、多尺度的图文搜索增强检索鲁棒性，并利用冷启动监督与强化学习将研究能力内化。实验表明，其支持上百次引擎交互，性能超越了基于 GPT-5 和 Gemini-2.5-pro 等闭源模型构建的工作流。

**亮点**:
  - 提出多轮、多实体、多尺度的多模态深度研究新范式
  - 通过冷启动监督与强化学习将深度研究能力内化至 MLLM
  - 在复杂搜索任务中显著超越基于 GPT-5 等最强闭源模型的工作流

---

###  11. 超越像素：基于图式驱动智能体推理的视觉隐喻迁移 (Beyond Pixels: Visual Metaphor Transfer via Schema-Driven Agentic Reasoning)

**论文链接**: [https://arxiv.org/abs/2602.01335](https://arxiv.org/abs/2602.01335)
**组织**: Tencent
**得分**: 33.12
**标签**: Frontier Lab
**Upvotes**: 11 | **Stars**: 0

**摘要**: 针对现有生成式AI仅限于像素对齐而难以捕捉抽象隐喻逻辑的痛点，本文提出视觉隐喻迁移（VMT）任务。该研究引入受认知科学启发的图式语法，构建了一个包含感知、迁移、生成及分层诊断的多智能体协作框架，实现了创意逻辑的解耦与重构。实验证明，该方法在隐喻一致性与创意性上显著优于SOTA基准。

**亮点**:
  - 提出视觉隐喻迁移（VMT）新任务及评价标准
  - 基于图式语法（Schema Grammar）实现抽象逻辑的结构化表示
  - 引入具备闭环回溯功能的分层诊断智能体以提升生成质量

---
