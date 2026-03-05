"""C5.1 知识图谱 Agent — 课程知识图谱构建（P2）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class KnowledgeGraphAgent(BaseAgent):
    """C5.1 知识图谱智能体

    为课程内容构建知识图谱，梳理知识点之间的层级关系、
    前置依赖、关联映射，支持个性化学习路径规划。
    """

    agent_id = "C5.1"
    agent_name = "知识图谱"
    system_prompt_template = "category_c/knowledge_graph_system.j2"
    user_prompt_template = "category_c/knowledge_graph_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：构建知识图谱\n",
            f"**需求描述：** {inp.get('query', '')}",
        ]

        ctx = inp.get("context", {})
        if ctx:
            parts.append("\n**附加上下文：**")
            for k, v in ctx.items():
                parts.append(f"- {k}: {v}")

        upstream = context.get("upstream")
        if upstream:
            parts.append(f"\n**上游数据：**\n```json\n{json.dumps(upstream, ensure_ascii=False, indent=2)}\n```")

        parts.append(
            "\n请构建一份课程知识图谱，包含：知识点节点列表、"
            "关系边列表、知识图谱概述、学习路径建议。"
            "同时输出JSON格式的结构化数据。"
        )
        return "\n".join(parts)

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        """解析输出，尝试提取结构化图谱数据"""
        output = AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )
        try:
            if "```json" in raw_output:
                json_str = raw_output.split("```json")[1].split("```")[0].strip()
                data = json.loads(json_str)
                output.structured_data = data
        except (json.JSONDecodeError, IndexError):
            pass
        return output


if __name__ == "__main__":
    run_agent_cli(KnowledgeGraphAgent, AgentInput)
