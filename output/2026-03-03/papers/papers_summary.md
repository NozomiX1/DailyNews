# 每日论文汇总 - 2026-03-03

**论文数量**: 20

---

###  1. OmniLottie：基于参数化 Lottie 标记的矢量动画生成 (OmniLottie: Generating Vector Animations via Parameterized Lottie Tokens)

**论文链接**: [https://arxiv.org/abs/2603.02138](https://arxiv.org/abs/2603.02138)
**组织**: Fudan University
**得分**: 73.97
**标签**: Frontier Lab
**Upvotes**: 113 | **Stars**: 118

**摘要**: 针对原始 Lottie JSON 文件结构复杂导致的生成难题，本文提出了 OmniLottie 框架。该方法设计了专用 Lottie 分词器将 JSON 转换为结构化序列，并结合预训练视觉语言模型处理多模态指令。此外，构建了大规模数据集 MMLottie-2M。实验证明，该框架能生成生动且语义对齐的高质量矢量动画。

**亮点**:
  - 设计专用 Lottie 分词器解决 JSON 结构学习难题
  - 结合预训练视觉语言模型实现多模态控制
  - 发布大规模 MMLottie-2M 矢量动画数据集

---

###  2. 利用参考指导微调在强化学习中攻克难题 (Learn Hard Problems During RL with Reference Guided Fine-tuning)

**论文链接**: [https://arxiv.org/abs/2603.01223](https://arxiv.org/abs/2603.01223)
**组织**: ByteDance Seed
**得分**: 63.12
**标签**: Super Lab
**Upvotes**: 11 | **Stars**: 0

**摘要**: 针对数学推理强化学习中奖励稀疏的问题，提出参考指导微调。该方法利用部分人类参考解引导模型生成符合自身分布的推理轨迹。实验显示，ReGFT 提升了模型解题能力，加速了 DAPO 训练，并显著提高了 RL 的最终性能。

**亮点**:
  - 提出 ReGFT 新架构
  - 解决 RL 奖励稀疏痛点
  - 提升 AIME 基准表现

---

###  3. WorldStereo：通过 3D 几何记忆衔接相机引导视频生成与场景重建 (WorldStereo: Bridging Camera-Guided Video Generation and Scene Reconstruction via 3D Geometric Memories)

**论文链接**: [https://arxiv.org/abs/2603.02049](https://arxiv.org/abs/2603.02049)
**组织**: Tencent
**得分**: 55.09
**标签**: Frontier Lab
**Upvotes**: 13 | **Stars**: 31

**摘要**: 针对视频扩散模型难以重建一致 3D 场景的问题，提出 WorldStereo 框架。该框架引入全局几何记忆和空间立体记忆模块，实现精确相机控制并注入 3D 结构先验。该方法无需联合训练，能生成多视角一致视频并支持高质量 3D 重建，展现了作为 World Model 的强大能力。

**亮点**:
  - 提出双几何记忆架构（全局几何记忆与空间立体记忆）
  - 无需联合训练实现精确相机控制与多视角一致性
  - 生成视频支持高质量 3D 重建，具备 World Model 能力

---

###  4. RubricBench: 实现模型生成评分标准与人类标准的对齐 (RubricBench: Aligning Model-Generated Rubrics with Human Standards)

**论文链接**: [https://arxiv.org/abs/2603.01562](https://arxiv.org/abs/2603.01562)
**组织**: Tencent Hunyuan
**得分**: 53.71
**标签**: Frontier Lab
**Upvotes**: 45 | **Stars**: 8

**摘要**: 针对LLM对齐任务中缺乏统一规则评估基准的问题，本文提出RubricBench。该基准包含1,147个经过多维过滤的对比样本，并配备了专家标注的原子化规则。实验表明，人类标注与模型生成的规则之间存在显著能力鸿沟，即便是SOTA模型也难以自主生成有效的评估标准。

**亮点**:
  - 构建包含 1,147 个样本的 RubricBench 评估基准
  - 引入多维过滤管道与专家标注的原子化规则
  - 揭示了模型自主生成评估标准的能力与人类存在显著差距

---

###  5. 从规模到速度：图像编辑的自适应测试时扩展 (From Scale to Speed: Adaptive Test-Time Scaling for Image Editing)

**论文链接**: [https://arxiv.org/abs/2603.00141](https://arxiv.org/abs/2603.00141)
**组织**: alibaba-inc
**得分**: 45.37
**标签**: Frontier Lab
**Upvotes**: 120 | **Stars**: 0

**摘要**: 针对测试时扩展在图像编辑中资源分配低效等问题，提出 ADE-CoT 框架。该框架包含难度感知资源分配、特定早期验证及投机性停止策略。实验表明，ADE-CoT 在多个模型上实现了优异的性能与效率权衡，相比 Best-of-N 加速 2 倍以上。

**亮点**:
  - 提出 ADE-CoT 自适应测试时扩展框架
  - 实现难度感知的动态资源分配与早期剪枝
  - 保持高性能的同时实现 2 倍以上推理加速

---

###  6. RL 何时助力医疗视觉语言模型？解耦视觉、SFT 与 RL 的收益 (When Does RL Help Medical VLMs? Disentangling Vision, SFT, and RL Gains)

**论文链接**: [https://arxiv.org/abs/2603.01301](https://arxiv.org/abs/2603.01301)
**组织**: Vector Institute
**得分**: 44.56
**标签**: Frontier Lab
**Upvotes**: 8 | **Stars**: 7

**摘要**: 针对RL在医疗VLM中作用不明的问题，本研究解耦了视觉、SFT和RL的影响。发现SFT拓展模型支持度，RL锐化输出分布。基于此提出的边界感知配方在多项医疗VQA基准中表现优异。

**亮点**:
  - 解耦视觉、SFT与RL收益的对照研究
  - 揭示SFT拓展支持度而RL锐化分布的机制
  - 提出边界感知配方实现强健的医疗VQA性能

---

###  7. Tool-R0：零数据环境下自演进的工具学习大语言模型智能体 (Tool-R0: Self-Evolving LLM Agents for Tool-Learning from Zero Data)

**论文链接**: [https://arxiv.org/abs/2602.21320](https://arxiv.org/abs/2602.21320)
**组织**: University of Illinois at Urbana-Champaign
**得分**: 43.76
**标签**: Frontier Lab
**Upvotes**: 8 | **Stars**: 6

**摘要**: 针对现有强化学习依赖人工标注限制智能体自我演进的问题，提出 Tool-R0 框架。该方法在零数据假设下，利用自博弈强化学习协同演进生成器与求解器，通过相互提出和解决挑战性任务实现自我进化。实验表明其性能相比基线模型提升 92.5%，并超越全监督工具调用基线。

**亮点**:
  - 提出零数据自演进框架 Tool-R0
  - 通过生成器与求解器协同演进实现自博弈
  - 性能超越全监督基线模型

---

###  8. VGGT-Det：挖掘 VGGT 内部先验实现无传感器几何的多视角室内 3D 目标检测 (VGGT-Det: Mining VGGT Internal Priors for Sensor-Geometry-Free Multi-View Indoor 3D Object Detection)

**论文链接**: [https://arxiv.org/abs/2603.00912](https://arxiv.org/abs/2603.00912)
**组织**: The Hong Kong University of Science and Technology
**得分**: 42.15
**标签**: 
**Upvotes**: 30 | **Stars**: 50

**摘要**: 针对现有检测依赖昂贵相机位姿的问题，提出首个无传感器几何框架 VGGT-Det。该方法通过注意力引导查询生成（AG）和查询驱动特征聚合（QD），挖掘 VGGT 内部的语义与几何先验，动态提升 2D 特征至 3D。实验表明，该方法在 ScanNet 和 ARKitScenes 上分别超越最佳基线 4.4 和 8.6 mAP@0.25。

**亮点**:
  - 首个无需传感器几何的室内 3D 检测框架
  - 提出 AG 和 QD 模块挖掘 VGGT 内部先验
  - 在 ScanNet 和 ARKitScenes 上取得显著性能提升

---

###  9. OpenAutoNLU：面向自然语言理解的开源自动机器学习库 (OpenAutoNLU: Open Source AutoML Library for NLU)

**论文链接**: [https://arxiv.org/abs/2603.01824](https://arxiv.org/abs/2603.01824)
**组织**: MTSAIR
**得分**: 40.16
**标签**: 
**Upvotes**: 40 | **Stars**: 28

**摘要**: 针对NLU任务中手动配置繁琐的问题，该库提出了数据感知的训练机制选择，实现零配置自动化。它集成了数据质量诊断、可配置的OOD检测及LLM功能，通过极简低代码API提供高效的NLU解决方案。

**亮点**:
  - 引入数据感知训练机制，实现零配置
  - 集成数据质量诊断与OOD检测
  - 支持LLM特性及极简低代码API

---

###  10. CHIMERA：用于可泛化大语言模型推理的紧凑型合成数据 (CHIMERA: Compact Synthetic Data for Generalizable LLM Reasoning)

**论文链接**: [https://arxiv.org/abs/2603.00889](https://arxiv.org/abs/2603.00889)
**组织**: Apple
**得分**: 39.3
**标签**: Frontier Lab
**Upvotes**: 35 | **Stars**: 0

**摘要**: 针对LLM推理训练存在的冷启动、覆盖面窄及标注瓶颈问题，本文提出CHIMERA合成数据集。该数据集包含9K个跨学科的长CoT样本，并采用自动化验证管道。实验表明，仅用该数据微调4B模型，即可在多项推理基准上媲美235B大模型的性能。

**亮点**:
  - 提出 CHIMERA 紧凑型合成数据集
  - 覆盖 8 大学科的长 CoT 轨迹
  - 4B 模型匹敌 235B 模型性能

---

###  11. ProtegoFed：针对穿插污染数据的无后门联邦指令微调 (ProtegoFed: Backdoor-Free Federated Instruction Tuning with Interspersed Poisoned Data)

**论文链接**: [https://arxiv.org/abs/2603.00516](https://arxiv.org/abs/2603.00516)
**组织**: Shanghai Jiao Tong University
**得分**: 37.04
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 7

**摘要**: 针对联邦指令微调中穿插污染数据致现有防御失效的问题，提出ProtegoFed框架。该方法利用频域梯度作为鲁棒信号，结合全局二次聚类机制协同识别与净化污染数据。实验表明其检测率达92-100%，攻击成功率降至近乎零且保持模型效用。

**亮点**:
  - 提出首个针对穿插污染数据的联邦指令微调防御框架
  - 利用频域梯度特征实现鲁棒的样本识别
  - 实现近零攻击成功率并保持模型主要任务性能

---

###  12. SWE-rebench V2：大规模语言无关的软件工程任务集 (SWE-rebench V2: Language-Agnostic SWE Task Collection at Scale)

**论文链接**: [https://arxiv.org/abs/2602.23866](https://arxiv.org/abs/2602.23866)
**组织**: Nebius
**得分**: 35.75
**标签**: 
**Upvotes**: 48 | **Stars**: 11

**摘要**: 针对RL训练SWE智能体缺乏大规模可复现环境的痛点，本文提出SWE-rebench V2自动化流水线。该方法利用交互式设置代理与LLM评委过滤，构建了包含3.2万任务、覆盖20种语言的数据集及预构建镜像，有效支持了跨语言的大规模SWE智能体训练。

**亮点**:
  - 构建涵盖20种语言的大规模SWE数据集
  - 提出语言无关的自动化任务收集流水线
  - 提供预构建镜像支持RL训练环境复现

---

###  13. CC-VQA：基于冲突与相关性感知的知识型视觉问答知识冲突缓解方法 (CC-VQA: Conflict- and Correlation-Aware Method for Mitigating Knowledge Conflict in Knowledge-Based Visual Question Answering)

**论文链接**: [https://arxiv.org/abs/2602.23952](https://arxiv.org/abs/2602.23952)
**组织**: Alibaba Cloud
**得分**: 34.91
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 3

**摘要**: 针对KB-VQA中静态模型知识与检索信息间的冲突，本文提出无训练方法CC-VQA。该方法包含以视觉为中心的上下文冲突推理及相关性引导编解码模块。在E-VQA等基准上达到SOTA，准确率提升3.3%至6.4%。

**亮点**:
  - 提出无训练的CC-VQA框架
  - 引入视觉信息解决知识冲突
  - 在多项基准测试中达到SOTA性能

---

###  14. MMR-Life：拼接真实生活场景的多模态多图像推理 (MMR-Life: Piecing Together Real-life Scenes for Multimodal Multi-image Reasoning)

**论文链接**: [https://arxiv.org/abs/2603.02024](https://arxiv.org/abs/2603.02024)
**组织**: ucas
**得分**: 33.01
**标签**: 
**Upvotes**: 39 | **Stars**: 8

**摘要**: 针对现有MLLM缺乏真实场景多图像推理基准的问题，提出MMR-Life基准。该数据集涵盖7种推理类型，评估显示GPT-5准确率仅58%，揭示了现有模型在跨图像整合与复杂推理方面的显著不足。

**亮点**:
  - 提出真实场景多模态多图像推理基准
  - 涵盖溯因、因果等七种推理类型
  - 揭示GPT-5等顶尖模型表现仍有巨大提升空间

---

###  15. FireRed-OCR 技术报告 (FireRed-OCR Technical Report)

**论文链接**: [https://arxiv.org/abs/2603.01840](https://arxiv.org/abs/2603.01840)
**组织**: Unknown
**得分**: 31.22
**标签**: 
**Upvotes**: 1 | **Stars**: 90

**摘要**: 针对通用 VLM 结构幻觉痛点，提出 FireRed-OCR 框架。通过构建“几何+语义”数据工厂及三阶段渐进训练（含 GRPO 强化学习），将 Qwen3-VL 转化为结构解析专家。在 OmniDocBench v1.5 上取得 92.94% SOTA 性能，超越 DeepSeek-OCR 2。

**亮点**:
  - OmniDocBench v1.5 达到 SOTA 性能
  - 构建“几何+语义”数据工厂
  - 采用三阶段渐进训练与 GRPO 强化学习

---

###  16. 基于观察与交互的规划 (Planning from Observation and Interaction)

**论文链接**: [https://arxiv.org/abs/2602.24121](https://arxiv.org/abs/2602.24121)
**组织**: University of Washington Robotics
**得分**: 30.76
**标签**: Frontier Lab
**Upvotes**: 0 | **Stars**: 4

**摘要**: 针对缺乏奖励函数和专家演示的真实机器人学习场景，提出了一种基于规划的逆向强化学习（IRL）算法，仅利用观察和交互构建世界模型。实验显示，该方法能在不到一小时内从零学会图像操作任务，样本效率和成功率显著优于现有的 IRL、RL 和行为克隆方法。

**亮点**:
  - 提出基于规划的 IRL 世界建模算法
  - 真实环境一小时内从零学习图像任务
  - 样本效率超越传统 IRL、RL 和 BC

---

###  17. Reasoning Core：面向符号预训练和后训练的可扩展程序化数据生成套件 (Reasoning Core: A Scalable Procedural Data Generation Suite for Symbolic Pre-training and Post-Training)

**论文链接**: [https://arxiv.org/abs/2603.02208](https://arxiv.org/abs/2603.02208)
**组织**: Reasoning Core
**得分**: 29.36
**标签**: 
**Upvotes**: 3 | **Stars**: 34

**摘要**: 针对现有生成器依赖固定模板、分布广度不足的问题，本文提出 Reasoning Core 套件，程序化生成涵盖逻辑规划、方程等五大核心领域的可验证符号数据。该方法利用外部求解器验证并提供推理链，支持课程设计。实验证明，混合该数据进行预训练在保持语言建模能力的同时提升了下游推理性能，且零样本评估显示对 GPT-5 等前沿模型具有挑战性。

**亮点**:
  - 涵盖五大核心领域的程序化数据生成套件
  - 集成外部求解器实现严格验证与难度控制
  - 预训练混合数据有效提升推理性能且无损语言能力

---

###  18. LaSER：将显式推理内化至密集检索的潜在空间 (LaSER: Internalizing Explicit Reasoning into Latent Space for Dense Retrieval)

**论文链接**: [https://arxiv.org/abs/2603.01425](https://arxiv.org/abs/2603.01425)
**组织**: TongyiLab
**得分**: 29.15
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 0

**摘要**: 针对密集检索无法利用 LLM 推理能力及显式推理延迟高的问题，提出 LaSER 框架。通过双视图机制将显式推理内化至潜在空间，实现了静默思考。实验表明该方法在推理密集型任务上超越 SOTA，兼顾了深度与效率。

**亮点**:
  - 提出 LaSER 自蒸馏框架
  - 双视图机制与轨迹对齐策略
  - 推理密集任务上超越 SOTA

---

###  19. ArtLLM: 利用 3D 大语言模型生成铰接式资产 (ArtLLM: Generating Articulated Assets via 3D LLM)

**论文链接**: [https://arxiv.org/abs/2603.01142](https://arxiv.org/abs/2603.01142)
**组织**: Tencent Hunyuan
**得分**: 28.03
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 针对现有方法生成可动3D物体时效率低、泛化性差的问题，本文提出了ArtLLM框架。该框架利用在大规模铰接数据集上训练的3D多模态大语言模型，从点云中自回归预测部件及运动学结构，并指导生成高保真几何。实验表明，ArtLLM在布局精度和关节预测上显著超越SOTA，且能鲁棒泛化至真实物体。

**亮点**:
  - 提出 ArtLLM 框架，利用 3D LLM 直接从点云生成铰接式资产
  - 实现部件与关节结构的统一自回归预测，支持复杂物体
  - 在 PartNet-Mobility 数据集上显著超越现有 SOTA 方法

---

###  20. 合成视觉基因组2：从视频中提取大规模时空场景图 (Synthetic Visual Genome 2: Extracting Large-scale Spatio-Temporal Scene Graphs from Videos)

**论文链接**: [https://arxiv.org/abs/2602.23543](https://arxiv.org/abs/2602.23543)
**组织**: University of Washington
**得分**: 26.59
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 0

**摘要**: 针对时空场景图数据稀缺，提出大规模SVG2数据集及TRaSER生成模型。该模型利用轨迹对齐及双重重采样机制，显著提升了物体关系与属性预测精度，并有效增强了视频问答任务的表现。

**亮点**:
  - 发布规模增加一个数量级的全景视频场景图数据集SVG2
  - 提出TRaSER模型，包含轨迹对齐及时空窗口重采样新模块
  - 关系与物体检测精度显著超越基座模型及GPT-5，提升VQA效果

---
