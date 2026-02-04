# 每日论文汇总 - 2026-02-03

**论文数量**: 16

---

### 🏆 1. 为何引导有效：大模型参数动态的统一视角 (Why Steering Works: Toward a Unified View of Language Model Parameter Dynamics)

**论文链接**: [https://arxiv.org/abs/2602.02343](https://arxiv.org/abs/2602.02343)
**组织**: alibaba
**得分**: 79.63
**标签**: Frontier Lab, Viral
**Upvotes**: 9 | **Stars**: 2708

**摘要**: 针对大模型微调、LoRA及激活干预等控制方法缺乏统一认知的痛点，本文提出将此类干预建模为控制信号诱导的动态权重更新框架。研究引入了偏好-效用分析方法，揭示了增强目标偏好与保持生成效用之间的权衡关系，并从激活流形视角解释了干预导致性能下降的机制。基于此，提出 SPLIT 引导方法，在提升偏好的同时更好地保留了模型原生效用。

**亮点**:
  - 构建了大模型权重干预与控制方法的统一理论框架
  - 揭示并量化了控制偏好与生成效用（Preference-Utility）的权衡关系
  - 提出 SPLIT 引导新方法，显著提升了受控生成的有效性

---

### 🏆 2. Kimi K2.5：视觉智能体智能 (Kimi K2.5: Visual Agentic Intelligence)

**论文链接**: [https://arxiv.org/abs/2602.02276](https://arxiv.org/abs/2602.02276)
**组织**: Moonshot AI
**得分**: 75.07
**标签**: Super Lab, Must Read
**Upvotes**: 130 | **Stars**: 0

**摘要**: Kimi K2.5 是由 Moonshot AI 推出的开源多模态智能体模型，通过文本与视觉的联合预训练、零视觉 SFT 及联合强化学习，实现了双模态的深度融合与互促。该研究引入了 Agent Swarm 并行智能体编排框架，能够将复杂任务动态分解并并发执行。实验显示，K2.5 在编程、推理及智能体任务中达到 SOTA 水平，且 Agent Swarm 将任务延迟降低了 4.5 倍。

**亮点**:
  - 提出文本与视觉联合优化的多模态智能体模型架构
  - 引入 Agent Swarm 并行编排框架，支持复杂任务动态分解
  - 在编程、视觉、推理等领域取得 SOTA 性能，显著提升执行效率

---

### 🏆 3. FSVideo：高压缩潜空间下的快速视频扩散模型 (FSVideo: Fast Speed Video Diffusion Model in a Highly-Compressed Latent Space)

**论文链接**: [https://arxiv.org/abs/2602.02092](https://arxiv.org/abs/2602.02092)
**组织**: ByteDance
**得分**: 63.2
**标签**: Super Lab, Must Read
**Upvotes**: 13 | **Stars**: 0

**摘要**: 针对视频扩散模型推理效率低的挑战，字节跳动提出 FSVideo。该框架采用时空下采样率达 64x64x4 的高度压缩自动编码器，并引入具有层级记忆设计的 Diffusion Transformer (DiT) 以优化层间信息流与上下文复用。结合多分辨率生成策略，该 14B 规模的模型在保持高重建质量的同时，推理速度比主流开源模型快一个数量级。

**亮点**:
  - 实现 64x64x4 的极高维度视频潜空间压缩
  - 提出带有层级记忆设计的 DiT 架构优化信息流
  - 生成速度较当前主流开源模型提升一个数量级

---

###  4. 世界模型量化的实证研究 (An Empirical Study of World Model Quantization)

**论文链接**: [https://arxiv.org/abs/2602.02110](https://arxiv.org/abs/2602.02110)
**组织**: HUAWEI Noah's Ark Lab
**得分**: 68.64
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 929

**摘要**: 针对世界模型计算与内存开销巨大的痛点，本研究以 DINO-WM 为代表，系统性地评估了后训练量化（PTQ）在不同位宽、粒度和规划视界下的表现。实验发现，分组权重量化能有效稳定低比特下的预测演化，且编码器与预测器模块间存在显著的量化敏感性不对称。研究揭示了过度量化会导致规划目标与任务成功率失齐，为在算力受限环境下部署世界模型提供了关键的实践指导。

**亮点**:
  - 首次系统性探讨后训练量化（PTQ）对世界模型性能的影响
  - 发现编码器与预测器模块之间存在高度不对称的量化敏感性
  - 识别出激进量化导致规划目标与任务成败失齐的新失效模式

---

###  5. SWE-Universe：将真实世界可验证环境扩展至百万级 (SWE-Universe: Scale Real-World Verifiable Environments to Millions)

**论文链接**: [https://arxiv.org/abs/2602.02361](https://arxiv.org/abs/2602.02361)
**组织**: Qwen
**得分**: 68.02
**标签**: Super Lab
**Upvotes**: 31 | **Stars**: 0

**摘要**: 针对软件工程（SWE）环境自动构建中良率低、验证弱及成本高等痛点，Qwen团队推出SWE-Universe框架。该框架通过定制化模型驱动的智能体，引入迭代自验证与闭环破解检测，成功将多语言可验证环境扩展至80万个量级。实验证明该环境在智能体中期训练与强化学习中价值巨大，助力Qwen3-Max-Thinking在SWE-Bench Verified上取得75.3%的突破性成绩。

**亮点**:
  - 实现了规模达80万个的真实世界多语言SWE可验证环境构建
  - 提出具备迭代自验证与破解检测能力的自动化构建智能体
  - 助力Qwen3-Max-Thinking在SWE-Bench Verified达到75.3%的领先水平

---

###  6. Causal Forcing：高质量实时交互视频生成的自回归扩散蒸馏优化方案 (Causal Forcing: Autoregressive Diffusion Distillation Done Right for High-Quality Real-Time Interactive Video Generation)

**论文链接**: [https://arxiv.org/abs/2602.02214](https://arxiv.org/abs/2602.02214)
**组织**: Tsinghua Machine Learning Group
**得分**: 63.46
**标签**: Frontier Lab
**Upvotes**: 17 | **Stars**: 111

**摘要**: 针对实时交互视频生成中，将双向视频扩散模型蒸馏为自回归（AR）模型时存在的理论架构鸿沟，本文提出了 Causal Forcing。研究指出传统 ODE 蒸馏因违反帧级单射性导致性能受损，通过引入 AR 教师进行初始化，成功桥接了架构差异。实验证明该方法在动态度上提升 19.3%，在指令遵循上提升 16.7%，显著优于现有 SOTA 模型。

**亮点**:
  - 提出 Causal Forcing 框架，解决自回归蒸馏中的理论不匹配问题
  - 通过 AR 教师进行 ODE 初始化以确保满足帧级单射性条件
  - 在动态度、视觉奖励及指令遵循等核心指标上大幅刷新 SOTA 纪录

---

###  7. SPARKLING：平衡信号保留与对称性破缺的宽度渐进式学习框架 (SPARKLING: Balancing Signal Preservation and Symmetry Breaking for Width-Progressive Learning)

**论文链接**: [https://arxiv.org/abs/2602.02472](https://arxiv.org/abs/2602.02472)
**组织**: ByteDance Seed
**得分**: 62.21
**标签**: Super Lab
**Upvotes**: 9 | **Stars**: 0

**摘要**: 渐进式学习通过逐步增加模型规模降低预训练成本，但训练中途的宽度扩展面临训练不稳定和梯度对称性导致的特征单一化挑战。本文提出 SPARKLING 框架，通过 RMS 尺度一致性实现信号保留以稳定激活统计量，并利用非对称优化器状态重置与学习率再预热实现对称性破缺。在 MoE 模型上的实验证明，该方法在两倍宽度扩展下可节省高达 35% 的训练成本。

**亮点**:
  - 提出 SPARKLING 框架有效解决中途宽度扩展的训练不稳定问题
  - 利用 RMS 尺度一致性与非对称优化器重置平衡信号稳定与特征多样性
  - 在 MoE 模型上实现 SOTA 性能并显著降低 35% 的计算开销

---

###  8. PixelGen：利用感知损失使像素扩散模型超越潜在扩散模型 (PixelGen: Pixel Diffusion Beats Latent Diffusion with Perceptual Loss)

**论文链接**: [https://arxiv.org/abs/2602.02493](https://arxiv.org/abs/2602.02493)
**组织**: Peking University
**得分**: 58.92
**标签**: Frontier Lab
**Upvotes**: 24 | **Stars**: 39

**摘要**: 针对潜在扩散模型（LDM）因依赖 VAE 产生的伪影与瓶颈问题，北京大学研究团队提出 PixelGen 框架。该方法回归端到端的像素空间生成，通过引入 LPIPS 局部感知损失与基于 DINO 的全局语义损失，有效解决了高维像素流形难以优化的难题。实验证明，PixelGen 在无需 VAE 和复杂阶段的情况下，ImageNet-256 的 FID 达到 5.11，且在文生图任务中表现出优于 LDM 基准的性能与扩展性。

**亮点**:
  - 提出无需 VAE 或潜在表征的端到端像素级扩散生成新范式
  - 引入 LPIPS 与 DINO 双重感知损失，协同优化局部纹理与全局语义
  - 在 ImageNet 及大规模文生图测试中性能超越主流潜在扩散模型（LDM）

---

###  9. Vision-DeepResearch：激发多模态大语言模型的深度研究能力 (Vision-DeepResearch: Incentivizing DeepResearch Capability in Multimodal Large Language Models)

**论文链接**: [https://arxiv.org/abs/2601.22060](https://arxiv.org/abs/2601.22060)
**组织**: Unknown
**得分**: 50.4
**标签**: 
**Upvotes**: 116 | **Stars**: 69

**摘要**: 针对现有多模态大模型（MLLM）在复杂搜索任务中存在的推理深度不足、难以处理视觉噪声以及搜索广度受限等问题，本文提出 Vision-DeepResearch。该框架引入了多轮、多实体、多尺度的视觉与文本深度研究范式，支持数十步推理及上百次引擎交互。通过冷启动监督与强化学习训练，将深度研究能力内化至模型中。实验显示，该模型性能显著优于基于 GPT-5、Gemini-2.5-pro 等强力闭源模型构建的现有工作流。

**亮点**:
  - 提出多轮、多实体、多尺度的多模态深度研究新范式
  - 利用冷启动监督与强化学习将搜索与推理能力内化至模型
  - 性能超越基于未来高性能闭源模型（如 GPT-5）的复杂工作流

---

###  10. RLAnything：在完全动态强化学习系统中构建环境、策略与奖励模型 (RLAnything: Forge Environment, Policy, and Reward Model in Completely Dynamic RL System)

**论文链接**: [https://arxiv.org/abs/2602.02488](https://arxiv.org/abs/2602.02488)
**组织**: Princeton AI Lab
**得分**: 48.5
**标签**: 
**Upvotes**: 23 | **Stars**: 190

**摘要**: 针对大模型及智能体场景中学习信号弱的挑战，本文提出 RLAnything 框架。该系统通过闭环优化动态构建环境、策略和奖励模型：策略受逐步与结果信号联合驱动，奖励模型通过一致性反馈进行联合优化，且具备自动环境适配能力。实验证明，该方法在 OSWorld 上提升 Qwen3-VL 性能 9.1%，在 LiveBench 上提升 Qwen2.5 性能 11.9%，优化后的奖励信号优于人类标签。

**亮点**:
  - 提出环境、策略与奖励模型协同演化的闭环优化框架
  - 引入基于一致性反馈的奖励模型与环境自动适配机制
  - 在 OSWorld 和 LiveBench 等复杂智能体任务中实现显著性能增长

---

###  11. Green-VLA：面向通用机器人的分阶段视觉-语言-动作模型 (Green-VLA: Staged Vision-Language-Action Model for Generalist Robots)

**论文链接**: [https://arxiv.org/abs/2602.00919](https://arxiv.org/abs/2602.00919)
**组织**: Sber Robotics Center
**得分**: 43.67
**标签**: 
**Upvotes**: 139 | **Stars**: 20

**摘要**: 针对机器人跨形态部署及泛化能力不足的问题，本文提出 Green-VLA 框架。该框架采用五阶段课程学习方案，涵盖多模态对齐、多形态预训练及 RL 策略对齐，并构建了 3000 小时的规模化数据流水线。通过统一的动作接口，Green-VLA 实现了对人形及多种机械臂的通用控制，在长程任务成功率和部署安全性上表现卓越。

**亮点**:
  - 提出五阶段分阶段训练课程学习框架
  - 构建支持人形与移动机械臂的统一动作接口
  - 引入强化学习（RL）对齐显著提升模型鲁棒性

---

###  12. RE-TRAC：面向深度搜索智能体的递归轨迹压缩框架 (RE-TRAC: REcursive TRAjectory Compression for Deep Search Agents)

**论文链接**: [https://arxiv.org/abs/2602.02486](https://arxiv.org/abs/2602.02486)
**组织**: Microsoft
**得分**: 39.71
**标签**: Frontier Lab
**Upvotes**: 11 | **Stars**: 2

**摘要**: 针对ReAct框架在线性搜索中难以回溯状态及全局感知的局限，本文提出RE-TRAC。该框架通过在每次轨迹后生成包含证据、不确定性及未来计划的结构化状态表示，实现了跨轨迹的递归探索与反思。实验表明，RE-TRAC在BrowseComp基准上性能优于ReAct 15-20%，且显著降低了工具调用和Token消耗。通过配套的微调方法，小模型亦能实现SOTA级别的搜索表现。

**亮点**:
  - 提出递归轨迹压缩机制实现跨轨迹反思与探索
  - BrowseComp基准性能相较ReAct提升15-20%
  - 显著降低长上下文搜索中的工具调用与Token开销

---

###  13. PISCES：基于最优传输对齐奖励的无标注文本生成视频后训练方法 (PISCES: Annotation-free Text-to-Video Post-Training via Optimal Transport-Aligned Rewards)

**论文链接**: [https://arxiv.org/abs/2602.01624](https://arxiv.org/abs/2602.01624)
**组织**: Microsoft
**得分**: 36.15
**标签**: Frontier Lab
**Upvotes**: 21 | **Stars**: 0

**摘要**: 针对文本生成视频（T2V）后训练中依赖昂贵人工标注或预训练模型嵌入不对齐的问题，微软提出 PISCES 框架。该框架引入双重最优传输（OT）对齐奖励模块：通过分布级 OT 奖励提升视觉质量与时序连贯性，通过离散 Token 级 OT 奖励强化文本与视频在空时维度的语义对应。实验证明，PISCES 在 VBench 指标上超越了主流有标注和无标注方法，且兼容多种优化范式。

**亮点**:
  - 提出首个通过最优传输（OT）视角改进无标注奖励监督的生成式后训练方法
  - 引入双重 OT 奖励模块，兼顾全局分布质量与细粒度 Token 语义对齐
  - 在长/短视频生成任务中均取得超越有标注方法的 SOTA 性能

---

###  14. Mind-Brush：将智能体认知搜索与推理整合至图像生成 (Mind-Brush: Integrating Agentic Cognitive Search and Reasoning into Image Generation)

**论文链接**: [https://arxiv.org/abs/2602.01756](https://arxiv.org/abs/2602.01756)
**组织**: Unknown
**得分**: 35.92
**标签**: 
**Upvotes**: 21 | **Stars**: 26

**摘要**: 针对现有文生图模型难以理解隐含意图及受限于静态先验的痛点，本文提出 Mind-Brush 统一智能体框架。该框架模拟“思考-调研-创作”的类人范式，通过主动检索多模态证据以辅助分布外概念生成，并运用推理工具解析隐式视觉约束。实验证明，该方法在 Mind-Bench 等多个基准上显著提升了基座模型能力，实现了知识驱动的动态图像生成。

**亮点**:
  - 提出模拟类人“思考-调研-创作”的智能体化生成工作流
  - 引入多模态动态检索技术，有效解决分布外（OOD）概念的生成难题
  - 发布 Mind-Bench 基准，涵盖实时新闻、数学及地理推理等复杂视觉任务

---

###  15. PromptRL：强化学习中提示词在流匹配图像生成中的关键作用 (PromptRL: Prompt Matters in RL for Flow-Based Image Generation)

**论文链接**: [https://arxiv.org/abs/2602.01382](https://arxiv.org/abs/2602.01382)
**组织**: CUHK
**得分**: 33.8
**标签**: 
**Upvotes**: 5 | **Stars**: 55

**摘要**: 针对流匹配模型在强化学习后训练中样本效率低及提示词过拟合的问题，本文提出 PromptRL 框架。该框架将语言模型作为可训练的提示词重写代理嵌入 RL 优化循环，实现提示词与生成器的协同训练。实验显示，该方法在 GenEval 等基准上达 SOTA 性能，且相比传统 RL 减少 2 倍采样量，显著提升了图像编辑与生成的对齐质量。

**亮点**:
  - 将可训练语言模型作为提示词精炼代理集成至 RL 优化循环
  - 在 GenEval (0.97) 和 OCR 准确率 (0.98) 等多项指标取得 SOTA 性能
  - 采样效率提升显著，相比传统方法减少了 2 倍以上的采样需求

---

###  16. 像素之外：基于模式驱动智能体推理的视觉隐喻迁移 (Beyond Pixels: Visual Metaphor Transfer via Schema-Driven Agentic Reasoning)

**论文链接**: [https://arxiv.org/abs/2602.01335](https://arxiv.org/abs/2602.01335)
**组织**: Tencent
**得分**: 33.52
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 0

**摘要**: 针对生成式 AI 仅局限于像素级对齐而缺乏高阶抽象逻辑捕捉能力的痛点，腾讯提出视觉隐喻迁移（VMT）任务。该研究构建了一个基于概念整合理论（CBT）的多智能体框架，利用模式语法（G）解耦关系不变性。通过感知、迁移、生成及分层诊断智能体的协同工作，实现从参考图到目标主体的隐喻逻辑重构。实验表明，该方法在隐喻一致性与视觉创意上显著优于现有 SOTA 模型。

**亮点**:
  - 提出视觉隐喻迁移（VMT）新任务及模式语法（Schema Grammar）
  - 构建基于概念整合理论的多智能体协作推理框架
  - 引入分层诊断智能体实现闭环纠错与高保真创意合成

---
