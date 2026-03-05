"""C1.8 教师手册 Agent — 编写教师教学指导手册（P1）"""

import json
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput


class TeacherManualAgent(BaseAgent):
    """C1.8 教师手册智能体

    编写面向授课教师的教学指导手册，提供详细的教学实施指南、
    常见问题应对策略、差异化教学建议和课堂管理提示。
    """

    agent_id = "C1.8"
    agent_name = "教师手册"
    system_prompt_template = "category_c/teacher_manual_system.j2"
    user_prompt_template = "category_c/teacher_manual_user.j2"
    input_model = AgentInput
    output_model = AgentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context.get("input", {})
        parts = [
            f"## 任务：生成教师手册\n",
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

        knowledge = context.get("knowledge")
        if knowledge:
            parts.append(f"\n**参考知识：**\n```json\n{json.dumps(knowledge, ensure_ascii=False, indent=2)}\n```")

        parts.append(
            "\n请生成一份面向教师的教学指导手册，包含：\n"
            "1. **课前准备清单**：\n"
            "   - 硬件环境检查（电脑、网络、软件安装等）\n"
            "   - 教学素材准备（课件、视频、代码示例等）\n"
            "   - 学生分组建议\n"
            "2. **教学流程指导**：\n"
            "   - 各环节的教学要点和时间把控建议\n"
            "   - 关键提问的参考答案和追问方向\n"
            "   - 板书/演示的操作提示\n"
            "3. **课堂管理建议**：\n"
            "   - 学生注意力管理策略\n"
            "   - 小组协作的组织方法\n"
            "   - 课堂纪律和安全注意事项\n"
            "4. **差异化教学策略**：\n"
            "   - 进阶任务（面向学有余力的学生）\n"
            "   - 辅助方案（面向学习困难的学生）\n"
            "5. **常见问题与应对**：\n"
            "   - 技术故障排查指南\n"
            "   - 学生常见错误及纠正方法\n"
            "   - 突发情况处理预案\n"
            "6. **评价工具**：课堂观察记录表、学生作品评价标准\n"
            "7. **教学反思模板**：课后反思的参考框架"
        )
        return "\n".join(parts)


if __name__ == "__main__":
    run_agent_cli(TeacherManualAgent, AgentInput)
