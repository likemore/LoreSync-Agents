# 🌍 LoreSync-Agents

> **A Multi-Agent Localization & Lore Consistency Framework for RPGs.**
> 基于多 Agent 协作与 RAG 的游戏剧情本地化与世界观一致性校验系统。

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Prototype-orange)

在重设定类游戏（如科幻、机甲、奇幻 RPG）的本地化过程中，保持上下文语境连贯和专有名词（机体型号、阵营、术语）的绝对一致性是最大的挑战。**LoreSync-Agents** 通过引入多 Agent 协同和动态术语库（RAG），将繁杂的后期人工校验时间缩短了 70% 以上，实现高质量的自动化本地化工作流。

## ✨ 核心特性 (Core Features)

- **🧠 语境长链推理 (Context-Aware Reasoning):** 拒绝逐句机翻。Context Agent 会前置分析文本的情感倾向、危急态势及角色身份，输出动态的语境提示词。
- **📚 强制术语校验 (Terminology RAG):** 挂载本地专有名词库（支持向 Milvus/Chroma 扩展），在翻译前后双向拦截术语偏差。
- **🤖 多 Agent 闭环审核 (Multi-Agent QA Loop):** 独立的 QA Agent 执行逆向交叉验证。如果不符合术语表或出现生硬机翻，QA Agent 会输出诊断报告并可配置打回重译。

## 🏗 系统架构 (Architecture)

系统由以下核心模块流转协作：

1. `TerminologyDB`: 检索源文本命中的世界观专属名词。
2. `Context Agent`: 抽取长链语境与隐藏设定。
3. `Translation Agent`: 结合术语与语境约束，生成初译文本。
4. `QA Agent`: 执行 `[原文] x [初译本] x [术语表]` 的三向交叉比对，输出最终校验状态。
