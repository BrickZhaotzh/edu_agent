"""C1.6 教学设计 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.teaching_design import TeachingDesignAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C1.6 教学设计")
st.caption("输出完整的教学设计文档，涵盖学情分析、教学目标、重难点、教法学法、教学过程与评价")

agent = TeachingDesignAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
