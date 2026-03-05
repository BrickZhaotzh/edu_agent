"""F2.1 满意度调研 — 满意度问卷设计与分析"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class SatisfactionSurveyAgent(BaseAgent):
    """满意度调研智能体

    设计课程满意度调研问卷，并对调研结果进行分析，
    输出改进建议。
    """

    agent_id = "F2.1"
    agent_name = "满意度调研"
    system_prompt_template = "category_f/satisfaction_survey_system.j2"
    user_prompt_template = "category_f/satisfaction_survey_user.j2"
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

        return f"""请根据以下信息，设计满意度调研方案或分析调研数据。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出（根据需求选择问卷设计或数据分析模式）：

### 问卷设计模式：
1. **调研目标**：核心调研问题与假设
2. **问卷结构**：
   - 基本信息题（2-3题）
   - 课程内容满意度（李克特5级量表）
   - 教学服务满意度
   - 学具体验满意度
   - 开放性建议题
3. **发放策略**：发放时间、渠道、激励措施
4. **数据分析框架**：预设的分析维度与方法

### 数据分析模式：
1. **数据概览**：样本量、回收率、有效率
2. **满意度评分**：各维度NPS/CSAT得分与趋势
3. **交叉分析**：按年级/校区/课程类型等维度交叉
4. **文本分析**：开放题关键词云与情感分析
5. **改进建议**：按优先级排列的改进行动项"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(SatisfactionSurveyAgent, AgentInput)
