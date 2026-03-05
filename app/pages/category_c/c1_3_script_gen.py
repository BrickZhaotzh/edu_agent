"""C1.3 逐字稿生成 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.script_gen import ScriptGenAgent
from src.core.models import ScriptGenInput
from app.components.chat_interface import render_chat_interface

st.header("C1.3 逐字稿生成")
st.caption("基于问题链生成教师课堂逐字稿，管线: C1.1 → C1.3 → C1.4")

agent = ScriptGenAgent()

# 上游数据展开区（来自 C1.1 问题链设计）
with st.expander("📥 上游数据（来自 C1.1 问题链设计）", expanded=False):
    upstream_question_chain = st.text_area(
        "粘贴 C1.1 问题链输出（JSON 格式）",
        value="",
        height=150,
        help="将 C1.1 问题链设计的输出粘贴到此处，系统将自动解析并传递给逐字稿生成",
        key="c1_3_upstream_question_chain",
    )

input_fields = {
    "lesson_topic": {
        "label": "课时主题",
        "type": "text",
        "default": "",
        "help": "输入本节课的教学主题",
    },
    "duration_minutes": {
        "label": "课时时长（分钟）",
        "type": "slider",
        "min": 20,
        "max": 90,
        "default": 45,
        "help": "设置课时总时长",
    },
}

render_chat_interface(agent, ScriptGenInput, input_fields)
