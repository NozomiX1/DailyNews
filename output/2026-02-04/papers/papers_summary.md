# 每日论文汇总 - 2026-02-04

**论文数量**: 12

---

### 🏆 1. WorldVQA：衡量多模态大模型的原子级世界知识 (WorldVQA: Measuring Atomic World Knowledge in Multimodal Large Language Models)

**论文链接**: [https://arxiv.org/abs/2602.02537](https://arxiv.org/abs/2602.02537)
**组织**: Moonshot AI
**得分**: 59.65
**标签**: Super Lab, Must Read
**Upvotes**: 5 | **Stars**: 0

**摘要**: 针对现有基准测试常将视觉知识检索与推理混淆的问题，Moonshot AI 推出 WorldVQA 评估基准。该基准通过将推理能力解耦，旨在严格衡量模型对视觉实体的“记忆”与命名能力。其包含从高频到长尾实体的分层分类体系，为评估多模态大模型的百科知识广度、视觉事实性及幻觉率建立了全新的严苛标准。

**亮点**:
  - 首个解耦推理、专注于原子级视觉知识的基准测试
  - 覆盖从头部到长尾实体的分层视觉百科体系
  - 为评估前沿模型幻觉率与知识边界提供新标准

---

###  2. 面向视觉生成的统一个性化奖励模型 (Unified Personalized Reward Model for Vision Generation)

**论文链接**: [https://arxiv.org/abs/2602.02380](https://arxiv.org/abs/2602.02380)
**组织**: Fudan University
**得分**: 54.8
**标签**: 
**Upvotes**: 17 | **Stars**: 692

**摘要**: 针对现有奖励模型采用单一偏好分布且对上下文不敏感的痛点，复旦大学提出 UnifiedReward-Flex。该模型将奖励建模与灵活的自适应推理相结合，通过动态构建细粒度评估准则来解析语义意图。采用从闭源 VLM 蒸馏推理轨迹（SFT）与直接偏好优化（DPO）的两阶段训练流程。实验表明，将其集成至 GRPO 框架能显著提升图像与视频生成的质量及人类偏好一致性。

**亮点**:
  - 提出 UnifiedReward-Flex 架构实现上下文自适应的奖励建模
  - 结合推理轨迹蒸馏与 DPO 的创新两阶段训练管线
  - 显著提升图像与视频生成模型在复杂场景下的对齐性能

---

###  3. MARS：基于反思搜索的模块化自动化 AI 研究智能体 (MARS: Modular Agent with Reflective Search for Automated AI Research)

**论文链接**: [https://arxiv.org/abs/2602.02660](https://arxiv.org/abs/2602.02660)
**组织**: Google
**得分**: 53.23
**标签**: Frontier Lab
**Upvotes**: 53 | **Stars**: 6

**摘要**: 针对自动化AI研究中评估成本高、归因难的挑战，Google提出MARS框架。该框架集成预算感知的MCTS搜索规划、模块化构建流水线及对比反思记忆机制，有效平衡了执行成本与性能。实验表明，MARS在MLE-Bench基准测试中取得开源框架SOTA性能，并展现出卓越的跨路径洞察泛化能力。

**亮点**:
  - 提出基于成本约束 MCTS 的预算感知规划机制
  - 采用“设计-分解-实现”模块化架构处理复杂研究任务
  - 在 MLE-Bench 榜单的开源框架中取得 SOTA 性能

---

###  4. LIVE：长时程交互式视频世界建模 (LIVE: Long-horizon Interactive Video World Modeling)

**论文链接**: [https://arxiv.org/abs/2602.03747](https://arxiv.org/abs/2602.03747)
**组织**: Microsoft Research
**得分**: 47.11
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 8

**摘要**: 针对自回归视频世界模型在长时程生成中误差累积的痛点，微软研究院提出 LIVE 模型。该方法通过创新的循环一致性（Cycle-consistency）目标函数，执行“前向推演-逆向重构”过程并计算扩散损失，从而显式约束误差传播，无需高成本的教师模型蒸馏。实验证明 LIVE 在长时程基准上达到 SOTA 性能，能生成远超训练长度的稳定高质量视频。

**亮点**:
  - 提出基于循环一致性的误差约束机制
  - 消除对教师模型蒸馏的依赖，降低计算成本
  - 实现长时程视频生成的 SOTA 性能

---

###  5. 面向快速视觉合成的保持多样性的分布匹配蒸馏 (Diversity-Preserved Distribution Matching Distillation for Fast Visual Synthesis)

**论文链接**: [https://arxiv.org/abs/2602.03139](https://arxiv.org/abs/2602.03139)
**组织**: City University of Hong Kong
**得分**: 42.91
**标签**: 
**Upvotes**: 36 | **Stars**: 49

**摘要**: 针对分布匹配蒸馏（DMD）因逆KL散度公式易导致模式崩溃的问题，本文提出了DP-DMD框架。该方法通过角色分离蒸馏策略，在首步采用目标预测目标（如v-prediction）以保持样本多样性，后续步骤则专注于DMD损失下的质量精炼。在无需感知网络、判别器或额外图像的情况下，该方法在文生图任务中实现了与SOTA相当的视觉质量并有效解决了多样性缺失问题。

**亮点**:
  - 提出角色分离的蒸馏框架 DP-DMD
  - 无需感知网络或判别器即可解决 DMD 的模式崩溃问题
  - 在保持生成多样性的同时达到 SOTA 级别的视觉性能

---

###  6. 思维链中不存在全局规划：揭示大语言模型的潜伏规划视野 (No Global Plan in Chain-of-Thought: Uncover the Latent Planning Horizon of LLMs)

**论文链接**: [https://arxiv.org/abs/2602.02103](https://arxiv.org/abs/2602.02103)
**组织**: Tencent
**得分**: 41.81
**标签**: Frontier Lab
**Upvotes**: 62 | **Stars**: 0

**摘要**: 本研究利用提出的 Tele-Lens 探针方法，深入分析了 LLM 在思维链（CoT）推理过程中的隐藏状态。研究发现模型在生成过程中表现出“近视视野”，即倾向于逐步的增量转换而非精确的全局规划。基于此发现，研究提出并验证了仅需少量 CoT 节点即可表征全路径不确定性的假设，并实现了在不损失性能的情况下自动识别并绕过冗余推理路径。

**亮点**:
  - 揭示了 LLM 在 CoT 推理中仅具备“近视”的局部规划能力而非全局规划
  - 提出 Tele-Lens 探针方法，通过隐藏状态量化模型的潜伏规划强度
  - 利用局部特征优化了 CoT 的不确定性估计，并实现高效的 CoT 路径旁路识别

---

###  7. daVinci-Agency：通过高效数据挖掘解锁长程智能体能力 (daVinci-Agency: Unlocking Long-Horizon Agency Data-Efficiently)

**论文链接**: [https://arxiv.org/abs/2602.02619](https://arxiv.org/abs/2602.02619)
**组织**: SII - GAIR
**得分**: 40.24
**标签**: 
**Upvotes**: 45 | **Stars**: 27

**摘要**: 针对大语言模型在长程任务中因高质量数据稀缺导致的能力瓶颈，本文提出 daVinci-Agency 框架。该方法创新性地利用软件工程中的 PR 序列构建结构化监督信号，通过任务分解、一致性维护和 Bug 修复轨迹模拟真实的软件演进。实验显示，仅需 239 条高质量样本即可显著提升模型性能，在 Toolathlon 基准测试中实现 47% 的相对增益。

**亮点**:
  - 创新性利用 Pull Request (PR) 序列作为长程监督信号
  - 极高的数据效率，仅需 239 个样本即可显著提升性能
  - 有效捕捉复杂任务中的因果依赖与迭代优化逻辑

---

###  8. 基于人类偏好学习特定查询评分标准的 DeepResearch 报告生成 (Learning Query-Specific Rubrics from Human Preferences for DeepResearch Report Generation)

**论文链接**: [https://arxiv.org/abs/2602.03619](https://arxiv.org/abs/2602.03619)
**组织**: Tencent
**得分**: 36.99
**标签**: Frontier Lab
**Upvotes**: 23 | **Stars**: 0

**摘要**: 针对深度研究报告生成中评价指标缺乏可验证性且人工评分难以扩展的痛点，腾讯团队提出了一种学习人类偏好且针对特定查询的评分标准生成流水线。该方法通过强化学习与混合奖励机制训练生成器，并引入多智能体马尔可夫状态（MaMs）工作流以增强长程推理能力。实验证明，该方法在 DeepResearch Bench 上优于所有开源基准，性能可比肩顶尖闭源模型。

**亮点**:
  - 提出首个与人类偏好对齐的特定查询评分标准生成器
  - 引入 MaMs 多智能体工作流解决长程推理报告生成难题
  - 性能在 DeepResearch Bench 上达到与领先闭源模型相当的水平

---

###  9. Privasis：从零构建最大规模的“公开”私有合成数据集 (Privasis: Synthesizing the Largest "Public" Private Dataset from Scratch)

**论文链接**: [https://arxiv.org/abs/2602.03183](https://arxiv.org/abs/2602.03183)
**组织**: NVIDIA
**得分**: 35.74
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 2

**摘要**: 针对AI智能体处理敏感数据时面临的隐私数据稀缺挑战，NVIDIA发布了Privasis，这是首个百万级全合成隐私数据集。该库包含140万条跨领域的多元化记录及5510万个标注属性。实验表明，基于此训练的4B轻量级脱敏模型在性能上超越了GPT-5等SOTA大模型，有效推动了隐私敏感领域的学术研究与模型应用。

**亮点**:
  - 发布首个百万级（1.4M记录）全合成隐私敏感数据集
  - 覆盖医疗、法律、财务等极具多样性的5510万个隐私属性标注
  - 轻量化脱敏模型（<=4B）性能超越 GPT-5 等顶级大语言模型

---

###  10. 降噪增声：通过指令净化实现推理的强化学习 (Less Noise, More Voice: Reinforcement Learning for Reasoning via Instruction Purification)

**论文链接**: [https://arxiv.org/abs/2601.21244](https://arxiv.org/abs/2601.21244)
**组织**: BAIDU
**得分**: 34.21
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 0

**摘要**: 针对 LLM 推理在强化学习（RLVR）中因提示词干扰导致探索效率低下的问题，百度提出了 LENS 框架。该方法通过识别并移除干扰 Token 进行指令净化，并利用净化后的成功样本引导原始噪声提示词下的策略优化。实验表明，LENS 在性能和收敛速度上均显著优于 GRPO，平均性能提升 3.88% 且加速 1.6 倍以上，为提升 RLVR 采样效率提供了新视角。

**亮点**:
  - 提出 LENS 框架通过指令净化显著提升 RL 探索效率
  - 实验性能超越 GRPO，实现 3.88% 的平均准确率增益
  - 训练收敛速度提升 1.6 倍以上，有效解决复杂任务采样难题

---

###  11. Parallel-Probe：通过二维探测实现高效的并行推理 (Parallel-Probe: Towards Efficient Parallel Thinking via 2D Probing)

**论文链接**: [https://arxiv.org/abs/2602.03845](https://arxiv.org/abs/2602.03845)
**组织**: University of Maryland College Park
**得分**: 31.66
**标签**: 
**Upvotes**: 23 | **Stars**: 10

**摘要**: 针对并行推理计算成本高昂且缺乏跨分支全局动态优化机制的问题，本文提出 2D probing 接口以分析推理过程中的宽深动态。研究发现推理共识具有早期稳定性且分支长度存在异构性，据此设计了无需训练的控制器 Parallel-Probe。该工具通过共识提前停止和偏差分支剪枝动态调节推理规模，在保持竞争力的准确率下，将总 Token 成本降低了 25.8% 以上。

**亮点**:
  - 提出 2D probing 接口揭示并行推理的宽深动态规律
  - 设计无需训练的 Parallel-Probe 控制器实现推理过程的动态剪枝
  - 在多个模型和基准测试中建立了更优的测试时缩放 Pareto 前沿

---

###  12. Search-R2：通过 Actor-Refiner 协同增强搜索集成推理能力 (Search-R2: Enhancing Search-Integrated Reasoning via Actor-Refiner Collaboration)

**论文链接**: [https://arxiv.org/abs/2602.03647](https://arxiv.org/abs/2602.03647)
**组织**: Tencent Hunyuan
**得分**: 30.83
**标签**: Frontier Lab
**Upvotes**: 6 | **Stars**: 0

**摘要**: 针对搜索集成推理中强化学习面临的信用分配难题，腾讯混元团队提出了 Search-R2 框架。该框架通过 Actor 生成初始推理轨迹，并由 Meta-Refiner 采用“剪枝与重生成”机制精准诊断并修复错误步骤。结合结果正确性与信息密度过程奖励的混合设计，Search-R2 在多项问答任务中显著超越了现有 RAG 与 RL 基准，实现了高精度且低开销的推理表现。

**亮点**:
  - 提出 Actor-Refiner 协作机制，通过针对性干预优化推理路径
  - 引入“剪枝与重生成”机制，实现细粒度的步骤级错误诊断与修复
  - 设计结合信息密度的混合奖励函数，解决强化学习中的信用分配问题

---
