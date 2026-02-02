# GitHub 热门项目 | 2026-02-02

## 📊 今日榜单

### 1. thedotmack/claude-mem
**语言**: TypeScript | **Stars**: 17414 | **今日**: +1469
**链接**: https://github.com/thedotmack/claude-mem

**摘要**: 该项目是专门为 Claude Code 打造的持久化记忆系统插件。它通过自动捕获开发者的编码会话、工具调用及观察结果，利用 Claude Agent SDK 进行 AI 语义压缩，并将其存储在本地数据库中。在后续会话中，它能智能注入相关历史上下文，解决 AI 助手在不同会话间“失忆”的痛点。其核心亮点在于分层检索机制（渐进式披露）以节省 Token，支持向量搜索，并提供 Web UI 实时查看记忆流，显著提升了中长周期项目的开发效率与连续性。

**技术栈**: TypeScript, Node.js, Bun, SQLite (FTS5), Chroma DB, Claude Agent SDK, uv

---

### 2. ThePrimeagen/99
**语言**: Lua | **Stars**: 2925 | **今日**: +298
**链接**: https://github.com/ThePrimeagen/99

**摘要**: 这是一个为 Neovim 打造的高效 AI Agent 插件，由知名开发者 ThePrimeagen 开发。该项目主张“去聊天化”的 AI 工作流，旨在为具备专业能力的开发者提供更精准的代码辅助。它核心功能包括基于上下文的函数自动填充和视觉选区代码处理，支持通过 `@` 符号触发自定义“技能”（Skill）补全，并能自动加载项目中的 AGENT.md 规则文件。其技术特点在于深度结合 Treesitter 和 LSP 获取上下文，追求极简、受限且高效的 AI 协作体验，避免了通用 AI 对话的冗余。

**技术栈**: Lua, Neovim, Treesitter, LSP, nvim-cmp

---

### 3. termux/termux-app
**语言**: Java | **Stars**: 49725 | **今日**: +97
**链接**: https://github.com/termux/termux-app

**摘要**: Termux 是一个在 Android 平台上运行的开源终端模拟器和 Linux 环境应用。其核心功能是在无需 Root 权限的情况下，为用户提供一个完整的 Linux 命令行体验，并支持基于 APT 的软件包管理系统。技术上，它集成了终端仿真技术（兼容 xterm）以及丰富的插件生态，如 API 接口、自动化任务和悬浮窗口等。它允许用户在移动端运行 Python、Node.js、Git 等工具，是移动端开发调试、系统管理、自动化脚本运行及 Linux 学习的极客必备神器。

**技术栈**: Java, Android SDK, APT, Shell, JNI, Gradle

---

### 4. pedramamini/Maestro
**语言**: TypeScript | **Stars**: 1162 | **今日**: +334
**链接**: https://github.com/pedramamini/Maestro

**摘要**: Maestro 是一款专为开发者设计的跨平台 AI Agent 编排指挥中心。它支持 Claude Code、OpenAI Codex 等多种代理，采用键盘优先的交互设计，旨在解决多项目并行时的注意力碎片化问题。核心功能包括利用 Git Worktrees 实现隔离的并行开发、通过 Playbooks 进行长达 24 小时的自动化任务运行，以及支持多 Agent 协作的群聊模式。项目还集成了远程控制、Token 成本追踪和文档关系图谱，是提升 Agent 辅助编程效率的高级工具。

**技术栈**: TypeScript, Node.js, Electron, Git, Markdown, CLI

---

### 5. netbirdio/netbird
**语言**: Go | **Stars**: 21844 | **今日**: +368
**链接**: https://github.com/netbirdio/netbird

**摘要**: NetBird 是一个基于 WireGuard 的开源零信任专有网络平台，旨在简化设备间的安全互联。它通过点对点（P2P）加密隧道连接机器，具备强大的 NAT 穿透能力（集成 WebRTC ICE 和 TURN 转发），且无需复杂的防火墙配置。项目集成了 SSO、MFA、细粒度访问控制和私有 DNS 管理，并支持量子抗性加密。相比传统 VPN，它提供了直观的 Web UI 和自动化管理能力，非常适合需要快速构建安全、高性能分布式网络的企业及个人用户。

**技术栈**: Go, WireGuard, WebRTC, Pion, Coturn, Rosenpass, eBPF, Docker, Terraform

---

### 6. OpenBMB/ChatDev
**语言**: Python | **Stars**: 29220 | **今日**: +75
**链接**: https://github.com/OpenBMB/ChatDev

**摘要**: ChatDev 2.0 (DevAll) 是一款由大语言模型驱动的零代码多智能体协同编排平台。它从最初的自动化软件开发系统演进为通用的智能体协作框架，允许用户通过可视化工作流或 YAML 配置，在无需编码的情况下定义智能体角色、工作流和任务，处理数据可视化、3D 生成、深度研究等复杂场景。该项目核心在于通过多智能体协作（如 CEO、CTO、程序员）自动化任务执行，支持人机交互反馈，是目前多智能体领域最具代表性的开源项目之一。

**技术栈**: Python, FastAPI, Vue 3, Vite, Node.js, uv, Docker, YAML, LLM API

---

### 7. autobrr/qui
**语言**: Go | **Stars**: 2644 | **今日**: +41
**链接**: https://github.com/autobrr/qui

**摘要**: qui 是一款基于 Go 语言开发的现代化 qBittorrent Web UI，旨在提供比原生界面更快速、响应更灵敏的交互体验。它采用单二进制分发，支持在一个界面中集中管理多个 qBittorrent 实例。该项目不仅优化了处理海量种子时的性能瓶颈，还内置了跨站辅种（Cross-Seed）、基于规则的自动化管理、定期备份恢复以及透明反向代理等高级功能。它为 PT/BT 玩家提供了高效的工作流自动化工具，是管理多下载服务器用户的理想解决方案。

**技术栈**: Go, Docker, qBittorrent API

---

### 8. badlogic/pi-mono
**语言**: TypeScript | **Stars**: 5381 | **今日**: +881
**链接**: https://github.com/badlogic/pi-mono

**摘要**: pi-mono 是一个功能全面的 AI Agent 开发工具集，核心是一个名为 'pi' 的交互式编程智能体。该项目采用 Monorepo 架构，提供了一整套 Agent 基础设施：包括支持 OpenAI、Anthropic、Google 等多供应商的统一 LLM API，具备工具调用和状态管理的 Agent 运行时，以及高性能的 TUI/Web UI 界面库。此外，它还集成了 Slack 机器人支持和基于 vLLM 的 GPU 部署管理工具。该项目通过将底层适配、逻辑运行与多端交互深度整合，为开发者快速构建、部署和扩展定制化 AI 助手提供了一站式解决方案。

**技术栈**: TypeScript, Node.js, vLLM, OpenAI API, Anthropic API, Google Gemini API, React/Web Components, TUI

---

### 9. VectifyAI/PageIndex
**语言**: Python | **Stars**: 12279 | **今日**: +818
**链接**: https://github.com/VectifyAI/PageIndex

**摘要**: PageIndex 是一款创新的“无向量”推理型 RAG 框架。它通过将长文档（如 PDF）构建成类似目录的分层树状索引，利用 LLM 的推理能力模拟人类专家的阅读习惯进行树搜索检索。该项目旨在解决传统 RAG 中“语义相似度不等于相关性”的问题，无需向量数据库和文本分块，显著提升了在金融、法律等复杂长文档场景下的检索准确率与可解释性。

**技术栈**: Python, OpenAI API, GPT-4o, MCP (Model Context Protocol), Markdown

---

### 10. karpathy/nanochat
**语言**: Python | **Stars**: 41453 | **今日**: +137
**链接**: https://github.com/karpathy/nanochat

**摘要**: 由 Andrej Karpathy 发起的开源项目，旨在提供一个极简且可黑客化的 LLM 实验框架。它涵盖了从分词、预训练、微调（SFT）、评估到推理及 Web UI 的完整生命周期。该项目核心目标是极高的训练效率，例如能在 3 小时内以约 $73 的成本训练出超越 GPT-2 性能的模型。代码结构清晰，抛弃了复杂的框架封装，非常适合开发者深入理解大模型底层实现、研究缩放定律以及在有限预算下构建自定义微型对话模型。

**技术栈**: Python, PyTorch, Muon Optimizer, uv, WandB, BPE Tokenization, Distributed Training

---

### 11. kovidgoyal/calibre
**语言**: Python | **Stars**: 23744 | **今日**: +183
**链接**: https://github.com/kovidgoyal/calibre

**摘要**: calibre 是一款功能极其强大的开源电子书管理神器，被誉为电子书界的“瑞士军刀”。它集成了电子书查看、格式转换、编辑和书库管理等核心功能，支持几乎所有主流电子书格式，并具备强大的元数据自动抓取、新闻转电子书以及跨平台同步能力。该项目凭借其长达十余年的持续维护、极高的社区活跃度和成熟的生态系统，成为全球电子书爱好者和研究者的首选工具，是 Python 开源大型桌面应用的典范。

**技术栈**: Python, C++, PyQt, Qt, CSS, bypy

---

### 12. langchain-ai/rag-from-scratch
**语言**: Jupyter Notebook | **Stars**: 6859 | **今日**: +94
**链接**: https://github.com/langchain-ai/rag-from-scratch

**摘要**: 该项目由 LangChain 团队推出，是一套从零构建检索增强生成（RAG）系统的权威教学代码库。它通过一系列 Jupyter Notebook 深入浅出地讲解了 RAG 的核心机制，包括数据索引、信息检索和文本生成等关键步骤。项目旨在帮助开发者理解如何利用外部数据扩展大语言模型的知识边界，解决模型事实召回率低和数据更新不及时的问题。结合配套视频教程，它为构建企业级 AI 助手和私有知识库提供了从底层原理到代码实现的完整路径，是掌握高级 RAG 技术的必读资源。

**技术栈**: LangChain, Python, Jupyter Notebook, RAG, LLM

---
