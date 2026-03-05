"""A2.1 行业竞品调研 — 竞品信息抓取+结构化对比+差异点提炼"""

import json
import logging
from typing import Any

from src.agents.base_agent import BaseAgent, run_agent_cli
from src.core.models import CompetitorResearchInput, CompetitorResearchOutput

logger = logging.getLogger(__name__)


class CompetitorResearchAgent(BaseAgent):
    """行业竞品调研智能体

    遵循七步调研框架：市场定位扫描、产品体系解构、商业模式剖析、
    政策与标准对齐、竞争格局定位、SWOT战略分析、战略建议。
    """

    agent_id = "A2.1"
    agent_name = "行业竞品调研"
    system_prompt_template = "category_a/competitor_research_system.j2"
    user_prompt_template = "category_a/competitor_research_user.j2"
    input_model = CompetitorResearchInput
    output_model = CompetitorResearchOutput

    def _build_context(self, input_data: CompetitorResearchInput) -> dict[str, Any]:
        context = super()._build_context(input_data)
        # 加载竞品报告知识库
        self.kb.load("competitor_reports")
        query = f"{input_data.target} {input_data.query}"
        context["knowledge"] = {
            "competitor_reports": self.kb.get_context_text("competitor_reports", query)
        }
        return context

    def _format_user_prompt(self, context: dict[str, Any]) -> str:
        inp = context["input"]
        kb_text = context.get("knowledge", {}).get("competitor_reports", "（无相关竞品报告）")
        target = inp.get("target", "")
        dimensions = inp.get("dimensions", ["产品", "课程", "商业", "政策"])
        dimensions_str = "、".join(dimensions)

        return f"""请对「{target}」进行深度竞品调研，覆盖维度：{dimensions_str}。

## 用户需求
{inp['query']}

## 参考竞品资料
{kb_text}

请按照以下七步框架输出完整调研报告：

### 第一步：市场定位扫描
分析目标在赛道细分、学段覆盖、场景类型、地域布局、模式形态等维度的坐标。

### 第二步：产品体系深度解构
- 课程与内容：课程体系架构、内容形式、核心教学法、竞赛导向程度、师资模式
- 技术平台与工具：编程工具、硬件生态、AI能力集成、平台特色
- 产品壁垒：专利、版权、数据、认证资质

### 第三步：商业模式剖析
- 盈利结构（ToB端/ToC端收入拆解）
- 定价策略（客单价、采购均价、Freemium模式）
- 获客与增长（渠道、加盟体系、裂变机制）

### 第四步：政策与标准对齐分析
评估与义务教育信息科技课程标准（2022版）、双减政策、教育数字化战略等的对齐程度。

### 第五步：竞争格局定位
输出竞争矩阵（ToB-ToC / 硬件-软件双轴），标注主要玩家坐标。

### 第六步：SWOT战略分析
内部优势/劣势 + 外部机会/威胁，形成战略矩阵。

### 第七步：战略建议
基于以上分析，给出差异化竞争策略和可执行的行动建议。

## 输出要求
- 数据优先，定量分析优于定性判断
- 对不确定信息标注「待核实」
- 使用表格、列表提升可读性"""

    def _parse_output(self, raw_output: str, context: dict[str, Any]) -> CompetitorResearchOutput:
        return CompetitorResearchOutput(
            agent_id=self.agent_id,
            agent_name=self.agent_name,
            content=raw_output,
        )


if __name__ == "__main__":
    run_agent_cli(CompetitorResearchAgent, CompetitorResearchInput)
