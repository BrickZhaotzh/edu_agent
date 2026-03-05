"""E1.4 语音合成 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_e.tts_gen import TTSGenAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("E1.4 语音合成")
st.caption("TTS脚本准备与语音合成配置")

agent = TTSGenAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
