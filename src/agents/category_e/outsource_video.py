"""E1.2 外包视频制作 — 生成外包视频制作需求文档"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class OutsourceVideoAgent(BaseAgent):
    """外包视频制作智能体

    生成完整的外包视频制作需求文档，包括项目概述、
    创意brief、技术要求、验收标准等，供外部制作团队使用。
    """

    agent_id = "E1.2"
    agent_name = "外包视频制作"
    system_prompt_template = "category_e/outsource_video_system.j2"
    user_prompt_template = "category_e/outsource_video_user.j2"
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

        return f"""请根据以下信息，生成外包视频制作需求文档。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出完整的视频外包需求文档，包含：
1. **项目概述**：项目背景、目标受众、视频用途
2. **创意Brief**：视频风格、调性、参考案例
3. **内容脚本大纲**：章节划分、每段核心信息点
4. **技术规格要求**：
   - 分辨率、帧率、码率
   - 时长要求
   - 字幕规范
   - 配音要求
5. **视觉要求**：品牌色、logo使用规范、字体规范
6. **交付物清单**：成品文件格式、源文件、字幕文件等
7. **项目排期**：里程碑节点与交付时间
8. **验收标准**：逐项验收条件
9. **预算参考**：制作复杂度与市场价格区间"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(OutsourceVideoAgent, AgentInput)
