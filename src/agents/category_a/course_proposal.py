"""A3.1 课程立项书 — 商业模式框架+多方案推演+可行性分析"""

import json
import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import CourseProposalInput, CourseProposalOutput

logger = logging.getLogger(__name__)


class CourseProposalAgent(BaseAgent):
    """课程立项书智能体

    生成完整的课程立项书，包含商业模式分析、多方案评估对比、
    可行性论证，为课程产品化决策提供依据。
    """

    agent_id = "A3.1"
    agent_name = "课程立项书"
    system_prompt_template = "category_a/course_proposal_system.j2"
    user_prompt_template = "category_a/course_proposal_user.j2"
    input_model = CourseProposalInput
    output_model = CourseProposalOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        course_name = inp.get("course_name", "")
        target_grade = inp.get("target_grade", "")
        subject_area = inp.get("subject_area", "人工智能")
        upstream = context.get("upstream", {})

        upstream_text = ""
        if upstream:
            upstream_text = f"\n## 上游分析结果\n{json.dumps(upstream, ensure_ascii=False, indent=2)}\n"

        return f"""请为以下课程生成完整的立项书：

## 课程基本信息
- **课程名称**：{course_name}
- **目标学段**：{target_grade}
- **学科领域**：{subject_area}

## 用户需求
{inp['query']}
{upstream_text}
请按以下结构输出课程立项书：

### 一、项目概述
1. 课程定位与目标受众
2. 市场需求分析（结合政策趋势与用户痛点）
3. 课程核心价值主张

### 二、商业模式框架
1. **价值主张**：课程解决什么问题，提供什么独特价值
2. **目标客户**：ToB（学校/教育局）和/或 ToC（家长/学生）
3. **渠道通路**：获客渠道与交付方式
4. **收入模式**：定价策略与盈利预期
5. **成本结构**：研发成本、运营成本、师资成本
6. **关键资源**：所需的核心能力与资源

### 三、多方案推演
设计至少3个不同的课程方案（如 精品小班/标准化大班/线上自学），每方案包含：
- 课程形态与交付方式
- 目标规模与营收预期
- 所需资源投入
- 风险评估

### 四、可行性分析
1. **技术可行性**：教学平台、工具链、硬件设备的就绪程度
2. **师资可行性**：教师招募/培训的难度与周期
3. **市场可行性**：目标市场规模、竞争格局、进入壁垒
4. **财务可行性**：投入产出比、回本周期、盈亏平衡点

### 五、实施路线图
关键里程碑、时间节点、资源分配计划

### 六、风险与应对
识别主要风险并给出预案"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> CourseProposalOutput:
        return CourseProposalOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(CourseProposalAgent, CourseProposalInput)
