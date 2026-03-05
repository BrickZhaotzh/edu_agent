"""D2.1 学具寻源 — 教具/学具供应商寻源与采购建议"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class SupplySourcingAgent(BaseAgent):
    """学具寻源智能体

    基于教具需求清单与规格说明，推荐供应商渠道、
    采购方案与成本优化建议。
    """

    agent_id = "D2.1"
    agent_name = "学具寻源"
    system_prompt_template = "category_d/supply_sourcing_system.j2"
    user_prompt_template = "category_d/supply_sourcing_user.j2"
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

        return f"""请根据以下信息，提供学具/教具的供应商寻源与采购建议。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出：
1. **供应商渠道推荐**：线上平台（淘宝教育、京东教育、1688等）、线下渠道、厂商直供
2. **品牌对比分析**：主流教具品牌的产品线、价格区间、口碑评价
3. **采购方案**：批量采购 vs 零散采购的成本对比
4. **成本优化建议**：替代方案、DIY方案、复用策略
5. **供应商评估要素**：资质认证、售后服务、交货周期、定制能力
6. **采购风险提示**：质量风险、供货风险、合规风险"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(SupplySourcingAgent, AgentInput)
