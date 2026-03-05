"""B1.5 大纲整合输出 Agent (P0)

将 B1.4 的细化单元内容整合为完整可交付的课程大纲。
接收 B1.4 upstream_output，输出供 B2.1 使用。
"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class OutlineIntegrationAgent(BaseAgent):
    """B1.5 大纲整合输出（接收B1.4，输出供B2.1）"""

    agent_id = "B1.5"
    agent_name = "大纲整合输出"
    system_prompt_template = "category_b/outline_integration_system.j2"
    user_prompt_template = "category_b/outline_integration_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        """回退提示词（当Jinja2模板不可用时）"""
        parts = [
            "## 大纲整合输出任务\n",
            f"### 用户需求\n{context['input']['query']}\n",
        ]

        if context.get("upstream"):
            parts.append(
                f"### 上游Agent输出（B1.4 单元细化主题）\n"
                f"```json\n{json.dumps(context['upstream'], ensure_ascii=False, indent=2)}\n```\n"
            )

        if context.get("knowledge"):
            parts.append("### 知识库参考\n")
            for kb_id, text in context["knowledge"].items():
                parts.append(f"#### {kb_id}\n{text}\n")

        parts.append(
            "### 输出要求\n"
            "请整合所有单元内容，输出完整的课程大纲文档，包含：\n"
            "课程封面信息、前言、目标总述、课标对齐总表、完整大纲、"
            "课时分配总表、评价体系总述、资源需求汇总、实施建议。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(OutlineIntegrationAgent, AgentInput)
