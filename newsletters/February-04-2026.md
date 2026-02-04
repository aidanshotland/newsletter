## 🚨 TOP TRENDS

### Notepad++ supply chain attack breakdown
A critical supply chain attack compromised Notepad++'s update infrastructure between June and October 2025, allowing threat actors to deploy malware. This incident highlights the vulnerability of widely used software to sophisticated attacks targeting update mechanisms. Developers should prioritize robust software supply chain security and verify all dependencies, even for trusted tools.
[Source: Hacker News](https://securelist.com/notepad-supply-chain-attack/118708/)

### Xcode 26.3 unlocks the power of agentic coding
Apple's Xcode 26.3 introduces native support for agentic coding, integrating AI agents like Anthropic's Claude Agent and OpenAI's Codex directly into the IDE. This update leverages the Model Context Protocol (MCP) to enable AI agents to autonomously handle complex coding tasks, including subagents and background processes. Developers gain powerful AI assistance within their familiar Apple development environment, streamlining workflows for app creation and maintenance.
[Source: Ars Technica](https://arstechnica.com/apple/2026/02/xcode-26-3-adds-support-for-claude-codex-and-other-agentic-tools-via-mcp/)

### Deno Sandbox
Deno has introduced Deno Sandbox, a new platform for securely executing untrusted code, particularly LLM-generated code that interacts with external APIs. It utilizes lightweight Linux microVMs with defense-in-depth security measures like granular permission controls and process isolation. This offers developers a safer environment for running AI-generated code, mitigating risks associated with arbitrary code execution and credential exposure.
[Source: Hacker News](https://deno.com/blog/introducing-deno-sandbox)

### France dumps Zoom and Teams as Europe seeks digital autonomy from the US
France has announced it will stop using Zoom and Microsoft Teams, opting for European alternatives in a move towards digital sovereignty from US tech giants. This decision underscores a broader European initiative to reduce reliance on non-EU cloud services and ensure data privacy and security for government communications. Developers and organizations should anticipate an increased demand for locally hosted and open-source collaboration tools in the European market.
[Source: Hacker News](https://apnews.com/article/europe-digital-sovereignty-big-tech-9f5388b68a0648514cebc8d92f682060)

## 🤖 AI INNOVATION

### Qwen3-Coder-Next for Agentic Coding
Alibaba's Qwen3-Coder-Next is a new open-weight model specifically fine-tuned for agentic coding applications, outperforming larger models in executable synthesis and RL-based environment interaction. Built on a hybrid MoE architecture, it achieves strong coding performance at lower inference costs and memory footprints. This provides a powerful, efficient, and open-source option for developers building autonomous coding agents or integrating advanced AI into their development tools.
[Source: Qwen.ai](https://qwen.ai/blog?id=qwen3-coder-next)

### OpenAI optimized its inference stack for all API customers to make its models faster.
OpenAI has announced a 40% speed increase for its GPT-5.2 and GPT-5.2-Codex models for all API customers due to inference stack optimizations. This significant performance boost directly translates to faster response times and lower latency for applications utilizing these advanced AI models. Developers can now build more responsive and efficient AI-powered features, improving user experience and potentially reducing operational costs for high-volume inference tasks.
[Source: TLDR_AI](https://threadreaderapp.com/thread/2018838297221726482.html?utm_source=tldrai)

### Agent Trace: Cursor Proposes an Open Specification for AI Code Attribution
Cursor has released Agent Trace, a draft open specification designed to standardize the attribution of AI-generated code within software projects. This RFC proposes a vendor-neutral format for recording AI contributions alongside human authorship in version-controlled codebases. This initiative aims to address provenance and accountability in AI-assisted development, offering a critical tool for maintaining code integrity and understanding the mixed authorship of modern software.
[Source: InfoQ](https://www.infoq.com/news/2026/02/agent-trace-cursor/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global)

### Vercel Introduces Skills.sh, an Open Ecosystem for Agent Commands
Vercel has launched Skills.sh, an open-source tool enabling AI agents to execute reusable actions or "skills" through a standardized command-line interface. This platform aims to create a discoverable ecosystem of agent capabilities, akin to a package manager for AI actions. Developers can leverage Skills.sh to easily integrate and share agent functionalities, fostering a more collaborative and efficient landscape for building agentic applications.
[Source: InfoQ](https://www.infoq.com/news/2026/02/vercel-agent-skills/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global)

### vm0-ai/vm0: the easiest way to run natural language-described workflows automatically
The vm0-ai/vm0 project on GitHub offers a platform to execute natural language-described workflows automatically in a cloud sandbox environment. This tool allows users to define complex tasks using plain English, which an autonomous agent then interprets and performs 24/7. Developers can use vm0 to automate repetitive or complex operational tasks, abstracting away the underlying scripting and infrastructure management through intuitive language commands.
[Source: GitHub Trending](https://github.com/vm0-ai/vm0)

## 🛡️ DEV & SECURITY

### AliSQL: Alibaba's open-source MySQL with vector and DuckDB engines
Alibaba has open-sourced AliSQL, an enhanced version of MySQL that integrates vector and DuckDB engines for advanced data processing. This hybrid database offers capabilities for both traditional transactional workloads and specialized analytical tasks, including vector similarity search. Developers can leverage AliSQL to build applications requiring combined SQL and vector database functionalities, such as AI-powered search or real-time analytics, within a familiar MySQL ecosystem.
[Source: Hacker News](https://github.com/alibaba/AliSQL)

### Java Explores Carrier Classes to Extend Data-Oriented Programming Beyond Records
OpenJDK's Amber project is proposing "carrier classes" and "carrier interfaces" to expand record-style data modeling in Java beyond the current limitations of records. This proposal aims to maintain concise state descriptions, derived methods, and pattern matching while offering more structural flexibility for Java types. This evolution allows developers to apply data-oriented programming principles more broadly, improving code clarity and reducing boilerplate for diverse data structures.
[Source: InfoQ](https://www.infoq.com/news/2026/02/java-beyond-records/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global)

### FBI couldn't get into WaPo reporter's iPhone because Lockdown Mode enabled
The FBI reportedly failed to access a Washington Post reporter's iPhone because Apple's Lockdown Mode feature was enabled. Lockdown Mode significantly hardens device security by severely limiting functionalities that could be exploited by sophisticated cyberattacks, such as Pegasus spyware. This case highlights the effectiveness of Lockdown Mode for individuals at high risk of targeted digital attacks, reinforcing its value for enhanced personal and journalistic privacy.
[Source: Hacker News](https://www.404media.co/fbi-couldnt-get-into-wapo-reporters-iphone-because-it-had-lockdown-mode-enabled/)

### GitHub Reworks Layered Defenses After Legacy Protections Block Legitimate Traffic
GitHub engineers discovered that stale abuse-mitigation rules were inadvertently blocking legitimate user traffic with "Too Many Requests" errors. This incident revealed the complexity of managing layered security defenses and the need for continuous evaluation of protection mechanisms. Organizations should regularly audit and update their security configurations to prevent unintended service disruptions, ensuring that older rules are retired when no longer relevant.
[Source: InfoQ](https://www.infoq.com/news/2026/02/github-layered-def/?utm_campaign=infoq_content&utm_source=infoq&utm_medium=feed&utm_term=global)

Generated from 118 articles across 9 sources.