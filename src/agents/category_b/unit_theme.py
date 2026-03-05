"""B1.3 单元主题架构 Agent (P0)

基于 B1.2 课标匹配结果设计单元主题体系。
接收 B1.2 upstream_output，输出供 B1.4 使用。
"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import UnitThemeInput, UnitThemeOutput


class UnitThemeAgent(BaseAgent):
    """B1.3 单元主题架构（接收B1.2，输出供B1.4）"""

    agent_id = "B1.3"
    agent_name = "单元主题架构"
    system_prompt_template = "category_b/unit_theme_system.j2"
    user_prompt_template = "category_b/unit_theme_user.j2"
    input_model = UnitThemeInput
    output_model = UnitThemeOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        """回退提示词（当Jinja2模板不可用时）"""
        inp = context["input"]
        parts = [
            "## 单元主题架构设计任务\n",
            f"- **课程名称**: {inp['course_name']}",
            f"- **单元总数**: {inp['total_units']}\n",
            f"### 用户需求\n{inp['query']}\n",
        ]

        if inp.get("standard_mapping"):
            parts.append(f"### 课标映射信息\n```json\n{json.dumps(inp['standard_mapping'], ensure_ascii=False, indent=2)}\n```\n")

        if context.get("upstream"):
            parts.append(f"### 上游Agent输出（B1.2 课标教材匹配结果）\n```json\n{json.dumps(context['upstream'], ensure_ascii=False, indent=2)}\n```\n")

        if context.get("knowledge"):
            parts.append("### 知识库参考\n")
            for kb_id, text in context["knowledge"].items():
                parts.append(f"#### {kb_id}\n{text}\n")

        parts.append(
            f"### 输出要求\n"
            f"请设计 {inp['total_units']} 个单元的主题架构，包含：单元名称、"
            f"核心概念、驱动性问题、学习目标、课标对齐、建议课时数、逻辑关系。"
        )
        return "\n".join(parts)

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> UnitThemeOutput:
        """解析输出，尝试提取结构化单元数据"""
        output = UnitThemeOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )

        # 尝试从原始输出中提取JSON格式的单元数据
        try:
            if "```json" in raw_output:
                json_str = raw_output.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_str)
                if isinstance(data, list):
                    output.units = data
                elif isinstance(data, dict) and "units" in data:
                    output.units = data["units"]
        except (json.JSONDecodeError, IndexError):
            pass

        return output


if __name__ == "__main__":
    run_agent_cli(UnitThemeAgent, UnitThemeInput)
