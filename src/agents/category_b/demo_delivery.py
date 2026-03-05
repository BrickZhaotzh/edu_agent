"""B2.2 Demo课交付 Agent (P3)

将教学设计打包为可直接演示交付的Demo课材料。
"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class DemoDeliveryAgent(BaseAgent):
    """B2.2 Demo课交付"""

    agent_id = "B2.2"
    agent_name = "Demo课交付"
    system_prompt_template = "category_b/demo_delivery_system.j2"
    user_prompt_template = "category_b/demo_delivery_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        """回退提示词（当Jinja2模板不可用时）"""
        parts = [
            "## Demo课交付包装任务\n",
            f"### 用户需求\n{context['input']['query']}\n",
        ]

        if context.get("upstream"):
            parts.append(
                f"### 上游参考数据\n"
                f"```json\n{json.dumps(context['upstream'], ensure_ascii=False, indent=2)}\n```\n"
            )

        if context.get("knowledge"):
            parts.append("### 知识库参考\n")
            for kb_id, text in context["knowledge"].items():
                parts.append(f"#### {kb_id}\n{text}\n")

        parts.append(
            "### 输出要求\n"
            "请输出完整的Demo课交付方案，包含：Demo课概述、核心卖点提炼、"
            "教学流程、学生互动体验设计、配套材料清单、演示注意事项、课后跟进方案。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(DemoDeliveryAgent, AgentInput)
