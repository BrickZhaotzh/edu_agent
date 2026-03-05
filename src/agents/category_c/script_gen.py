"""C1.3 逐字稿生成 Agent — 基于问题链生成教师课堂逐字稿（P0）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import ScriptGenInput, ScriptGenOutput


class ScriptGenAgent(BaseAgent):
    """C1.3 逐字稿生成智能体

    核心管线中间节点：接收 C1.1 问题链设计的输出，
    生成教师课堂教学逐字稿，输出将作为 C1.4 分镜脚本的上游输入。
    管线: C1.1 → C1.3 → C1.4
    """

    agent_id = "C1.3"
    agent_name = "逐字稿生成"
    system_prompt_template = "category_c/script_gen_system.j2"
    user_prompt_template = "category_c/script_gen_user.j2"
    input_model = ScriptGenInput
    output_model = ScriptGenOutput

    def _build_context(self, input_data: ScriptGenInput) -> dict[str, Any]:
        """覆写上下文构建，将 question_chain 字段合并到 upstream 供模板使用"""
        context = super()._build_context(input_data)

        # 如果 question_chain 字段有数据，合并到 upstream 方便模板和回退提示词使用
        if input_data.question_chain:
            upstream = context.get("upstream") or {}
            if not isinstance(upstream, dict):
                upstream = {}
            upstream["question_chain"] = input_data.question_chain
            context["upstream"] = upstream

        return context

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：生成教学逐字稿\n",
            f"**课时主题：** {inp.get('lesson_topic', '')}",
            f"**课时时长：** {inp.get('duration_minutes', 45)} 分钟",
        ]

        # 问题链数据（来自 C1.1 上游或直接输入）
        question_chain = inp.get("question_chain", [])
        upstream = context.get("upstream", {})
        if not question_chain and isinstance(upstream, dict):
            question_chain = upstream.get("question_chain", [])

        if question_chain:
            parts.append("\n**问题链（来自C1.1上游）：**")
            for i, q in enumerate(question_chain, 1):
                parts.append(f"{i}. {json.dumps(q, ensure_ascii=False)}")

        query = inp.get("query", "")
        if query:
            parts.append(f"\n**补充需求：** {query}")

        if upstream:
            parts.append(f"\n**上游管线数据：**\n```json\n{json.dumps(upstream, ensure_ascii=False, indent=2)}\n```")

        knowledge = context.get("knowledge")
        if knowledge:
            parts.append(f"\n**参考知识：**\n```json\n{json.dumps(knowledge, ensure_ascii=False, indent=2)}\n```")

        parts.append(
            "\n请基于以上问题链和课时信息，生成一份完整的教师逐字稿，要求：\n"
            "1. 按教学环节分段（导入、新授、练习、总结等），每段标注时间分配\n"
            "2. 逐字记录教师的口语表达，包括过渡语、提问语、引导语\n"
            "3. 标注互动环节（学生活动、小组讨论、实操练习等）\n"
            "4. 标注关键知识点和教学重点\n"
            "5. 语言风格适合K-12课堂，生动、亲切、有感染力"
        )
        return "\n".join(parts)

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> ScriptGenOutput:
        """解析输出，尝试提取逐字稿分段和字数统计"""
        output = ScriptGenOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
            total_word_count=len(raw_output),
        )
        try:
            if "```json" in raw_output:
                json_str = raw_output.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_str)
                if isinstance(data, list):
                    output.script_sections = data
                elif isinstance(data, dict) and "script_sections" in data:
                    output.script_sections = data["script_sections"]
        except (json.JSONDecodeError, IndexError):
            pass
        return output


if __name__ == "__main__":
    run_agent_cli(ScriptGenAgent, ScriptGenInput)
