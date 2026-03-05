"""C2.1 实验PRD Agent — 撰写实验项目需求文档（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class ExperimentPRDAgent(BaseAgent):
    """C2.1 实验PRD智能体

    为科创教育实验项目撰写产品需求文档（PRD），
    详细描述实验目标、材料清单、操作流程、安全注意事项等。
    """

    agent_id = "C2.1"
    agent_name = "实验PRD"
    system_prompt_template = "category_c/experiment_prd_system.j2"
    user_prompt_template = "category_c/experiment_prd_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：撰写实验PRD\n",
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
            "\n请撰写一份完整的实验项目PRD，包含实验名称、实验目标、适用学段、"
            "材料清单、实验原理、操作步骤、安全注意事项、预期结果、评价标准、常见问题排查。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(ExperimentPRDAgent, AgentInput)
