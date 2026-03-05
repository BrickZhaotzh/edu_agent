"""C4.1 资源上传 Agent — 教学资源上传整理辅助（P3）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class ResourceUploadAgent(BaseAgent):
    """C4.1 资源上传智能体

    辅助教学资源的上传整理工作，包括资源分类标签生成、
    元数据填写、文件命名规范、资源描述撰写等。
    """

    agent_id = "C4.1"
    agent_name = "资源上传"
    system_prompt_template = "category_c/resource_upload_system.j2"
    user_prompt_template = "category_c/resource_upload_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：资源上传辅助\n",
            f"**资源信息：** {inp.get('query', '')}",
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
            "\n请生成完整的资源上传辅助方案，包含：分类标签、关键词、"
            "资源描述、适用学段/学科、关联课标/知识点、文件命名建议、上传检查清单。"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(ResourceUploadAgent, AgentInput)
