"""C5.1 知识图谱 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.knowledge_graph import KnowledgeGraphAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C5.1 知识图谱")
st.caption("构建课程知识图谱，梳理知识点层级关系、前置依赖和关联映射")

agent = KnowledgeGraphAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
