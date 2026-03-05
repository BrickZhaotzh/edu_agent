"""C4.1 资源上传 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.resource_upload import ResourceUploadAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C4.1 资源上传")
st.caption("辅助教学资源上传整理，包括分类标签生成、元数据填写、命名规范和描述撰写")

agent = ResourceUploadAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
