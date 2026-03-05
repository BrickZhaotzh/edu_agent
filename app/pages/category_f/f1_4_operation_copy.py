"""F1.4 运营文案 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_f.operation_copy import OperationCopyAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("F1.4 运营文案")
st.caption("日常运营文案撰写")

agent = OperationCopyAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
