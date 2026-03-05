"""B1.1 课程整体规划 Agent (P1)

综合课程规划，输出课程目标、时间线、资源需求等完整规划方案。
"""

from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class CoursePlanningAgent(BaseAgent):
    """B1.1 课程整体规划"""

    agent_id = "B1.1"
    agent_name = "课程整体规划"
    system_prompt_template = "category_b/course_planning_system.j2"
    user_prompt_template = "category_b/course_planning_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        """回退提示词（当Jinja2模板不可用时）"""
        parts = [
            "## 课程整体规划任务\n",
            f"### 用户需求\n{context['input']['query']}\n",
        ]

        if context.get("upstream"):
            import json
            parts.append(f"### 上游数据\n```json\n{json.dumps(context['upstream'], ensure_ascii=False, indent=2)}\n```\n")

        if context.get("knowledge"):
            parts.append("### 知识库参考\n")
            for kb_id, text in context["knowledge"].items():
                parts.append(f"#### {kb_id}\n{text}\n")

        parts.append(
            "### 输出要求\n"
            "请输出完整的课程整体规划方案，包含：课程概述、课程目标、"
            "课程大纲、实施时间线、资源需求、评价方案。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(CoursePlanningAgent, AgentInput)
