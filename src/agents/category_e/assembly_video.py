"""E1.3 学具搭建视频 — 学具组装/搭建视频脚本"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class AssemblyVideoAgent(BaseAgent):
    """学具搭建视频智能体

    生成学具组装/搭建视频的完整脚本，包含分步骤操作说明、
    旁白文案、画面指导与安全提示。
    """

    agent_id = "E1.3"
    agent_name = "学具搭建视频"
    system_prompt_template = "category_e/assembly_video_system.j2"
    user_prompt_template = "category_e/assembly_video_user.j2"
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

        return f"""请根据以下信息，生成学具搭建/组装视频脚本。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出：
1. **视频大纲**：整体结构、预计时长
2. **材料清点环节**：开场展示所有零部件与工具
3. **分步骤搭建脚本**（每步包含）：
   - 步骤编号与标题
   - 操作说明（动作描述）
   - 旁白文案（口播内容）
   - 画面指导（机位、特写、标注）
   - 预计耗时
   - 常见错误提醒
4. **安全提示**：每个涉及安全风险的步骤需标注注意事项
5. **完成效果展示**：搭建完成后的功能演示脚本
6. **拍摄建议**：
   - 推荐机位与灯光布置
   - 需要特写的关键操作
   - 后期字幕与标注建议"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(AssemblyVideoAgent, AgentInput)
