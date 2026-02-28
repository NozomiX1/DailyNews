# 每日论文汇总 - 2026-02-27

**论文数量**: 10

---

###  1. MobilityBench：面向真实世界移动场景的路径规划智能体评估基准 (MobilityBench: A Benchmark for Evaluating Route-Planning Agents in Real-World Mobility Scenarios)

**论文链接**: [https://arxiv.org/abs/2602.22638](https://arxiv.org/abs/2602.22638)
**组织**: alibaba-inc
**得分**: 71.26
**标签**: Frontier Lab
**Upvotes**: 90 | **Stars**: 94

**摘要**: 针对LLM路径规划智能体评估难、环境非确定性问题，提出基于真实用户数据的MobilityBench基准及确定性沙箱。实验显示现有模型擅长基础规划，但在个性化偏好约束规划上仍有显著提升空间。

**亮点**:
  - 构建大规模真实场景基准 MobilityBench
  - 设计确定性 API-replay 评估沙箱
  - 揭示现有模型在偏好约束规划上的局限

---

###  2. 想象力有助于视觉推理，但目前并非在潜在空间中 (Imagination Helps Visual Reasoning, But Not Yet in Latent Space)

**论文链接**: [https://arxiv.org/abs/2602.22766](https://arxiv.org/abs/2602.22766)
**组织**: Tsinghua University
**得分**: 53.93
**标签**: Frontier Lab
**Upvotes**: 33 | **Stars**: 11

**摘要**: 针对多模态大语言模型潜在视觉推理的有效性问题，本文通过因果中介分析发现潜在词元与输入及答案间存在因果断层，且视觉编码能力有限。为此，提出CapImagine方法，通过文本引导模型进行显式想象。实验表明，该方法在视觉基准上显著优于潜在空间基线，验证了显式想象路径的优越性。

**亮点**:
  - 通过因果中介分析揭示潜在推理机制的无效性
  - 发现潜在词元与输入及输出之间存在双重因果断层
  - 提出CapImagine显式文本想象方法，性能超越潜在空间基线

---

###  3. 从盲点到收益：大型多模态模型的诊断驱动迭代训练 (From Blind Spots to Gains: Diagnostic-Driven Iterative Training for Large Multimodal Models)

**论文链接**: [https://arxiv.org/abs/2602.22859](https://arxiv.org/abs/2602.22859)
**组织**: Unknown
**得分**: 46.4
**标签**: 
**Upvotes**: 142 | **Stars**: 28

**摘要**: 针对现有LMM训练依赖静态数据难以发现盲点的问题，提出诊断驱动渐进进化(DPE)框架。该方法通过诊断引导数据生成与强化，利用多智能体生成高质量数据并动态调整数据配比。实验表明DPE能实现持续的性能提升，是一种可扩展的持续训练范式。

**亮点**:
  - 提出诊断驱动渐进进化 (DPE) 框架
  - 利用多智能体实现动态数据生成与质量控制
  - 在多个基准测试中验证了持续训练收益

---

###  4. 定义通用世界模型的一致性三位一体原则 (The Trinity of Consistency as a Defining Principle for General World Models)

**论文链接**: [https://arxiv.org/abs/2602.23152](https://arxiv.org/abs/2602.23152)
**组织**: OpenDataLab
**得分**: 44.18
**标签**: 
**Upvotes**: 178 | **Stars**: 15

**摘要**: 针对当前世界模型缺乏理论框架的问题，本文提出“一致性三位一体”（模态、空间、时间）作为核心原则，并引入 CoW-Bench 基准以统一评估视频生成与统一多模态模型。该框架为通用世界模型的构建提供了原则性路径，明确了现有局限与未来架构要求。

**亮点**:
  - 提出一致性三位一体（模态、空间、时间）理论框架
  - 发布 CoW-Bench 统一评估基准
  - 系统回顾多模态学习向统一架构演进的轨迹

---

###  5. OmniGAIA：迈向原生全模态 AI 智能体 (OmniGAIA: Towards Native Omni-Modal AI Agents)

**论文链接**: [https://arxiv.org/abs/2602.22897](https://arxiv.org/abs/2602.22897)
**组织**: Unknown
**得分**: 41.97
**标签**: 
**Upvotes**: 46 | **Stars**: 34

**摘要**: 针对现有模型多局限于双模态的问题，本文提出了全模态基准 OmniGAIA 和原生智能体 OmniAtlas。该架构通过全模态事件图合成数据，并利用事后引导树探索与 OmniDPO 进行训练，有效增强了模型在复杂场景下的跨模态推理与工具使用能力。

**亮点**:
  - 构建全模态智能体基准 OmniGAIA
  - 提出原生全模态智能体 OmniAtlas
  - 引入 OmniDPO 细粒度纠错训练

---

###  6. 通用智能体评估 (General Agent Evaluation)

**论文链接**: [https://arxiv.org/abs/2602.22953](https://arxiv.org/abs/2602.22953)
**组织**: IBM Research
**得分**: 39.71
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 6

**摘要**: 针对现有基准偏向特定领域导致无法公平评估通用智能体的问题，本文提出统一协议及Exgentic评估框架。实验建立了首个开放通用智能体排行榜，结果显示通用智能体在无需特定环境调优的情况下，能跨环境泛化并达到与专用智能体相当的性能。

**亮点**:
  - 提出Exgentic通用智能体评估框架
  - 发布首个开放通用智能体排行榜
  - 验证通用智能体无需微调的跨环境泛化能力

---

###  7. 混合在线与离线优化的探索性记忆增强 LLM 智能体 (Exploratory Memory-Augmented LLM Agent via Hybrid On- and Off-Policy Optimization)

**论文链接**: [https://arxiv.org/abs/2602.23008](https://arxiv.org/abs/2602.23008)
**组织**: Microsoft
**得分**: 37.87
**标签**: Frontier Lab
**Upvotes**: 26 | **Stars**: 0

**摘要**: 针对 LLM 智能体在强化学习中的探索瓶颈，提出 EMPO^2 框架。该架构通过记忆增强探索并结合混合在线离线优化。实验显示其显著超越 GRPO，在分布外任务中无需参数更新即可展现强适应性。

**亮点**:
  - 提出 EMPO^2 混合 RL 框架
  - 结合记忆机制显著提升探索性能
  - OOD 场景下无需参数更新即可适应新任务

---

###  8. EmbodMocap：面向具身智能体的野外 4D 人体-场景重建 (EmbodMocap: In-the-Wild 4D Human-Scene Reconstruction for Embodied Agents)

**论文链接**: [https://arxiv.org/abs/2602.23205](https://arxiv.org/abs/2602.23205)
**组织**: Unknown
**得分**: 35.58
**标签**: 
**Upvotes**: 9 | **Stars**: 45

**摘要**: 针对现有动捕系统成本高限制野外数据采集的问题，提出EmbodMocap方法。该方案利用两部移动iPhone进行双视角联合标定，实现了统一的度量空间下的人体与场景重建。实验验证了其优于单视角的性能，并成功应用于机器人控制等具身任务。

**亮点**:
  - 提出低成本便携式双iPhone采集管线
  - 实现统一的度量空间人体与场景重建
  - 支持机器人运动控制等下游具身任务

---

###  9. AgentDropoutV2：通过测试时校正或拒绝剪枝优化多智能体系统信息流 (AgentDropoutV2: Optimizing Information Flow in Multi-Agent Systems via Test-Time Rectify-or-Reject Pruning)

**论文链接**: [https://arxiv.org/abs/2602.23258](https://arxiv.org/abs/2602.23258)
**组织**: Harbin Institute of Technology
**得分**: 33.52
**标签**: 
**Upvotes**: 23 | **Stars**: 14

**摘要**: 针对多智能体系统中错误信息级联的痛点，本文提出AgentDropoutV2测试时校正或拒绝剪枝框架。该方法作为主动防火墙，利用检索增强校正器动态校正错误或剪除不可修复输出，无需重训。实验显示其在数学基准上平均准确率提升6.3%，具备良好的鲁棒性与自适应性。

**亮点**:
  - 无需重新训练的测试时优化框架
  - 提出主动防火墙与检索增强校正机制
  - 数学基准任务平均准确率提升6.3%

---

###  10. VGG-T^3：大规模离线前馈 3D 重建 (VGG-T^3: Offline Feed-Forward 3D Reconstruction at Scale)

**论文链接**: [https://arxiv.org/abs/2602.23361](https://arxiv.org/abs/2602.23361)
**组织**: NVIDIA
**得分**: 33.52
**标签**: Frontier Lab
**Upvotes**: 11 | **Stars**: 0

**摘要**: 针对离线前馈 3D 重建计算量随输入图像数呈二次方增长的瓶颈，提出 VGG-T^3 模型。该方法通过测试时训练将场景几何的键值空间提炼为固定大小 MLP，使计算量随图像数线性增长。实验显示，千张图像重建仅需 54 秒，提速 11.6 倍且精度优于同类线性方法。

**亮点**:
  - 提出基于测试时训练的 VGG-T^3 架构
  - 实现计算复杂度从二次方到线性的降低
  - 千张图像 54 秒极速重建与 SOTA 精度

---
