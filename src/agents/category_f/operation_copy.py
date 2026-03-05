"""F1.4 运营文案 — 日常运营文案撰写"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class OperationCopyAgent(BaseAgent):
    """运营文案智能体

    生成日常运营所需的各类文案，包括公众号推文、
    朋友圈文案、社群通知、活动预告等。
    """

    agent_id = "F1.4"
    agent_name = "运营文案"
    system_prompt_template = "category_f/operation_copy_system.j2"
    user_prompt_template = "category_f/operation_copy_user.j2"
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

        return f"""请根据以下信息，撰写运营文案。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请根据需求场景输出对应文案：
1. **公众号推文版**（如适用）：标题 + 正文（800-1500字），含引导关注与转化
2. **朋友圈版**（如适用）：精炼文案（100字内）+ emoji + 配图建议
3. **社群通知版**（如适用）：群公告格式，突出关键信息与行动指引
4. **短信/push版**（如适用）：60字内精炼版本

写作要求：
- 符合教育行业调性，专业但不刻板
- 突出家长关心的核心价值点
- 包含明确的行动号召（CTA）
- 适当使用数据增强说服力"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(OperationCopyAgent, AgentInput)
