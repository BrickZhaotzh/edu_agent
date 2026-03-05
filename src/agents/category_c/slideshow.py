"""C1.5 课件生成 Agent — 生成PPT课件内容框架（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class SlideshowAgent(BaseAgent):
    """C1.5 课件生成智能体

    根据教学设计和逐字稿生成结构清晰的PPT课件内容框架，
    包括每页幻灯片的标题、要点、视觉建议和备注。
    """

    agent_id = "C1.5"
    agent_name = "课件生成"
    system_prompt_template = "category_c/slideshow_system.j2"
    user_prompt_template = "category_c/slideshow_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：生成课件内容大纲\n",
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

        knowledge = context.get("knowledge")
        if knowledge:
            parts.append(f"\n**参考知识：**\n```json\n{json.dumps(knowledge, ensure_ascii=False, indent=2)}\n```")

        parts.append(
            "\n请生成课件（PPT）内容大纲，要求：\n"
            "1. **封面页**：课程标题、副标题、授课信息\n"
            "2. **目录页**：教学环节概览\n"
            "3. **内容页**：每页包含标题、核心要点（不超过5条）、配图建议、动画建议\n"
            "4. **互动页**：标注需要学生互动的页面（提问、讨论、实操等）\n"
            "5. **总结页**：知识回顾、课后任务\n"
            "6. 每页附带演讲者备注（对应逐字稿片段）\n"
            "7. 整体风格适合K-12课堂，图文并茂、重点突出"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(SlideshowAgent, AgentInput)
