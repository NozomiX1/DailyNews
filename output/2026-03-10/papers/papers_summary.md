# 每日论文汇总 - 2026-03-10

**论文数量**: 24

---

### 🏆 1. 从窄视到全景视角：注意力引导的冷启动重塑多模态推理 (From Narrow to Panoramic Vision: Attention-Guided Cold-Start Reshapes Multimodal Reasoning)

**论文链接**: [https://arxiv.org/abs/2603.03825](https://arxiv.org/abs/2603.03825)
**组织**: Qwen
**得分**: 75.27
**标签**: Super Lab, Must Read
**Upvotes**: 8 | **Stars**: 8

**摘要**: 本文研究了多模态大推理模型训练中冷启动阶段的作用机制。研究者提出视觉注意力分数(VAS)指标，发现推理性能与VAS高度相关(r=0.9616)。令人惊讶的是，多模态冷启动未能提升VAS，呈现出“懒散注意力定位“现象，而纯文本冷启动反而增加VAS。为验证因果关系，研究团队设计了无需训练的注意力干预方法，推理时性能提升1-2%。进一步提出AVAR框架，整合视觉锚定数据合成、注意力引导目标和奖励塑造，在Qwen2.5-VL-7B上于7个多模态推理基准平均提升7.0%。

**亮点**:
  - 发现多模态冷启动存在“懒散注意力定位“反常现象
  - 提出VAS注意力指标，实现推理性能精准预测(r=0.9616)
  - AVAR框架使Qwen2.5-VL-7B平均提升7.0%

---

### 🏆 2. AutoResearch-RL：面向自主神经架构发现的永久自评估强化学习代理框架 (AutoResearch-RL: Perpetual Self-Evaluating Reinforcement Learning Agents for Autonomous Neural Architecture Discovery)

**论文链接**: [https://arxiv.org/abs/2603.07300](https://arxiv.org/abs/2603.07300)
**组织**: Anthropic
**得分**: 62.61
**标签**: Super Lab, Must Read
**Upvotes**: 9 | **Stars**: 0

**摘要**: 本研究提出AutoResearch-RL框架，该框架让强化学习代理能够在无人工干预的情况下自主进行神经架构和超超参数研究。核心设计将任务分解为：冻结的环境（保证实验公平性）、可变的目标训练脚本（代理的可编辑状态）、以及累积实验结果以指导后续决策的元学习器。代理通过近端策略优化（PPO）算法学习，根据验证bits-per-byte（val-bpb）奖励信号进行策略更新。在单GPU纳米聊天预训练基准上的实验表明，AutoResearch-RL能在约300次夜间迭代后自动发现与人工调优基线相当或更优的配置。

**亮点**:
  - 提出AutoResearch-RL框架，实现完全自主的神经架构发现
  - 采用冻结环境+可变目标脚本+元学习器三分离设计保证公平比较
  - 单GPU上约300次迭代即可达到或超越人工调优基线性能

---

###  3. LoGeR：基于混合内存的长上下文几何重建 (LoGeR: Long-Context Geometric Reconstruction with Hybrid Memory)

**论文链接**: [https://arxiv.org/abs/2603.03269](https://arxiv.org/abs/2603.03269)
**组织**: Deepmind
**得分**: 102.99
**标签**: Super Lab
**Upvotes**: 42 | **Stars**: 227

**摘要**: 本论文针对前馈几何基础模型在扩展到分钟级长视频时面临的二次注意力复杂度或有限内存问题，提出LoGeR架构。该方法将视频分块处理，利用强双向先验进行块内高保真推理。核心创新在于学习-based混合内存模块：参数化TTT内存锚定全局坐标框架防止尺度漂移，非参数化SWA机制保留未压缩上下文用于高精度相邻对齐。实验表明，该方法可在128帧上训练并泛化至数千帧，在KITTI上ATE降低超74%，实现全局一致的长程重建。

**亮点**:
  - 提出LoGeR架构，首次实现分钟级视频的前馈式3D几何重建
  - 混合内存模块（TTT+SWA）解决长程一致性与精度对齐难题
  - 在KITTI数据集上ATE降低超74%，达到新的SOTA性能

---

###  4. HY-WU（第一部分）：可扩展功能性神经记忆框架及在文本引导图像编辑中的实例化 (HY-WU (Part I): An Extensible Functional Neural Memory Framework and An Instantiation in Text-Guided Image Editing)

**论文链接**: [https://arxiv.org/abs/2603.07236](https://arxiv.org/abs/2603.07236)
**组织**: Tencent Hunyuan
**得分**: 58.65
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 208

**摘要**: 背景：基础模型在长时间部署中面临目标漂移、用户偏好演变和新任务出现的挑战，现有适配流程采用静态权重范式导致各目标间的妥协与干扰。方法：提出HY-WU（权重释放）框架，核心是将功能性记忆实现为神经模块，从实例条件实时合成权重更新，生成实例特定的算子。结论：该方法避免了测试时优化，实现了无需覆写共享权重的持续学习和即时个性化。

**亮点**:
  - 提出功能性神经记忆框架HY-WU，实现实例级权重动态生成
  - 避免持续学习中的权重覆写与灾难性遗忘问题
  - 无需测试时优化即可实现即时个性化适配

---

###  5. Holi-Spatial：将视频流演化为整体性3D空间智能 (Holi-Spatial: Evolving Video Streams into Holistic 3D Spatial Intelligence)

**论文链接**: [https://arxiv.org/abs/2603.07660](https://arxiv.org/abs/2603.07660)
**组织**: Unknown
**得分**: 51.29
**标签**: 
**Upvotes**: 69 | **Stars**: 110

**摘要**: 本研究针对空间智能研究中大规模细粒度3D数据稀缺的难题，提出Holi-Spatial——首个全自动、大规模、空间感知的多模态数据集构建管道。该方法从原始视频输入自动构建3D高斯溅射（3DGS）重建、对象级语义标注及空间问答对，无需人工干预。最终构建的Holi-Spatial-4M包含12K个3DGS场景、320K个3D边界框和1.2M个空间QA对。实验表明，该方法在ScanNet、ScanNet++和DL3DV数据集上显著优于现有前馈和每场景优化方法，微调视觉语言模型后空间推理性能也获得显著提升。

**亮点**:
  - 首个全自动大规模3D空间智能数据集构建管道
  - 构建Holi-Spatial-4M：含12K 3DGS场景、1.2M空间QA对的大规模数据集
  - 在ScanNet等基准数据集上显著超越现有方法

---

###  6. 故事中迷失：大型语言模型长篇故事生成中的一致性缺陷 (Lost in Stories: Consistency Bugs in Long Story Generation by LLMs)

**论文链接**: [https://arxiv.org/abs/2603.05890](https://arxiv.org/abs/2603.05890)
**组织**: Unknown
**得分**: 45.48
**标签**: 
**Upvotes**: 74 | **Stars**: 40

**摘要**: 本研究针对LLM长篇故事生成中的一致性问题提出解决方案。当前的故事生成基准主要关注情节质量和流畅性，缺乏对一致性错误的系统评估。研究团队构建了ConStory-Bench基准，包含2000个跨四个任务场景的提示，并定义了包含19个细分子类别的五类错误分类法。同时开发了ConStory-Checker自动管道，可检测矛盾并提供明确的文本证据。通过对多种LLM的评估发现：一致性错误最常出现在事实和时间维度、倾向于发生在叙事中部和高熵文本段中，且某些错误类型存在共现趋势。

**亮点**:
  - 提出ConStory-Bench基准，系统评估长篇故事生成的叙事一致性
  - 定义五类错误分类法（19个子类别），覆盖事实、时间、人物等维度
  - 发现一致性错误的时间与位置分布规律

---

###  7. HiAR：基于层级去噪的高效自回归长视频生成方法 (HiAR: Efficient Autoregressive Long Video Generation via Hierarchical Denoising)

**论文链接**: [https://arxiv.org/abs/2603.08703](https://arxiv.org/abs/2603.08703)
**组织**: Unknown
**得分**: 39.62
**标签**: 
**Upvotes**: 24 | **Stars**: 41

**摘要**: 自回归扩散模型在生成长视频时面临时间连续性维护和错误累积导致的逐步质量下降问题。现存方法通过在高度去噪的上下文上条件化来确保连续性，但这会加剧错误传播。本文提出HiAR层级去噪框架，核心思想是在与当前块相同噪声水平的上下文中进行条件处理，实现跨所有块的因果生成。此外，引入前向KL正则化器以保留运动多样性。在VBench 20秒视频生成任务中，HiAR达到最佳整体评分且时间漂移最低，推理速度提升1.8倍。

**亮点**:
  - 提出层级去噪框架HiAR，解决自回归长视频生成中的错误累积问题
  - 实现因果生成跨所有去噪步骤，推理速度提升1.8倍
  - VBench 20秒生成任务中达到SOTA整体评分，时间漂移最低

---

###  8. CoCo：代码即思维链的文本到图像预览与稀有概念生成 (CoCo: Code as CoT for Text-to-Image Preview and Rare Concept Generation)

**论文链接**: [https://arxiv.org/abs/2603.08652](https://arxiv.org/abs/2603.08652)
**组织**: Unknown
**得分**: 38.31
**标签**: 
**Upvotes**: 29 | **Stars**: 28

**摘要**: 现有基于思维链(CoT)的文本到图像生成方法主要依赖抽象自然语言规划，难以精确处理复杂空间布局和结构化视觉元素。本研究提出CoCo框架，将推理过程表示为可执行代码：首先生成指定场景结构布局的代码，在沙盒环境中执行渲染确定性草图图像，再通过细粒度图像编辑优化生成最终高保真结果。为训练该模型，构建了CoCo-10K数据集。实验在StructT2IBench、OneIG-Bench和LongText-Bench上分别比直接生成提升68.83%、54.8%和41.23%，优于其他CoT增强方法，验证了代码驱动推理在精确可控文本到图像生成中的有效性。

**亮点**:
  - 代码即思维链(Code-as-CoT)新范式，实现可验证的中间规划
  - 构建CoCo-10K结构化草图-成图配对数据集
  - 在三个基准测试上显著优于直接生成和其他CoT方法

---

###  9. 突破训练瓶颈：代码模型的高效稳定强化学习 (Breaking Training Bottlenecks: Effective and Stable Reinforcement Learning for Coding Models)

**论文链接**: [https://arxiv.org/abs/2603.07777](https://arxiv.org/abs/2603.07777)
**组织**: Microsoft Research
**得分**: 35.74
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 2

**摘要**: 针对现代代码生成模型输出更长、能力增长更快、训练动态变化导致传统训练方法失效的问题，微软提出MicroCoder-GRPO改进的组相对策略优化方法，包含条件截断掩码、多样性温度选择和高裁剪率KL损失移除三个创新。在LiveCodeBench v6上相比强基线提升17.6%，扩展上下文评估下提升更显著。发布的新训练数据集MicroCoder-Dataset在300步内比主流数据集性能提升3倍，评估框架准确率提升约25%速度提升约40%。

**亮点**:
  - 提出MicroCoder-GRPO三创新突破代码模型训练瓶颈
  - LiveCodeBench v6相对提升17.6%，扩展上下文评估收益更显著
  - 发布MicroCoder-Dataset训练语料，300步内性能提升3倍

---

###  10. Sparse-BitNet：1.58位LLM天然适配半结构化稀疏化 (Sparse-BitNet: 1.58-bit LLMs are Naturally Friendly to Semi-Structured Sparsity)

**论文链接**: [https://arxiv.org/abs/2603.05168](https://arxiv.org/abs/2603.05168)
**组织**: Microsoft Research
**得分**: 34.91
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 3

**摘要**: 半结构化N:M稀疏性和低比特量化是提升LLM效率的两条主要路径，但此前研究相对独立。本文首次探索二者结合，发现1.58-bit BitNet比全精度模型更适配N:M稀疏化。提出Sparse-BitNet统一框架，创新性地联合实现1.58-bit量化与动态N:M稀疏化，并确保训练稳定性。实验表明，在多种模型规模和训练模式下，1.58-bit BitNet在相同稀疏度下性能下降显著小于全精度基线，可容忍更高结构化稀疏度才出现精度崩溃。借助自定义稀疏张量核心，训练和推理阶段均实现高达1.30倍加速。

**亮点**:
  - 首次提出Sparse-BitNet统一框架，实现1.58-bit量化与N:M稀疏化联合训练
  - 1.58-bit BitNet比全精度模型更适配半结构化稀疏，性能下降更小
  - 自定义稀疏张量核心实现训练推理双重加速，最高1.30倍

---

###  11. NLE：基于非自回归LLM的转录编辑语音识别 (NLE: Non-autoregressive LLM-based ASR by Transcript Editing)

**论文链接**: [https://arxiv.org/abs/2603.08397](https://arxiv.org/abs/2603.08397)
**组织**: IBM
**得分**: 34.64
**标签**: Frontier Lab
**Upvotes**: 14 | **Stars**: 0

**摘要**: 针对自回归LLM语音识别系统因顺序解码导致的高延迟问题，IBM提出NLE非自回归方法，将语音识别重构为条件转录编辑任务。该方法从预训练语音编码器提取声学嵌入和初始假设，通过双向LLM编辑器利用潜在对齐目标进行优化，并采用交错填充策略利用Transformer身份映射偏差。在Open ASR leaderboard上，NLE++实现5.67%平均WER，RTFx达1630；单 utterance场景下相比AR基线获得27倍加速，显著提升了实时语音识别的可行性。

**亮点**:
  - NAR方法实现5.67% WER的领先性能
  - 27倍加速突破AR模型的延迟瓶颈
  - 创新性转录编辑范式替代自回归解码

---

###  12. 扩展智能体能力而非上下文：大规模工具空间的高效强化微调 (Scaling Agentic Capabilities, Not Context: Efficient Reinforcement Finetuning for Large Toolspaces)

**论文链接**: [https://arxiv.org/abs/2603.06713](https://arxiv.org/abs/2603.06713)
**组织**: Microsoft Research
**得分**: 34.58
**标签**: Frontier Lab
**Upvotes**: 13 | **Stars**: 0

**摘要**: 研究背景：智能体系统在大规模工具生态中面临长程任务规划与弱监督挑战，小语言模型（SLM）易出现上下文饱和、执行错误累积及奖励稀疏问题。核心方法：提出ATLAS框架，包含两项关键贡献——将上下文控制与执行结构作为可学习决策，结合迭代式工具加载与程序化工具编排以约束上下文增长；提出基于评分标准的强化微调，将任务成功分解为结构化准则并使用小型评判模型实现可扩展训练。实验结论：在MCP基准上，相较通用RL基线取得显著提升，4B参数的SLM在更紧凑的参数与上下文预算下达到前沿智能体性能水平。

**亮点**:
  - 提出ATLAS框架，解决大规模工具空间下SLM的上下文饱和与执行错误问题
  - 创新性采用基于评分标准的强化微调，利用小型评判模型实现可扩展训练
  - 4B参数SLM在紧凑预算下接近前沿智能体性能

---

###  13. TDM-R1: 利用不可微奖励强化少步扩散模型 (TDM-R1: Reinforcing Few-Step Diffusion Models with Non-Differentiable Reward)

**论文链接**: [https://arxiv.org/abs/2603.07700](https://arxiv.org/abs/2603.07700)
**组织**: HKUST
**得分**: 34.53
**标签**: 
**Upvotes**: 12 | **Stars**: 30

**摘要**: 少步生成模型降低了图像和视频生成成本，但现有强化学习方法严重依赖可微奖励模型，无法利用人类二元喜好、物体计数等重要的不可微奖励信号。本文提出TDM-R1强化学习范式，基于Trajectory Distribution Matching构建，将学习过程解耦为替代奖励学习和生成器学习，并开发了沿确定性生成轨迹获取每步奖励信号的实用方法。实验表明，TDM-R1在文本渲染、视觉质量和偏好对齐等任务上实现了域内和域外指标的SOTA性能，并可有效扩展到Z-Image模型，仅用4步NFEs即可持续超越其100步变体。

**亮点**:
  - 首次提出适用于少步扩散模型的不可微奖励强化学习范式
  - 实现域内和域外指标上的SOTA强化学习性能
  - 仅用4步NFEs即可超越100步变体的生成质量

---

###  14. CARE-Edit：用于上下文图像编辑的条件感知专家路由 (CARE-Edit: Condition-Aware Routing of Experts for Contextual Image Editing)

**论文链接**: [https://arxiv.org/abs/2603.08589](https://arxiv.org/abs/2603.08589)
**组织**: Unknown
**得分**: 33.95
**标签**: 
**Upvotes**: 30 | **Stars**: 12

**摘要**: 针对现有统一扩散编辑器存在的任务干扰和异构需求适应难题，本文提出条件感知专家路由（CARE-Edit）方法。该架构通过轻量级latent-attention路由器将扩散token动态分配给Text、Mask、Reference、Base四个专门专家，采用Mask Repaint模块细化空间引导，并使用稀疏top-K选择和Latent Mixture模块融合多专家输出。实验表明该方法在擦除、替换、文本驱动编辑和风格迁移等上下文编辑任务上表现优异，有效缓解了多条件输入下的颜色渗透和风格漂移问题。

**亮点**:
  - 提出Condition-Aware路由机制，动态分配计算资源给专门专家
  - 多模态条件感知处理，缓解多条件冲突导致的颜色渗透和风格漂移
  - 在上下文图像编辑任务（擦除、替换、风格迁移等）取得良好效果

---

###  15. 百万基准测试：语言代理与人类专家的差距有多大？ (\$OneMillion-Bench: How Far are Language Agents from Human Experts?)

**论文链接**: [https://arxiv.org/abs/2603.07980](https://arxiv.org/abs/2603.07980)
**组织**: Beijing Institute for General Artificial Intelligence
**得分**: 33.7
**标签**: 
**Upvotes**: 22 | **Stars**: 15

**摘要**: 随着语言模型从聊天助手演变为能够进行多步推理和工具使用的长期代理，现有基准测试仍局限于结构化或考试风格任务，难以满足现实专业需求。该研究提出OneMillion-Bench基准测试，包含400个专家策划的任务，涵盖法律、金融、工业、医疗和自然科学领域，要求代理检索权威来源、解决冲突证据、应用领域特定规则并做出约束决策。评估协议采用基于评分标准的方式，评估事实准确性、逻辑一致性、实践可行性和专业合规性，旨在为领域密集型场景中的代理可靠性、专业深度和实践准备情况提供统一测试平台。

**亮点**:
  - 提出涵盖5大专业领域、400个专家策划任务的OneMillion-Bench基准测试
  - 采用多维度评分协议评估代理的事实准确性、逻辑一致性和专业合规性
  - 专注于经济后果重大的真实世界专业场景，填补现有基准测试空白

---

###  16. OfficeQA Pro：面向企业级端到端基于文档推理的评估基准 (OfficeQA Pro: An Enterprise Benchmark for End-to-End Grounded Reasoning)

**论文链接**: [https://arxiv.org/abs/2603.08655](https://arxiv.org/abs/2603.08655)
**组织**: Databricks
**得分**: 32.01
**标签**: 
**Upvotes**: 2 | **Stars**: 73

**摘要**: 本论文提出了OfficeQA Pro基准，用于评估AI代理在大型异构文档语料库上的多文档推理能力。语料库包含近100年的美国国债公告，共89000页和超过2600万个数值，含133个需要精确文档解析、检索和分析推理的问题。实验表明，前沿LLM仅依靠参数知识时准确率不足5%，即使加上网络搜索也仅达12%；直接提供文档后平均得分34.1%。研究发现，使用Databricks的ai_parse_document生成的结构化文档表示可为代理带来16.1%的平均相对性能提升，表明结构化表示对企业级基于文档的推理任务具有重要价值。

**亮点**:
  - 构建了包含89000页和2600万数值的美国国债公告企业评估基准
  - 结构化文档表示可带来16.1%的平均相对性能提升
  - 前沿LLM在该基准上准确率均低于5%，表明存在显著改进空间

---

###  17. 规模化数据难度：通过强化学习处理新鲜且具挑战性的问题提升代码模型 (Scaling Data Difficulty: Improving Coding Models via Reinforcement Learning on Fresh and Challenging Problems)

**论文链接**: [https://arxiv.org/abs/2603.07779](https://arxiv.org/abs/2603.07779)
**组织**: Microsoft Research
**得分**: 29.15
**标签**: Frontier Lab
**Upvotes**: 4 | **Stars**: 0

**摘要**: 本研究针对代码生成模型训练中高-quality数据集稀缺的难题，提出四阶段数据处理框架，包含收集、处理、过滤、验证环节，并设计基于LLM的自动难度过滤框架（predict-calibrate-select），采用五维难度度量指标筛选挑战性问题。创建的MicroCoder数据集包含数万道精选竞赛编程题。在严格未见的LiveCodeBench基准上，该数据集在300训练步内实现3倍性能提升，中难题表现持续优于基线，整体性能最高提升17.2%，验证了难度感知的数据策展能有效提升模型在挑战性任务上的表现。

**亮点**:
  - 提出四阶段数据处理框架与LLM难度过滤机制
  - MicroCoder数据集使300步训练获得3倍性能提升
  - 中难题上实现最高17.2%相对性能提升

---

###  18. MWM：动作条件一致性预测的移动世界模型 (MWM: Mobile World Models for Action-Conditioned Consistent Prediction)

**论文链接**: [https://arxiv.org/abs/2603.07799](https://arxiv.org/abs/2603.07799)
**组织**: Peking University
**得分**: 27.69
**标签**: Frontier Lab
**Upvotes**: 0 | **Stars**: 2

**摘要**: 现有导航世界模型缺乏动作条件一致性，多步 rollout 时视觉预测会漂移从而影响规划效果。为解决此问题，本文提出 MWM 移动世界模型，采用两阶段训练框架结合结构预训练与动作条件一致性（ACC）后训练，并引入推理一致性状态蒸馏（ICSD）实现少步扩散蒸馏。实验在基准和真实世界任务中验证了视觉保真度、轨迹准确性和规划成功率的一致性提升。

**亮点**:
  - 提出两阶段训练框架结合 ACC 后训练提升动作条件一致性
  - 引入 ICSD 少步扩散蒸馏方法保持 rollout 一致性
  - 在视觉保真度、轨迹准确性和规划成功率上获一致提升

---

###  19. PureCC：文本到图像概念定制的纯学习 (PureCC: Pure Learning for Text-to-Image Concept Customization)

**论文链接**: [https://arxiv.org/abs/2603.07561](https://arxiv.org/abs/2603.07561)
**组织**: Kling Team
**得分**: 27.47
**标签**: 
**Upvotes**: 8 | **Stars**: 12

**摘要**: 现有概念定制方法在高质量和多样化概念定制方面取得显著成果，但常忽视学习新概念时对原始模型行为和能力的影响。为此，PureCC提出一种解耦学习目标，将目标概念的隐式指导与原始条件预测相结合，使模型在训练时能保持对原始能力的关注。基于此目标，PureCC设计了双分支训练流程，包括冻结提取器提供纯化目标概念表示作为隐式指导，以及可训练流模型生成原始条件预测，共同实现个性化概念的纯学习。此外，引入自适应引导尺度λ*动态调整目标概念的引导强度，平衡定制保真度与模型保持。实验表明，PureCC在保持原始行为和能力的同时实现了高保真概念定制的最先进性能。

**亮点**:
  - 提出解耦学习目标实现概念定制中的纯学习
  - 双分支训练流程保持原始模型能力
  - 引入自适应引导尺度平衡定制与保真度

---

###  20. 尺度空间扩散 (Scale Space Diffusion)

**论文链接**: [https://arxiv.org/abs/2603.08709](https://arxiv.org/abs/2603.08709)
**组织**: Unknown
**得分**: 26.0
**标签**: 
**Upvotes**: 7 | **Stars**: 11

**摘要**: 本研究揭示了扩散模型中高噪声状态仅包含与小型下采样图像相当信息的特性，指出在高分辨率下处理噪声状态是一种计算浪费。为解决这一问题，论文提出将尺度空间理论融入扩散过程，采用下采样作为线性降质操作，设计了尺度空间扩散框架。同时引入Flexi-UNet架构，支持分辨率保持和分辨率提升的去噪操作。实验在CelebA和ImageNet数据集上验证了框架的有效性，并分析了不同分辨率和网络深度下的扩展行为。

**亮点**:
  - 提出将尺度空间理论融入扩散模型的新框架
  - 高噪声扩散状态信息量不超过小型下采样图像
  - Flexi-UNet支持分辨率保持和提升的去噪

---

###  21. CaTok：利用 Mean Flow 实现一维因果图像 Token 化 (CaTok: Taming Mean Flows for One-Dimensional Causal Image Tokenization)

**论文链接**: [https://arxiv.org/abs/2603.06449](https://arxiv.org/abs/2603.06449)
**组织**: ShareLab-SII
**得分**: 25.89
**标签**: 
**Upvotes**: 5 | **Stars**: 13

**摘要**: 本研究针对自回归语言模型的因果tokenization难以扩展到视觉领域的问题，提出CaTok——一种基于MeanFlow解码器的一维因果图像tokenizer。该方法通过跨时间间隔选择tokens并绑定至MeanFlow目标，学习支持快速一步生成和高保真多步采样的因果1D表示。同时引入REPA-A正则化，将encoder特征与视觉基础模型对齐以加速训练。实验表明，CaTok在ImageNet重建任务上达到SOTA水平，FID为0.75，PSNR为22.53，SSIM为0.674，且训练轮次更少。

**亮点**:
  - 提出首个基于MeanFlow的一维因果图像tokenizer CaTok
  - ImageNet重建达到SOTA：0.75 FID、22.53 PSNR、0.674 SSIM
  - 支持快速一步生成与高保真多步采样，训练效率提升

---

###  22. 视觉基础模型的通用知识蒸馏用于语义分割 (Generalizable Knowledge Distillation from Vision Foundation Models for Semantic Segmentation)

**论文链接**: [https://arxiv.org/abs/2603.02554](https://arxiv.org/abs/2603.02554)
**组织**: Unknown
**得分**: 24.86
**标签**: 
**Upvotes**: 2 | **Stars**: 20

**摘要**: 本研究针对知识蒸馏在语义分割中忽视域外泛化能力的问题。传统KD方法在蒸馏视觉基础模型(VFMs)时往往损害其对未知数据的鲁棒性。为此提出GKD框架，采用两阶段策略：第一阶段通过选择性特征蒸馏学习领域无关表示，第二阶段冻结表示进行任务适应以减轻过拟合。此外引入基于查询的软蒸馏机制，学生特征作为查询从教师模型检索可迁移空间知识。在5个域泛化基准的实验中，F2F蒸馏提升1.9%，F2L蒸馏提升10.6%。

**亮点**:
  - 提出多阶段GKD框架增强域泛化能力
  - 引入基于查询的软蒸馏机制选择性提取VFM知识
  - 在F2F和F2L蒸馏场景分别提升1.9%和10.6%

---

###  23. CAST：用于一致性视频检索的视觉状态转换建模 (CAST: Modeling Visual State Transitions for Consistent Video Retrieval)

**论文链接**: [https://arxiv.org/abs/2603.08648](https://arxiv.org/abs/2603.08648)
**组织**: Google
**得分**: 24.56
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 0

**摘要**: 随着长视频内容创作的兴起，将短片段组合成连贯的故事线变得愈发重要。然而，现有视频检索方法在推理时缺乏上下文感知，优先考虑局部语义对齐而忽视状态和身份一致性。本文正式定义了一致性视频检索（CVR）任务，并在YouCook2、COIN和CrossTask数据集上构建了诊断基准。提出CAST（上下文感知状态转换）方法，这是一种轻量级即插即用的适配器，可兼容多种冻结的视觉-语言嵌入空间。CAST通过从视觉历史预测状态条件残差更新（Δ），为潜在状态演化引入显式归纳偏置。实验表明，CAST在YouCook2和CrossTask上显著提升性能，在COIN上保持竞争力，并在多种基础骨干网络上一致超越零样本基线。此外，CAST还能为黑盒视频生成候选（如Veo）提供有用的重排序信号，促进时间上更连贯的延续。

**亮点**:
  - 提出一致性视频检索（CVR）新任务及诊断基准
  - CAST方法作为即插即用适配器，兼容多种视觉-语言模型
  - 为Veo等视频生成模型提供有效重排序信号

---

###  24. ByteFlow：基于自适应字节压缩的无分词器语言建模 (ByteFlow: Language Modeling through Adaptive Byte Compression without a Tokenizer)

**论文链接**: [https://arxiv.org/abs/2603.03583](https://arxiv.org/abs/2603.03583)
**组织**: Amazon
**得分**: 24.56
**标签**: Frontier Lab
**Upvotes**: 1 | **Stars**: 0

**摘要**: 现有语言模型依赖固定的子词分词器，导致模型粒度僵化。本研究提出ByteFlow Net，一种全新的层次化架构，彻底去除分词器，让模型自主学习将原始字节流分割为语义单元。该方法基于潜在表示的编码率进行压缩驱动分割，通过Top-K选择保持静态计算图。实验表明，基于压缩的分块策略显著优于基于BPE的Transformer和既往字节级架构，证明了端到端无分词器建模不仅可行而且更加有效。

**亮点**:
  - 提出ByteFlow Net层次化架构，实现无分词器自适应字节压缩
  - 基于编码率的压缩驱动分割，学习语义有意义的分块边界
  - 性能超越BPE基Transformer和既往字节级架构

---
