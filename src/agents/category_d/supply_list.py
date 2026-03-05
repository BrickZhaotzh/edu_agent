"""D1.1 教具需求清单 — 根据课程内容生成教具/学具材料清单"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class SupplyListAgent(BaseAgent):
    """教具需求清单智能体

    基于课程大纲与教学设计，自动生成完整的教具/学具材料清单，
    包含名称、规格、数量、用途等结构化信息。
    """

    agent_id = "D1.1"
    agent_name = "教具需求清单"
    system_prompt_template = "category_d/supply_list_system.j2"
    user_prompt_template = "category_d/supply_list_user.j2"
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

        return f"""请根据以下课程信息，生成完整的教具/学具需求清单。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出：
1. **材料清单总表**：名称、规格型号、单位数量、单价估算、用途说明
2. **分课时材料清单**：按课时拆解所需材料
3. **耗材 vs 非耗材分类**
4. **采购优先级建议**：必备/可选/替代方案
5. **安全注意事项**：涉及安全风险的材料标注"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(SupplyListAgent, AgentInput)
