"""F1.1 宣传海报文案 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_f.poster_copy import PosterCopyAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("F1.1 宣传海报文案")
st.caption("课程宣传海报文案生成")

agent = PosterCopyAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
