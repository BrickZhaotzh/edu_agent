"""C1.8 教师手册 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.teacher_manual import TeacherManualAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C1.8 教师手册")
st.caption("编写教师教学指导手册，提供实施指南、常见问题应对和差异化教学建议")

agent = TeacherManualAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
