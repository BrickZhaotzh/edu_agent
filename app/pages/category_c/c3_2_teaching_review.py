"""C3.2 教学审核 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.teaching_review import TeachingReviewAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C3.2 教学审核")
st.caption("教学内容全方位质量审核，覆盖科学准确性、规范性、课标对齐度等维度")

agent = TeachingReviewAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
