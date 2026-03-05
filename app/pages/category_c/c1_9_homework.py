"""C1.9 课后作业 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.homework import HomeworkAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C1.9 课后作业")
st.caption("设计分层课后作业，覆盖基础巩固、能力提升和拓展创新，符合双减要求")

agent = HomeworkAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
