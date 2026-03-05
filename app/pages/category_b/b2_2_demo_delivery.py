"""B2.2 Demo课交付 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_b.demo_delivery import DemoDeliveryAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("B2.2 Demo课交付")
st.caption("将课时设计转化为可直接交付的Demo课完整方案（含课件要点、互动设计、教师用语）")

agent = DemoDeliveryAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
