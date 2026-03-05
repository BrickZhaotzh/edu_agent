"""C2.2 编程样例 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.code_example import CodeExampleAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C2.2 编程样例")
st.caption("为中小学编程教学设计代码样例，支持 Python、Scratch、Arduino 等平台")

agent = CodeExampleAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
