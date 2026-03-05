"""C1.4 分镜脚本 Agent — 将逐字稿转化为视频分镜脚本（P0）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import StoryboardInput, StoryboardOutput


class StoryboardAgent(BaseAgent):
    """C1.4 分镜脚本智能体

    核心管线终点：接收 C1.3 逐字稿生成的输出，
    转化为视频分镜脚本，用于录课和微课视频制作。
    管线: C1.1 → C1.3 → C1.4
    """

    agent_id = "C1.4"
    agent_name = "分镜脚本"
    system_prompt_template = "category_c/storyboard_system.j2"
    user_prompt_template = "category_c/storyboard_user.j2"
    input_model = StoryboardInput
    output_model = StoryboardOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：生成分镜脚本\n",
            f"**视频风格：** {inp.get('video_style', '讲解+演示')}",
        ]

        script_content = inp.get("script_content", "")
        if script_content:
            # 截取前3000字避免过长
            display_content = script_content[:3000]
            if len(script_content) > 3000:
                display_content += "\n...(已截断，完整逐字稿共{}字)".format(len(script_content))
            parts.append(f"\n**逐字稿内容（来自C1.3上游）：**\n{display_content}")

        query = inp.get("query", "")
        if query:
            parts.append(f"\n**补充需求：** {query}")

        upstream = context.get("upstream")
        if upstream:
            parts.append(f"\n**上游管线数据：**\n```json\n{json.dumps(upstream, ensure_ascii=False, indent=2)}\n```")

        knowledge = context.get("knowledge")
        if knowledge:
            parts.append(f"\n**参考知识：**\n```json\n{json.dumps(knowledge, ensure_ascii=False, indent=2)}\n```")

        parts.append(
            "\n请基于以上逐字稿内容，生成一份完整的视频分镜脚本，每个分镜包含：\n"
            "1. **镜号**：分镜编号\n"
            "2. **时长**：该分镜持续时间（秒）\n"
            "3. **画面描述**：画面内容、构图、动画效果\n"
            "4. **镜头运动**：推、拉、摇、移、固定等\n"
            "5. **配音/旁白**：对应的教师口播文本\n"
            "6. **字幕**：需要显示的文字内容\n"
            "7. **素材提示**：需要准备的图片、视频、动画素材\n"
            "8. **转场方式**：与下一个分镜的衔接方式"
        )
        return "\n".join(parts)

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> StoryboardOutput:
        """解析输出，尝试提取结构化分镜数据"""
        output = StoryboardOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )
        try:
            if "```json" in raw_output:
                json_str = raw_output.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_str)
                if isinstance(data, list):
                    output.scenes = data
                elif isinstance(data, dict) and "scenes" in data:
                    output.scenes = data["scenes"]
        except (json.JSONDecodeError, IndexError):
            pass
        return output


if __name__ == "__main__":
    run_agent_cli(StoryboardAgent, StoryboardInput)
