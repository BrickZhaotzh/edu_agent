"""A2.1 行业竞品调研 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_a.competitor_research import CompetitorResearchAgent
from src.core.models import CompetitorResearchInput
from app.components.chat_interface import render_chat_interface

st.header("A2.1 行业竞品调研")
st.caption("竞品信息抓取 + 结构化对比 + 差异点提炼")

agent = CompetitorResearchAgent()

input_fields = {
    "target": {
        "label": "调研目标",
        "type": "text",
        "default": "",
        "help": "输入机构名称或赛道方向，如 '编程猫' 或 'STEAM教育赛道'",
    },
    "dimensions": {
        "label": "调研维度",
        "type": "multiselect",
        "options": ["产品", "课程", "技术", "商业", "政策", "竞赛", "市场"],
        "default": ["产品", "课程", "商业", "政策"],
        "help": "选择需要覆盖的调研维度",
    },
}

render_chat_interface(agent, CompetitorResearchInput, input_fields)
