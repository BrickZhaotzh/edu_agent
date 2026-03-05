"""A6.1 生态资源评估 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_a.resource_assessment import ResourceAssessmentAgent
from src.core.models import ResourceAssessmentInput
from app.components.chat_interface import render_chat_interface

st.header("A6.1 生态资源评估")
st.caption("资源录入 + 分类标签 + 复用性评估")

agent = ResourceAssessmentAgent()

input_fields = {
    "resource_name": {
        "label": "资源名称",
        "type": "text",
        "default": "",
        "help": "输入待评估的资源名称",
    },
    "resource_type": {
        "label": "资源类型",
        "type": "select",
        "options": [
            "", "教材", "教案", "课件", "视频", "软件工具",
            "硬件套件", "实验器材", "在线平台", "竞赛资源", "其他",
        ],
        "help": "选择资源的类型分类",
    },
    "resource_description": {
        "label": "资源描述",
        "type": "textarea",
        "default": "",
        "help": "简要描述资源的内容、来源和特点",
    },
}

render_chat_interface(agent, ResourceAssessmentInput, input_fields)
