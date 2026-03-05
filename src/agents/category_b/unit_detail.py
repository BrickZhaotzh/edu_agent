"""B1.4 单元细化主题 Agent (P0)

将 B1.3 的宏观单元主题拆解为具体子主题和课时安排。
接收 B1.3 upstream_output，输出供 B1.5 使用。
"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class UnitDetailAgent(BaseAgent):
    """B1.4 单元细化主题（接收B1.3，输出供B1.5）"""

    agent_id = "B1.4"
    agent_name = "单元细化主题"
    system_prompt_template = "category_b/unit_detail_system.j2"
    user_prompt_template = "category_b/unit_detail_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        """回退提示词（当Jinja2模板不可用时）"""
        parts = [
            "## 单元细化主题任务\n",
            f"### 用户需求\n{context['input']['query']}\n",
        ]

        if context.get("upstream"):
            parts.append(
                f"### 上游Agent输出（B1.3 单元主题架构）\n"
                f"```json\n{json.dumps(context['upstream'], ensure_ascii=False, indent=2)}\n```\n"
            )

        if context.get("knowledge"):
            parts.append("### 知识库参考\n")
            for kb_id, text in context["knowledge"].items():
                parts.append(f"#### {kb_id}\n{text}\n")

        parts.append(
            "### 输出要求\n"
            "请对每个单元进行细化展开，包含：子主题列表、课时安排表、"
            "关键学习活动、评价任务、资源清单。\n"
            "子主题需标注认知层次（Bloom分类）和建议教学策略。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(UnitDetailAgent, AgentInput)
