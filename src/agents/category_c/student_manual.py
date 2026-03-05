"""C1.7 学生手册 Agent — 编写学生活动手册（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class StudentManualAgent(BaseAgent):
    """C1.7 学生手册智能体

    编写适合中小学生阅读和使用的学生活动手册，
    语言通俗易懂，包含学习目标、活动指引、操作步骤等。
    """

    agent_id = "C1.7"
    agent_name = "学生手册"
    system_prompt_template = "category_c/student_manual_system.j2"
    user_prompt_template = "category_c/student_manual_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：生成学生手册\n",
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
            "\n请生成一份面向学生的学习手册，要求：\n"
            "1. **课程信息**：课题名称、课时、学习准备\n"
            "2. **学习目标**：用学生能理解的语言描述本课要达成的目标\n"
            "3. **知识卡片**：核心概念的通俗解释，配合生活化类比\n"
            "4. **操作指南**：分步骤的操作说明（适用于实操类课程）\n"
            "   - 每步配截图/示意图描述\n"
            "   - 标注易错点和注意事项\n"
            "5. **课堂练习**：与教学环节对应的练习任务\n"
            "6. **知识小结**：本课核心要点归纳（思维导图形式）\n"
            "7. **拓展阅读**：推荐资源和延伸学习方向\n"
            "8. 语言风格须符合目标学段学生的认知水平，生动有趣"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(StudentManualAgent, AgentInput)
