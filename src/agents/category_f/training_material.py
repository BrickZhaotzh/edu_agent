"""F1.3 培训材料 — 教师培训材料生成"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class TrainingMaterialAgent(BaseAgent):
    """培训材料智能体

    生成教师培训所需的各类材料，包括培训手册、教学指南、
    常见问题手册、评估表等。
    """

    agent_id = "F1.3"
    agent_name = "培训材料"
    system_prompt_template = "category_f/training_material_system.j2"
    user_prompt_template = "category_f/training_material_user.j2"
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

        return f"""请根据以下信息，生成教师培训材料。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出完整的教师培训材料包，包含：
1. **培训手册**：
   - 课程体系概览
   - 教学理念与方法论
   - 各单元教学要点与难点
   - 课堂管理技巧
2. **教学操作指南**：
   - 学具使用说明（分步骤）
   - 软件/平台操作流程
   - 课前准备checklist
3. **常见问题手册**：
   - 教学常见问题Q&A（10-15个）
   - 学具故障排除指南
   - 课堂突发情况处理
4. **评估工具**：
   - 学生学习评估量表
   - 课堂观察记录表
   - 教师自评表
5. **培训日程安排**：培训时间表与分组活动设计
6. **考核标准**：培训后考核内容与通过标准"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(TrainingMaterialAgent, AgentInput)
