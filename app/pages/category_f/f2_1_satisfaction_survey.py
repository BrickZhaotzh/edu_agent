"""F2.1 满意度调研 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_f.satisfaction_survey import SatisfactionSurveyAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("F2.1 满意度调研")
st.caption("满意度问卷设计与分析")

agent = SatisfactionSurveyAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
