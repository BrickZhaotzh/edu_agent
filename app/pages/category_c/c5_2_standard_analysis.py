"""C5.2 课标分析 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.standard_analysis import StandardAnalysisAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C5.2 课标分析")
st.caption("深度解读国家课程标准，提取核心素养要求、内容标准和学业质量标准")

agent = StandardAnalysisAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
