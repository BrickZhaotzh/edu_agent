"""D1.2 教具示意图 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_d.supply_diagram import SupplyDiagramAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("D1.2 教具示意图")
st.caption("生成教具/学具的文字描述与示意图说明")

agent = SupplyDiagramAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
