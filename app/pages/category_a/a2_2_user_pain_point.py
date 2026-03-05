"""A2.2 用户痛点分析 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_a.user_pain_point import UserPainPointAgent
from src.core.models import UserPainPointInput
from app.components.chat_interface import render_chat_interface

st.header("A2.2 用户痛点分析")
st.caption("调研问卷生成 + 数据分析 + 用户画像建模")

agent = UserPainPointAgent()

input_fields = {
    "target_user": {
        "label": "目标用户",
        "type": "select",
        "options": ["教师", "学生", "家长", "学校管理者"],
        "help": "选择要分析的目标用户群体",
    },
    "scenario": {
        "label": "使用场景",
        "type": "text",
        "default": "",
        "help": "描述用户的具体使用场景，如 '课后编程社团教学'",
    },
}

render_chat_interface(agent, UserPainPointInput, input_fields)
