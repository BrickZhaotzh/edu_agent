"""B1.3 单元主题架构 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_b.unit_theme import UnitThemeAgent
from src.core.models import UnitThemeInput
from app.components.chat_interface import render_chat_interface

st.header("B1.3 单元主题架构")
st.caption("根据课程规划与课标映射，设计单元主题体系与知识进阶路径")

agent = UnitThemeAgent()

with st.expander("📥 导入上游数据（可选）"):
    upstream_data = st.text_area("粘贴上游智能体的输出内容", height=200, key="upstream_b1_3")
    if upstream_data:
        st.info("已加载上游数据")

input_fields = {
    "course_name": {
        "label": "课程名称",
        "type": "text",
        "default": "",
        "help": "输入课程名称，如 '小学人工智能启蒙'",
    },
    "total_units": {
        "label": "单元总数",
        "type": "slider",
        "min": 4,
        "max": 16,
        "default": 8,
        "help": "设置课程包含的单元数量",
    },
}

render_chat_interface(agent, UnitThemeInput, input_fields)
