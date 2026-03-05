"""F1.2 课程介绍页 — 课程详情介绍页内容生成"""

import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import AgentInput, AgentOutput

logger = logging.getLogger(__name__)


class CourseIntroAgent(BaseAgent):
    """课程介绍页智能体

    生成课程详情介绍页的完整内容，适用于官网、小程序、
    招生手册等场景。
    """

    agent_id = "F1.2"
    agent_name = "课程介绍页"
    system_prompt_template = "category_f/course_intro_system.j2"
    user_prompt_template = "category_f/course_intro_user.j2"
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

        return f"""请根据以下信息，生成课程介绍页内容。

## 用户需求
{inp['query']}
{upstream_text}

{f"## 参考资料{chr(10)}{kb_text}" if kb_text else ""}

请输出完整的课程介绍页内容，包含以下模块：
1. **课程头图区文案**：一句话课程定位
2. **课程亮点**（3-5个亮点，每个含图标建议+标题+描述）
3. **课程简介**：200-300字课程概述
4. **适合人群**：目标学段与学生画像
5. **课程大纲**：单元/课时列表，每项含主题与简介
6. **学习成果**：学完后能获得的能力/作品/证书
7. **师资介绍**：师资团队描述模板
8. **上课方式**：授课形式、时长、班型
9. **家长常见问题**（FAQ，3-5个）
10. **报名信息**：价格展示区文案、优惠信息、报名引导

写作要求：
- 家长视角，突出教育价值
- 适度使用数据增强可信度
- SEO友好，包含关键词"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> AgentOutput:
        return AgentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(CourseIntroAgent, AgentInput)
