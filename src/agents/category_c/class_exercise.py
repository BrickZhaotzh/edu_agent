"""C3.3 随堂练习 Agent — 设计课堂即时练习题（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class ClassExerciseAgent(BaseAgent):
    """C3.3 随堂练习智能体

    设计课堂即时练习题，帮助教师在教学过程中检测学生学习效果，
    练习题短小精悍、针对性强，可在3-5分钟内完成。
    """

    agent_id = "C3.3"
    agent_name = "随堂练习"
    system_prompt_template = "category_c/class_exercise_system.j2"
    user_prompt_template = "category_c/class_exercise_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：设计随堂练习\n",
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
            "\n请设计一组随堂练习（3-5题），每道题标注考查知识点，"
            "提供参考答案和讲评要点，总用时控制在3-5分钟。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(ClassExerciseAgent, AgentInput)
