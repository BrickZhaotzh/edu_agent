"""D1.1 教具需求清单 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_d.supply_list import SupplyListAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("D1.1 教具需求清单")
st.caption("根据课程内容生成教具/学具材料清单")

agent = SupplyListAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
