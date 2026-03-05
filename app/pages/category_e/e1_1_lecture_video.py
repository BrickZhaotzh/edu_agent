"""E1.1 说课视频 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_e.lecture_video import LectureVideoAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("E1.1 说课视频")
st.caption("说课视频脚本与制作指南")

agent = LectureVideoAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
