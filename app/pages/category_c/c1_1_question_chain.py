"""C1.1 问题链设计 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.question_chain import QuestionChainAgent
from src.core.models import QuestionChainInput
from app.components.chat_interface import render_chat_interface

st.header("C1.1 问题链设计")
st.caption("基于教学目标设计布鲁姆认知层次问题链，核心管线起点")

agent = QuestionChainAgent()

input_fields = {
    "lesson_topic": {
        "label": "课时主题",
        "type": "text",
        "default": "",
        "help": "输入本节课的教学主题",
    },
    "teaching_objectives": {
        "label": "教学目标",
        "type": "multiselect",
        "options": [
            "了解基本概念",
            "理解核心原理",
            "掌握操作技能",
            "能够分析问题",
            "学会评价方案",
            "完成创新设计",
        ],
        "default": [],
        "help": "选择本节课需要达成的教学目标（对应布鲁姆认知层级）",
    },
}

render_chat_interface(agent, QuestionChainInput, input_fields)
