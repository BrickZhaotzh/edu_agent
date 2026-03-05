"""D2.1 学具寻源 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_d.supply_sourcing import SupplySourcingAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("D2.1 学具寻源")
st.caption("教具/学具供应商寻源与采购建议")

agent = SupplySourcingAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
