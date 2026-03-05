"""C3.4 微课评审 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.micro_lesson_review import MicroLessonReviewAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C3.4 微课评审")
st.caption("评审微课内容质量，从教学设计、内容准确性、视觉呈现、节奏把控等维度综合评审")

agent = MicroLessonReviewAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
