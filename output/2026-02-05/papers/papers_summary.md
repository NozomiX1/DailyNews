# 每日论文汇总 - 2026-02-05

**论文数量**: 12

---

### 🏆 1. WideSeek-R1：通过多智能体强化学习探索广度扩展以实现广泛信息寻取 (WideSeek-R1: Exploring Width Scaling for Broad Information Seeking via Multi-Agent Reinforcement Learning)

**论文链接**: [https://arxiv.org/abs/2602.04634](https://arxiv.org/abs/2602.04634)
**组织**: RLinf
**得分**: 70.29
**标签**: Viral
**Upvotes**: 84 | **Stars**: 2397

**摘要**: 针对大模型在处理广度信息寻取任务时因单一智能体串行工作而产生的效率瓶颈，本文提出 WideSeek-R1 框架。该框架采用“主导-子智能体”架构，利用多智能体强化学习（MARL）优化协同调度与并行执行。实验显示，4B 参数的 WideSeek-R1 在 WideSearch 基准上的性能可媲美 671B 的 DeepSeek-R1，且性能随并行智能体数量增加而持续提升，验证了广度扩展的有效性。

**亮点**:
  - 提出 WideSeek-R1 框架，开辟了 LLM 广度扩展（Width Scaling）的新路径
  - 利用多智能体强化学习（MARL）实现高效的并行任务调度与执行
  - 4B 小模型性能比肩 671B 超大模型，展现出极高的计算效率与扩展性

---

###  2. CL-bench：针对情境学习（Context Learning）能力的基准测试 (CL-bench: A Benchmark for Context Learning)

**论文链接**: [https://arxiv.org/abs/2602.03587](https://arxiv.org/abs/2602.03587)
**组织**: Tencent
**得分**: 70.47
**标签**: Frontier Lab
**Upvotes**: 18 | **Stars**: 321

**摘要**: 针对大语言模型过度依赖预训练知识而忽视从实时复杂情境中学习的问题，腾讯提出了CL-bench。该基准包含500个复杂情境和1899项任务，要求模型利用情境中全新的领域知识、规则和程序进行推理。实验显示，前沿模型平均得分仅17.2%，即使是顶级模型表现也远不理想，揭示了情境学习是当前模型解决真实世界复杂任务的关键瓶颈。

**亮点**:
  - 定义并量化了超越传统ICL和长文本检索的“情境学习”能力
  - 构建了包含31,607条专家验证标准的高难度复杂任务数据集
  - 揭示了前沿语言模型在处理非预训练新知识时的巨大性能差距

---

###  3. HY3D-Bench：面向3D资产生成的开源生态系统 (HY3D-Bench: Generation of 3D Assets)

**论文链接**: [https://arxiv.org/abs/2602.03907](https://arxiv.org/abs/2602.03907)
**组织**: Tencent Hunyuan
**得分**: 67.38
**标签**: Frontier Lab
**Upvotes**: 22 | **Stars**: 163

**摘要**: 针对3D内容创作中数据处理的瓶颈，腾讯混元团队推出HY3D-Bench开源生态系统。该方案包含25万个高保真3D对象，提供水密网格及结构化部件级分解，支持精细化感知与编辑。此外，通过AIGC合成管线新增12.5万个资产以增强长尾类别多样性。实验证明该数据集成功支撑了Hunyuan3D-2.1-Small的训练，为3D感知和机器人领域提供了高质量基础数据。

**亮点**:
  - 发布包含25万个高保真、训练就绪对象的3D资产库
  - 引入结构化部件级分解，实现更细粒度的控制与编辑
  - 构建可扩展AIGC管线，通过12.5万合成资产弥补现实分布差距

---

###  4. 残差上下文扩散语言模型 (Residual Context Diffusion Language Models)

**论文链接**: [https://arxiv.org/abs/2601.22954](https://arxiv.org/abs/2601.22954)
**组织**: University of California, Berkeley
**得分**: 61.36
**标签**: Frontier Lab
**Upvotes**: 29 | **Stars**: 45

**摘要**: 针对扩散语言模型(dLLM)在重掩码过程中丢弃低置信度标记导致的计算浪费，本文提出残差上下文扩散(RCD)。RCD将丢弃的标记表征转化为上下文残差并在下步去噪中重新注入。该方法通过解耦的两阶段训练实现，在提升5-10%精度的同时，使 AIME 任务的推理步数减少4-5倍，显著优化了并行解码效率。

**亮点**:
  - 提出残差上下文回收机制避免重掩码过程中的计算浪费
  - 采用解耦的两阶段训练流水线有效绕过显存瓶颈
  - 在 AIME 挑战性任务中实现精度翻倍及 4-5 倍的推理加速

---

###  5. 基于多尺度结构生成的蛋白质自回归建模 (Protein Autoregressive Modeling via Multiscale Structure Generation)

**论文链接**: [https://arxiv.org/abs/2602.04883](https://arxiv.org/abs/2602.04883)
**组织**: ByteDance Seed
**得分**: 58.03
**标签**: Super Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 本文提出 PAR，首个用于蛋白质骨架生成的多尺度自回归框架。该方法模拟“雕刻”过程，通过从粗到细的层次化预测实现结构建模。PAR 包含多尺度下采样、自回归 Transformer 编码器及流式解码器，并引入噪声上下文学习缓解暴露偏差。实验证明 PAR 在无条件生成中具有优异的 Scaling 效应，并具备强大的零样本泛化能力，支持无需微调的基序脚手架和提示词引导生成。

**亮点**:
  - 提出首个从粗到细的多尺度蛋白质骨架自回归生成框架 PAR
  - 通过噪声上下文学习与计划采样有效解决了自回归模型中的暴露偏差问题
  - 展现出强大的零样本泛化性能，支持柔性的基序脚手架设计与条件生成

---

###  6. 基于 Dummy Head 的高效自回归视频扩散模型 (Efficient Autoregressive Video Diffusion with Dummy Head)

**论文链接**: [https://arxiv.org/abs/2601.20499](https://arxiv.org/abs/2601.20499)
**组织**: Microsoft Research
**得分**: 52.77
**标签**: Frontier Lab
**Upvotes**: 5 | **Stars**: 41

**摘要**: 针对自回归视频扩散模型中多头自注意力机制对历史帧利用率不足的问题，本文发现约 25% 的注意力头几乎仅关注当前帧。为此提出 Dummy Forcing 方案，通过异构内存分配和动态头编程减少头级上下文冗余，并结合上下文打包技术实现激进的缓存压缩。该方法无需额外训练即可实现 2.0 倍推理加速，支持 24.3 FPS 视频生成，且质量损失低于 0.5%。

**亮点**:
  - 提出无需训练的 Dummy Forcing 插件式加速方案
  - 实现 2.0 倍推理加速并支持 24.3 FPS 的实时视频生成
  - 揭示并利用了自回归扩散模型中注意力头的上下文冗余特性

---

###  7. 自提示语言模型增强强化学习研究 (Self-Hinting Language Models Enhance Reinforcement Learning)

**论文链接**: [https://arxiv.org/abs/2602.03143](https://arxiv.org/abs/2602.03143)
**组织**: Microsoft Research
**得分**: 51.94
**标签**: Frontier Lab
**Upvotes**: 21 | **Stars**: 12

**摘要**: 针对 GRPO 算法在稀疏终端奖励下因组内样本奖励趋同导致优势函数塌缩的问题，微软研究院提出 SAGE 框架。该框架在训练中引入紧凑的自提示（如计划或分解）以增加采样多样性，通过特权监督改善策略分布，而推理时无需提示。实验表明，SAGE 在 Llama-3.2 和 Qwen 系列模型上的表现一致优于 GRPO，有效提升了模型对齐效果。

**亮点**:
  - 提出 SAGE 框架解决 GRPO 在稀疏奖励下的优势塌缩问题
  - 利用训练期特权自提示作为自适应课程，增加采样多样性
  - 在多款主流 LLM 及 6 项基准测试中均取得显著性能提升

---

###  8. D-CORE：激励大推理模型在复杂工具使用中的任务分解能力 (D-CORE: Incentivizing Task Decomposition in Large Reasoning Models for Complex Tool Use)

**论文链接**: [https://arxiv.org/abs/2602.02160](https://arxiv.org/abs/2602.02160)
**组织**: alibaba-inc
**得分**: 47.25
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 7

**摘要**: 针对大推理模型（LRM）在复杂工具场景中因缺乏子任务分解能力而导致的“懒惰推理”问题，阿里团队提出D-CORE框架。该框架通过自蒸馏激发任务分解能力，并利用多样性强化学习恢复反思推理。实验显示，D-CORE-14B在BFCLv3基准上达到79.3%的准确率，性能超越其规模5倍的70B模型，刷新了SOTA纪录。

**亮点**:
  - 提出D-CORE两阶段训练框架，解决大推理模型的“懒惰推理”问题
  - 14B参数规模模型在性能上显著超越主流70B大模型
  - 在BFCLv3工具调用基准测试中刷新SOTA纪录

---

###  9. FASA：频率感知稀疏注意力机制 (FASA: Frequency-aware Sparse Attention)

**论文链接**: [https://arxiv.org/abs/2602.03152](https://arxiv.org/abs/2602.03152)
**组织**: alibaba-inc
**得分**: 45.34
**标签**: Frontier Lab
**Upvotes**: 110 | **Stars**: 0

**摘要**: 针对长文本大模型 KV 缓存显存占用过高的痛点，本文提出 FASA 框架。通过挖掘 RoPE 在频率块级别的功能稀疏性，FASA 利用“主导”频率块动态预测 Token 重要性并剔除冗余缓存。实验表明，FASA 在保持近乎无损精度的前提下，在 AIME24 任务上仅需 18.9% 的缓存即可实现 2.56 倍加速，有效解决了长文本推理的瓶颈问题。

**亮点**:
  - 揭示了 RoPE 编码在频率块层面的功能稀疏性新见解
  - 实现查询感知的动态 Token 剔除，大幅降低 KV 缓存带宽和计算开销
  - 在 LongBench 等基准测试中展现出极高的鲁棒性与接近 Oracle 的精度

---

###  10. A-RAG：通过分层检索接口扩展智能体检索增强生成 (A-RAG: Scaling Agentic Retrieval-Augmented Generation via Hierarchical Retrieval Interfaces)

**论文链接**: [https://arxiv.org/abs/2602.03442](https://arxiv.org/abs/2602.03442)
**组织**: muset.ai
**得分**: 39.29
**标签**: 
**Upvotes**: 18 | **Stars**: 49

**摘要**: 针对现有RAG系统因检索决策僵化而无法充分利用模型推理能力的问题，本文提出A-RAG框架。该框架通过向模型直接暴露关键词搜索、语义搜索和块读取三种分层工具，使智能体能够自主进行跨粒度的自适应检索。实验表明，A-RAG在多个开放域QA基准上以更低的Token消耗实现了优于现有方法的性能，并展现出随模型规模和测试时计算量增加的良好扩展性。

**亮点**:
  - 提出 A-RAG 智能体框架，允许模型自主参与多粒度检索决策
  - 设计关键词、语义和块读取的分层检索接口体系
  - 在降低检索 Token 成本的同时显著提升了 SOTA 性能

---

###  11. 多智能体讨论中的上下文学习 (Context Learning for Multi-Agent Discussion)

**论文链接**: [https://arxiv.org/abs/2602.02350](https://arxiv.org/abs/2602.02350)
**组织**: Tsinghua University
**得分**: 38.8
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 4

**摘要**: 针对多智能体讨论（MAD）中因上下文不一致导致难以达成共识的问题，清华大学提出 M2CL 方法。该方法为每个智能体引入上下文生成器，通过自适应机制动态生成指令，优化信息组织并控制输出差异。实验显示，M2CL 在推理和具身任务中比现有方法提升 20%-50%，能有效避免噪声干扰，促进多智能体系统达成正确共识。

**亮点**:
  - 提出 M2CL 框架实现动态上下文指令生成
  - 引入自适应机制解决讨论不一致与过早收敛问题
  - 在多项挑战性任务上实现 20%-50% 的性能提升

---

###  12. Quant VideoGen：基于 2-Bit KV 缓存量化的自回归长视频生成 (Quant VideoGen: Auto-Regressive Long Video Generation via 2-Bit KV-Cache Quantization)

**论文链接**: [https://arxiv.org/abs/2602.02958](https://arxiv.org/abs/2602.02958)
**组织**: University of California, Berkeley
**得分**: 38.58
**标签**: Frontier Lab
**Upvotes**: 32 | **Stars**: 0

**摘要**: 针对自回归视频生成中 KV 缓存占用极大（常超 30GB）导致部署困难及长视频一致性下降的痛点，本文提出无需训练的量化框架 QVG。该方案通过语义感知平滑利用视频时空冗余，并引入渐进式残差量化实现由粗到精的压缩。实验表明，QVG 实现了高达 7 倍的显存压缩，延迟开销低于 4%，且在多个基准上刷新了生成质量与显存效率的 Pareto 前沿。

**亮点**:
  - 实现高达 7 倍的 KV 缓存显存压缩
  - 无需额外训练的端到端量化方案
  - 显著降低长视频生成的时空一致性损耗

---
