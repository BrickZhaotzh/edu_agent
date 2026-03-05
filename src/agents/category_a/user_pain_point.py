"""A2.2 用户痛点分析 — 调研问卷生成+痛点分析+用户画像构建"""

import json
import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import UserPainPointInput, UserPainPointOutput

logger = logging.getLogger(__name__)


class UserPainPointAgent(BaseAgent):
    """用户痛点分析智能体

    针对目标用户群体生成调研问卷、分析痛点、构建用户画像，
    为课程产品设计提供用户洞察支撑。
    """

    agent_id = "A2.2"
    agent_name = "用户痛点分析"
    system_prompt_template = "category_a/user_pain_point_system.j2"
    user_prompt_template = "category_a/user_pain_point_user.j2"
    input_model = UserPainPointInput
    output_model = UserPainPointOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        target_user = inp.get("target_user", "教师")
        scenario = inp.get("scenario", "")
        scenario_text = f"，使用场景为「{scenario}」" if scenario else ""

        return f"""请针对K-12科创教育领域的「{target_user}」用户群体{scenario_text}，进行深度痛点分析。

## 用户需求
{inp['query']}

请完成以下三项任务：

### 一、调研问卷设计
设计一份结构化调研问卷，包含：
1. **基础信息题**（3-5题）：用户画像相关的基本属性
2. **使用行为题**（5-8题）：当前教学/学习行为与工具使用情况
3. **痛点挖掘题**（5-8题）：遇到的困难、不满意之处、未被满足的需求
4. **需求优先级题**（3-5题）：功能/服务的重要度排序
5. **开放性题目**（2-3题）：捕捉意料之外的洞察

每题标注题型（单选/多选/量表/开放）和设计意图。

### 二、痛点分析
基于行业经验和用户研究方法论，归纳该用户群体的核心痛点：
1. **功能性痛点**：现有工具/课程无法满足的功能需求
2. **体验性痛点**：使用过程中的摩擦和不便
3. **情感性痛点**：焦虑、无力感等情绪层面的困扰
4. **经济性痛点**：成本、性价比方面的顾虑

每个痛点标注严重程度（高/中/低）和出现频率（高/中/低）。

### 三、用户画像构建
构建2-3个典型用户画像（Persona），每个包含：
- 基本属性（年龄、职务、地域、学校类型）
- 核心诉求与目标
- 典型使用场景
- 关键痛点与决策因素
- 一句话概括"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> UserPainPointOutput:
        return UserPainPointOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(UserPainPointAgent, UserPainPointInput)
