# 每日论文汇总 - 2026-02-24

**论文数量**: 6

---

###  1. SimToolReal：面向零样本灵巧工具操作的对象中心策略 (SimToolReal: An Object-Centric Policy for Zero-Shot Dexterous Tool Manipulation)

**论文链接**: [https://arxiv.org/abs/2602.16863](https://arxiv.org/abs/2602.16863)
**组织**: Stanford University
**得分**: 50.92
**标签**: Frontier Lab
**Upvotes**: 12 | **Stars**: 16

**摘要**: 针对工具操作数据收集难及依赖任务特定设计的问题，提出 SimToolReal。该方法通过程序化生成多样化类工具物体并训练单一策略，使其将物体移动至随机姿态。实验显示，该方法在 120 次真实实验中无需特定训练即可泛化，性能优于先前方法 37%，且匹敌特定任务的专业策略。

**亮点**:
  - 实现强力的零样本真实世界泛化
  - 基于程序化生成与通用目标的训练策略
  - 性能超越先前基线方法 37%

---

###  2. VLANeXt：构建强力视觉-语言-动作模型的秘诀 (VLANeXt: Recipes for Building Strong VLA Models)

**论文链接**: [https://arxiv.org/abs/2602.18532](https://arxiv.org/abs/2602.18532)
**组织**: MMLab@NTU
**得分**: 42.54
**标签**: 
**Upvotes**: 39 | **Stars**: 43

**摘要**: 针对现有视觉-语言-动作模型设计碎片化问题，本研究在统一框架下系统剖析了基础组件、感知与动作建模三个维度，提炼出12项关键发现并提出了VLANeXt模型。该模型在LIBERO及LIBERO-plus基准测试中超越先前方法，并在真实实验中表现出优异的泛化能力。

**亮点**:
  - 系统解析 VLA 模型设计空间
  - 提炼 12 项关键构建经验
  - 在 LIBERO 基准测试中实现 SOTA 性能

---

###  3. TOPReward：将令牌概率作为机器人技术的隐式零样本奖励 (TOPReward: Token Probabilities as Hidden Zero-Shot Rewards for Robotics)

**论文链接**: [https://arxiv.org/abs/2602.19313](https://arxiv.org/abs/2602.19313)
**组织**: Ai2
**得分**: 40.71
**标签**: Frontier Lab
**Upvotes**: 21 | **Stars**: 1

**摘要**: 针对RL中奖励稀疏问题，提出TOPReward，利用预训练视频VLM的内部token logits提取隐式任务进度。在130多个零样本任务中实现0.947相关性，显著优于SOTA基线。

**亮点**:
  - 提出基于Token Logits的TOPReward机制
  - 零样本评估中显著超越SOTA基线
  - 支持多种机器人平台与下游应用

---

###  4. Mobile-O：移动设备上的统一多模态理解与生成 (Mobile-O: Unified Multimodal Understanding and Generation on Mobile Device)

**论文链接**: [https://arxiv.org/abs/2602.20161](https://arxiv.org/abs/2602.20161)
**组织**: Mohamed Bin Zayed University of Artificial Intelligence
**得分**: 37.61
**标签**: 
**Upvotes**: 18 | **Stars**: 35

**摘要**: 针对移动端部署难题，提出轻量级统一多模态模型Mobile-O。通过核心模块MCP融合特征并采用四元组格式训练，该模型在GenEval达74%，速度超越竞品6-11倍，首次在iPhone上实现端侧实时统一多模态处理。

**亮点**:
  - GenEval 74% 性能表现
  - 提出 Mobile Conditioning Projector
  - iPhone 端 3 秒实时运行

---

###  5. 足式机器人接触锚定本体感觉里程计 (Contact-Anchored Proprioceptive Odometry for Quadruped Robots)

**论文链接**: [https://arxiv.org/abs/2602.17393](https://arxiv.org/abs/2602.17393)
**组织**: ucas
**得分**: 33.91
**标签**: 
**Upvotes**: 1 | **Stars**: 132

**摘要**: 针对无外部传感器足式机器人的里程计漂移问题，提出一种仅依赖IMU和电机数据的纯本体感觉状态估计器。该方法将支撑腿视为运动学锚点，结合高度聚类纠偏和IK-CKF滤波，有效抑制了长期漂移，并在多种四足及轮足平台上实现了高精度闭环导航。

**亮点**:
  - 仅使用IMU和电机数据的纯本体感觉方案
  - 提出接触锚定机制利用足端约束抑制漂移
  - 应用逆运动学容积卡尔曼滤波优化速度观测

---

###  6. DODO：离散 OCR 扩散模型 (DODO: Discrete OCR Diffusion Models)

**论文链接**: [https://arxiv.org/abs/2602.16872](https://arxiv.org/abs/2602.16872)
**组织**: Amazon Web Services (AWS)
**得分**: 31.5
**标签**: Frontier Lab
**Upvotes**: 7 | **Stars**: 0

**摘要**: 针对 OCR 任务中自回归解码速度慢、成本高的问题，提出 DODO 模型。这是首个利用块离散扩散的 VLM，通过分块生成缓解了全局扩散的同步错误。实验表明，该方法在保持近乎 SOTA 准确率的同时，推理速度较自回归基线提升了 3 倍。

**亮点**:
  - 提出块离散扩散机制，解决全局扩散同步错误
  - 首个利用离散扩散实现 OCR 并行解码的 VLM
  - 近乎 SOTA 精度，推理速度提升 3 倍

---
