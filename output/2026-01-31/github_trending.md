# GitHub 热门项目 | 2026-01-31

## 📊 今日榜单

### 1. ThePrimeagen/99
**语言**: Lua | **Stars**: 2447 | **今日**: +542
**链接**: https://github.com/ThePrimeagen/99

**摘要**: 由知名开发者 ThePrimeagen 打造的 Neovim AI 助手，旨在为资深程序员提供“恰到好处”的 AI 工作流。该项目避开了复杂的聊天界面，专注于精准的代码填充（fill_in_function）与选区操作。其核心特色是通过 AGENT.md 和自定义 SKILL.md 文件进行上下文增强，支持利用 @ 符号在补全菜单中快速引入规则。项目强调对 AI 能力的克制使用，通过局部规则限制来提高生成代码的准确性，是 Neovim 极简主义 AI 方案的典型代表。

**技术栈**: Lua, Neovim API, Treesitter, nvim-cmp, opencode

---

### 2. microsoft/BitNet
**语言**: Python | **Stars**: 27394 | **今日**: +137
**链接**: https://github.com/microsoft/BitNet

**摘要**: 这是微软官方推出的 1-bit 大语言模型（如 BitNet b1.58）推理框架。该项目基于 llama.cpp 构建，通过高度优化的内核实现了 1.58-bit 模型在 CPU 和 GPU 上的快速、无损推理。其核心优势在于极高的能效比和极低的内存需求，在 x86 和 ARM 架构上可实现 2-6 倍的加速并降低 70% 以上的功耗，支持在单颗 CPU 上运行百亿级参数模型，极大地推动了 LLM 在边缘设备和本地端的部署落地。

**技术栈**: Python, C++, CMake, Clang, llama.cpp, T-MAC, CUDA

---

### 3. microsoft/agent-lightning
**语言**: Python | **Stars**: 12716 | **今日**: +516
**链接**: https://github.com/microsoft/agent-lightning

**摘要**: Agent Lightning 是微软开发的一款高性能 AI Agent 训练与优化框架。其核心优势在于“零代码侵入”特性，能够无缝集成到 LangChain、AutoGen、CrewAI 等主流框架或纯 Python 编写的 Agent 中。它通过 Tracer 机制自动收集执行轨迹、工具调用及奖励反馈，并利用强化学习（RL）、自动提示词优化（APO）和监督微调（SFT）等算法实现 Agent 性能的闭环提升。该项目解决了 Agent 在复杂任务中难以通过反馈进行自我进化和大规模训练的痛点，极大降低了智能体调优的门槛。

**技术栈**: Python, Reinforcement Learning, vLLM, LangChain, AutoGen, CrewAI, OpenAI SDK

---

### 4. PaddlePaddle/PaddleOCR
**语言**: Python | **Stars**: 69689 | **今日**: +171
**链接**: https://github.com/PaddlePaddle/PaddleOCR

**摘要**: PaddleOCR 是百度出品的工业级 OCR 与文档 AI 引擎。其 3.0+ 版本不仅支持 100 多种语言的端到端文字识别（PP-OCRv5），更进化为强大的文档解析工具（PP-StructureV3）与智能信息抽取系统（PP-ChatOCRv4）。它能将复杂 PDF、图像、表格及公式精准转化为 Markdown/JSON 结构化数据，并集成 0.9B 超轻量级多模态大模型（PaddleOCR-VL）。项目以高精度、低资源占用及对昇腾、昆仑芯等国产硬件的深度优化著称，是 RAG 和大模型应用中处理非结构化文档的首选开源方案。

**技术栈**: PaddlePaddle, Python, ERNIE, VLM, ONNX, OpenVINO, TensorRT, MCP Server

---

### 5. anthropics/claude-plugins-official
**语言**: Shell | **Stars**: 5962 | **今日**: +237
**链接**: https://github.com/anthropics/claude-plugins-official

**摘要**: 该项目是 Anthropic 官方维护的 Claude Code 插件目录，旨在为 Claude Code 提供高质量的扩展生态系统。它包含官方自研及第三方合作伙伴提供的插件，基于模型上下文协议（MCP）构建。核心功能包括通过插件集成斜杠命令（Slash Commands）、自定义代理（Agents）和技能（Skills），允许开发者将外部工具和自动化流程直接嵌入到 Claude 的编码环境中。作为官方中心化仓库，它为 Claude Code 提供了标准化的分发与发现机制，是提升 AI 编码效率的核心资源。

**技术栈**: MCP (Model Context Protocol), JSON, Shell, Claude Code

---

### 6. microsoft/PowerToys
**语言**: C# | **Stars**: 128810 | **今日**: +46
**链接**: https://github.com/microsoft/PowerToys

**摘要**: Microsoft PowerToys 是由微软官方推出的开源系统增强工具集，旨在为 Windows 高级用户提供强大的自定义功能并简化日常任务。该项目包含超过 25 种实用工具，如 FancyZones 窗口分屏管理、PowerToys Run 全局快速搜索、PowerRename 批量重命名以及 Text Extractor 屏幕文字识别等。技术上主要基于 C# 和 C++ 开发，利用 WinAppSDK 和 WebView2 提供原生性能与现代化 UI。它是优化 Windows 体验、提升办公与开发效率的首选神兵利器。

**技术栈**: C#, .NET, C++, WinAppSDK, WebView2, MSIX

---

### 7. termux/termux-app
**语言**: Java | **Stars**: 49577 | **今日**: +41
**链接**: https://github.com/termux/termux-app

**摘要**: Termux 是一款功能强大的 Android 终端模拟器和 Linux 环境应用，无需 root 权限即可在手机上提供接近完整的 Linux 命令行体验。它核心集成了 apt 包管理系统，允许用户安装并运行 Python、Git、Node.js、SSH 等海量开源工具。项目采用 Java 开发，具有极高的扩展性，支持通过插件调用 Android 硬件 API、设置桌面小部件及自动化任务。它是开发者在移动端进行代码调试、远程运维、运行自动化脚本以及学习 Linux 系统的首选神器，是 Android 平台上最成熟的开源 Linux 环境解决方案。

**技术栈**: Java, Android SDK, Linux, Apt, Shell, XTerm

---

### 8. openclaw/openclaw
**语言**: TypeScript | **Stars**: 135212 | **今日**: +14780
**链接**: https://github.com/openclaw/openclaw

**摘要**: OpenClaw 是一款强大的开源个人 AI 助手框架，旨在让用户在私有设备上运行完全受控的智能代理。其核心亮点在于极强的渠道整合能力，支持 WhatsApp、Telegram、iMessage、Slack 等十余种通讯平台。项目提供语音唤醒（Voice Wake）、实时画布（Canvas）以及浏览器自动化控制等高级功能，并内置 Docker 沙箱以确保执行工具的安全。它不仅是一个聊天机器人，更是一个集成了多模态交互、跨平台通讯与本地自动化任务的高集成度个人助理解决方案。

**技术栈**: TypeScript, Node.js, Tailscale, Docker, ElevenLabs, discord.js, grammY, Baileys, Nix

---

### 9. pedroslopez/whatsapp-web.js
**语言**: JavaScript | **Stars**: 21028 | **今日**: +137
**链接**: https://github.com/pedroslopez/whatsapp-web.js

**摘要**: 这是一个基于 Node.js 的 WhatsApp 客户端库，通过 Puppeteer 封装 WhatsApp Web 网页版接口，为开发者提供了一套完整的自动化 API。该项目支持多设备登录，核心功能涵盖消息收发、多媒体传输、群组管理、联系人操作及投票创建等。其优势在于无需支付官方 API 费用即可实现深度功能定制，是构建 WhatsApp 聊天机器人、自动化通知系统和社群管理工具的高效解决方案。

**技术栈**: Node.js, Puppeteer, JavaScript

---

### 10. AlexanderGrooff/mermaid-ascii
**语言**: Go | **Stars**: 895 | **今日**: +74
**链接**: https://github.com/AlexanderGrooff/mermaid-ascii

**摘要**: 这是一个由 Go 语言编写的命令行工具，专门用于将 Mermaid 流程图和时序图转换为 ASCII 或 Unicode 字符艺术并直接在终端输出。它支持多种图表方向、带标签的连线、参与者别名以及通过 classDef 实现的颜色显示。项目不仅提供了灵活的布局间距调整（如水平/垂直间距、边框边距），还支持通过 Docker 启动 Web 交互界面。它解决了在纯终端环境或纯文本文件中预览和展示 Mermaid 拓扑结构的痛点，是命令行重度用户的效率利器。

**技术栈**: Go, Docker, Nix

---

### 11. reconurge/flowsint
**语言**: TypeScript | **Stars**: 2204 | **今日**: +120
**链接**: https://github.com/reconurge/flowsint

**摘要**: Flowsint 是一款开源的现代 OSINT（开源情报）图谱探索平台，专为网络安全分析师和调查员设计。它通过直观的可视化图表展示实体间的复杂关系，集成了域名、IP、社交媒体、加密货币及数据泄露等多维度的自动化丰富工具（Enrichers）。项目强调隐私保护，所有数据均存储在本地，并采用模块化架构，支持通过 n8n 扩展工作流，是进行数字调查、资产侦察和威胁分析的高效工具。

**技术栈**: TypeScript, FastAPI, Python, Neo4j, PostgreSQL, Celery, Pydantic, Docker, Poetry

---

### 12. cline/cline
**语言**: TypeScript | **Stars**: 57419 | **今日**: +44
**链接**: https://github.com/cline/cline

**摘要**: Cline 是一款集成在 IDE 中的自主 AI 编程智能体，利用 Claude 3.5 Sonnet 的 Agentic 能力实现复杂的软件开发任务。它不仅能提供代码建议，还能在用户授权下自主创建与编辑文件、执行终端命令、使用浏览器进行 Web 调试。通过支持 Model Context Protocol (MCP)，Cline 可以扩展自定义工具，处理从代码编写到运维部署的全流程任务。其核心优势在于深度集成 VS Code 及其 shell 环境，并提供完善的变更预览与回滚机制，是目前最领先的开源 AI 编程助手之一。

**技术栈**: TypeScript, VS Code Extension API, Claude 3.5 Sonnet, Model Context Protocol (MCP), OpenRouter, Ollama, Puppeteer

---
