"""A6.1 生态资源评估 — 资源分类标签+复用性评分+使用建议"""

import json
import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import ResourceAssessmentInput, ResourceAssessmentOutput

logger = logging.getLogger(__name__)


class ResourceAssessmentAgent(BaseAgent):
    """生态资源评估智能体

    对教育生态中的各类资源进行分类、标签、复用性评估，
    给出资源整合与使用建议。
    """

    agent_id = "A6.1"
    agent_name = "生态资源评估"
    system_prompt_template = "category_a/resource_assessment_system.j2"
    user_prompt_template = "category_a/resource_assessment_user.j2"
    input_model = ResourceAssessmentInput
    output_model = ResourceAssessmentOutput

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        resource_name = inp.get("resource_name", "")
        resource_type = inp.get("resource_type", "")
        resource_description = inp.get("resource_description", "")

        type_text = f"（类型：{resource_type}）" if resource_type else ""
        desc_text = f"\n- **资源描述**：{resource_description}" if resource_description else ""

        return f"""请对以下教育生态资源进行全面评估：

## 资源信息
- **资源名称**：{resource_name}{type_text}{desc_text}

## 用户需求
{inp['query']}

请按以下结构输出评估报告：

### 一、资源分类与标签

1. **一级分类**：（硬件资源/软件资源/内容资源/人力资源/渠道资源/政策资源）
2. **二级标签**：
   - 学科标签：适用学科方向
   - 学段标签：适用学段范围
   - 场景标签：适用教学场景
   - 技术标签：涉及的技术领域
3. **资源属性**：
   - 开放程度（开源/商用/定制）
   - 获取难度（易获取/需授权/需采购）
   - 维护状态（活跃/稳定/停更）

### 二、质量评估

| 评估维度 | 得分（1-10） | 说明 |
|----------|-------------|------|
| 内容准确性 | | |
| 教学适配性 | | |
| 技术成熟度 | | |
| 文档完整度 | | |
| 社区活跃度 | | |

### 三、复用性评分（满分100分）

从以下角度评估资源的复用潜力：
1. **跨学段复用性**：能否适配不同年级（权重20%）
2. **跨学科复用性**：能否迁移到其他学科（权重20%）
3. **跨场景复用性**：校内/校外/线上是否通用（权重15%）
4. **定制化难度**：二次开发/适配的成本（权重15%）
5. **标准化程度**：接口、格式的规范性（权重15%）
6. **生命周期**：预期可用年限与更新频率（权重15%）

综合复用性得分：__/100

### 四、使用建议

1. **最佳使用场景**：最适合在什么情况下使用
2. **整合建议**：如何与现有课程/产品体系整合
3. **替代方案**：市场上可替代的同类资源
4. **风险提示**：使用中需注意的风险点
5. **投入产出评估**：引入该资源的预期ROI"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> ResourceAssessmentOutput:
        return ResourceAssessmentOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(ResourceAssessmentAgent, ResourceAssessmentInput)
