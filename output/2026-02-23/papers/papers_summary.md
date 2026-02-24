# 每日论文汇总 - 2026-02-23

**论文数量**: 4

---

### 🏆 1. 推理模型是否隐式知晓何时停止思考？ (Does Your Reasoning Model Implicitly Know When to Stop Thinking?)

**论文链接**: [https://arxiv.org/abs/2602.08354](https://arxiv.org/abs/2602.08354)
**组织**: ByteDance
**得分**: 74.92
**标签**: Super Lab, Must Read
**Upvotes**: 101 | **Stars**: 0

**摘要**: 针对大推理模型使用长思维链导致的冗余与低效问题，研究发现模型隐式知晓何时停止思考。为此提出SAGE采样范式及SAGE-RL方法，将高效模式融入推理。实验显示，该方法在多个数学基准测试上显著提升了准确性与效率。

**亮点**:
  - 揭示大推理模型隐式具备停止思考的能力
  - 提出SAGE自感知引导高效推理范式
  - SAGE-RL在数学基准上实现精度与效率双提升

---

###  2. 利用 LoRA 权重基跨越视觉类比空间 (Spanning the Visual Analogy Space with a Weight Basis of LoRAs)

**论文链接**: [https://arxiv.org/abs/2602.15727](https://arxiv.org/abs/2602.15727)
**组织**: NVIDIA
**得分**: 47.29
**标签**: Frontier Lab
**Upvotes**: 9 | **Stars**: 10

**摘要**: 针对现有视觉类比方法使用单一 LoRA 导致泛化受限的问题，提出了 LoRWeB 方法。该方法通过可学习的 LoRA 模块基和轻量级编码器，动态组合变换基元以处理输入类比对。实验表明，该方法达到 SOTA 性能，显著提升了未知视觉变换的泛化能力。

**亮点**:
  - 达到 SOTA 性能
  - 提出 LoRWeB 动态 LoRA 基架构
  - 显著提升未见变换泛化能力

---

###  3. VESPO：用于稳定离策略大语言模型训练的变分序列级软策略优化 (VESPO: Variational Sequence-Level Soft Policy Optimization for Stable Off-Policy LLM Training)

**论文链接**: [https://arxiv.org/abs/2602.10693](https://arxiv.org/abs/2602.10693)
**组织**: rednote-hilab
**得分**: 43.26
**标签**: 
**Upvotes**: 160 | **Stars**: 14

**摘要**: 针对LLM强化学习中策略陈旧导致的训练不稳定问题，提出了变分序列级软策略优化（VESPO）。该方法通过变分推导获得闭式重塑核，直接处理序列级重要性权重。实验表明，VESPO在64倍陈旧度和全异步环境下保持训练稳定，并在Dense和MoE模型上取得持续性能提升。

**亮点**:
  - 提出 VESPO 算法解决策略陈旧问题
  - 变分推导统一序列级重要性采样理论
  - 支持高陈旧度及全异步稳定训练

---

###  4. ReIn：基于推理植入的对话错误恢复 (ReIn: Conversational Error Recovery with Reasoning Inception)

**论文链接**: [https://arxiv.org/abs/2602.17022](https://arxiv.org/abs/2602.17022)
**组织**: University of Illinois at Urbana-Champaign
**得分**: 24.56
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 0

**摘要**: 针对LLM智能体在面对用户错误时难以恢复且无法微调的问题，该文提出推理植入方法。ReIn通过外部模块识别错误并生成恢复计划，将其植入智能体推理过程以指导修正行动。实验表明，该方法在无需修改模型和提示的情况下，显著提升了任务成功率和泛化能力，优于显式提示修改策略。

**亮点**:
  - 提出 Reasoning Inception (ReIn) 测试时干预机制
  - 无需修改模型参数或系统提示词即可实现错误恢复
  - 在任务成功率与泛化能力上超越显式提示修改方法

---
