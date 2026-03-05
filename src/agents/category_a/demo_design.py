"""A4.1 Demo课设计 — 基于课例知识库的示范课设计"""

import json
import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import DemoDesignInput, DemoDesignOutput

logger = logging.getLogger(__name__)


class DemoDesignAgent(BaseAgent):
    """Demo课设计智能体

    基于课例知识库，设计针对特定主题和学段的Demo示范课，
    输出完整的教学设计方案与活动安排。
    """

    agent_id = "A4.1"
    agent_name = "Demo课设计"
    system_prompt_template = "category_a/demo_design_system.j2"
    user_prompt_template = "category_a/demo_design_user.j2"
    input_model = DemoDesignInput
    output_model = DemoDesignOutput

    def _build_context(self, input_data: DemoDesignInput) -> dict[str, Any]:
        context = super()._build_context(input_data)
        # 加载课例知识库
        self.kb.load("course_examples")
        query = f"{input_data.course_topic} {input_data.target_grade}"
        context["knowledge"] = {
            "course_examples": self.kb.get_context_text("course_examples", query)
        }
        return context

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        kb_text = context.get("knowledge", {}).get("course_examples", "（无相关课例参考）")
        topic = inp.get("course_topic", "")
        grade = inp.get("target_grade", "")
        duration = inp.get("duration_minutes", 45)

        return f"""请设计一节Demo示范课：

## 课程基本信息
- **课程主题**：{topic}
- **目标学段**：{grade}
- **课时长度**：{duration}分钟

## 用户需求
{inp['query']}

## 参考课例
{kb_text}

请按以下结构输出Demo课设计方案：

### 一、课程概述
1. 主题说明与课程定位
2. 学情分析（目标学段学生的认知水平与前置知识）
3. 教学目标（知识与技能/过程与方法/情感态度价值观）

### 二、教学设计
按时间线规划完整教学流程：

1. **导入环节**（约{duration // 9}分钟）
   - 情境创设 / 问题引入 / 兴趣激发

2. **新知讲授**（约{duration // 3}分钟）
   - 核心概念讲解
   - 演示与示范

3. **实践操作**（约{duration // 3}分钟）
   - 动手实验 / 编程实践 / 项目任务
   - 分组合作安排

4. **展示交流**（约{duration // 9}分钟）
   - 学生成果展示
   - 互评与讨论

5. **总结拓展**（约{duration // 9}分钟）
   - 知识总结与思维导图
   - 课后拓展任务

### 三、教学资源清单
- 软件工具（编程平台、演示软件等）
- 硬件设备（如需要）
- 教学素材（课件、视频、示例代码等）

### 四、评价设计
- 过程性评价要点
- 成果评价标准

### 五、教学反思预设
- 可能遇到的教学难点及应对策略
- 差异化教学建议"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> DemoDesignOutput:
        return DemoDesignOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(DemoDesignAgent, DemoDesignInput)
