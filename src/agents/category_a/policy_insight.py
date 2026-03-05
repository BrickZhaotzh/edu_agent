"""A1.1 政策洞察分析 — 多渠道政策检索+课标映射+课程适配建议"""

import json
import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import PolicyInsightInput, PolicyInsightOutput

logger = logging.getLogger(__name__)


class PolicyInsightAgent(BaseAgent):
    """政策洞察分析智能体

    对指定省份/学科方向进行政策检索，映射至课程标准，
    并给出课程适配建议。
    """

    agent_id = "A1.1"
    agent_name = "政策洞察分析"
    system_prompt_template = "category_a/policy_insight_system.j2"
    user_prompt_template = "category_a/policy_insight_user.j2"
    input_model = PolicyInsightInput
    output_model = PolicyInsightOutput

    def _build_context(self, input_data: PolicyInsightInput) -> dict[str, Any]:
        context = super()._build_context(input_data)
        # 自动加载政策知识库
        self.kb.load("policies")
        query_parts = [input_data.query]
        if input_data.province:
            query_parts.append(input_data.province)
        if input_data.subject:
            query_parts.append(input_data.subject)
        context["knowledge"] = {
            "policies": self.kb.get_context_text("policies", " ".join(query_parts))
        }
        return context

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        kb_text = context.get("knowledge", {}).get("policies", "（无相关政策文档）")
        province = inp.get("province", "全国")
        subject = inp.get("subject", "人工智能")
        grade = inp.get("grade_range", "")

        return f"""请基于以下政策参考资料，分析{province}地区{subject}方向{f"（{grade}）" if grade else ""}的政策动向：

## 用户需求
{inp['query']}

## 参考政策文档
{kb_text}

请输出：
1. **政策要点摘要**：列出关键政策及核心条款
2. **课标映射分析**：将政策要求映射到具体课程标准
3. **课程适配建议**：基于政策分析给出课程设计建议"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> PolicyInsightOutput:
        return PolicyInsightOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(PolicyInsightAgent, PolicyInsightInput)
