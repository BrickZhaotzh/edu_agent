"""C1.2 方案稿撰写 Agent — 撰写规范的教学方案文档（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class ProposalDraftAgent(BaseAgent):
    """C1.2 方案稿撰写智能体

    根据教学需求撰写完整的教学方案稿，包含课程概述、教学目标、
    教学重难点、教学流程、评价方式等核心要素。
    """

    agent_id = "C1.2"
    agent_name = "方案稿撰写"
    system_prompt_template = "category_c/proposal_draft_system.j2"
    user_prompt_template = "category_c/proposal_draft_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：撰写教学方案稿\n",
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
            "\n请撰写一份完整的教学方案稿，包含课程信息、教学目标、教学重难点、"
            "教学准备、教学流程（含时间分配）、板书设计、教学反思要点。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(ProposalDraftAgent, AgentInput)
