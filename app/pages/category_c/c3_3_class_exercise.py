"""C3.3 随堂练习 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.class_exercise import ClassExerciseAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C3.3 随堂练习")
st.caption("设计课堂即时练习题，短小精悍、针对性强，可在 3-5 分钟内完成")

agent = ClassExerciseAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
