"""B1.1 课程整体规划 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_b.course_planning import CoursePlanningAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("B1.1 课程整体规划")
st.caption("基于需求与学段定位，生成课程整体规划方案（目标、范围、学时分配）")

agent = CoursePlanningAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
