"""A4.1 Demo课设计 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_a.demo_design import DemoDesignAgent
from src.core.models import DemoDesignInput
from app.components.chat_interface import render_chat_interface

st.header("A4.1 Demo课设计")
st.caption("基于优秀课例知识库的课程设计")

agent = DemoDesignAgent()

input_fields = {
    "course_topic": {
        "label": "课程主题",
        "type": "text",
        "default": "",
        "help": "输入Demo课的主题，如 '用Scratch制作智能垃圾分类器'",
    },
    "target_grade": {
        "label": "目标学段",
        "type": "select",
        "options": ["全部", "小学", "初中", "高中"],
        "help": "选择课程面向的学段",
    },
    "duration_minutes": {
        "label": "课时长度（分钟）",
        "type": "slider",
        "min": 20,
        "max": 90,
        "default": 45,
        "help": "设置Demo课的时长",
    },
}

render_chat_interface(agent, DemoDesignInput, input_fields)
