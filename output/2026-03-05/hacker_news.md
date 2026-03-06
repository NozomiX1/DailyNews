# Hacker News Top 30 | 2026-03-05

## 📊 今日概览

- 📰 **News**: 28 条
- 🚀 **Show HN**: 1 条
- 💼 **Jobs**: 1 条

---

## 📰 News (28)

### 1. Wikipedia was in read-only mode following mass admin account compromise
> Score: 900 | Comments: 312

**摘要**: 维基百科因大规模管理员账户泄露进入只读模式。攻击利用JS蠕虫在Common.js中自我复制并破坏页面，社区热议其技术原理及清理难度。

**关键点**:
- 维基百科因管理员账户泄露安全事件被迫进入只读模式
- 攻击涉及一种注入Common.js的JavaScript蠕虫，能自动破坏页面
- 社区评论指出清理难度极大，因为数据库历史记录本身也是传播载体

**社区观点**: 混合

🔗 [原文](https://www.wikimediastatus.net)
💬 [评论区](https://news.ycombinator.com/item?id=47263323)

💬 *精选评论*:
> "See the public phab ticket: <a href="https:&#x2F;&#x2F;phabricator.wikimedia.org&#x2F;T419143" rel="..." — @tux3
> "Wow. This worm is fascinating. It seems to do the following:- Inject itself into the MediaWiki:Co..." — @nhubbard

---

### 2. Judge orders government to begin refunding more than $130B in tariffs
> Score: 825 | Comments: 615

**摘要**: 法官勒令政府退还超1300亿美元关税。社区热议关税战的不合理性、法院未及时干预的失职，以及企业是否会既赚差价又获退税。

**关键点**:
- 法官命令政府退还超过1300亿美元的关税。
- 社区批评之前的关税战不仅针对敌人也针对盟友，质疑法院未能及时叫停。
- 焦点在于退款流向，担忧企业已转嫁成本给消费者却双重获利。

**社区观点**: 负面

🔗 [原文](https://www.wsj.com/politics/policy/judge-orders-government-to-begin-refunding-more-than-130-billion-in-tariffs-fdc1e62c)
💬 [评论区](https://news.ycombinator.com/item?id=47261688)

💬 *精选评论*:
> "Here&#x27;s a gift link to access it if you don&#x27;t have a subscription:<a href="https:&#x2F;&..." — @SyneRyder
> "Side topic, but this number puts into how crazy it was for trump[0] to go on tariff war against enem..." — @trymas

---

### 3. GPT-5.4
> Score: 663 | Comments: 576

**摘要**: OpenAI发布GPT-5.4，主打百万级上下文、原生计算机控制及思维规划功能。社区对其性能提升表示赞赏，但强烈吐槽版本命名混乱、产品线过于复杂。

**关键点**:
- GPT-5.4集成推理与编码能力，支持100万Token上下文及原生计算机控制
- 引入GPT-5.4 Thinking模式，可预先规划思维并允许中途调整响应
- 模型在多项基准测试中优于前代，且Token使用效率更高

**社区观点**: 混合

🔗 [原文](https://openai.com/index/introducing-gpt-5-4/)
💬 [评论区](https://news.ycombinator.com/item?id=47265045)

💬 *精选评论*:
> "I find it quite funny how this blog post has a big &quot;Ask ChatGPT&quot; box at the bottom. So you..." — @Philip-J-Fry
> "What a model mess!OpenAI now has three price points: GPT 5.1, GPT 5.2 and now GPT 5.4. There vers..." — @__jl__

---

### 4. CBP tapped into the online advertising ecosystem to track peoples’ movements
> Score: 379 | Comments: 159

**摘要**: 美国CBP利用在线广告数据追踪民众，数据源涉及游戏、健身应用。社区热议隐私侵犯、法律漏洞及公款滥用问题。

**关键点**:
- CBP通过购买广告数据（来自游戏、健身应用等）追踪民众精确位置
- 此前ICE也购买了类似监控工具，议员正敦促调查此事
- 社区评论讨论数据准确性、隐私法执法漏洞及纳税人资金被用于监控的讽刺

**社区观点**: 负面

🔗 [原文](https://www.404media.co/cbp-tapped-into-the-online-advertising-ecosystem-to-track-peoples-movements/)
💬 [评论区](https://news.ycombinator.com/item?id=47249387)

💬 *精选评论*:
> "https:&#x2F;&#x2F;archive.md&#x2F;N..." — @ece
> "I work with Ad Data a lot in my job, and there&#x27;s a lot of misconceptions about what this data t..." — @legitster

---

### 5. Good software knows when to stop
> Score: 351 | Comments: 195

**摘要**: 故事讽刺了软件过度设计，特别是盲目集成AI导致工具臃肿。社区热议软件应适时停止开发，专注于核心功能和稳定性，而非无休止的功能蔓延。

**关键点**:
- 讽刺了盲目将AI集成进基础工具（如ls命令）的荒谬现象。
- 社区呼吁软件应保持简洁，拒绝功能蔓延，承认“已完成”的价值。
- 用户赞赏像Sublime Text和notepad.exe这样专注、高效且不过度开发的工具。

**社区观点**: 正面

🔗 [原文](https://ogirardot.writizzy.com/p/good-software-knows-when-to-stop)
💬 [评论区](https://news.ycombinator.com/item?id=47261561)

💬 *精选评论*:
> "&gt;Ignore feature requests — don&#x27;t build what users ask for; understand the underlying prob..." — @john_strinlai
> "We should normalize &quot;finished&quot; software products that stop feature creep and focus strictl..." — @wenbin

---

### 6. A GitHub Issue Title Compromised 4k Developer Machines
> Score: 341 | Comments: 79

**摘要**: GitHub issue标题的提示注入导致AI机器人执行恶意代码，窃取凭证并发布含后门的npm包，感染4000台机器。社区批评安全疏忽及issues触发的危险性。

**关键点**:
- 攻击通过GitHub issue标题进行提示注入，诱导AI triage bot执行恶意npm安装命令
- 利用GitHub Actions缓存投毒机制窃取了NPM发布凭证
- 被攻陷的cline@2.3.0版本在8小时内导致约4000台开发者机器安装了恶意AI代理OpenClaw

**社区观点**: 混合

🔗 [原文](https://grith.ai/blog/clinejection-when-your-ai-tool-installs-another)
💬 [评论区](https://news.ycombinator.com/item?id=47263595)

💬 *精选评论*:
> "This article only rehashes primary sources that have already been submitted to HN (including the ori..." — @jonchurch_
> "The article should have also emphasized that GitHub&#x27;s issues trigger is just as dangerou..." — @pzmarzly

---

### 7. 10% of Firefox crashes are caused by bitflips
> Score: 321 | Comments: 183

**摘要**: Firefox工程师证实10%崩溃由位翻转导致，引发社区对硬件故障误伤软件的讨论，呼吁普及ECC内存标准。

**关键点**:
- Firefox数据显示约10%的崩溃是由内存位翻转或硬件故障引起的。
- 团队通过部署用户端内存测试器验证了检测硬件问题的启发式算法。
- 社区讨论了硬件可靠性对软件开发的影响，并抱怨ECC内存难以获取。

**社区观点**: 混合

🔗 [原文](https://mas.to/@gabrielesvelto/116171750653898304)
💬 [评论区](https://news.ycombinator.com/item?id=47252971)

💬 *精选评论*:
> "I&#x27;ve told this story before on HN, but my biz partner at ArenaNet, Mike O&#x27;Brien (creator o..." — @netcoyote
> "This is quite surprising to me, since I thought the percentage would be a lot lesser.But I don’t ..." — @newscracker

---

### 8. The Brand Age
> Score: 246 | Comments: 215

**摘要**: 文章讲述瑞士表业如何从精密制造转型为奢侈品牌以度过危机。社区讨论了品牌化的利弊及人们为地位和营销付费的心理。

**关键点**:
- 瑞士钟表业因日本竞争、汇率飙升和石英技术三重打击而濒临崩溃。
- 幸存企业通过转型为奢侈品牌，在销量下降的同时实现了营收的飞跃。
- 在技术抹平产品差异的时代，品牌成为核心价值，即所谓的“品牌时代”。

**社区观点**: 混合

🔗 [原文](https://paulgraham.com/brandage.html)
💬 [评论区](https://news.ycombinator.com/item?id=47264756)

💬 *精选评论*:
> "I actually dislike most &quot;branding&quot;, by which I mean, I dislike when the name&#x2F;logo of ..." — @socalgal2
> "Interesting historical anecdote: the Swiss became the world&#x27;s best watchmakers because, in Prot..." — @d_burfoot

---

### 9. Proton Mail Helped FBI Unmask Anonymous 'Stop Cop City' Protester
> Score: 244 | Comments: 122

**摘要**: Proton Mail移交支付数据助FBI锁定匿名抗议者。社区热议隐私服务的法律合规性与用户匿名误区。

**关键点**:
- Proton Mail响应瑞士政府要求提供支付数据，协助FBI识别了“Stop Cop City”相关的匿名账号
- 事件表明即便使用端到端加密服务，元数据如支付信息仍可能导致用户身份泄露
- 社区对此褒贬不一：有人批评隐私不足，有人指出Proton必须守法且用户未做好匿名措施

**社区观点**: 混合

🔗 [原文](https://www.404media.co/proton-mail-helped-fbi-unmask-anonymous-stop-cop-city-protestor/)
💬 [评论区](https://news.ycombinator.com/item?id=47267628)

💬 *精选评论*:
> "Unsurprising.If you don&#x27;t want to receive the punishment for thought crimes, which is being ..." — @jesse_dot_id
> "People will never understand, Proton is a privacy based email server, it is not the dark web where y..." — @h4kunamata

---

### 10. Where things stand with the Department of War
> Score: 216 | Comments: 172

**摘要**: Anthropic被战争部列为供应链风险并将起诉，但承诺继续为美军提供AI支持。CEO称与军方共同点多于分歧，引发社区对AI军事化及术语使用的伦理争议。

**关键点**:
- Anthropic收到战争部信函被列为供应链风险，公司认为不合法并将起诉
- 风险指定范围狭窄，仅适用于直接涉及战争部合同的Claude使用
- Dario Amodei为泄露的内部不当言论道歉，重申不参与作战决策

**社区观点**: 混合

🔗 [原文](https://www.anthropic.com/news/where-stand-department-war)
💬 [评论区](https://news.ycombinator.com/item?id=47269263)

💬 *精选评论*:
> "It is incredible how far the overton window has moved on this issue.When I graduated in 2007, it ..." — @hglaser
> "Around 10 years ago, in college, in Calculus class I had a very ambitious classmate, wanted to go to..." — @agigao

---

### 11. The next generations of Bubble Tea, Lip Gloss, and Bubbles are available now
> Score: 129 | Comments: 47

**摘要**: Charmbracelet 发布 TUI 框架 v2，引入 Cursed Renderer 提升渲染性能，适配 AI 时代终端需求。社区热议 CLI 界面的复古美学与现代实用性。

**关键点**:
- Bubble Tea、Lip Gloss、Bubbles 发布 v2.0.0 版本，引入基于 ncurses 的 Cursed Renderer 渲染引擎。
- 大幅优化渲染性能，支持内联图片、剪贴板传输等高级终端特性，专为 AI 代理优化。
- 该生态系统已被 NVIDIA、GitHub 等公司及超 25,000 个开源项目使用。

**社区观点**: 混合

🔗 [原文](https://charm.land/blog/v2/)
💬 [评论区](https://news.ycombinator.com/item?id=47268662)

💬 *精选评论*:
> "Please, a simple web page that tells me what this does, and why I should use it. Links to github hav..." — @zabzonk
> "My favourite library from these folks is gum (<a href="https:&#x2F;&#x2F;github.com&#x2F;charmbracel..." — @jasongi

---

### 12. Hardware hotplug events on Linux, the gory details
> Score: 121 | Comments: 7

**摘要**: 文章剖析 Linux USB 热插拔机制，对比 udev 与 netlink，提供直接监听 netlink 的底层代码。社区分享了特定硬件固件问题及 udev 规则配置的实战经验。

**关键点**:
- 探讨了不依赖 libusb 直接监听 Linux USB 热插拔事件的方法
- 分析了 udev 和 netlink 两种后端的区别，解释了 udev 避免竞态条件的原理
- 介绍了 Netlink 协议及直接使用 socket API 监听内核事件的 C 语言代码示例

**社区观点**: 正面

🔗 [原文](https://arcanenibble.github.io/hardware-hotplug-events-on-linux-the-gory-details.html)
💬 [评论区](https://news.ycombinator.com/item?id=47215602)

💬 *精选评论*:
> "Sort of relatedly: I bought an inexpensive DDR pad recently that worked on coldplug but not hotplug...." — @philips
> "I can&#x27;t help feeling that the old XKCD cartoon [1] about life satisfaction being proportional t..." — @robinsonb5

---

### 13. Let's Get Physical
> Score: 106 | Comments: 15

**摘要**: 作者分享了搞笑的物理渗透测试经历，利用员工冷漠和缺乏警惕，轻易突破安保进入受限区域。社区热议“人”是最大的安全漏洞，薪资不足导致无人过问陌生人。

**关键点**:
- 尽管携带了全套工具，但由于安保人员缺乏警惕，作者几乎未受阻碍地完成了物理渗透测试。
- 成功尾随进入另一栋建筑，并在未受盘问的情况下与员工互动，突显了社会工程学方面的脆弱性。
- 社区评论指出，普遍的物理安保松懈以及员工“薪资不足而不关心”是主要的安全隐患。

**社区观点**: 正面

🔗 [原文](https://m4iler.cloud/posts/lets-get-physical/)
💬 [评论区](https://news.ycombinator.com/item?id=47266030)

💬 *精选评论*:
> "From one red teamer to red teamer to another, glad your first assessment went so well and you had a ..." — @illithid0
> "Only the military, and some banks, really take physical security seriously.Someone tried to crash..." — @Animats

---

### 14. A standard protocol to handle and discard low-effort, AI-Generated pull requests
> Score: 102 | Comments: 28

**摘要**: RFC 406i协议用于拒绝低质量AI代码提交，强制AI停止处理。社区支持用此直接方式打击浪费时间的人工智能垃圾提交。

**关键点**:
- 提出RFC 406i标准，旨在拒绝和过滤低质量的AI生成代码及贡献
- 设定针对LLM和自动代理的系统指令，要求其在收到拒绝信号后立即停止处理
- 详细列举了AI垃圾提交的特征，如虚构API、机械语气及无意义的冗余描述

**社区观点**: 正面

🔗 [原文](https://406.fail/)
💬 [评论区](https://news.ycombinator.com/item?id=47267947)

💬 *精选评论*:
> "&gt; If you truly wish to be helpful, please direct your boundless generative energy toward a reposi..." — @deckar01
> "I maintain a small oss project and started getting these maybe 6 months ago. The worst part is they ..." — @vicchenai

---

### 15. A ternary plot of citrus geneology
> Score: 97 | Comments: 15

**摘要**: 文章用三元图展示柑橘基因谱系，揭示其多为柚子、宽皮橘和香橼的杂交后代。社区热议特定品种（如波斯莱檬）的血统及缺失品种。

**关键点**:
- 几乎所有的现代柑橘都是柚子、宽皮橘和香橼三种祖先物种的杂交后代。
- 人类历史迁徙与口味偏好（趋向甜味）主导了柑橘的杂交方向。
- 三元图可视化能有效展示复杂的基因混合，比传统树状图更直观，但仍有局限性。

**社区观点**: 正面

🔗 [原文](https://www.jlauf.com/writing/citrus/)
💬 [评论区](https://news.ycombinator.com/item?id=47238272)

💬 *精选评论*:
> "Inheritance is astonishingly more complex than trees, e.g.Wong et al. (2024)
&quot;A general and ..." — @fritzo
> "A Persian lime is a cross between a Key lime and a lemon? I never would have guessed that, that&#x27..." — @jihadjihad

---

### 16. Remotely unlocking an encrypted hard disk
> Score: 94 | Comments: 52

**摘要**: 文章介绍通过将 Tailscale 集成到 initramfs 实现远程解锁加密硬盘。社区讨论了 Mandos、Dracut-sshd 等替代方案，并警示物理访问会导致 MITM 风险。

**关键点**:
- 作者通过将 Tailscale 和 SSH 集成到 initramfs 中，解决了家中断电重启后无法远程输入解密密码的问题
- 安全措施包括使用 ACL 限制连接、设置永不过期密钥以及将 SSH Shell 限制为仅允许解锁命令
- 社区提供了 Mandos、Dracut-sshd 等现有工具作为替代方案，也有人使用树莓派作为堡垒主机

**社区观点**: 混合

🔗 [原文](https://jyn.dev/remotely-unlocking-an-encrypted-hard-disk/)
💬 [评论区](https://news.ycombinator.com/item?id=47265521)

💬 *精选评论*:
> "If you want to be able to reboot remotely, and non-interactively (i.e. while you sleep), I (a..." — @teddyh
> "I have a very similar setup to the author, but instead of running Tailscale in my initramfs, I have ..." — @abound

---

### 17. OpenTitan Shipping in Production
> Score: 86 | Comments: 11

**摘要**: OpenTitan芯片已量产并用于Chromebook，作为首个开源信任根支持后量子密码学。社区虽有庆祝，但也担忧厂商控制与代码审查难度。

**关键点**:
- OpenTitan现已在商用Chromebook中出货，由Nuvoton生产
- 它是首个开源硅信任根(RoT)，支持后量子密码学(SLH-DSA)
- 项目具备高代码覆盖率(>90%)和严格的质量标准

**社区观点**: 混合

🔗 [原文](https://opensource.googleblog.com/2026/03/opentitan-shipping-in-production.html)
💬 [评论区](https://news.ycombinator.com/item?id=47265619)

💬 *精选评论*:
> "I worked on OpenTitan for around 5 years at lowRISC. It certainly has its ups and downs but it&#x27;..." — @gchadwick
> "Clicking through links eventually led to <a href="https:&#x2F;&#x2F;lowrisc.org&#x2F;ibex&#x2F;" rel..." — @yjftsjthsd-h

---

### 18. Labor market impacts of AI: A new measure and early evidence
> Score: 74 | Comments: 77

**摘要**: Anthropic研究提出新指标衡量AI对就业影响，发现目前AI实际覆盖率低且未导致大规模失业。热议点在于AI提升生产力反而导致工作量增加，而非裁员。

**关键点**:
- 新指标“观测暴露度”显示AI实际应用远低于理论极限，高暴露职业增长预期放缓。
- 研究未发现高暴露工作者失业率系统性上升，但年轻工作者招聘可能放缓。
- 社区反馈AI主要提高了生产力门槛和强度，而非减少工作总量，且存在对公司数据的信任质疑。

**社区观点**: 混合

🔗 [原文](https://www.anthropic.com/research/labor-market-impacts)
💬 [评论区](https://news.ycombinator.com/item?id=47268391)

💬 *精选评论*:
> "I don&#x27;t write code for a living but I administer and maintain it.Every time I say this peopl..." — @bandrami
> "I&#x27;m working on a project right now, that is heavily informed by AI. I wouldn&#x27;t even..." — @ChrisMarshallNY

---

### 19. AI and the Ship of Theseus
> Score: 60 | Comments: 63

**摘要**: AI利用测试套件重写代码挑战版权，削弱GPL效力；社区热议开源许可简化及知识产权存废问题。

**关键点**:
- AI能仅凭测试套件重写代码，在保持功能一致的同时改变设计，模糊了版权边界。
- Copyleft（如GPL）依赖版权执行，但AI重写可轻易绕过限制，促使代码转向MIT等宽松协议。
- 社区对AI重写代码的法律地位、知识产权的有效性以及开源未来的走向存在分歧。

**社区观点**: 混合

🔗 [原文](https://lucumr.pocoo.org/2026/3/5/theseus/)
💬 [评论区](https://news.ycombinator.com/item?id=47263048)

💬 *精选评论*:
> "&gt; I personally think all of this is exciting. I’m a strong supporter of putting things in the ope..." — @cheesecompiler
> "In this emerging reality, the whole spectrum of open-source licenses effectively collapses toward ju..." — @nomdep

---

### 20. GLiNER2: Unified Schema-Based Information Extraction
> Score: 43 | Comments: 3

**摘要**: GLiNER2是基于统一模式的零样本信息提取模型，主打CPU优先运行。社区关注其运行效率及零样本能力。

**关键点**:
- 基于统一模式的信息提取模型，支持零样本学习
- 注重CPU优先设计，便于部署和运行
- 社区对其技术潜力表示赞赏，并关注性能数据

**社区观点**: 正面

🔗 [原文](https://github.com/fastino-ai/GLiNER2)
💬 [评论区](https://news.ycombinator.com/item?id=47266736)

💬 *精选评论*:
> "Very cool stuff. Love the focus on CPU-first.Would also love to see some throughput numbers on ba..." — @iwhalen
> "Zero-shot encoder models are so cool. I&#x27;ll definitely be checking this out.If you&#x27;re lo..." — @deepsquirrelnet

---

### 21. Ethiopia gets $350M World Bank financing for its digital ID project (2024)
> Score: 36 | Comments: 22

**摘要**: 世行批准3.5亿美元资助埃塞俄比亚数字ID项目，拟于2024年全面推广。社区热议数字身份的必要性及对隐私等方面的担忧。

**关键点**:
- 世行批准3.5亿美元支持埃塞俄比亚Fayda数字ID项目，其中5000万美元为赠款，旨在提升金融包容性。
- 埃塞俄比亚计划于2024年在银行交易中强制使用该数字ID，目前项目试点已注册350万人。
- 社区讨论呈现混合观点，一方认为数字ID是现代生活必需，另一方则担忧其在隐私和投票等领域的应用。

**社区观点**: 混合

🔗 [原文](https://www.mariblock.com/stories/ethiopia-to-get-350-million-world-bank-financing-for-its-digital-id-project)
💬 [评论区](https://news.ycombinator.com/item?id=47267694)

💬 *精选评论*:
> "I remember many years ago (maybe around 2014?) reading about a smallish European country that implem..." — @sparky_z
> "The comments here seem to have a negative sentiment towards this project, and I want to understand t..." — @pinkmuffinere

---

### 22. Launch HN: Vela (YC W26) – AI for complex scheduling
> Score: 36 | Comments: 37

**摘要**: YC W26项目Vela利用AI解决复杂调度问题。社区讨论其与Clara、Doodle等现有工具的区别，以及在猎头和手术排期等高难度场景的应用潜力。

**关键点**:
- Vela主打AI复杂调度，强调无需用户改变现有流程
- 解决了如猎头公司需要独立邮件和Zoom账号等特定痛点
- 社区对比了Clara和Doodle，并建议拓展至手术室调度等垂直领域

**社区观点**: 混合

💬 [评论区](https://news.ycombinator.com/item?id=47264741)

⚠️ *正文获取失败*

💬 *精选评论*:
> "I really like the framing of the case studies, the emphasis on Vela taking over their current proces..." — @3rodents
> "How does this compare to solutions like e.g. Clara[0] that have been around for a decade?A lot of..." — @hobofan

---

### 23. Converting dash cam videos into Panoramax images
> Score: 35 | Comments: 7

**摘要**: 作者分享了将行车记录仪视频转化为Panoramax可用的地理标记图像的技术流程。社区热议了元数据提取细节及Panoramax在地图生态中的重要性。

**关键点**:
- Mapillary支持直接上传视频，Panoramax需将视频预处理为地理标记图像。
- 作者使用exiftool提取GPS元数据，并利用Python进行线性插值。
- 流程包含提取GPS、生成均匀分布点、截取图像及写入元数据四步。

**社区观点**: 混合

🔗 [原文](https://www.openstreetmap.org/user/FeetAndInches/diary/408268)
💬 [评论区](https://news.ycombinator.com/item?id=47215180)

💬 *精选评论*:
> "I hadn&#x27;t seen Panoramax before, but I&#x27;m finding exploring it frustrating.If I look at M..." — @nl
> "&quot;Step 1 - Getting GPS data from the video&quot;Feels like a &quot;draw a circle. draw the re..." — @dylan604

---

### 24. Stop Using Grey Text (2025)
> Score: 20 | Comments: 7

**摘要**: 作者批评网页设计中低对比度灰色文字，建议用CSS修正。评论区指出作者双重标准，并讨论深灰色与屏幕亮度的平衡。

**关键点**:
- 作者抨击网页设计中使用低对比度灰色文字的做法，认为这影响可读性且无需特意编写代码实现。
- 建议使用 `prefers-contrast` CSS媒体查询来提升网站的无障碍体验。
- 评论区指出作者自家网站也使用了灰色文字，存在双重标准，并讨论了深灰色的合理性及屏幕亮度的影响。

**社区观点**: 混合

🔗 [原文](https://catskull.net/stop-using-grey-text.html)
💬 [评论区](https://news.ycombinator.com/item?id=47268574)

💬 *精选评论*:
> "Isn&#x27;t most of the text on the page grey? It&#x27;s not white, it&#x27;s rgb(215,215,216). And t..." — @tejohnso
> "Dark&#x2F;charcoal grey is better than pure black for text. But it&#x27;s still dark enough that mos..." — @SoftTalker

---

### 25. Hacking Super Mario 64 using covering spaces
> Score: 10 | Comments: 2

**摘要**: 文章用拓扑学中的覆盖空间原理解释《超级马里奥64》的“平行宇宙”机制，社区热议其与著名速通视频“0.5次按键 A”及QPU理论的关联。

**关键点**:
- 定义了拓扑学中的覆盖空间和通用覆盖，并结合甜甜圈和圆的例子进行可视化解释。
- 揭示了《超级马里奥64》中的“平行宇宙”本质上是覆盖空间在游戏内存溢出下的实现。
- 探讨了通过双曲几何和覆盖空间概念来理解游戏世界的无限复制结构。

**社区观点**: 正面

🔗 [原文](https://happel.ai/posts/covering-spaces-geometries-visualized/)
💬 [评论区](https://news.ycombinator.com/item?id=47215042)

💬 *精选评论*:
> "Was anyone who played this back in the day on an N64 able to wall-jump on top of the castle?..." — @t1234s
> "This reminds me of pannenkoek2012&#x27;s work on Super Mario 64: SM64 - Watch for Rolling Rocks 0.5x..." — @entelechy0

---

### 26. How to install and start using LineageOS on your phone
> Score: 9 | Comments: 2

**摘要**: 本文涵盖LineageOS的构建、Android架构及ADB使用。社区指出该文更适于进阶开发者，并警告OTA更新可能导致设备重置。

**关键点**:
- 详解LineageOS的构建流程、Git管理及Android底层架构（如VINTF、SELinux）
- 介绍在设备上使用LineageOS的开发工具（ADB、Android.bp）和关键配置
- 社区反馈：内容偏向进阶笔记，建议避免OTA更新而采用手动更新以防数据丢失

**社区观点**: 混合

🔗 [原文](https://lockywolf.net/2026-02-19_How-to-install-and-start-using-LineageOS-on-your-phone.d/index.html)
💬 [评论区](https://news.ycombinator.com/item?id=47269288)

💬 *精选评论*:
> "I’m so confused by this submission. It’s not a guide but a collection of notes from someone (in chin..." — @joecool1029
> "I personally had big problems doing an OTA update within LineageOS that required a factory reset aft..." — @Dwedit

---

### 27. Nobody ever got fired for using a struct
> Score: 8 | Comments: 0

**摘要**: Feldera 揭示 SQL 编译生成的数百个字段的 Rust 结构体导致性能瓶颈，打破了常规编程认知。

**关键点**:
- Feldera 引擎将 SQL 表行编译为 Rust 结构体
- 包含大量 Optional 字段的超宽结构体引发了严重的性能问题
- 分析了 Rust 结构体的内存布局及其对性能的影响

**社区观点**: 中性

🔗 [原文](https://www.feldera.com/blog/nobody-ever-got-fired-for-using-a-struct)
💬 [评论区](https://news.ycombinator.com/item?id=47225655)

---

### 28. The Home Computer War
> Score: 3 | Comments: 0

**摘要**: 1979年Atari和TI开创混合型家用电脑，引发价格战使其成为大众消费品。Radio Shack推出源于农业项目的Color Computer。

**关键点**:
- Atari和TI结合PC与游戏机特性推出新品，初期定价高昂，未能达到大众市场预期。
- TI推出低价版99/4A引发价格战，家用电脑成为中产阶级圣诞热门商品，模糊了教育与娱乐的界限。
- Radio Shack的TRS-80 Color Computer诞生于联邦资助的'绿拇指计划'，最初旨在为农民提供信息终端。

**社区观点**: 中性

🔗 [原文](https://technicshistory.com/2026/03/06/the-home-computer-war/)
💬 [评论区](https://news.ycombinator.com/item?id=47269914)

---

## 🚀 Show HN (1)

### 1. Show HN: Jido 2.0, Elixir Agent Framework
> Score: 251 | Comments: 55

**摘要**: Jido 2.0 发布，基于 Elixir BEAM 的智能体框架，主打纯函数与高并发。社区热议其架构优化及 AI 场景下的可靠性。

**关键点**:
- 基于 Elixir BEAM 运行时，主打高并发与容错能力，相比 Python/TS 更稳健。
- 架构回归简单，采用纯函数设计，Agent 即数据，易于测试与调试。
- 引入策略模式（如 FSM, ReAct），并将 Actions 和 Signals 拆分为独立包。

**社区观点**: 正面

🔗 [原文](https://jido.run/blog/jido-2-0-is-here)
💬 [评论区](https://news.ycombinator.com/item?id=47263036)

💬 *精选评论*:
> "I really like the focus on “data and pure functions” from the beginning of the post.I’ve read a l..." — @kzemek
> "I haven&#x27;t used Jido for anything yet, but it&#x27;s one of those projects I check in on once a ..." — @mmcclure

---

## 💼 Jobs (1)

### 1. Structured AI (YC F25) Is Hiring
> Score: 1 | Comments: 0

**摘要**: Structured AI（YC F25）招聘机械设计工程师，年薪8-8.5万美元，1年以上经验，地点纽约或美国远程。

**关键点**:
- 公司Structured AI属于YC F25批次，专注于建筑工程领域的AI劳动力
- 招聘机械设计工程师（创始团队/顾问），年薪8万-8.5万美元
- 要求1年以上经验，仅限美国公民/签证，支持纽约或全美远程

**社区观点**: 中性

🔗 [原文](https://www.ycombinator.com/companies/structured-ai/jobs/3cQY6Cu-mechanical-design-engineer-founding-team-consultant)
💬 [评论区](https://news.ycombinator.com/item?id=47267236)

---
