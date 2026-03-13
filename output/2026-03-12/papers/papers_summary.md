# 每日论文汇总 - 2026-03-12

**论文数量**: 14

---

### 🏆 1. OpenClaw-RL：通过对话训练任意智能体 (OpenClaw-RL: Train Any Agent Simply by Talking)

**论文链接**: [https://arxiv.org/abs/2603.10165](https://arxiv.org/abs/2603.10165)
**组织**: Princeton AI Lab
**得分**: 88.41
**标签**: Frontier Lab, Viral
**Upvotes**: 70 | **Stars**: 2035

**摘要**: 现有智能体强化学习系统未将交互产生的下一状态信号作为在线学习源。本研究提出OpenClaw-RL框架，核心观点是下一状态信号是通用的，策略可同时从所有信号中学习。这些信号包含两类信息：一是评估信号，通过过程奖励模型（PRM）提取为标量奖励；二是指令信号，通过事后引导的策略内蒸馏（OPD）恢复。框架采用异步设计，模型服务实时请求、PRM评判交互、训练器更新策略三者并行。实验表明，该方法使智能体能通过用户使用自动改进，并支持终端、GUI、SWE任务和工具调用等多场景可扩展强化学习。

**亮点**:
  - 首次将下一状态信号作为智能体在线学习源
  - 提出Hindsight-Guided OPD实现指令级方向优势监督
  - 异步架构实现实时服务、评判与训练的零协调开销

---

### 🏆 2. CodePercept：面向多模态大语言模型的代码锚定视觉STEM感知 (CodePercept: Code-Grounded Visual STEM Perception for MLLMs)

**论文链接**: [https://arxiv.org/abs/2603.10757](https://arxiv.org/abs/2603.10757)
**组织**: Qwen
**得分**: 78.72
**标签**: Super Lab, Must Read
**Upvotes**: 8 | **Stars**: 15

**摘要**: 本论文探究多模态大语言模型(MLLMs)在STEM视觉推理中的失败根源——究竟是感知缺陷还是推理局限？通过系统性缩放分析，研究者发现缩放感知能力始终优于缩放推理能力，揭示感知是制约当前STEM视觉推理的关键杠杆。基于此，提出利用代码作为强大感知媒介的理念，构建了包含100万图像-描述-代码三元组的大规模数据集ICC-1M，采用代码锚定描述生成和STEM图像到代码翻译两种方法消除幻觉。同时引入STEM2Code-Eval基准，通过代码生成重建图像来直接评估视觉感知能力。

**亮点**:
  - 通过系统性缩放分析发现感知是制约STEM视觉推理的关键因素
  - 提出代码作为感知媒介的新范式，构建100万规模ICC-1M数据集
  - 引入STEM2Code-Eval基准，通过代码生成实现可验证的视觉感知评估

---

### 🏆 3. 代码空间响应预言机：使用大型语言模型生成可解释的多智能体策略 (Code-Space Response Oracles: Generating Interpretable Multi-Agent Policies with Large Language Models)

**论文链接**: [https://arxiv.org/abs/2603.10098](https://arxiv.org/abs/2603.10098)
**组织**: Deepmind
**得分**: 54.16
**标签**: Super Lab, Must Read
**Upvotes**: 1 | **Stars**: 0

**摘要**: 本文提出CSRO框架，解决多智能体强化学习中策略难以解释的问题。传统PSRO方法依赖深度学习产生的黑盒策略，作者将最佳响应计算重新定义为代码生成任务，直接用LLM生成人类可读的政策代码。该方法利用LLM的预训练知识发现复杂策略，通过零样本提示、迭代优化和AlphaEvolve分布式进化系统增强性能。实验表明CSRO在性能上与基线方法相当，同时产出多样化的可解释策略。

**亮点**:
  - 提出CSRO框架，用LLM替代RL预言机生成可解释策略
  - 将策略计算重新定义为代码生成任务
  - 实现与基线相当的性能同时保留策略可解释性

---

###  4. Flash-KMeans：高速且内存高效的正则K-Means算法 (Flash-KMeans: Fast and Memory-Efficient Exact K-Means)

**论文链接**: [https://arxiv.org/abs/2603.09229](https://arxiv.org/abs/2603.09229)
**组织**: UC Berkeley
**得分**: 71.87
**标签**: Frontier Lab
**Upvotes**: 52 | **Stars**: 172

**摘要**: k-means传统上主要用于离线数据处理，作者重新审视该算法以支持现代AI系统中的在线计算需求。研究指出当前GPU实现的k-means受制于系统底层约束：赋值阶段因N×K距离矩阵在HBM中显式实例化而产生严重IO瓶颈；质心更新阶段因不规则的scatter式聚合导致硬件级原子写争用。针对这些问题，提出Flash-KMeans包含两大核心创新：FlashAssign将距离计算与在线argmin融合，完全绕过中间内存实例化；sort-inverse update构建逆映射将高争用原子scatters转化为高带宽的分段局部归约。实验在NVIDIA H200上实现最高17.9倍端到端加速，较cuML快33倍，较FAISS快200倍。

**亮点**:
  - 提出FlashAssign核方法，融合距离计算与在线argmin以消除中间内存实例化
  - 设计sort-inverse update机制，将原子写争用转为分段局部归约
  - 在NVIDIA H200上实现最高17.9倍加速，显著优于cuML和FAISS

---

###  5. LLM2Vec-Gen：大型语言模型的生成式嵌入 (LLM2Vec-Gen: Generative Embeddings from Large Language Models)

**论文链接**: [https://arxiv.org/abs/2603.10913](https://arxiv.org/abs/2603.10913)
**组织**: McGill NLP Group
**得分**: 36.76
**标签**: 
**Upvotes**: 23 | **Stars**: 26

**摘要**: 本论文提出LLM2Vec-Gen方法，解决传统基于LLM的文本嵌入器仅编码输入语义而忽视输入-输出映射的问题。该方法采用自监督范式，不直接编码输入，而是学习表示模型的潜在响应。通过向LLM词汇表添加可训练特殊token，附加到输入并优化以固定长度序列表示LLM响应，训练由LLM自身补全和蒸馏目标引导，且LLM主干保持冻结。实验在MTEB上取得最先进自监督性能，较最佳无监督嵌入教师提升9.3%；有害内容检索减少43.2%，推理能力提升29.3%；嵌入具有可解释性可解码为文本。

**亮点**:
  - MTEB自监督性能SOTA，超越最佳无监督方法9.3%
  - 创新生成式嵌入范式，学习表示LLM潜在响应
  - 可迁移LLM安全对齐和推理能力，有害内容检索减少43.2%

---

###  6. SVG-EAR：基于错误感知路由的无参数线性补偿稀疏视频生成方法 (SVG-EAR: Parameter-Free Linear Compensation for Sparse Video Generation via Error-aware Routing)

**论文链接**: [https://arxiv.org/abs/2603.08982](https://arxiv.org/abs/2603.08982)
**组织**: UC Berkeley
**得分**: 34.96
**标签**: Frontier Lab
**Upvotes**: 15 | **Stars**: 0

**摘要**: Diffusion Transformers（DiTs）已成为视频生成的主流骨干网络，但其二次注意力计算成本是主要瓶颈。本研究提出SVG-EAR方法，利用语义聚类后发现键值具有强相似性，可通过聚类中心无参数地近似被跳过的注意力块并恢复其贡献。同时引入错误感知路由，轻量级探针估计每个块的补偿误差，精确选择误差成本比最高的块进行补偿。在Wan2.2和HunyuanVideo视频扩散任务上，SVG-EAR分别实现1.77倍和1.93倍加速，同时保持PSNR达29.759和31.043，建立了质量-效率的Pareto前沿。

**亮点**:
  - 无参数线性补偿分支，避免训练开销和分布偏移
  - 错误感知路由精确选择高误差块进行补偿
  - 在Wan2.2和HunyuanVideo上分别实现1.77x和1.93x加速

---

###  7. V_{0.5}: 基于通用价值模型的稀疏强化学习rollout先验方法 (V_{0.5}: Generalist Value Model as a Prior for Sparse RL Rollouts)

**论文链接**: [https://arxiv.org/abs/2603.10848](https://arxiv.org/abs/2603.10848)
**组织**: LongCat
**得分**: 31.09
**标签**: Frontier Lab
**Upvotes**: 7 | **Stars**: 0

**摘要**: 本论文针对可验证奖励强化学习（RLVR）中稀疏rollout导致的高方差问题，提出V_{0.5}方法。该方法将通用价值模型预测的先验基准线与稀疏rollout的实证均值进行自适应融合，并引入实时统计测试和动态预算分配机制，平衡价值模型的系统性偏差与稀疏采样的高方差。在6个数学推理基准上的实验表明，V_{0.5}显著优于GRPO和DAPO，实现了更快的收敛速度和超过10%的性能提升，即使在组大小仅为4的极端稀疏条件下也能保证稳定的策略梯度。

**亮点**:
  - 在组大小为4的极端稀疏条件下仍能保证稳定的策略梯度
  - 引入实时统计测试动态分配rollout预算，最小化基准估计器的MSE
  - 在6个数学推理基准上性能提升超10%，显著优于GRPO和DAPO

---

###  8. 大型语言模型工具使用的上下文强化学习 (In-Context Reinforcement Learning for Tool Use in Large Language Models)

**论文链接**: [https://arxiv.org/abs/2603.08068](https://arxiv.org/abs/2603.08068)
**组织**: National University of Singapore
**得分**: 28.55
**标签**: 
**Upvotes**: 19 | **Stars**: 7

**摘要**: 本研究针对大语言模型内部知识受限的问题，提出ICRL（上下文强化学习）框架。该方法通过在强化学习的rollout阶段引入few-shot提示来替代传统的监督微调（SFT），使模型学习调用Python解释器等外部工具。随着训练推进，上下文示例数量逐渐减少，最终实现零样本工具调用。在推理和工具使用基准上的实验表明，ICRL达到了最先进的性能，证明其作为可扩展、数据高效替代方案的可行性。

**亮点**:
  - 提出ICRL框架，突破性地无需监督微调即可实现工具调用
  - 创新性地在RL rollout中引入few-shot提示，逐步过渡到零样本设置
  - 在推理和工具使用基准上达到SOTA性能

---

###  9. COMIC：智能体驱动的素描喜剧视频生成 (COMIC: Agentic Sketch Comedy Generation)

**论文链接**: [https://arxiv.org/abs/2603.11048](https://arxiv.org/abs/2603.11048)
**组织**: University of Washington
**得分**: 28.03
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 本研究提出一个全自动AI系统，用于生成类似《周六夜现场》的素描喜剧短视频。系统采用基于真实制作工作室角色的多智能体群体，通过迭代竞争、评估和改进来优化创意质量与多样性。核心贡献在于引入与真实观众偏好对齐的LLM评论家，通过分析YouTube喜剧视频语料库自动评估幽默感。实验表明，该框架生成的视频接近专业制作水平，并在视频生成任务上达到SOTA性能。

**亮点**:
  - 提出基于多智能体群体的全自动喜剧视频生成框架
  - 引入LLM评论家自动评估幽默感，对齐真实观众偏好
  - 生成的喜剧视频质量接近专业制作水平，视频生成SOTA

---

###  10. UniCom：基于压缩连续语义表示的统一多模态建模框架 (UniCom: Unified Multimodal Modeling via Compressed Continuous Semantic Representations)

**论文链接**: [https://arxiv.org/abs/2603.10702](https://arxiv.org/abs/2603.10702)
**组织**: Tencent Hunyuan
**得分**: 28.03
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 当前统一多模态模型依赖离散视觉tokenizer，但离散化会丢失细粒度语义信息，影响视觉理解性能；而直接建模连续语义表示又面临高维生成建模的收敛慢和训练不稳定问题。本研究提出UniCom框架，通过压缩连续表示统一多模态理解和生成。研究发现减少通道维度比空间下采样更有效，并设计基于注意力的语义压缩器将密集特征蒸馏为紧凑表示。实验表明transfusion架构优于query-based设计，UniCom在统一模型中达到SOTA生成性能，同时保持丰富的语义先验，在图像编辑中提供出色可控性，且不依赖VAE也能保持图像一致性。

**亮点**:
  - 在统一多模态模型中实现SOTA生成性能
  - 提出基于注意力的语义压缩器，通道维度压缩比空间下采样更有效
  - 验证transfusion架构在收敛速度和一致性上优于query-based设计

---

###  11. LLM潜在空间中的因果概念图用于逐步推理 (Causal Concept Graphs in LLM Latent Space for Stepwise Reasoning)

**论文链接**: [https://arxiv.org/abs/2603.10377](https://arxiv.org/abs/2603.10377)
**组织**: New York University
**得分**: 28.03
**标签**: Frontier Lab
**Upvotes**: 3 | **Stars**: 0

**摘要**: 稀疏自编码器可以定位概念在语言模型中的位置，但无法揭示概念在多步推理中如何交互。本文提出因果概念图(CCG)：一个基于稀疏可解释潜在特征的有向无环图，边捕捉概念间的因果依赖关系。该方法结合任务条件化稀疏自编码器进行概念发现与DAGMA风格可微结构学习进行图恢复，并引入因果保真度分数(CFS)评估图引导干预效果。在GPT-2 Medium上对ARC-Challenge、StrategyQA和LogiQA进行评估，CCG实现CFS=5.654±0.625，显著优于ROME风格追踪(3.382±0.233)、SAE仅排序(2.479±0.196)和随机基线(1.032±0.034)，p<0.0001。

**亮点**:
  - 提出因果概念图(CCG)建模LLM潜在空间中的概念交互
  - 在多步推理基准上CFS显著优于现有方法(p<0.0001)
  - 学习得到的图稀疏(边密度5-6%)且跨种子稳定

---

###  12. 多智能体自我中心视频问答研究（MA-EgoQA） (MA-EgoQA: Question Answering over Egocentric Videos from Multiple Embodied Agents)

**论文链接**: [https://arxiv.org/abs/2603.09827](https://arxiv.org/abs/2603.09827)
**组织**: KAIST AI
**得分**: 27.05
**标签**: 
**Upvotes**: 25 | **Stars**: 4

**摘要**: 随着具身AI代理在人类生活场景中的应用增多，理解多代理协同获取的自我中心视频成为关键挑战。本研究首次形式化定义了多长时序自我中心视频同步理解问题，并构建了MA-EgoQA基准数据集，包含1.7k道涵盖社交交互、任务协调、心理理论、时间推理和环境交互五类问题。提出EgoMAS基线模型，通过跨代理共享记忆机制和动态检索策略实现多流信息整合。实验表明当前方法在处理多自我中心视频流时性能显著不足，揭示了系统级多代理感知理解的未来研究方向。

**亮点**:
  - 首次定义多智能体自我中心视频问答新任务
  - 构建1.7k问题规模的MA-EgoQA基准数据集
  - 提出EgoMAS模型实现跨代理共享记忆与动态检索

---

###  13. ID-LoRA：基于In-Context LoRA的身份驱动音视频个性化生成 (ID-LoRA: Identity-Driven Audio-Video Personalization with In-Context LoRA)

**论文链接**: [https://arxiv.org/abs/2603.10256](https://arxiv.org/abs/2603.10256)
**组织**: Tel Aviv University
**得分**: 26.71
**标签**: 
**Upvotes**: 11 | **Stars**: 8

**摘要**: 现有视频个性化方法将视觉和音频分开处理，无法实现声音与画面动作的同步。本研究提出ID-LoRA模型，首次在一个生成过程中同时个性化主体的外观和语音。方法通过In-Context LoRA参数高效适配LTX-2联合音视频扩散骨干，并引入负时间位置编码解决参考与生成token的冲突，以及身份引导机制增强说话人特征保留。实验表明，该方法在语音相似度上比Kling 2.6 Pro提升24%，仅需约3000个训练样本即可达到优异性能。

**亮点**:
  - 首次实现音视频单一模型联合个性化生成
  - 引入身份引导机制增强说话人特征保留
  - 仅需~3K训练样本达到SOTA语音相似度

---

###  14. V2M-Zero：零配对时间对齐的视频到音乐生成 (V2M-Zero: Zero-Pair Time-Aligned Video-to-Music Generation)

**论文链接**: [https://arxiv.org/abs/2603.11042](https://arxiv.org/abs/2603.11042)
**组织**: Adobe Research
**得分**: 26.59
**标签**: Frontier Lab
**Upvotes**: 2 | **Stars**: 0

**摘要**: 现有文本到音乐模型缺乏细粒度时间控制，难以生成与视频事件时间对齐的音乐。本研究提出V2M-Zero方法，通过关键洞察——时间同步需匹配变化时机和程度而非语义内容——利用预训练音视频编码器计算模态内事件曲线来捕捉共享的时间结构。无需跨模态配对训练，仅需微调文本到音乐模型即可在推理时替换视频事件曲线。在OES-Pub、MovieGenBench-Music和AIST++数据集上，相较于配对数据基线，音频质量提升5-21%，语义对齐提升13-15%，时间同步提升21-52%，舞蹈视频节拍对齐提升28%。

**亮点**:
  - 提出零配对视频到音乐生成新范式，无需跨模态配对训练
  - 通过模态内事件曲线实现时间同步，验证了时间结构共享假设
  - 在多数据集上实现音频质量、语义对齐、时间同步的全面提升

---
