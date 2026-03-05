"""F3.1 FAQ智能答疑 — 课程FAQ智能问答系统"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class FAQBotAgent(BaseAgent):
    """FAQ智能答疑智能体

    基于课程知识库，提供智能问答服务，覆盖课程内容答疑、
    学具使用指导、常见问题解答等场景。
    """

    agent_id = "F3.1"
    agent_name = "FAQ智能答疑"
    system_prompt_template = "category_f/faq_bot_system.j2"
    user_prompt_template = "category_f/faq_bot_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _build_context(self, input_data: AgentInput) -> dict[str, Any]:
        context = super()._build_context(input_data)
        # 自动加载FAQ知识库
        self.kb.load("faq")
        context["knowledge"] = {
            "faq": self.kb.get_context_text("faq", input_data.query)
        }
        return context

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        kb_text = context.get("knowledge", {}).get("faq", "（无相关FAQ文档）")

        return f"""请基于FAQ知识库回答以下问题。

## 用户问题
{inp['query']}

## FAQ知识库参考
{kb_text}

请输出：
1. **直接回答**：简洁明了地回答用户问题
2. **详细说明**：必要时提供补充解释与操作步骤
3. **相关问题推荐**：列出2-3个相关常见问题
4. **未匹配处理**：如果知识库中无相关信息，诚实说明并给出建议渠道

回答要求：
- 语言亲切、易懂，适合家长和学生阅读
- 涉及操作步骤时使用编号列表
- 重要信息用加粗标注"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(FAQBotAgent, AgentInput)
