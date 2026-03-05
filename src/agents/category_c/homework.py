"""C1.9 课后作业 Agent — 设计分层课后作业和练习（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class HomeworkAgent(BaseAgent):
    """C1.9 课后作业智能体

    设计分层、多样化的课后作业和练习，覆盖基础巩固、能力提升和
    拓展创新三个层次，符合「双减」政策要求。
    """

    agent_id = "C1.9"
    agent_name = "课后作业"
    system_prompt_template = "category_c/homework_system.j2"
    user_prompt_template = "category_c/homework_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：设计课后作业\n",
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
            "\n请设计一套分层课后作业，要求：\n"
            "1. **基础巩固层（必做）**：\n"
            "   - 3-5道基础题，覆盖本课核心知识点\n"
            "   - 题型：填空、选择、判断、简答等\n"
            "   - 难度：课堂练习水平，确保大部分学生能独立完成\n"
            "2. **能力提升层（选做）**：\n"
            "   - 2-3道应用题，需要综合运用本课知识\n"
            "   - 题型：编程实践、方案设计、分析论述等\n"
            "   - 难度：需要一定思考和探索\n"
            "3. **拓展挑战层（挑战）**：\n"
            "   - 1-2道开放性题目，鼓励创新和深度探索\n"
            "   - 题型：项目式作业、研究性学习、创意设计等\n"
            "   - 难度：需要自主学习和拓展\n"
            "4. **参考答案**：每道题的详细解答过程\n"
            "5. **评分标准**：每道题的评分要点和分值分配\n"
            "6. **完成时间建议**：各层级的预估完成时间"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(HomeworkAgent, AgentInput)
