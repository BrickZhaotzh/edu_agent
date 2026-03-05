"""C3.1 拼音标注 Agent — 为低年级教学材料添加拼音标注（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class PinyinAnnotatorAgent(BaseAgent):
    """C3.1 拼音标注智能体

    为低年级（小学1-3年级）教学材料添加拼音标注，
    确保拼音准确、格式规范，帮助低龄学生自主阅读。
    """

    agent_id = "C3.1"
    agent_name = "拼音标注"
    system_prompt_template = "category_c/pinyin_annotator_system.j2"
    user_prompt_template = "category_c/pinyin_annotator_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：拼音标注\n",
            f"**待标注文本：** {inp.get('query', '')}",
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
            "\n请为以上文本内容添加准确的拼音标注。"
            "注意多音字需根据语境选择正确读音，英文和数字无需标注。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(PinyinAnnotatorAgent, AgentInput)
