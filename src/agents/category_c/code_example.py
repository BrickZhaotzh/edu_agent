"""C2.2 编程样例 Agent — 设计教学编程代码样例（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class CodeExampleAgent(BaseAgent):
    """C2.2 编程样例智能体

    为中小学编程教学设计代码样例，支持Python、Scratch、Arduino等
    常用教学语言和平台，代码注释清晰、难度适当。
    """

    agent_id = "C2.2"
    agent_name = "编程样例"
    system_prompt_template = "category_c/code_example_system.j2"
    user_prompt_template = "category_c/code_example_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：设计编程样例\n",
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

        parts.append(
            "\n请设计一份完整的编程教学样例，包含项目名称、适用学段、编程语言/平台、"
            "学习目标、完整代码（含详细中文注释）、运行说明、拓展挑战、常见错误提示。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(CodeExampleAgent, AgentInput)
