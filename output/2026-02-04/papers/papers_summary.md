# 每日论文汇总 - 2026-02-04

**论文数量**: 9

---

### 🏆 1. WorldVQA：衡量多模态大语言模型的原子级世界知识 (WorldVQA: Measuring Atomic World Knowledge in Multimodal Large Language Models)

**论文链接**: [https://arxiv.org/abs/2602.02537](https://arxiv.org/abs/2602.02537)
**组织**: Moonshot AI
**得分**: 58.96
**标签**: Super Lab, Must Read
**Upvotes**: 5 | **Stars**: 0

**摘要**: 针对当前多模态模型评估中知识检索与推理能力混淆的痛点，Moonshot AI 推出 WorldVQA 基准。该基准通过解耦推理过程，严格衡量模型对视觉实体的“原子级”记忆与命名能力，涵盖从常见到长尾稀有实体的分层体系。研究旨在为视觉事实性提供严谨测试，确立评估前沿模型百科知识广度与幻觉率的新标准。

**亮点**:
  - 提出首个专注于解耦推理、纯粹衡量视觉原子知识的评估基准
  - 构建了涵盖从头部常见类到长尾稀有实体的分层视觉实体分类体系
  - 为评估 MLLM 的视觉幻觉率和百科全书式知识广度建立了新标准

---

###  2. 视觉生成的统一个性化奖励模型 (Unified Personalized Reward Model for Vision Generation)

**论文链接**: [https://arxiv.org/abs/2602.02380](https://arxiv.org/abs/2602.02380)
**组织**: Fudan University
**得分**: 53.78
**标签**: 
**Upvotes**: 15 | **Stars**: 689

**摘要**: 针对现有奖励模型因采用单一评价标准而导致与人类主观偏好失配的问题，复旦大学提出 UnifiedReward-Flex。该模型将奖励建模与灵活的情境自适应推理相结合，通过动态构建分层评估指标捕捉细粒度视觉线索。采用闭源 VLM 知识蒸馏与 DPO 两阶段训练优化。实验表明，将其集成至 GRPO 框架可显著提升图像与视频生成的对齐质量与表现。

**亮点**:
  - 提出 UnifiedReward-Flex 架构实现情境自适应的动态奖励评估
  - 采用从高级闭源 VLM 蒸馏推理链及 DPO 的两阶段训练方案
  - 成功集成至 GRPO 框架并显著提升了图像和视频生成的 SOTA 性能

---

###  3. 思维链中缺乏全局规划：揭示大语言模型的潜在规划视野 (No Global Plan in Chain-of-Thought: Uncover the Latent Planning Horizon of LLMs)

**论文链接**: [https://arxiv.org/abs/2602.02103](https://arxiv.org/abs/2602.02103)
**组织**: Tencent
**得分**: 40.91
**标签**: Frontier Lab
**Upvotes**: 56 | **Stars**: 0

**摘要**: 本研究探讨了大语言模型（LLM）在思维链（CoT）推理过程中的内部规划机制。针对 LLM 是否在生成 CoT 前已具备全局规划的争议，研究者提出 Tele-Lens 探测方法分析隐藏状态。实验表明，LLM 的规划视野具有“近视”性，倾向于增量式状态转换而非全局规划。基于此发现，研究验证了通过少数 CoT 节点即可表征整体路径的不确定性，并实现了在不降低性能的情况下自动识别可跳过 CoT 的推理场景。

**亮点**:
  - 提出 Tele-Lens 探测方法揭示 LLM 的潜在规划强度
  - 发现 LLM 的推理过程具有“近视”特征且缺乏全局规划
  - 验证了通过局部 CoT 位置进行高效不确定性估计的可行性

---

###  4. MARS：基于反思搜索的自动化 AI 研究模块化代理 (MARS: Modular Agent with Reflective Search for Automated AI Research)

**论文链接**: [https://arxiv.org/abs/2602.02660](https://arxiv.org/abs/2602.02660)
**组织**: Google
**得分**: 38.47
**标签**: Frontier Lab
**Upvotes**: 34 | **Stars**: 0

**摘要**: 针对自动化 AI 研究中计算成本高且性能归因难的痛点，Google 提出 MARS 框架。该框架通过基于 MCTS 的预算感知规划平衡执行开销与性能，采用模块化构建流程管理复杂代码，并利用对比反思记忆提取高信号洞察。MARS 在 MLE-Bench 上取得开源框架 SOTA 性能，并展现出显著的跨分支知识迁移能力。

**亮点**:
  - 提出基于成本约束 MCTS 的预算感知规划算法
  - 在 MLE-Bench 基准测试中达到开源框架 SOTA 水平
  - 通过对比反思记忆实现 63% 的跨分支经验有效迁移

---

###  5. 基于人类偏好的 DeepResearch 报告生成：学习特定查询的评价标准 (Learning Query-Specific Rubrics from Human Preferences for DeepResearch Report Generation)

**论文链接**: [https://arxiv.org/abs/2602.03619](https://arxiv.org/abs/2602.03619)
**组织**: Tencent
**得分**: 35.92
**标签**: Frontier Lab
**Upvotes**: 20 | **Stars**: 0

**摘要**: 本文针对 DeepResearch 报告生成中评估信号缺失、现有评价标准（Rubrics）难以兼顾细粒度与可扩展性的痛点，提出了一种训练与人类偏好对齐的特定查询 Rubric 生成器。该方法通过结合人类偏好监督与 LLM 评估的混合奖励强化学习进行优化，并引入多智能体马尔可夫状态（MaMs）工作流以增强长程推理。实验表明，该系统在 DeepResearch Bench 上超越了所有开源基线，性能比肩领先的闭源模型。

**亮点**:
  - 提出首个与人类偏好对齐的特定查询评价标准生成器
  - 引入 MaMs 多智能体马尔可夫状态工作流优化长程推理
  - 性能超越所有开源基线并在 DeepResearch 领域达到 SOTA

---

###  6. 减噪增效：基于指令净化的推理强化学习 (Less Noise, More Voice: Reinforcement Learning for Reasoning via Instruction Purification)

**论文链接**: [https://arxiv.org/abs/2601.21244](https://arxiv.org/abs/2601.21244)
**组织**: BAIDU
**得分**: 33.92
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 0

**摘要**: 针对强化学习（RLVR）在复杂任务中探索效率低和训练不稳定的痛点，百度提出 LENS 框架。该方法通过识别并剔除指令中的干扰令牌进行净化，利用净化后的成功采样指导原始噪声环境下的策略优化。实验证明，LENS 在推理性能上显著优于 GRPO，平均提升 3.88% 且训练速度提升逾 1.6 倍。

**亮点**:
  - 提出 LENS 框架通过指令净化解决 RL 探索效率问题
  - 实现比 GRPO 算法快 1.6 倍以上的收敛速度
  - 开辟了通过剪枝干扰令牌提升强化学习探索效率的新路径

---

###  7. daVinci-Agency：利用软件演进数据解锁高效长程智能体能力 (daVinci-Agency: Unlocking Long-Horizon Agency Data-Efficiently)

**论文链接**: [https://arxiv.org/abs/2602.02619](https://arxiv.org/abs/2602.02619)
**组织**: SII - GAIR
**得分**: 33.52
**标签**: 
**Upvotes**: 39 | **Stars**: 10

**摘要**: 针对大语言模型在处理长程智能体任务时面临的高质量数据稀缺及复杂依赖建模难点，本文提出 daVinci-Agency。该框架创新性地将 GitHub 的 Pull Request (PR) 序列转化为监督信号，通过连续提交实现任务分解，并利用真实的 Bug 修复轨迹进行可验证的性能优化。实验显示，仅需 239 个 PR 样本进行微调，即可使 GLM-4.6 在 Toolathlon 基准上实现 47% 的性能提升，显著增强了模型在复杂软件工程场景下的长程目标导向能力。

**亮点**:
  - 提出基于 Pull Request 序列挖掘真实长程监督信号的新范式
  - 实现极高的数据效率，仅需 239 个样本即可显著提升模型性能
  - 生成包含平均 8.5 万 token 的超长复杂任务轨迹，有效捕捉因果依赖

---

###  8. 面向快速视觉合成的保持多样性分布匹配蒸馏 (Diversity-Preserved Distribution Matching Distillation for Fast Visual Synthesis)

**论文链接**: [https://arxiv.org/abs/2602.03139](https://arxiv.org/abs/2602.03139)
**组织**: City University of Hong Kong
**得分**: 32.24
**标签**: 
**Upvotes**: 31 | **Stars**: 9

**摘要**: 针对分布匹配蒸馏（DMD）在少步生成任务中因其 reverse-KL 形式导致模式崩溃（Mode Collapse）的问题，本文提出 DP-DMD 框架。该方法通过角色分离蒸馏策略，在首步利用目标预测（如 v-prediction）来保持样本多样性，后续步骤则专注于标准 DMD 损失下的质量精炼。在无需判别器或辅助网络的情况下，DP-DMD 实现了与 SOTA 相当的视觉质量并有效保留了图像多样性。

**亮点**:
  - 提出角色分离蒸馏框架 (Role-separated distillation)
  - 有效缓解 DMD 蒸馏中的模式崩溃问题
  - 无需感知损失或判别器的极简高效架构

---

###  9. Search-R2：通过 Actor-Refiner 协作增强搜索集成推理 (Search-R2: Enhancing Search-Integrated Reasoning via Actor-Refiner Collaboration)

**论文链接**: [https://arxiv.org/abs/2602.03647](https://arxiv.org/abs/2602.03647)
**组织**: Tencent Hunyuan
**得分**: 28.74
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 0

**摘要**: 针对搜索集成推理中强化学习面临的信度分配难题，腾讯混元团队提出 Search-R2 框架。该框架采用 Actor-Refiner 协作机制，由 Actor 生成初始推理路径，Meta-Refiner 通过“剪枝与重生成”机制对错误步骤进行针对性修复。结合结果正确性与量化检索信息密度的密集过程奖励，该方法在多跳问答任务中显著优于现有 RAG 和 RL 基线，实现了更高效的推理性能。

**亮点**:
  - 提出 Actor-Refiner 协作框架实现针对性推理干预
  - 引入量化检索信息密度的密集过程奖励解决信度分配难题
  - 在多跳问答实验中一致优于强 RAG 和 RL 基准

---
