"""F1.1 宣传海报文案 — 课程宣传海报文案生成"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class PosterCopyAgent(BaseAgent):
    """宣传海报文案智能体

    根据课程信息与营销目标，生成宣传海报文案，
    包含主标题、副标题、卖点列表、行动号召等。
    """

    agent_id = "F1.1"
    agent_name = "宣传海报文案"
    system_prompt_template = "category_f/poster_copy_system.j2"
    user_prompt_template = "category_f/poster_copy_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        kb_text = ""
        if context.get("knowledge"):
            kb_text = "\n".join(
                f"### {k}\n{v}" for k, v in context["knowledge"].items()
            )

        upstream_text = ""
        if context.get("upstream"):
            upstream_text = f"\n## 上游输入\n{context['upstream']}"

        return f"""请根据以下信息，生成宣传海报文案。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请提供3套不同风格的海报文案方案，每套包含：
1. **主标题**（10字以内，有冲击力）
2. **副标题**（20字以内，补充说明）
3. **核心卖点**（3-4个短句，每句8字以内）
4. **课程信息区**：适用年级、课时数、上课形式
5. **行动号召**（CTA）：报名引导文案
6. **视觉风格建议**：配色方案、主视觉元素、整体调性

风格方向：
- 方案A：专业权威型（突出课标对齐、师资实力）
- 方案B：趣味吸引型（突出动手实操、科技酷炫）
- 方案C：家长痛点型（突出升学价值、能力培养）"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(PosterCopyAgent, AgentInput)
