"""A5.1 Demo评分模型 — 多维度评分+自动化评审"""

import json
import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import DemoScoringInput, DemoScoringOutput

logger = logging.getLogger(__name__)


class DemoScoringAgent(BaseAgent):
    """Demo评分模型智能体

    对Demo课内容进行多维度评分，提供结构化评审意见，
    支持自动化质量把控。
    """

    agent_id = "A5.1"
    agent_name = "Demo评分模型"
    system_prompt_template = "category_a/demo_scoring_system.j2"
    user_prompt_template = "category_a/demo_scoring_user.j2"
    input_model = DemoScoringInput
    output_model = DemoScoringOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        demo_content = inp.get("demo_content", "")
        dimensions = inp.get("scoring_dimensions", [
            "内容质量", "教学设计", "互动性", "技术准确性", "趣味性"
        ])
        dimensions_str = "、".join(dimensions)

        return f"""请对以下Demo课内容进行多维度评分与评审：

## 评分维度
{dimensions_str}

## 用户需求
{inp['query']}

## Demo课内容
{demo_content}

请按以下结构输出评审报告：

### 一、各维度评分（满分100分）

对每个维度进行独立评分，格式如下：

| 维度 | 得分 | 评级 | 简要说明 |
|------|------|------|----------|
（逐维度填写）

### 二、综合评分
- 加权总分（各维度等权重计算）
- 综合评级（A/B/C/D）
- 一句话总评

### 三、详细评审意见

对每个维度给出详细评审：

#### 1. {dimensions[0] if dimensions else '内容质量'}
- **优点**：具体列举做得好的地方
- **不足**：具体指出需要改进之处
- **改进建议**：可操作的优化方向

（以此类推其他维度）

### 四、关键改进优先级
按重要性排序列出最需要改进的3-5个要点，标注：
- 改进难度（高/中/低）
- 预期提升幅度（高/中/低）
- 建议优先级（P0/P1/P2）

### 五、总体建议
- 是否达到可交付标准
- 下一步行动建议"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> DemoScoringOutput:
        return DemoScoringOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(DemoScoringAgent, DemoScoringInput)
