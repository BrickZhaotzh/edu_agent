"""E1.1 说课视频 — 说课视频脚本与制作指南"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class LectureVideoAgent(BaseAgent):
    """说课视频智能体

    生成说课视频的完整脚本与制作指南，涵盖说教材、说学情、
    说教法、说教学过程等标准说课环节。
    """

    agent_id = "E1.1"
    agent_name = "说课视频"
    system_prompt_template = "category_e/lecture_video_system.j2"
    user_prompt_template = "category_e/lecture_video_user.j2"
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

        return f"""请根据以下信息，生成说课视频脚本与制作指南。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出：
1. **说课视频脚本**（按标准说课流程）：
   - 说教材：教材分析、内容地位与作用
   - 说学情：学生知识基础、认知特点、学习难点
   - 说教学目标：知识与技能、过程与方法、情感态度价值观
   - 说教法学法：教学方法选择与依据
   - 说教学过程：完整的教学环节设计与时间分配
   - 说板书设计：板书结构与关键词
   - 说教学反思：预设反思要点
2. **分镜提示**：每个环节对应的画面建议（PPT、演示、实操等）
3. **制作指南**：
   - 录制环境要求
   - 着装与仪态建议
   - PPT设计要点
   - 后期剪辑建议
4. **时长规划**：各环节时间分配（总时长10-15分钟）"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(LectureVideoAgent, AgentInput)
