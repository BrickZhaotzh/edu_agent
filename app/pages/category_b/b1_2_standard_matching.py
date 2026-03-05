"""B1.2 课标教材匹配 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_b.standard_matching import StandardMatchingAgent
from src.core.models import StandardMatchingInput
from app.components.chat_interface import render_chat_interface

st.header("B1.2 课标教材匹配")
st.caption("将课程内容与国家课程标准、主流教材版本进行精准映射")

agent = StandardMatchingAgent()

input_fields = {
    "subject": {
        "label": "学科方向",
        "type": "select",
        "options": ["人工智能", "科学", "信息科技"],
        "help": "选择需要匹配课标的学科方向",
    },
    "grade": {
        "label": "年级",
        "type": "select",
        "options": ["全部", "小学", "初中", "高中"],
        "help": "选择目标年级",
    },
    "textbook_version": {
        "label": "教材版本",
        "type": "text",
        "default": "",
        "help": "填写教材版本，如 '人教版'、'北师大版'，留空表示通用",
    },
}

render_chat_interface(agent, StandardMatchingInput, input_fields)
