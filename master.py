import json
from typing import Dict, Any

# ==========================================
# 0. 底层 LLM 调用接口 (需替换为真实 API)
# ==========================================
def call_llm(system_prompt: str, user_content: str) -> str:
    """
    模拟调用大语言模型 API。
    实际落地时，请在此处接入 OpenAI、Gemini 或 DeepSeek 的 SDK。
    """
    # 这里通过简单的关键字匹配来模拟 LLM 的智能回复，保证代码可直接运行演示
    if "语境与语气分析" in system_prompt:
        return "语气：急迫、紧张。语境：战场上的紧急汇报，带有科幻/机甲背景。角色态度：对长官保持敬意，但局势危急。"
    
    elif "执行本地化翻译" in system_prompt:
        return "指挥官，京宝梵的推进器过热了！如果我们不立刻关闭米诺夫斯基驱动器，这台机动战士就会爆炸！"
    
    elif "QA 与术语校验" in system_prompt:
        return json.dumps({
            "status": "PASS",
            "final_translation": "指挥官，京宝梵的推进器过热了！如果我们不立刻关闭米诺夫斯基驱动器，这台机动战士就会爆炸！",
            "issues_fixed": "未发现术语冲突，翻译符合中式科幻轻小说语感。",
            "terminology_used": ["京宝梵", "米诺夫斯基驱动器", "机动战士"]
        }, ensure_ascii=False)
    
    return "LLM 回复"

# ==========================================
# 1. RAG 组件：术语知识库 (向量数据库的平替)
# ==========================================
class TerminologyDB:
    def __init__(self):
        # 模拟预先导入的世界观设定词典
        self.db = {
            "Kampfer": "京宝梵",
            "Minovsky drive": "米诺夫斯基驱动器",
            "MS": "机动战士 (Mobile Suit)",
            "Commander": "指挥官"
        }
        
    def search(self, text: str) -> Dict[str, str]:
        """模拟向量检索，提取文本中命中的专有名词及其标准译名"""
        matched_terms = {}
        for eng_term, zh_term in self.db.items():
            if eng_term.lower() in text.lower():
                matched_terms[eng_term] = zh_term
        return matched_terms

# ==========================================
# 2. 多 Agent 定义
# ==========================================
class ContextAgent:
    def analyze(self, source_text: str) -> str:
        sys_prompt = "你是一个游戏剧情语境分析师。请分析输入文本的语境与语气分析、情感色彩以及潜在的背景设定。输出简短的分析报告。"
        return call_llm(sys_prompt, f"原文: {source_text}")

class TranslationAgent:
    def translate(self, source_text: str, context: str, terms: Dict[str, str]) -> str:
        sys_prompt = (
            "你是一个资深游戏本地化翻译专家。请严格参考提供的【语境设定】和【术语表】执行本地化翻译。\n"
            "要求：符合中文母语习惯，保持角色的口癖与情感。"
        )
        user_prompt = f"""
        【语境设定】: {context}
        【强制术语表】: {json.dumps(terms, ensure_ascii=False)}
        【待翻译原文】: {source_text}
        """
        return call_llm(sys_prompt, user_prompt)

class QAAgent:
    def verify(self, source_text: str, draft_translation: str, terms: Dict[str, str]) -> Dict[str, Any]:
        sys_prompt = (
            "你是一个无情的本地化 QA 与术语校验机器。你的任务是交叉比对原文、初译和术语表。\n"
            "1. 检查术语是否被正确且一致地使用。\n"
            "2. 检查是否有漏译或生硬的机器翻译感。\n"
            "请必须以 JSON 格式输出结果，包含字段：status (PASS/FAIL), final_translation, issues_fixed, terminology_used。"
        )
        user_prompt = f"""
        【原文】: {source_text}
        【初译本】: {draft_translation}
        【应包含的术语】: {json.dumps(terms, ensure_ascii=False)}
        """
        response = call_llm(sys_prompt, user_prompt)
        try:
            return json.loads(response)
        except:
            return {"status": "ERROR", "final_translation": draft_translation, "error": "JSON 解析失败"}

# ==========================================
# 3. 主编排流 (Workflow Orchestration)
# ==========================================
class LocalizationWorkflow:
    def __init__(self):
        self.term_db = TerminologyDB()
        self.context_agent = ContextAgent()
        self.translation_agent = TranslationAgent()
        self.qa_agent = QAAgent()
        
    def process(self, source_text: str):
        print(f"📥 收到源文本: {source_text}\n" + "-"*40)
        
        # 步骤 1: 检索术语 (RAG)
        terms = self.term_db.search(source_text)
        print(f"🔍 命中术语库: {terms}")
        
        # 步骤 2: Context Agent 分析语境 (长链推理的前置准备)
        context = self.context_agent.analyze(source_text)
        print(f"🧠 语境分析完成:\n{context}")
        
        # 步骤 3: Translation Agent 进行初译
        draft = self.translation_agent.translate(source_text, context, terms)
        print(f"✍️  初版翻译生成: {draft}")
        
        # 步骤 4: QA Agent 校验并输出闭环结果
        qa_result = self.qa_agent.verify(source_text, draft, terms)
        print("\n✅ QA 校验报告:")
        print(json.dumps(qa_result, indent=2, ensure_ascii=False))
        
        return qa_result

# ==========================================
# 测试运行
# ==========================================
if __name__ == "__main__":
    # 一段典型的带有复杂设定的机甲类游戏文本
    test_text = "Commander, the Kampfer unit's thrusters are overheating! If we don't disengage the Minovsky drive, the MS will explode!"
    
    workflow = LocalizationWorkflow()
    workflow.process(test_text)