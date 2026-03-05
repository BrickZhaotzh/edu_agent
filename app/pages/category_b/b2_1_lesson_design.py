"""B2.1 单节课时设计 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_b.lesson_design import LessonDesignAgent
from src.core.models import LessonDesignInput
from app.components.chat_interface import render_chat_interface

st.header("B2.1 单节课时设计")
st.caption("基于单元大纲，生成单节课的完整教学设计（目标、环节、评价）")

agent = LessonDesignAgent()

with st.expander("📥 导入上游数据（可选）"):
    upstream_data = st.text_area("粘贴上游智能体的输出内容", height=200, key="upstream_b2_1")
    if upstream_data:
        st.info("已加载上游数据")

input_fields = {
    "unit_name": {
        "label": "单元名称",
        "type": "text",
        "default": "",
        "help": "输入所属单元名称，如 '图像识别入门'",
    },
    "lesson_topic": {
        "label": "课时主题",
        "type": "text",
        "default": "",
        "help": "输入本节课的具体主题，如 '认识卷积神经网络'",
    },
    "lesson_number": {
        "label": "第几课时",
        "type": "number",
        "default": 1,
        "help": "本节课在单元中的序号",
    },
    "duration_minutes": {
        "label": "课时时长（分钟）",
        "type": "slider",
        "min": 20,
        "max": 90,
        "default": 45,
        "help": "设置本节课的时长",
    },
}

render_chat_interface(agent, LessonDesignInput, input_fields)
