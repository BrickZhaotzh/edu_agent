"""D1.5 需求规格说明书 — 生成学具/教具的详细需求规格文档"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class RequirementSpecAgent(BaseAgent):
    """需求规格说明书智能体

    基于教具需求清单（D1.1上游输出），生成详细的需求规格说明书，
    涵盖功能需求、性能指标、验收标准等。
    Pipeline: D1.1 -> D1.5
    """

    agent_id = "D1.5"
    agent_name = "需求规格说明书"
    system_prompt_template = "category_d/requirement_spec_system.j2"
    user_prompt_template = "category_d/requirement_spec_user.j2"
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
            upstream_text = f"\n## 上游输入（D1.1 教具需求清单）\n{context['upstream']}"

        return f"""请根据以下信息，生成详细的学具/教具需求规格说明书。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出完整的需求规格说明书，包含：
1. **项目概述**：背景、目标、适用学段
2. **功能需求**：每项学具的功能描述与使用场景
3. **性能指标**：尺寸、材质、精度、耐用性等技术参数
4. **安全要求**：符合GB相关标准、无毒无害、年龄适配
5. **外观要求**：颜色、标识、包装规范
6. **验收标准**：逐项验收条件与测试方法
7. **质量保证**：保修期、售后服务要求
8. **附录**：参考标准清单、术语表"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(RequirementSpecAgent, AgentInput)
