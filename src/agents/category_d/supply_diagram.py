"""D1.2 教具示意图 — 生成教具/学具的文字描述与示意图说明"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class SupplyDiagramAgent(BaseAgent):
    """教具示意图智能体

    基于教具需求清单，生成每项教具/学具的文字外观描述、
    结构说明与组装示意图文字稿，可用于后续图形化输出。
    """

    agent_id = "D1.2"
    agent_name = "教具示意图"
    system_prompt_template = "category_d/supply_diagram_system.j2"
    user_prompt_template = "category_d/supply_diagram_user.j2"
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

        return f"""请根据以下信息，生成教具/学具的示意图文字描述。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请为每项教具/学具输出：
1. **外观描述**：整体外观、尺寸比例、颜色配色方案
2. **结构分解图说明**：各组成部分的名称、位置、连接方式
3. **关键细节标注**：接口类型、传感器位置、操作按钮等
4. **组装示意说明**：分步骤的组装顺序与注意事项
5. **使用场景图说明**：教具在课堂中的使用状态描述
6. **图片生成提示词**：可用于AI绘图工具的英文提示词"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(SupplyDiagramAgent, AgentInput)
