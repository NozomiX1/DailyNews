# 每日论文汇总 - 2026-02-18

**论文数量**: 8

---

###  1. GLM-5：从氛围编码迈向智能体工程 (GLM-5: from Vibe Coding to Agentic Engineering)

**论文链接**: [https://arxiv.org/abs/2602.15763](https://arxiv.org/abs/2602.15763)
**组织**: Unknown
**得分**: 62.99
**标签**: 
**Upvotes**: 47 | **Stars**: 1142

**摘要**: 针对从简易编程向复杂智能体工程转型的需求，GLM-5采用DSA架构降低成本并保持长上下文保真度。该模型引入异步强化学习基础设施及算法，解耦生成与训练，显著提升长视距交互学习能力。实验表明，GLM-5在开源基准达SOTA，且在端到端软件工程任务中表现卓越。

**亮点**:
  - 主流开源基准达到SOTA性能
  - 提出异步RL基础设施与算法
  - 突破端到端软件工程实战能力

---

###  2. SkillsBench：跨多样化任务基准测试 Agent Skills 的有效性 (SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks)

**论文链接**: [https://arxiv.org/abs/2602.12670](https://arxiv.org/abs/2602.12670)
**组织**: BenchFlow
**得分**: 56.83
**标签**: 
**Upvotes**: 43 | **Stars**: 423

**摘要**: 针对现有 Agent Skills 缺乏标准化评估的问题，提出 SkillsBench 基准，涵盖 11 个领域的 86 项任务。实验对比了无技能、精选技能和自生成技能，发现精选技能平均提升 16.2% 通过率，但自生成技能无效；精简技能优于长文档，且小模型配合技能可媲美大模型。

**亮点**:
  - 推出 SkillsBench 基准以评估 Agent Skills 有效性
  - 发现自生成技能无效，仅精选技能显著提升性能
  - 证实小模型配合精简技能可媲美大模型

---

###  3. 关于自适应优化器中掩码更新出奇的有效性 (On Surprising Effectiveness of Masking Updates in Adaptive Optimizers)

**论文链接**: [https://arxiv.org/abs/2602.15322](https://arxiv.org/abs/2602.15322)
**组织**: Google
**得分**: 31.5
**标签**: Frontier Lab
**Upvotes**: 7 | **Stars**: 0

**摘要**: 针对LLM训练依赖复杂优化器的问题，本文发现随机掩码参数更新非常有效，并提出了基于动量-梯度对齐掩码的Magma优化器。实验表明，Magma在1B模型预训练中困惑度较Adam降低超19%，且计算开销极低。

**亮点**:
  - 提出随机掩码参数更新机制，诱导几何正则化
  - 设计Magma优化器，利用动量对齐调节更新
  - 1B模型预训练性能显著优于Adam和Muon

---

###  4. 社交化是否在 AI 智能体社会中涌现？Moltbook 案例研究 (Does Socialization Emerge in AI Agent Society? A Case Study of Moltbook)

**论文链接**: [https://arxiv.org/abs/2602.14299](https://arxiv.org/abs/2602.14299)
**组织**: Tianyi Lab
**得分**: 30.18
**标签**: 
**Upvotes**: 24 | **Stars**: 7

**摘要**: 针对AI智能体社会是否涌现社交化的问题，本文以Moltbook为案例，引入量化诊断框架分析动态演化。研究发现系统虽处于动态平衡，但因高个体惯性和缺乏共享记忆，智能体间无法形成共识，证明仅靠规模不足诱导社交化。

**亮点**:
  - 提出 AI 智能体动态演化量化诊断框架
  - 揭示个体惯性与缺乏共享记忆阻碍社交化
  - 基于 Moltbook 的大规模系统性诊断

---

###  5. Causal-JEPA：通过对象级潜在干预学习世界模型 (Causal-JEPA: Learning World Models through Object-Level Latent Interventions)

**论文链接**: [https://arxiv.org/abs/2602.11389](https://arxiv.org/abs/2602.11389)
**组织**: Brown University
**得分**: 29.35
**标签**: 
**Upvotes**: 4 | **Stars**: 28

**摘要**: 针对现有世界模型难以捕捉交互依赖动态的问题，本文提出了C-JEPA架构。该方法将掩码联合嵌入预测扩展至对象级表示，通过对象掩码强制模型基于其他物体推断状态，从而引入因果归纳偏置。实验显示，C-JEPA在反事实推理任务上准确率提升约20%，且在控制任务中仅需1%的潜在特征即可达到与基于块模型相当的性能。

**亮点**:
  - 提出基于对象级掩码的C-JEPA世界模型
  - 反事实推理性能绝对提升约20%
  - 规划效率显著提升，仅需1%潜在特征

---

###  6. ResearchGym：在真实世界 AI 研究中评估语言模型智能体 (ResearchGym: Evaluating Language Model Agents on Real-World AI Research)

**论文链接**: [https://arxiv.org/abs/2602.15112](https://arxiv.org/abs/2602.15112)
**组织**: Unknown
**得分**: 27.45
**标签**: 
**Upvotes**: 16 | **Stars**: 6

**摘要**: 针对评估智能体端到端研究能力的痛点，提出 ResearchGym 基准。该平台基于顶会论文构建 39 个子任务，要求智能体自主提出假设并实验。实验显示，即使是最先进的 GPT-5 也存在明显的能力-可靠性差距，虽偶有超越 SOTA 的表现，但整体完成率仅 26.5%，且存在资源管理不善等长视界失败模式。

**亮点**:
  - 提出真实世界端到端 AI 研究评估基准 ResearchGym
  - 揭示 GPT-5 等前沿模型存在显著的能力-可靠性差距
  - 验证了智能体在特定单次运行中可达 SOTA 性能

---

###  7. 重访柏拉图表征假设：亚里士多德视角 (Revisiting the Platonic Representation Hypothesis: An Aristotelian View)

**论文链接**: [https://arxiv.org/abs/2602.14486](https://arxiv.org/abs/2602.14486)
**组织**: Unknown
**得分**: 27.0
**标签**: 
**Upvotes**: 9 | **Stars**: 10

**摘要**: 针对现有表征相似性度量受网络规模混淆的问题，提出基于排列的零假设校准框架。研究发现校准后全局谱测度的表象收敛消失，但局部邻域相似性仍保持显著一致性，据此提出神经网络表征收敛于共享局部邻域关系的“亚里士多德表征假设”。

**亮点**:
  - 提出基于排列的零假设校准框架
  - 修正了现有度量对网络规模的混淆
  - 提出亚里士多德表征假设

---

###  8. 用于一致性视频世界模型的几何感知旋转位置嵌入 (Geometry-Aware Rotary Position Embedding for Consistent Video World Model)

**论文链接**: [https://arxiv.org/abs/2602.07854](https://arxiv.org/abs/2602.07854)
**组织**: Tsinghua University
**得分**: 26.59
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 0

**摘要**: 针对现有视频世界模型缺乏空间持久性及重访场景时易产生幻觉的问题，本文提出 ViewRope。这是一种将相机光线方向直接注入自注意力层的几何感知编码，利用相对光线几何而非像素局部性来维持 3D 一致性。此外，结合几何感知帧稀疏注意力，该方法在降低计算成本的同时显著提升了长期场景稳定性。

**亮点**:
  - 提出 ViewRope 几何感知编码机制
  - 解决视频世界模型的空间一致性问题
  - 引入 ViewBench 基准并提升计算效率

---
