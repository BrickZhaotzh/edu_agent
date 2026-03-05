"""C1.10 评价量规 Agent — 设计教学评价量规（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class RubricAgent(BaseAgent):
    """C1.10 评价量规智能体

    设计科学、可操作的教学评价量规（rubric），
    支持过程性评价和终结性评价，促进以评促学。
    """

    agent_id = "C1.10"
    agent_name = "评价量规"
    system_prompt_template = "category_c/rubric_system.j2"
    user_prompt_template = "category_c/rubric_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：设计评价量规\n",
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
            "\n请设计一套教学评价量规，要求：\n"
            "1. **评价维度设计**（建议4-6个维度）：\n"
            "   - 知识掌握：对核心概念和原理的理解程度\n"
            "   - 技能应用：实际操作和动手能力\n"
            "   - 思维能力：分析、推理、创新思维表现\n"
            "   - 协作交流：团队合作和表达能力\n"
            "   - 学习态度：参与度、主动性、专注度\n"
            "   - （可根据课程特点增减维度）\n"
            "2. **等级标准**（每个维度4个等级）：\n"
            "   - 优秀（A）：具体描述达到优秀的表现特征\n"
            "   - 良好（B）：具体描述达到良好的表现特征\n"
            "   - 合格（C）：具体描述达到合格的表现特征\n"
            "   - 待提升（D）：具体描述需要改进的表现特征\n"
            "3. **权重分配**：各维度的权重百分比\n"
            "4. **评价方式建议**：\n"
            "   - 教师评价、同伴互评、自评的使用场景\n"
            "   - 过程性评价与终结性评价的结合方式\n"
            "5. **评分表模板**：可直接使用的评分记录表\n"
            "6. **使用说明**：评价量规的使用方法和注意事项"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(RubricAgent, AgentInput)
