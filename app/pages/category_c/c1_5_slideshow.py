"""C1.5 课件生成 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.slideshow import SlideshowAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C1.5 课件生成")
st.caption("生成结构清晰的PPT课件内容框架，包括标题、要点、视觉建议和备注")

agent = SlideshowAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
