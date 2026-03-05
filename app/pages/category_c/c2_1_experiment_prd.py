"""C2.1 实验PRD — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.experiment_prd import ExperimentPRDAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C2.1 实验PRD")
st.caption("为科创教育实验项目撰写产品需求文档，含目标、材料清单、流程及安全事项")

agent = ExperimentPRDAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
