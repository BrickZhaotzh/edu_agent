"""F1.3 培训材料 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_f.training_material import TrainingMaterialAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("F1.3 培训材料")
st.caption("教师培训材料生成")

agent = TrainingMaterialAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
