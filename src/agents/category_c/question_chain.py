"""C1.1 问题链设计 Agent — 基于教学目标设计布鲁姆认知层次问题链（P0）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import QuestionChainInput, QuestionChainOutput


class QuestionChainAgent(BaseAgent):
    """C1.1 问题链设计智能体

    核心管线起点：设计符合布鲁姆认知层次的问题链，
    输出将作为 C1.3 逐字稿生成的上游输入。
    """

    agent_id = "C1.1"
    agent_name = "问题链设计"
    system_prompt_template = "category_c/question_chain_system.j2"
    user_prompt_template = "category_c/question_chain_user.j2"
    input_model = QuestionChainInput
    output_model = QuestionChainOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        """格式化 user 提示词（当不使用Jinja2模板时的回退方案）"""
        inp = context.get("input", {})
        parts = [
            f"## 任务：设计问题链\n",
            f"**课时主题：** {inp.get('lesson_topic', '')}",
        ]

        objectives = inp.get("teaching_objectives", [])
        if objectives:
            parts.append("\n**教学目标：**")
            for i, obj in enumerate(objectives, 1):
                parts.append(f"{i}. {obj}")

        query = inp.get("query", "")
        if query:
            parts.append(f"\n**补充需求：** {query}")

        upstream = context.get("upstream")
        if upstream:
            parts.append(f"\n**上游数据：**\n```json\n{json.dumps(upstream, ensure_ascii=False, indent=2)}\n```")

        parts.append(
            "\n请设计一条完整的问题链（5-8个问题），覆盖从低阶到高阶的认知层级。"
            "每个问题请包含：编号、问题文本、认知层级、设计意图、预期学生回答、教师追问建议。"
        )
        return "\n".join(parts)

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> QuestionChainOutput:
        """解析输出，尝试提取结构化问题链"""
        output = QuestionChainOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )
        # 尝试从 Markdown 中提取结构化问题数据
        try:
            if "```json" in raw_output:
                json_str = raw_output.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_str)
                if isinstance(data, list):
                    output.questions = data
                elif isinstance(data, dict) and "questions" in data:
                    output.questions = data["questions"]
        except (json.JSONDecodeError, IndexError):
            pass
        return output


if __name__ == "__main__":
    run_agent_cli(QuestionChainAgent, QuestionChainInput)
