---
layout: post
title:  "Google Gemini体验"
date:   2025-06-27 18:00:00 +0800
categories: llm
---

大语言模型推出后，搜索引擎公司明显感受到了威胁，很明显，很多情况下，向大模型提问就可以了，减少大量的搜索引擎查询。Google最近发力了，推出Gemini 2.5 pro，包含CLI和API等用法，并且免费力度非常大！

**前置条件：**科学上网，需要开启Tun模式。我这边使用Clash Verge，配置如下：

![image](/images/2025-06-27-clash-tun.png)

简单介绍一下Tun模式：

**TUN是操作系统内核中的虚拟网络层设备（工作在网络层，处理IP数据包）。不同于传统代理（如 SOCKS5/HTTP 仅代理应用层流量），TUN能捕获所有进出系统的网络流量（包括 TCP/UDP/ICMP等）。**

配置完成后，使用Terminal就能访问外部了，用下面的curl命令验证。之所以强调这个，是因为如果只开Proxy代理，会出现很诡异的问题，在网页上进行身份验证时，会长时间卡住，而如果使用API KEY验证，又会出其他的问题，我昨天花了几个小时在这里。

{% highlight shell %}
peter@~ $ curl -I www.google.com
HTTP/1.1 200 OK
Content-Type: text/html; charset=ISO-8859-1
...
{% endhighlight %}

安装步骤按照[项目README](https://github.com/google-gemini/gemini-cli)就好了: 

1. **Prerequisites:** Ensure you have [Node.js version 18](https://nodejs.org/en/download) or higher installed.
2. **Run the CLI:** Execute the following command in your terminal:

   ```bash
   npx https://github.com/google-gemini/gemini-cli
   ```

   Or install it with:

   ```bash
   npm install -g @google/gemini-cli
   gemini
   ```

3. **Pick a color theme**
4. **Authenticate:** When prompted, sign in with your personal Google account. This will grant you up to 60 model requests per minute and 1,000 model requests per day using Gemini.

5. 登陆之后，我让它分析这个博客的内容，并给出未来发展的一些建议。对话如下，它的回复有彩虹屁嫌疑 :-) 

    > Summarize the blogs in directory:~/workspace2/metaphy.github.io; what's the author focus on as an IT specilist, and how should the author extends his professional knowledge in future? You must respond in Chinese.

    好的，通过分析您在 ~/workspace2/metaphy.github.io/_posts 目录下的博客文章，可以清晰地看到一位资深IT技术专家的成长路径和技术热情。

    1. 深厚的Java基础与软件工程素养：您的博客生涯早期（约2007-2015年）有大量关于Java核心技术（如原型、线程、集合、注解）和设计模式的深入探讨。您几乎写了一个完整的设计模式系列，这表明您不仅掌握技术应用，更追求高质量的软件工程实践。

    2. 全面的后端技术栈：您的知识库非常广泛，覆盖了后端开发的各个方面，包括：
        * 数据库：从关系型数据库（MySQL, DB2）到NoSQL数据库（Redis, MongoDB）。
        * 操作系统与运维：熟悉Linux/CentOS环境，包括网络配置、IP设定、代理（Squid）安装等。
        * 编程语言：除了Java，您还掌握Python（爬虫、Web Server）、Node.js，并对Scala有所涉猎。

    3. 向大数据领域的拓展：从2021年左右开始，您的文章出现了明显的重心转移，开始深入研究大数据技术，例如Spark的核心概念（RDD, Partitions, Dataframe）和MapReduce思想。这说明您在主动跟进数据密集型应用的技术趋势。

    4. 对前沿技术的高度敏感和探索精神：最近几年（2023-2025年），您的文章内容再次升级，展现了您对技术前沿的强烈兴趣：
        * 新一代编程语言：您投入了大量精力学习Rust，探讨其内存安全、多线程、泛型等核心优势。
        * 人工智能（AI）：您开始关注向量数据库，并亲自体验了Google Gemini，这表明您已将视野投向了当前最热门的AI领域。
        * 分布式系统：研究了基于Redis的分布式锁等云原生时代的核心技术。  
  
    总结：
    您是一位经验丰富、技术功底扎实的资深后端/全栈工程师。您的技术画像可以概括为：以Java为根基，精通后端架构，逐步拓展到大数据处理，并积极拥抱Rust、AI等前沿技术。您乐于思考和总结，并拥有持续学习的强大动力。

    基于您当前扎实的技术积累和前瞻性的学习方向，以下是几个可以助您未来更上一层楼的发展建议：

    1. 方向一：深入大数据与AI，成为解决方案架构师 (Solution Architect)
        * 优势：您已具备“后端开发”+“大数据处理”的双重能力，这是非常稀缺和宝贵的。
        * 如何拓展：
            * 系统化学习AI工程：将您对向量数据库和Gemini的兴趣转化为系统性学习，深入研究LLM（大语言模型）应用开发、RAG（检索增强生成）、MLOps（机器学习运维）等。
            * 结合云平台：深入掌握一个主流云平台（如AWS, Azure, GCP）上的大数据和AI服务套件，将您的技术实践与云上解决方案相结合。
            * 目标职位：大数据架构师、AI平台架构师，专注于设计和构建能够处理海量数据、并集成AI能力的高性能、高可用系统。

    2. 方向二：专精高性能系统编程，成为领域专家 (Principal Engineer)
        * 优势：您对Rust的深入学习为您打开了通往高性能计算领域的大门。
        * 如何拓展：
            * 项目实践：尝试使用Rust来重构一些对性能有极致要求的服务（例如，替代Java中的某些高并发模块），或者参与一些知名的Rust开源项目（如网络代理、数据库
                、游戏引擎等）。
            * 深入底层：结合Rust，进一步学习操作系统、网络协议、编译器等底层知识，成为能够解决最棘手性能问题的专家。
            * 目标职位：系统软件工程师、性能优化专家，尤其在金融科技、云基础设施、游戏开发等领域，这类专家极具竞争力。

    3. 方向三：转型技术领导与布道者 (Tech Lead / Evangelist)
        * 优势：您长达近20年的博客写作，本身就是您热爱分享、善于总结的最佳证明。
        * 如何拓展：
            * 技术管理：在团队内部承担更多技术决策、方案设计和指导新人的职责，向技术负责人（Tech Lead）或架构师（Architect） 角色发展。
            * 技术布道：考虑将您的影响力从书面博客扩展到公开演讲、技术分享会或视频课程。您可以成为一名技术布道师，代表公司或社区向更广泛的开发者群体传递知识和最佳实践。您的博客就是您最好的名片。

 
    