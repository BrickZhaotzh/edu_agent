"""C3.1 拼音标注 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.pinyin_annotator import PinyinAnnotatorAgent
from src.core.models import AgentInput
from app.components.chat_interface import render_chat_interface

st.header("C3.1 拼音标注")
st.caption("为低年级教学材料添加拼音标注，确保拼音准确、格式规范")

agent = PinyinAnnotatorAgent()

input_fields = {}

render_chat_interface(agent, AgentInput, input_fields)
