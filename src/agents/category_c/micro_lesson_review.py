"""C3.4 微课评审 Agent — 微课内容质量评审（P2）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class MicroLessonReviewAgent(BaseAgent):
    """C3.4 微课评审智能体

    评审微课（5-15分钟短视频课程）的内容质量，
    从教学设计、内容准确性、视觉呈现、节奏把控等维度进行综合评审。
    """

    agent_id = "C3.4"
    agent_name = "微课评审"
    system_prompt_template = "category_c/micro_lesson_review_system.j2"
    user_prompt_template = "category_c/micro_lesson_review_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：微课内容评审\n",
            f"**待评审内容：** {inp.get('query', '')}",
        ]

        ctx = inp.get("context", {})
        if ctx:
            parts.append("\n**附加上下文：**")
            for k, v in ctx.items():
                parts.append(f"- {k}: {v}")

        upstream = context.get("upstream")
        if upstream:
            parts.append(f"\n**上游数据：**\n```json\n{json.dumps(upstream, ensure_ascii=False, indent=2)}\n```")

        parts.append(
            "\n请对以上微课内容进行全面评审，输出评审报告，包含："
            "综合评分、各维度评分及评语、亮点总结、改进建议清单、总体评价。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(MicroLessonReviewAgent, AgentInput)
