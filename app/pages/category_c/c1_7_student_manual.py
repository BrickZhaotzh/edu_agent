"""C1.7 学生手册 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.student_manual import StudentManualAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C1.7 学生手册")
st.caption("编写适合中小学生的活动手册，包含学习目标、活动指引、操作步骤")

agent = StudentManualAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
