"""B1.2 课标教材匹配 Agent (P0)

课标与教材的精准匹配分析，管线起点。
输出供 B1.3 单元主题架构 使用。
"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import StandardMatchingInput, StandardMatchingOutput


class StandardMatchingAgent(BaseAgent):
    """B1.2 课标教材匹配（管线起点）"""

    agent_id = "B1.2"
    agent_name = "课标教材匹配"
    system_prompt_template = "category_b/standard_matching_system.j2"
    user_prompt_template = "category_b/standard_matching_user.j2"
    input_model = StandardMatchingInput
    output_model = StandardMatchingOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        """回退提示词（当Jinja2模板不可用时）"""
        inp = context["input"]
        parts = [
            "## 课标教材匹配任务\n",
            f"- **学科**: {inp['subject']}",
            f"- **年级**: {inp['grade']}",
        ]
        if inp.get("textbook_version"):
            parts.append(f"- **教材版本**: {inp['textbook_version']}")

        parts.append(f"\n### 用户需求\n{inp['query']}\n")

        if context.get("knowledge"):
            parts.append("### 知识库参考\n")
            for kb_id, text in context["knowledge"].items():
                parts.append(f"#### {kb_id}\n{text}\n")

        parts.append(
            "### 输出要求\n"
            "请输出课标与教材的匹配分析报告，包含：课标要求梳理、"
            "教材内容映射、匹配度评估、覆盖缺口分析、补充建议。"
        )
        return "\n".join(parts)

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> StandardMatchingOutput:
        """解析输出，尝试提取结构化匹配数据"""
        output = StandardMatchingOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )

        # 尝试从原始输出中提取JSON格式的匹配数据
        try:
            if "```json" in raw_output:
                json_str = raw_output.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_str)
                if isinstance(data, list):
                    output.matches = data
                elif isinstance(data, dict) and "matches" in data:
                    output.matches = data["matches"]
        except (json.JSONDecodeError, IndexError):
            pass

        return output


if __name__ == "__main__":
    run_agent_cli(StandardMatchingAgent, StandardMatchingInput)
