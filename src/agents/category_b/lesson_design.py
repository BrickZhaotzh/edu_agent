"""B2.1 单节课时设计 Agent (P0)

基于 B1.5 课程大纲进行单课时的详细教学设计。
接收 B1.5 upstream_output。
"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import LessonDesignInput, LessonDesignOutput


class LessonDesignAgent(BaseAgent):
    """B2.1 单节课时设计（接收B1.5）"""

    agent_id = "B2.1"
    agent_name = "单节课时设计"
    system_prompt_template = "category_b/lesson_design_system.j2"
    user_prompt_template = "category_b/lesson_design_user.j2"
    input_model = LessonDesignInput
    output_model = LessonDesignOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        """回退提示词（当Jinja2模板不可用时）"""
        inp = context["input"]
        parts = [
            "## 单节课时设计任务\n",
            f"- **单元名称**: {inp['unit_name']}",
            f"- **课时主题**: {inp['lesson_topic']}",
            f"- **第几课时**: 第{inp['lesson_number']}课时",
            f"- **时长**: {inp['duration_minutes']}分钟\n",
            f"### 用户需求\n{inp['query']}\n",
        ]

        if context.get("upstream"):
            parts.append(
                f"### 上游Agent输出（B1.5 课程大纲）\n"
                f"```json\n{json.dumps(context['upstream'], ensure_ascii=False, indent=2)}\n```\n"
            )

        if context.get("knowledge"):
            parts.append("### 知识库参考\n")
            for kb_id, text in context["knowledge"].items():
                parts.append(f"#### {kb_id}\n{text}\n")

        parts.append(
            "### 输出要求\n"
            "请输出完整的单节课时教学设计方案，包含：教学目标、重难点、"
            "教学准备、教学过程（精确到分钟）、课堂评价、作业/延伸。"
        )
        return "\n".join(parts)

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> LessonDesignOutput:
        """解析输出，尝试提取结构化教学设计数据"""
        output = LessonDesignOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )

        # 尝试从原始输出中提取JSON格式的结构化数据
        try:
            if "```json" in raw_output:
                json_str = raw_output.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_str)
                if isinstance(data, dict):
                    if "objectives" in data:
                        output.objectives = data["objectives"]
                    if "activities" in data:
                        output.activities = data["activities"]
                    if "assessment" in data:
                        output.assessment = data["assessment"]
        except (json.JSONDecodeError, IndexError):
            pass

        return output


if __name__ == "__main__":
    run_agent_cli(LessonDesignAgent, LessonDesignInput)
