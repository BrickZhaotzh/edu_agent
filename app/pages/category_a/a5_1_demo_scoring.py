"""A5.1 Demo评分模型 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_a.demo_scoring import DemoScoringAgent
from src.core.models import DemoScoringInput
from app.components.chat_interface import render_chat_interface

st.header("A5.1 Demo评分模型")
st.caption("多维度评分标准 + 自动评审")

agent = DemoScoringAgent()

input_fields = {
    "demo_content": {
        "label": "Demo课内容",
        "type": "textarea",
        "default": "",
        "help": "粘贴或输入待评分的Demo课内容文本",
    },
    "scoring_dimensions": {
        "label": "评分维度",
        "type": "multiselect",
        "options": ["内容质量", "教学设计", "互动性", "技术准确性", "趣味性"],
        "default": ["内容质量", "教学设计", "互动性", "技术准确性", "趣味性"],
        "help": "选择需要评估的维度",
    },
}

render_chat_interface(agent, DemoScoringInput, input_fields)
