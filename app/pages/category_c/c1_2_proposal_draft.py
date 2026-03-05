"""C1.2 方案稿撰写 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.proposal_draft import ProposalDraftAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C1.2 方案稿撰写")
st.caption("撰写规范的教学方案文档，包含课程概述、教学目标、重难点、流程及评价")

agent = ProposalDraftAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
