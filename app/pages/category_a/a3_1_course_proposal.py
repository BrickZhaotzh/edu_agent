"""A3.1 课程立项书 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_a.course_proposal import CourseProposalAgent
from src.core.models import CourseProposalInput
from app.components.chat_interface import render_chat_interface

st.header("A3.1 课程立项书")
st.caption("商业模式框架 + 多方案推演 + 可行性分析")

agent = CourseProposalAgent()

input_fields = {
    "course_name": {
        "label": "课程名称",
        "type": "text",
        "default": "",
        "help": "输入拟立项的课程名称",
    },
    "target_grade": {
        "label": "目标学段",
        "type": "select",
        "options": ["全部", "小学", "初中", "高中"],
        "help": "选择课程面向的学段",
    },
    "subject_area": {
        "label": "学科领域",
        "type": "select",
        "options": ["人工智能", "科学", "信息科技", "STEAM", "创客"],
        "help": "选择课程所属学科领域",
    },
}

render_chat_interface(agent, CourseProposalInput, input_fields)
