"""C1.10 评价量规 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.rubric import RubricAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C1.10 评价量规")
st.caption("设计科学、可操作的教学评价量规，支持过程性评价和终结性评价")

agent = RubricAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
