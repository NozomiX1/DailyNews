# 每日论文汇总 - 2026-02-09

**论文数量**: 15

---

###  1. 百川-M3：模拟临床问诊以实现可靠的医疗决策 (Baichuan-M3: Modeling Clinical Inquiry for Reliable Medical Decision-Making)

**论文链接**: [https://arxiv.org/abs/2602.06570](https://arxiv.org/abs/2602.06570)
**组织**: Baichuan Intelligent Technology
**得分**: 102.02
**标签**: Super Lab
**Upvotes**: 53 | **Stars**: 186

**摘要**: 针对现有医疗模型在开放咨询中被动响应及事实可靠性不足的痛点，百川智能推出 Baichuan-M3。该模型通过模拟医生系统化工作流，实现了主动信息获取、长程推理整合及自适应幻觉抑制。实验显示，Baichuan-M3 在 HealthBench 等医疗评测中达到 SOTA 性能，在临床问诊、建议及安全性方面显著优于强力基座模型，实现了从被动问答向主动决策支持的转变。

**亮点**:
  - 实现从被动问答向主动临床决策支持的范式转移
  - 引入自适应幻觉抑制技术确保医疗事实可靠性
  - 在 HealthBench 和 ScanBench 等多项权威测试中取得 SOTA 性能

---

###  2. Canzona：针对分布式矩阵优化器的统一、异步且负载均衡框架 (Canzona: A Unified, Asynchronous, and Load-Balanced Framework for Distributed Matrix-based Optimizers)

**论文链接**: [https://arxiv.org/abs/2602.06079](https://arxiv.org/abs/2602.06079)
**组织**: Qwen
**得分**: 63.52
**标签**: Super Lab
**Upvotes**: 12 | **Stars**: 0

**摘要**: 针对大模型训练中矩阵优化器（如 Shampoo、Muon）与分布式框架张量分片冲突导致的计算冗余和负载不均衡问题，本文提出 Canzona 框架。该框架通过解耦逻辑优化器分配与物理参数分布，在数据并行下采用 alpha 平衡静态分区，在张量并行下利用微组调度实现异步计算流水线。在 Qwen3 32B 模型测试中，实现 1.57 倍端到端加速，并将优化器步延迟降低 5.8 倍。

**亮点**:
  - 提出解耦逻辑优化器分配与物理参数分布的统一分布式框架
  - 通过 alpha 平衡分区与微组调度有效解决负载不均并隐藏计算开销
  - 在 Qwen3 32B 规模下实现 1.57 倍端到端加速，大幅提升训练效率

---

###  3. 大语言模型强化微调过程中的熵动力学研究 (On the Entropy Dynamics in Reinforcement Fine-Tuning of Large Language Models)

**论文链接**: [https://arxiv.org/abs/2602.03392](https://arxiv.org/abs/2602.03392)
**组织**: Unknown
**得分**: 57.97
**标签**: 
**Upvotes**: 44 | **Stars**: 521

**摘要**: 针对大语言模型强化微调（RFT）中缺乏对熵动力学原理性理解的痛点，本文建立了一套分析 RFT 过程熵变的理论框架。研究从单次 Logit 更新的判别式出发，推导出熵变的一阶表达式，并将其扩展至 GRPO 算法。基于该理论提出的熵判别器裁剪方法，能有效平衡训练中的探索与利用。实验证实了理论的有效性，为优化 LLM 微调动态提供了新见解。

**亮点**:
  - 建立了大模型 RFT 熵动力学的首个系统性理论框架
  - 推导并统一了 GRPO 等策略优化算法中的熵更新公式
  - 提出熵判别器裁剪（Entropy-discriminator clipping）显著优化探索平衡

---

###  4. AudioSAE：利用稀疏自编码器解析音频处理模型 (AudioSAE: Towards Understanding of Audio-Processing Models with Sparse AutoEncoders)

**论文链接**: [https://arxiv.org/abs/2602.05027](https://arxiv.org/abs/2602.05027)
**组织**: HUAWEI Noah's Ark Lab
**得分**: 46.26
**标签**: Frontier Lab
**Upvotes**: 40 | **Stars**: 2

**摘要**: 本文针对音频模型内部表示缺乏可解释性的痛点，提出在 Whisper 和 HuBERT 编码层应用稀疏自编码器（SAE）。研究证明 SAE 能有效解耦声学、语义及环境噪音等特征，且超过 50% 的特征具有跨种子稳定性。实验表明，通过特征引导可将 Whisper 的误检测率降低 70%，同时发现 SAE 特征与人类大脑 EEG 活动存在相关性，展现了其在理解音频模型及实际应用中的巨大潜力。

**亮点**:
  - 首次在 Whisper 和 HuBERT 等大规模音频模型中系统性应用 SAE 进行解释性研究
  - 利用特征引导技术在几乎不损耗 WER 的情况下将 Whisper 误检测率降低 70%
  - 验证了 SAE 特征与人类语音感知过程中的 EEG 活动具有显著相关性

---

###  5. OdysseyArena：面向长程、主动及归纳式交互的大语言模型智能体基准测试 (OdysseyArena: Benchmarking Large Language Models For Long-Horizon, Active and Inductive Interactions)

**论文链接**: [https://arxiv.org/abs/2602.05843](https://arxiv.org/abs/2602.05843)
**组织**: Unknown
**得分**: 38.73
**标签**: 
**Upvotes**: 50 | **Stars**: 19

**摘要**: 针对现有智能体评估局限于显式规则和短程规划的问题，本文推出OdysseyArena框架，强调长程、主动及归纳式交互。该框架通过四大原语构建交互环境，并设立Lite版与Challenge版（支持200+步长交互）评估任务。实验表明，即便领先的LLM在归纳发现潜规则方面仍存在明显短板，揭示了实现自主探索的核心瓶颈。

**亮点**:
  - 提出首个聚焦于归纳式学习（Inductive）能力的智能体基准
  - 设计了超过200步的极端长程交互压力测试
  - 揭示了现有顶尖模型在自主发现环境演化规律上的显著缺陷

---

###  6. MSign：通过恢复稳定秩防止大语言模型训练不稳定的优化器 (MSign: An Optimizer Preventing Training Instability in Large Language Models via Stable Rank Restoration)

**论文链接**: [https://arxiv.org/abs/2602.01734](https://arxiv.org/abs/2602.01734)
**组织**: Microsoft
**得分**: 37.94
**标签**: Frontier Lab
**Upvotes**: 28 | **Stars**: 0

**摘要**: 针对大语言模型预训练中梯度爆炸导致的训练崩溃问题，本文识别出崩溃前权重矩阵稳定秩下降及相邻层雅可比矩阵对齐度增加的现象，并证明其导致梯度范数随深度呈指数增长。为此提出 MSign 优化器，通过定期应用矩阵符号（sign）操作恢复稳定秩。实验表明，该方法在 5M 至 3B 参数模型上能有效防止训练失败，且额外计算开销低于 7.0%。

**亮点**:
  - 揭示了权重矩阵稳定秩下降与训练崩溃之间的理论关联
  - 提出新型优化器 MSign，通过定期矩阵符号操作恢复稳定性
  - 在最高 3B 参数规模下验证了防崩溃的有效性且计算开销极低

---

###  7. 以表为搜：将长程智能体信息检索重构为表格填充任务 (Table-as-Search: Formulate Long-Horizon Agentic Information Seeking as Table Completion)

**论文链接**: [https://arxiv.org/abs/2602.06724](https://arxiv.org/abs/2602.06724)
**组织**: AIDC-AI
**得分**: 37.22
**标签**: 
**Upvotes**: 1 | **Stars**: 246

**摘要**: 针对长程信息检索智能体在纯文本上下文中难以维持搜索状态和一致性的痛点，本文提出 Table-as-Search (TaS) 结构化规划框架。该方法将检索任务重构为表格填充，利用外部数据库记录搜索候选（行）与约束信息（列），使空单元格成为显式搜索计划。TaS 统一了深搜、广搜及深度广搜模式，实验表明其在稳健性与效率上显著优于现有商业系统和 SOTA 基准。

**亮点**:
  - 提出 TaS 框架将长程检索任务转化为结构化的表格填充过程
  - 通过外部数据库显式管理搜索状态，解决纯文本上下文的易碎性问题
  - 统一并显著提升了深搜、广搜及 DeepWide Search 的性能与稳健性

---

###  8. DreamDojo：基于大规模人体视频的通用机器人世界模型 (DreamDojo: A Generalist Robot World Model from Large-Scale Human Videos)

**论文链接**: [https://arxiv.org/abs/2602.06949](https://arxiv.org/abs/2602.06949)
**组织**: NVIDIA
**得分**: 34.98
**标签**: Frontier Lab
**Upvotes**: 19 | **Stars**: 0

**摘要**: 针对机器人灵巧操作建模中数据规模有限及动作标签缺失的挑战，NVIDIA 推出 DreamDojo 通用世界模型。该模型利用目前最大规模的 44k 小时第一人称人体视频进行预训练，通过引入连续潜动作作为代理动作，有效解决了无标签视频的知识迁移难题。经蒸馏后的模型支持 10.81 FPS 实时生成，在复杂接触任务和 OOD 基准测试中展现出卓越的物理一致性与动作可控性。

**亮点**:
  - 采用目前最大规模（44k 小时）的人体视频数据集进行预训练
  - 提出连续潜动作（Latent Actions）作为跨域知识迁移的统一代理
  - 实现 10.81 FPS 的实时生成速度，支持在线遥操作与策略评估

---

###  9. OmniMoE：通过大规模编排原子专家实现的高效混合专家架构 (OmniMoE: An Efficient MoE by Orchestrating Atomic Experts at Scale)

**论文链接**: [https://arxiv.org/abs/2602.05711](https://arxiv.org/abs/2602.05711)
**组织**: Beijing Academy of Artificial Intelligence
**得分**: 32.97
**标签**: 
**Upvotes**: 4 | **Stars**: 52

**摘要**: 针对细粒度 MoE 架构在专家特化与硬件效率间的权衡难题，本文提出 OmniMoE 系统算法协同设计框架。该框架引入向量级“原子专家”，通过笛卡尔积路由将复杂度降至 O(sqrt(N))，并利用以专家为中心的调度将零散访存转化为高效矩阵运算。在 1.7B 激活参数下，其推理速度较 PEER 提升 10.9 倍，在多个基准测试中展现了卓越的零样本性能与硬件效率。

**亮点**:
  - 提出向量级“原子专家”设计，将专家细粒度推向逻辑极限
  - 通过笛卡尔积路由将大规模索引空间的路由复杂度从 O(N) 降至 O(sqrt(N))
  - 推理延迟较 PEER 降低 10.9 倍，成功兼顾了大规模细粒度 MoE 的精度与速度

---

###  10. compar:IA：法国政府推出的大规模法语指令与偏好数据众包平台 (compar:IA: The French Government's LLM arena to collect French-language human prompts and preference data)

**论文链接**: [https://arxiv.org/abs/2602.06669](https://arxiv.org/abs/2602.06669)
**组织**: Ministère de la Culture (SNUM)
**得分**: 32.19
**标签**: 
**Upvotes**: 3 | **Stars**: 59

**摘要**: 针对大语言模型在非英语环境下性能及文化对齐不足的问题，法国文化部推出了开源平台 compar:IA。该平台利用盲测成对比较机制，从公众中收集真实场景下的法语提示词与偏好数据。截至2026年2月，已积累逾60万条指令和25万次投票。研究团队开源了相关数据集和排行榜，为多语言模型的RLHF与DPO对齐提供了关键的数字化公共基础设施。

**亮点**:
  - 由法国政府主导的大规模法语人类偏好数据开源项目
  - 积累超过 60 万条真实世界提示词和 25 万项偏好投票
  - 提供可复用的开源架构以支持多语言 AI 生态的对齐与评估

---

###  11. POINTS-GUI-G：GUI 界面元素定位技术的演进之路 (POINTS-GUI-G: GUI-Grounding Journey)

**论文链接**: [https://arxiv.org/abs/2602.06391](https://arxiv.org/abs/2602.06391)
**组织**: Unknown
**得分**: 32.09
**标签**: 
**Upvotes**: 14 | **Stars**: 21

**摘要**: 该研究旨在提升 GUI 智能体在自动化任务中的元素定位（Grounding）能力。基于 POINTS-1.5 基础模型，通过精细化数据工程、视觉编码器微调以及引入可验证奖励的强化学习，成功开发了 POINTS-GUI-G-8B。实验证明，强化学习能显著提升感知任务的精度，该模型在 ScreenSpot-Pro 和 OSWorld-G 等多个基准测试中均取得了 SOTA 性能。

**亮点**:
  - 在 ScreenSpot-Pro 和 OSWorld-G 等多个 GUI 定位榜单达到 SOTA 水平
  - 证明了强化学习（RL）能显著提升以感知为主的 GUI 定位任务精度
  - 提出了包含数据格式统一、增强及难度分级的精细化数据工程体系

---

###  12. MemGUI-Bench：针对动态环境下移动 GUI 智能体记忆能力的基准测试 (MemGUI-Bench: Benchmarking Memory of Mobile GUI Agents in Dynamic Environments)

**论文链接**: [https://arxiv.org/abs/2602.06075](https://arxiv.org/abs/2602.06075)
**组织**: Zhejiang University
**得分**: 30.86
**标签**: 
**Upvotes**: 13 | **Stars**: 18

**摘要**: 针对现有移动 GUI 智能体基准测试在记忆能力评估上的严重缺失（相关任务仅占约 10%），浙江大学团队提出了 MemGUI-Bench。该基准包含系统性的记忆分类法、涵盖 26 个应用的 128 个跨时空维度任务，以及配套的 MemGUI-Eval 自动化评估流水线。实验评估了 11 种 SOTA 智能体，揭示了它们在动态环境中普遍存在的记忆缺陷及 5 种典型失败模式。

**亮点**:
  - 提出首个专注于移动端 GUI 智能体长短期及跨会话记忆能力的基准测试。
  - 设计了包含渐进式审查（Progressive Scrutiny）机制的自动化评估框架。
  - 系统性分析并总结了当前 SOTA 智能体在记忆任务中的 5 种核心失败模式。

---

###  13. OmniVideo-R1：基于查询意图与模态注意力的强化视听推理框架 (OmniVideo-R1: Reinforcing Audio-visual Reasoning with Query Intention and Modality Attention)

**论文链接**: [https://arxiv.org/abs/2602.05847](https://arxiv.org/abs/2602.05847)
**组织**: Tencent
**得分**: 28.03
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 针对现有全景视频模型在视听理解任务中难以协同处理多模态信息的痛点，腾讯提出 OmniVideo-R1 强化推理框架。该框架通过基于自监督学习的密集查询定位和基于对比学习的模态注意力融合两大核心策略，显著提升了模型利用全模态线索进行推理的能力。实验结果表明，OmniVideo-R1 在多个基准测试中均优于强基线模型，展现出卓越的性能与泛化性。

**亮点**:
  - 提出基于自监督学习的密集查询定位策略
  - 引入基于对比学习的模态注意力融合机制
  - 在多项视听理解任务中实现性能突破

---

###  14. ReMiT：基于强化学习引导的中期训练实现大语言模型迭代进化 (ReMiT: RL-Guided Mid-Training for Iterative LLM Evolution)

**论文链接**: [https://arxiv.org/abs/2602.03075](https://arxiv.org/abs/2602.03075)
**组织**: Tencent
**得分**: 28.03
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 针对传统 LLM 训练缺乏从后训练反馈至预训练机制的问题，腾讯提出 ReMiT 框架。该方法聚焦于预训练末期的退火阶段，利用强化学习微调模型的推理先验知识对 Token 进行动态重加权，优先学习关键推理路径。实验表明，ReMiT 在数学、代码等 10 项基准上平均提升 3%，成功构建了模型自我强化的迭代飞轮，使后续训练持续受益。

**亮点**:
  - 提出强化学习引导的中期训练（Mid-Training）新范式
  - 实现从后训练到基础模型的双向迭代反馈闭环
  - 在数学、代码和通用推理任务中取得显著性能增益

---

###  15. SEMA：一种简单且有效的多轮越狱攻击学习框架 (SEMA: Simple yet Effective Learning for Multi-Turn Jailbreak Attacks)

**论文链接**: [https://arxiv.org/abs/2602.06854](https://arxiv.org/abs/2602.06854)
**组织**: Microsoft
**得分**: 27.62
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 针对多轮越狱攻击中存在的探索复杂度和意图漂移痛点，微软提出了 SEMA 框架。该框架通过预填充自微调稳定学习过程，并采用感知意图漂移的强化学习奖励机制，在维持有害目标的同时生成有效的多轮攻击提示。实验显示，SEMA 在 AdvBench 上取得了 80.1% 的平均攻击成功率，显著超越现有 SOTA 方案，为大模型安全性的压力测试提供了高效工具。

**亮点**:
  - 提出一种无需外部数据或既有策略的多轮越狱攻击训练框架
  - 引入意图漂移感知奖励机制，有效平衡意图对齐与攻击合规风险
  - 在多个模型上实现 SOTA 性能，攻击成功率较现有最优方法提升 33.9%

---
