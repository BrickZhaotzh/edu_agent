"""C1.6 教学设计 Agent — 输出完整的教学设计文档（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class TeachingDesignAgent(BaseAgent):
    """C1.6 教学设计智能体

    按照教学设计规范输出完整的教学设计文档，涵盖学情分析、
    教学目标、重难点分析、教法学法、教学过程设计、评价设计。
    """

    agent_id = "C1.6"
    agent_name = "教学设计"
    system_prompt_template = "category_c/teaching_design_system.j2"
    user_prompt_template = "category_c/teaching_design_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：生成教学设计文档\n",
            f"**需求描述：** {inp.get('query', '')}",
        ]

        ctx = inp.get("context", {})
        if ctx:
            parts.append("\n**附加上下文：**")
            for k, v in ctx.items():
                parts.append(f"- {k}: {v}")

        upstream = context.get("upstream")
        if upstream:
            parts.append(f"\n**上游数据：**\n```json\n{json.dumps(upstream, ensure_ascii=False, indent=2)}\n```")

        knowledge = context.get("knowledge")
        if knowledge:
            parts.append(f"\n**参考知识：**\n```json\n{json.dumps(knowledge, ensure_ascii=False, indent=2)}\n```")

        parts.append(
            "\n请生成一份规范的教学设计文档，包含以下部分：\n"
            "1. **基本信息**：课题名称、学科、年级、课时、教材版本\n"
            "2. **教学分析**：\n"
            "   - 课标分析（对应的课程标准要求）\n"
            "   - 教材分析（本节内容在教材中的地位与作用）\n"
            "   - 学情分析（学生已有知识基础和认知特点）\n"
            "3. **教学目标**：知识与技能、过程与方法、情感态度价值观\n"
            "4. **教学重难点**：重点、难点及突破策略\n"
            "5. **教学策略**：教学方法、教学手段、信息技术融合\n"
            "6. **教学过程**：\n"
            "   - 各环节详细设计（含时间、教师活动、学生活动、设计意图）\n"
            "7. **板书设计**：结构化板书内容\n"
            "8. **教学评价**：过程性评价与终结性评价方案\n"
            "9. **教学反思**：预设反思要点"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(TeachingDesignAgent, AgentInput)
