"""C3.2 教学审核 Agent — 教学内容全方位质量审核（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class TeachingReviewAgent(BaseAgent):
    """C3.2 教学审核智能体

    对教学内容进行全方位质量审核，包括科学准确性、教学规范性、
    课标对齐度、语言表达、政治敏感性等维度。
    """

    agent_id = "C3.2"
    agent_name = "教学审核"
    system_prompt_template = "category_c/teaching_review_system.j2"
    user_prompt_template = "category_c/teaching_review_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：教学内容审核\n",
            f"**待审核内容：** {inp.get('query', '')}",
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
            "\n请对以上教学内容进行全方位审核，输出审核报告，包含："
            "审核总评、各维度评分、具体问题清单（含位置、问题描述、"
            "严重程度和修改建议）、审核总结。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(TeachingReviewAgent, AgentInput)
