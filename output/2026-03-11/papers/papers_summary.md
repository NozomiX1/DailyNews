# 每日论文汇总 - 2026-03-11

**论文数量**: 11

---

###  1. MM-Zero：零数据自进化的多模型视觉语言模型 (MM-Zero: Self-Evolving Multi-Model Vision Language Models From Zero Data)

**论文链接**: [https://arxiv.org/abs/2603.09206](https://arxiv.org/abs/2603.09206)
**组织**: NVIDIA
**得分**: 60.49
**标签**: Frontier Lab
**Upvotes**: 36 | **Stars**: 34

**摘要**: 本文提出MM-Zero，首个基于强化学习的VLM零数据自进化框架。不同于之前的两角色设置，该框架引入三角色自进化训练架构：Proposer生成抽象视觉概念并制定问题，Coder将概念转化为可执行代码渲染视觉图像，Solver对生成内容进行多模态推理。三个角色均从同一基础模型初始化，使用GRPO训练并结合执行反馈、视觉验证和难度平衡机制。实验表明MM-Zero在多种多模态基准测试上提升了VLM推理性能，为多模态模型的自改进提供了可扩展路径。

**亮点**:
  - 首个实现VLM零数据自进化的RL框架
  - 提出三角色自进化架构（Proposer/Coder/Solver）
  - 在多模态基准测试上取得SOTA性能

---

###  2. 几何引导的强化学习用于多视角一致的3D场景编辑 (Geometry-Guided Reinforcement Learning for Multi-view Consistent 3D Scene Editing)

**论文链接**: [https://arxiv.org/abs/2603.03143](https://arxiv.org/abs/2603.03143)
**组织**: AMAP-ML
**得分**: 52.49
**标签**: 
**Upvotes**: 125 | **Stars**: 82

**摘要**: 利用2D扩散模型先验进行3D编辑是新兴范式，但多视角一致性保持仍是难题，且3D一致编辑配对数据极度稀缺导致监督微调不可行。本文提出RL3DEdit框架，巧妙地将3D一致性验证任务交给强化学习，而非生成任务。利用VGGT模型的鲁棒先验，将编辑图像输入后通过置信度图和姿态估计误差构建奖励信号，有效将2D编辑先验锚定到3D一致流形上。实验表明该方法实现了稳定的多视角一致性，在编辑质量和效率上超越现有SOTA方法。

**亮点**:
  - 创新性将3D一致性验证任务分配给RL而非生成任务
  - 利用VGGT模型的置信度图和姿态误差作为奖励信号实现3D一致性
  - 在编辑质量和效率上超越现有SOTA方法

---

###  3. Omni-Diffusion：基于掩码离散扩散的统一多模态理解与生成 (Omni-Diffusion: Unified Multimodal Understanding and Generation with Masked Discrete Diffusion)

**论文链接**: [https://arxiv.org/abs/2603.06577](https://arxiv.org/abs/2603.06577)
**组织**: Nanjing University
**得分**: 44.43
**标签**: 
**Upvotes**: 37 | **Stars**: 62

**摘要**: 当前多模态大语言模型主要采用自回归架构，存在效率与架构创新空间。本研究提出Omni-Diffusion，首个基于掩码离散扩散的任意到任意多模态语言模型，统一处理文本、语音和图像的理解与生成。该方法直接建模离散多模态token的联合分布，支持双模态及多模态任务。实验在多种基准数据集上取得领先或持平性能，验证了离散扩散模型作为多模态基础模型架构的巨大潜力。

**亮点**:
  - 首个基于掩码离散扩散的统一多模态模型
  - 支持文本、语音、图像的任意到任意转换
  - 在多模态基准测试中达到领先性能

---

###  4. InternVL-U：面向理解、推理、生成与编辑的统一多模态模型平民化 (InternVL-U: Democratizing Unified Multimodal Models for Understanding, Reasoning, Generation and Editing)

**论文链接**: [https://arxiv.org/abs/2603.09877](https://arxiv.org/abs/2603.09877)
**组织**: Unknown
**得分**: 44.33
**标签**: 
**Upvotes**: 28 | **Stars**: 86

**摘要**: 统一多模态模型在保持语义理解与生成能力之间存在固有权衡。本文提出InternVL-U，一个轻量级4B参数的统一多模态模型。核心设计采用统一上下文建模与模偶特定模块化架构，结合解耦视觉表示，集成SOTA多模态大语言模型与MMDiT视觉生成头。针对高语义密度任务构建了基于CoT推理的数据合成管道。实验表明，4B参数的InternVL-U在生成和编辑任务上超越了3倍以上规模的BAGEL等基线模型，同时保持强大的多模态理解和推理能力，实现了性能与效率的优异平衡。

**亮点**:
  - 4B参数超越14B模型，性能效率比优异
  - 提出统一上下文建模与解耦视觉表示的新架构
  - 构建基于CoT推理的高语义密度任务数据合成管道

---

###  5. 让视觉语言模型走上球场：体育空间智能基准测试 (Stepping VLMs onto the Court: Benchmarking Spatial Intelligence in Sports)

**论文链接**: [https://arxiv.org/abs/2603.09896](https://arxiv.org/abs/2603.09896)
**组织**: Unknown
**得分**: 40.66
**标签**: 
**Upvotes**: 21 | **Stars**: 52

**摘要**: 体育运动是测试视觉语言模型空间智能的理想场景，因为其涉及高强度人体运动和动态物体交互。本文提出CourtSI，这是首个针对体育场景的大规模空间智能数据集，包含超过100万QA对，涵盖空间计数、距离测量、定位和关系推理，涵盖羽毛球、网球和乒乓球等代表性网运动。实验在3686个QA对的CourtSI-Bench上评估了25个VLM模型，揭示了人类-AI性能差距及现有基准的泛化局限性。在CourtSI上微调Qwen3-VL-8B后，准确率提升23.5个百分点，并能有效泛化到未见运动类型，展现了体育场景作为推进VLM空间智能的可行路径。

**亮点**:
  - 首个体育场景大规模空间智能数据集CourtSI，包含100万+ QA对
  - 在CourtSI-Bench上评估25个VLM模型，揭示人类-AI性能差距
  - 微调Qwen3-VL-8B准确率提升23.5%，展现良好泛化能力

---

###  6. 思考召回：推理如何解锁LLM的参数知识 (Thinking to Recall: How Reasoning Unlocks Parametric Knowledge in LLMs)

**论文链接**: [https://arxiv.org/abs/2603.09906](https://arxiv.org/abs/2603.09906)
**组织**: Google
**得分**: 40.24
**标签**: Frontier Lab
**Upvotes**: 45 | **Stars**: 0

**摘要**: 本研究探讨了推理在LLM中对简单单跳事实问题的作用。研究发现，启用推理能够显著扩展模型的参数知识召回能力，使原本无法触及的正确答案变得可获取。通过设计的受控实验，研究团队识别出两大关键机制：(1)计算缓冲效应——模型利用生成的推理token进行独立于语义内容的潜在计算；(2)事实 priming——生成主题相关事实作为语义桥梁促进正确答案检索。同时，研究揭示了 generative self-retrieval 机制的风险：推理过程中的幻觉会增加最终答案的幻觉概率。最终表明，通过优先选择无幻觉的事实推理轨迹可直接提升模型准确性。

**亮点**:
  - 启用推理可解锁LLM参数知识召回的新能力
  - 揭示计算缓冲效应和事实 priming 两大核心机制
  - 推理过程中的幻觉会传播并增加最终答案的幻觉风险

---

###  7. VLM-SubtleBench：视觉语言模型与人类级细微比较推理的差距还有多大？ (VLM-SubtleBench: How Far Are VLMs from Human-Level Subtle Comparative Reasoning?)

**论文链接**: [https://arxiv.org/abs/2603.07888](https://arxiv.org/abs/2603.07888)
**组织**: KRAFTON
**得分**: 25.79
**标签**: 
**Upvotes**: 9 | **Stars**: 8

**摘要**: 本论文提出了VLM-SubtleBench基准，用于评估视觉语言模型（VLMs）在细微比较推理方面的能力。研究背景是现有比较推理基准主要关注差异显著的图像，无法满足工业异常检测、医学影像等实际应用对细微差异识别的需求。该基准涵盖10种差异类型（属性、状态、情感、时间、空间、存在、数量、质量、视角、行动），并覆盖工业、空中、医学等多个领域。实验对多个专有和开源VLM进行评估，结果揭示了模型与人类性能之间存在系统性差距，为未来VLM在细微比较推理方面的改进提供了基础。

**亮点**:
  - 提出首个针对细微比较推理的VLM基准VLM-SubtleBench
  - 涵盖10种差异类型，跨越工业、空中、医学等多个领域
  - 揭示VLM与人类在细微差异识别上的系统性性能差距

---

###  8. MiniAppBench：评估 LLM 驱动的助手从文本响应向交互式 HTML 响应转变 (MiniAppBench: Evaluating the Shift from Text to Interactive HTML Responses in LLM-Powered Assistants)

**论文链接**: [https://arxiv.org/abs/2603.09652](https://arxiv.org/abs/2603.09652)
**组织**: Unknown
**得分**: 24.56
**标签**: 
**Upvotes**: 8 | **Stars**: 7

**摘要**: 随着大语言模型在代码生成方面的进展，人类与AI的交互正从静态文本向动态交互式HTML应用（称MiniApps）转变。然而现有基准测试主要关注算法正确性或静态布局重建，无法评估此类新范式的能力。为填补空白，论文提出MiniAppBench——首个评估原则驱动交互式应用生成的综合基准，从拥有10M+生成的真实应用中提炼500个任务，涵盖游戏、科学、工具等六领域。同时提出MiniAppEval智能体评估框架，利用浏览器自动化进行类人探索性测试，从意图、静态、动态三维度评估。实验表明当前LLM生成高质量MiniApps仍面临重大挑战，而MiniAppEval与人类判断高度一致。

**亮点**:
  - 首个评估交互式HTML应用生成的综合基准 MiniAppBench
  - 提出基于浏览器自动化的智能体评估框架 MiniAppEval
  - 当前LLM在生成高质量MiniApps方面仍面临重大挑战

---

###  9. 言出必行：用于指令跟随的语音提示数据集 (Do What I Say: A Spoken Prompt Dataset for Instruction-Following)

**论文链接**: [https://arxiv.org/abs/2603.09881](https://arxiv.org/abs/2603.09881)
**组织**: Unknown
**得分**: 24.01
**标签**: 
**Upvotes**: 6 | **Stars**: 8

**摘要**: 语音大型语言模型（SLLMs）发展迅速，但现有评估多基于文本提示，无法反映真实语音交互场景。本研究提出DOWIS数据集，包含9个任务、11种语言的人工录制语音和文本提示，每对任务-语言提供10种提示变体，覆盖五种风格。基于该数据集对主流SLLMs进行基准测试，发现文本提示始终优于语音提示，尤其在低资源和跨语言场景；仅在语音输出任务中，语音提示才能缩小性能差距。研究强调了SLLM评估中引入语音提示的必要性。

**亮点**:
  - 提出首个多语言语音提示基准数据集DOWIS，涵盖11种语言
  - 揭示文本提示在SLLM评估中普遍优于语音提示
  - 发现语音输出任务中语音提示可弥补性能差距

---

###  10. 基于对角蒸馏的流式自回归视频生成 (Streaming Autoregressive Video Generation via Diagonal Distillation)

**论文链接**: [https://arxiv.org/abs/2603.09488](https://arxiv.org/abs/2603.09488)
**组织**: The Chinese University of Hong Kong
**得分**: 23.24
**标签**: 
**Upvotes**: 5 | **Stars**: 8

**摘要**: 本研究针对预训练扩散模型在实时流式视频生成中的计算效率问题，提出Diagonal Distillation方法。现有视频蒸馏方法沿用图像技术，忽视时间依赖性，导致运动一致性下降和误差累积。核心创新在于采用不对称生成策略：早期多步去噪、后期少步处理，使后续块继承早期块的丰富外观信息，并通过隐式光流建模保持运动质量。该方法在对齐隐式噪声预测与实际推理条件的同时，有效缓解了误差传播。实验表明，该方法可在2.61秒内生成5秒视频，达到31 FPS，实现277.3倍加速。

**亮点**:
  - 提出Diagonal Distillation对角蒸馏方法，突破视频蒸馏的时间依赖性难题
  - 采用早期多步-后期少步的不对称生成策略，缓解误差累积与饱和问题
  - 实现277.3倍加速，达到31 FPS实时视频生成性能

---

###  11. 面向生成式视频创作的文本原生界面 (A Text-Native Interface for Generative Video Authoring)

**论文链接**: [https://arxiv.org/abs/2603.09072](https://arxiv.org/abs/2603.09072)
**组织**: Adobe
**得分**: 20.69
**标签**: Frontier Lab
**Upvotes**: 0 | **Stars**: 0

**摘要**: 视频创作需要学习专业复杂的工具，而文本写作是人们自然掌握的能力。本文提出Doki，一个文本原生生成式视频创作界面，将视频创作与自然文本写作过程对齐。在Doki中，文本写作是主要交互方式，用户可在单一文档中定义资产、构建场景、创建镜头、精细编辑和添加音频。研究团队阐述了该文本优先方法的设计原则，并通过一系列示例展示其能力。为评估实际使用效果，进行了为期一周的部署研究，参与者涵盖不同水平的视频创作 expertise。结果表明该工作为生成式视频界面提供了 fundamental shift，开创了视觉故事创作的新方式。

**亮点**:
  - Adobe推出文本原生视频创作界面Doki
  - 以文本写作为核心交互方式定义资产、场景、镜头和音频
  - 一周部署研究验证文本优先方法的可行性与可访问性

---
