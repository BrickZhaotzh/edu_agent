"""C5.2 课标分析 Agent — 深度课程标准解读与分析（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class StandardAnalysisAgent(BaseAgent):
    """C5.2 课标分析智能体

    深度解读和分析国家课程标准（如信息科技课标、科学课标等），
    提取核心素养要求、内容标准、学业要求和学业质量标准。
    """

    agent_id = "C5.2"
    agent_name = "课标分析"
    system_prompt_template = "category_c/standard_analysis_system.j2"
    user_prompt_template = "category_c/standard_analysis_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：课程标准分析\n",
            f"**分析需求：** {inp.get('query', '')}",
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
            "\n请进行深度课标分析，输出：课标概述、核心素养解读、"
            "内容标准分析（按学段/模块）、学业要求提取、教学建议、"
            "评价建议、与其他学科的交叉映射。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(StandardAnalysisAgent, AgentInput)
