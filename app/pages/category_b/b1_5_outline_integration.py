"""B1.5 大纲整合输出 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_b.outline_integration import OutlineIntegrationAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("B1.5 大纲整合输出")
st.caption("汇总 B1.1-B1.4 全部成果，生成完整的课程大纲文档")

agent = OutlineIntegrationAgent()

with st.expander("📥 导入上游数据（可选）"):
    upstream_data = st.text_area("粘贴上游智能体的输出内容", height=200, key="upstream_b1_5")
    if upstream_data:
        st.info("已加载上游数据")

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
