# 每日论文汇总 - 2026-02-04

**论文数量**: 10

---

### 🏆 1. WorldVQA：衡量多模态大语言模型的原子级世界知识 (WorldVQA: Measuring Atomic World Knowledge in Multimodal Large Language Models)

**论文链接**: [https://arxiv.org/abs/2602.02537](https://arxiv.org/abs/2602.02537)
**组织**: Moonshot AI
**得分**: 58.96
**标签**: Super Lab, Must Read
**Upvotes**: 5 | **Stars**: 0

**摘要**: 针对当前多模态大模型（MLLM）评估中视觉知识检索与逻辑推理能力混淆的问题，Moonshot AI 提出 WorldVQA 基准。该基准通过解耦推理与检索，专注于衡量模型对视觉实体的“原子级记忆”能力。WorldVQA 采用分层分类体系，涵盖从头部常见物体到长尾稀有实体的定位与命名。实验表明，该基准能有效作为视觉事实性的严苛测试，为评估前沿模型的百科知识广度与幻觉率建立新标准。

**亮点**:
  - 提出首个专注于原子级视觉知识检索的解耦评估基准
  - 构建了涵盖常见到长尾实体的分层视觉实体分类体系
  - 为评估多模态模型的视觉事实性与幻觉率提供严苛标准

---

###  2. 面向视觉生成的统一个性化奖励模型 (Unified Personalized Reward Model for Vision Generation)

**论文链接**: [https://arxiv.org/abs/2602.02380](https://arxiv.org/abs/2602.02380)
**组织**: Fudan University
**得分**: 53.76
**标签**: 
**Upvotes**: 15 | **Stars**: 687

**摘要**: 针对现有奖励模型因采用固定评估准则而无法适配主观、语境相关人类偏好的痛点，复旦大学提出 UnifiedReward-Flex。该模型将奖励建模与语境自适应推理相结合，通过动态构建分层评估标准来解读语义意图并锚定视觉证据。经两阶段训练（VLM 蒸馏 SFT 与 DPO）并集成至 GRPO 框架，在图像与视频合成任务中显著提升了偏好对齐性能与生成质量。

**亮点**:
  - 提出支持语境自适应推理的统一个性化奖励模型 UnifiedReward-Flex
  - 采用闭源 VLM 知识蒸馏与 DPO 结合的两阶段优化策略
  - 在图像与视频生成任务中实现了更精准的人类偏好对齐性能

---

###  3. 思维链中缺乏全局规划：揭示大语言模型的潜在规划视野 (No Global Plan in Chain-of-Thought: Uncover the Latent Planning Horizon of LLMs)

**论文链接**: [https://arxiv.org/abs/2602.02103](https://arxiv.org/abs/2602.02103)
**组织**: Tencent
**得分**: 40.15
**标签**: Frontier Lab
**Upvotes**: 48 | **Stars**: 0

**摘要**: 本文针对大语言模型（LLM）在思维链（CoT）推理中内部状态与表述轨迹的关系展开研究。通过提出的 Tele-Lens 探测方法，研究者发现 LLM 在推理过程中表现出“近视”特征，即主要进行增量式转换，而非精确的全局规划。基于此发现，研究验证了利用少量 CoT 位置即可实现有效的不确定性估计，并证明自动识别 CoT 旁路可在不损失性能的前提下优化推理效率。

**亮点**:
  - 提出 Tele-Lens 探测方法，揭示了 LLM 内部的潜在规划强度
  - 发现 LLM 在 CoT 推理中仅具备局部“近视”视野，缺乏全局规划能力
  - 通过 CoT 关键位置实现了高效的不确定性估计和推理旁路识别

---

###  4. MARS：基于反思搜索的模块化自动 AI 研究智能体 (MARS: Modular Agent with Reflective Search for Automated AI Research)

**论文链接**: [https://arxiv.org/abs/2602.02660](https://arxiv.org/abs/2602.02660)
**组织**: Google
**得分**: 38.32
**标签**: Frontier Lab
**Upvotes**: 33 | **Stars**: 0

**摘要**: 针对自动 AI 研究中计算成本高昂和性能归因模糊的挑战，谷歌提出 MARS 框架。该框架结合受成本约束的蒙特卡洛树搜索（MCTS）进行预算感知规划，采用“设计-分解-实现”流水线进行模块化构建，并通过比较反思记忆提取高信号见解。MARS 在 MLE-Bench 上达到开源框架 SOTA 水平，并展现出显著的跨分支知识迁移与泛化能力。

**亮点**:
  - 提出受成本约束的蒙特卡洛树搜索 (MCTS) 规划机制
  - 在 MLE-Bench 基准测试中取得开源框架 SOTA 性能
  - 实现 63% 的跨分支知识迁移，展现“顿悟”式泛化能力

---

###  5. 从人类偏好中学习特定查询的评估标准以优化深度调研报告生成 (Learning Query-Specific Rubrics from Human Preferences for DeepResearch Report Generation)

**论文链接**: [https://arxiv.org/abs/2602.03619](https://arxiv.org/abs/2602.03619)
**组织**: Tencent
**得分**: 35.92
**标签**: Frontier Lab
**Upvotes**: 20 | **Stars**: 0

**摘要**: 针对深度调研报告生成中缺乏可验证奖励信号及评估标准颗粒度不足的问题，腾讯团队提出了一套训练与人类偏好对齐的特定查询评估标准（Rubric）生成器的流程。该方法结合人类偏好监督与强化学习，并引入多智能体马尔可夫状态（MaMs）工作流以增强长程推理。实验证明，该方法生成的标准更具区分度，在 DeepResearch Bench 上超越了所有开源基准并比肩领先闭源模型。

**亮点**:
  - 提出首个自动生成人类偏好对齐的特定查询评估标准（Rubric）框架
  - 引入 MaMs 多智能体马尔可夫状态工作流以优化长程推理报告生成
  - 性能在 DeepResearch Bench 上达到 SOTA 级别，显著超越开源基准

---

###  6. 减噪增声：通过指令净化实现推理强化学习 (Less Noise, More Voice: Reinforcement Learning for Reasoning via Instruction Purification)

**论文链接**: [https://arxiv.org/abs/2601.21244](https://arxiv.org/abs/2601.21244)
**组织**: BAIDU
**得分**: 33.92
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 0

**摘要**: 针对强化学习（RLVR）在复杂任务中因提示词干扰导致探索效率低、训练不稳的痛点，百度提出 LENS 框架。该方法先通过识别并剔除干扰 token 进行指令净化，再将净化后的成功采样经验迁移至原始带噪提示词的策略优化中。实验表明，LENS 在性能和收敛速度上显著优于 GRPO，平均提升 3.88% 且加速 1.6 倍以上。

**亮点**:
  - 提出 LENS 采样框架，有效解决提示词干扰导致的探索失败
  - 引入指令净化（Instruction Purification）技术提升采样效率
  - 相比 GRPO 实现 1.6 倍以上的训练加速和显著的性能提升

---

###  7. daVinci-Agency：通过 Pull Request 序列高效解锁长程智能体能力 (daVinci-Agency: Unlocking Long-Horizon Agency Data-Efficiently)

**论文链接**: [https://arxiv.org/abs/2602.02619](https://arxiv.org/abs/2602.02619)
**组织**: SII - GAIR
**得分**: 33.4
**标签**: 
**Upvotes**: 38 | **Stars**: 10

**摘要**: 针对大语言模型在长程智能体任务中面临的高质量训练数据稀缺问题，本文提出 daVinci-Agency。该方法利用软件开发中的 Pull Request (PR) 序列作为监督信号，通过任务分解、长期一致性维护及可验证的修复轨迹构建复杂数据。实验证明，仅用 239 个样本微调 GLM-4.6 即可在 Toolathlon 榜单取得 47% 的相对性能提升，显著提升了长程数据的获取效率。

**亮点**:
  - 创新性地利用 PR 序列作为真实长程轨迹的自动监督来源
  - 生成包含超 8.5 万 token 和 116 次工具调用的高质量超长轨迹
  - 展现出极高的数据效率，微调少量样本即可大幅提升模型性能

---

###  8. 保留多样性的分布匹配蒸馏：实现快速视觉合成 (Diversity-Preserved Distribution Matching Distillation for Fast Visual Synthesis)

**论文链接**: [https://arxiv.org/abs/2602.03139](https://arxiv.org/abs/2602.03139)
**组织**: City University of Hong Kong
**得分**: 32.08
**标签**: 
**Upvotes**: 30 | **Stars**: 9

**摘要**: 针对分布匹配蒸馏（DMD）因反向 KL 散度导致模式崩塌的痛点，本文提出 DP-DMD 角色分离蒸馏框架。该方法将蒸馏步骤解耦：首步通过 v-prediction 目标保留样本多样性，后续步骤利用标准 DMD 损失进行质量精炼。DP-DMD 无需判别器或感知骨干，在极低计算开销下实现了与 SOTA 相当的文生图效果。

**亮点**:
  - 提出角色分离的蒸馏框架 DP-DMD
  - 无需感知损失或判别器即可解决模式崩塌
  - 在保持生成多样性的同时达到 SOTA 视觉质量

---

###  9. 针对泛癌症筛查的扫视与聚焦强化学习框架 (Glance and Focus Reinforcement for Pan-cancer Screening)

**论文链接**: [https://arxiv.org/abs/2601.19103](https://arxiv.org/abs/2601.19103)
**组织**: The Hong Kong University of Science and Technology
**得分**: 28.05
**标签**: 
**Upvotes**: 4 | **Stars**: 24

**摘要**: 针对大规模CT泛癌症筛查中微小病灶定位难和前景背景极度失衡的挑战，本文提出GF-Screen强化学习框架。该框架效仿医生的“扫视与聚焦”策略，利用Glance模型初步定位并由Focus模型精确分割，通过强化学习机制实现非微分操作的优化。引入组相对学习范式提升了检测效率并降低假阳性。在FLARE25挑战赛中位居榜首，性能显著超越上届冠军。

**亮点**:
  - 提出仿生放射科医生诊断策略的GF-Screen强化学习架构
  - 引入组相对学习范式（Group Relative Learning）显著降低假阳性
  - 在MICCAI FLARE25泛癌症挑战赛中性能大幅超越上届冠军

---

###  10. Search-R2：通过 Actor-Refiner 协作增强搜索集成推理 (Search-R2: Enhancing Search-Integrated Reasoning via Actor-Refiner Collaboration)

**论文链接**: [https://arxiv.org/abs/2602.03647](https://arxiv.org/abs/2602.03647)
**组织**: Tencent Hunyuan
**得分**: 27.62
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 针对搜索集成推理在强化学习中面临的多尺度信用分配及奖励稀疏问题，腾讯混元提出 Search-R2 框架。该框架采用 Actor 生成初始轨迹、Meta-Refiner 执行“剪枝再生成”诊断修复的协作机制。通过结合结果正确性与信息密度的混合奖励设计，Search-R2 在多跳问答任务中显著超越了传统 RAG 和 RL 基线，以极低开销实现了卓越的推理准确性。

**亮点**:
  - 提出 Actor-Refiner 协同优化的搜索推理框架
  - 引入“剪枝再生成”机制实现细粒度错误修复
  - 设计量化信息密度的混合过程奖励函数

---
