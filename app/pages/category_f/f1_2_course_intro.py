"""F1.2 课程介绍页 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_f.course_intro import CourseIntroAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("F1.2 课程介绍页")
st.caption("课程详情介绍页内容生成")

agent = CourseIntroAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
