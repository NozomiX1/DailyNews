# 每日论文汇总 - 2026-02-18

**论文数量**: 8

---

###  1. GLM-5：从直觉编程走向智能体工程 (GLM-5: from Vibe Coding to Agentic Engineering)

**论文链接**: [https://arxiv.org/abs/2602.15763](https://arxiv.org/abs/2602.15763)
**组织**: Unknown
**得分**: 63.29
**标签**: 
**Upvotes**: 50 | **Stars**: 1142

**摘要**: GLM-5旨在推动从直觉编程向智能体工程转型。通过采用DSA架构和异步强化学习算法，该模型显著降低了训练与推理成本。GLM-5在开源基准中取得SOTA性能，并在真实编程任务中超越基线，展现出强大的端到端工程能力。

**亮点**:
  - 主要开源基准测试达到 SOTA 性能
  - 提出异步强化学习基础设施及 DSA 架构
  - 在真实端到端软件工程任务中表现卓越

---

###  2. SkillsBench：评估 Agent 技能跨多样任务有效性的基准 (SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks)

**论文链接**: [https://arxiv.org/abs/2602.12670](https://arxiv.org/abs/2602.12670)
**组织**: BenchFlow
**得分**: 56.94
**标签**: 
**Upvotes**: 44 | **Stars**: 423

**摘要**: 针对缺乏评估 Agent 技能有效性的标准，提出了 SkillsBench 基准，涵盖 11 个领域的 86 个任务。实验发现，精选技能使平均通过率提升 16.2%，但模型自生成技能无效；小模型配合技能可匹敌大模型。

**亮点**:
  - 提出 SkillsBench 基准
  - 精选技能显著提升但领域差异大
  - 小模型加技能匹敌大模型

---

###  3. 探究自适应优化器中掩码更新机制的惊人有效性 (On Surprising Effectiveness of Masking Updates in Adaptive Optimizers)

**论文链接**: [https://arxiv.org/abs/2602.15322](https://arxiv.org/abs/2602.15322)
**组织**: Google
**得分**: 31.5
**标签**: Frontier Lab
**Upvotes**: 7 | **Stars**: 0

**摘要**: 针对LLM训练依赖密集自适应优化器的痛点，本文提出基于动量对齐的梯度掩码方法Magma。该方法通过随机掩码引入几何正则化，在LLM预训练中超越Adam和Muon，显著降低困惑度且计算开销极低。

**亮点**:
  - 超越现有SOTA优化器的性能
  - 提出Magma（动量对齐梯度掩码）架构
  - 1B模型困惑度较Adam降低19%

---

###  4. AI 智能体社会中是否会出现社会化？——基于 Moltbook 的案例研究 (Does Socialization Emerge in AI Agent Society? A Case Study of Moltbook)

**论文链接**: [https://arxiv.org/abs/2602.14299](https://arxiv.org/abs/2602.14299)
**组织**: Tianyi Lab
**得分**: 30.18
**标签**: 
**Upvotes**: 24 | **Stars**: 7

**摘要**: 针对AI智能体社会演化问题，该研究对Moltbook平台进行了大规模系统性诊断，提出包含语义稳定性和个体惯性的动态量化框架。研究发现尽管全局语义趋稳，但强个体惯性和缺乏共享记忆阻碍了共识形成，表明仅靠规模无法诱导社会化。

**亮点**:
  - 提出AI智能体社会动态演化量化框架
  - 揭示Moltbook系统处于动态平衡状态
  - 证明规模与交互密度不足以引发社会化

---

###  5. Causal-JEPA：通过对象级潜在干预学习世界模型 (Causal-JEPA: Learning World Models through Object-Level Latent Interventions)

**论文链接**: [https://arxiv.org/abs/2602.11389](https://arxiv.org/abs/2602.11389)
**组织**: Brown University
**得分**: 29.35
**标签**: 
**Upvotes**: 4 | **Stars**: 28

**摘要**: 针对现有世界模型难以捕捉依赖交互的动态问题，本文提出 C-JEPA 架构，将掩码联合嵌入预测扩展至对象级表示。通过对象级掩码强制模型从其他对象推断状态，从而引入因果归纳偏置。实验表明，该方法在反事实推理中提升约 20%，且仅需 1% 的潜在特征即可实现高效的智能体规划。

**亮点**:
  - 提出基于对象级掩码的 C-JEPA 世界模型
  - 通过潜在干预引入因果归纳偏置
  - 规划效率显著提升，仅用 1% 特征达到可比性能

---

###  6. ResearchGym：在真实世界 AI 研究中评估语言模型智能体 (ResearchGym: Evaluating Language Model Agents on Real-World AI Research)

**论文链接**: [https://arxiv.org/abs/2602.15112](https://arxiv.org/abs/2602.15112)
**组织**: Unknown
**得分**: 27.45
**标签**: 
**Upvotes**: 16 | **Stars**: 6

**摘要**: 针对评估智能体端到端研究能力的难题，本文提出 ResearchGym 基准。该平台基于5篇顶会论文构建任务，要求智能体自主提出假设、运行实验并超越基线。实验显示，GPT-5 等模型存在显著的“能力-可靠性”差距，尽管偶能达到 SOTA，但普遍面临资源管理差和成功率低的问题。

**亮点**:
  - 提出 ResearchGym 端到端研究评估基准
  - 揭示前沿模型存在显著的能力-可靠性差距
  - 定位了上下文限制等长期规划失败模式

---

###  7. 重探柏拉图表征假说：亚里士多德视角 (Revisiting the Platonic Representation Hypothesis: An Aristotelian View)

**论文链接**: [https://arxiv.org/abs/2602.14486](https://arxiv.org/abs/2602.14486)
**组织**: Unknown
**得分**: 27.0
**标签**: 
**Upvotes**: 9 | **Stars**: 10

**摘要**: 针对现有表征相似性度量受网络规模混淆的问题，提出一种基于排列的零校准框架。该框架修正了度量偏差，揭示了全局光谱度量的收敛现象实为假象，而局部邻域关系跨模态仍保持一致，据此提出神经网络收敛于共享局部邻域关系的“亚里士多德表征假说”。

**亮点**:
  - 揭示现有相似性度量受网络规模混淆
  - 提出基于排列的零校准框架
  - 提出亚里士多德表征假说

---

###  8. 用于一致性视频世界模型的几何感知旋转位置编码 (Geometry-Aware Rotary Position Embedding for Consistent Video World Model)

**论文链接**: [https://arxiv.org/abs/2602.07854](https://arxiv.org/abs/2602.07854)
**组织**: Tsinghua University
**得分**: 26.59
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 0

**摘要**: 现有视频世界模型在长轨迹中缺乏空间持久性，常在相机重访时产生幻觉。本文提出 ViewRope，将相机射线方向注入自注意力层，利用相对射线几何提供 3D 一致性归纳偏置。此外，提出几何感知稀疏注意力机制以提高效率。实验表明，该方法显著提升了长期一致性并降低了计算成本。

**亮点**:
  - 提出 ViewRope 几何感知编码
  - 提出几何感知稀疏注意力机制
  - 构建 ViewBench 评测基准

---
