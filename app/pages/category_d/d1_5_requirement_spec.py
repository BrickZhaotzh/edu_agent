"""D1.5 需求规格说明书 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_d.requirement_spec import RequirementSpecAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("D1.5 需求规格说明书")
st.caption("生成学具/教具的详细需求规格文档")

agent = RequirementSpecAgent()

with st.expander("📥 导入上游数据（可选）"):
    upstream_data = st.text_area("粘贴上游智能体的输出内容", height=200, key="upstream_d1_5")
    if upstream_data:
        st.info("已加载上游数据")

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
