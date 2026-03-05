"""A1.1 政策洞察分析 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_a.policy_insight import PolicyInsightAgent
from src.core.models import PolicyInsightInput
from app.components.chat_interface import render_chat_interface

st.header("A1.1 政策洞察分析")
st.caption("多渠道政策检索 + 课标映射 + 课程适配建议")

agent = PolicyInsightAgent()

input_fields = {
    "province": {
        "label": "目标省份",
        "type": "select",
        "options": [
            "", "北京", "上海", "广东", "江苏", "浙江", "山东", "四川",
            "湖北", "湖南", "河南", "河北", "福建", "安徽", "陕西",
            "重庆", "天津", "辽宁", "吉林", "黑龙江", "云南", "贵州",
            "广西", "山西", "江西", "海南", "甘肃", "内蒙古", "宁夏",
            "新疆", "西藏", "青海",
        ],
        "help": "留空表示全国范围",
    },
    "subject": {
        "label": "学科方向",
        "type": "select",
        "options": ["人工智能", "科学", "信息科技"],
        "help": "选择需要分析的学科方向",
    },
    "grade_range": {
        "label": "学段范围",
        "type": "select",
        "options": ["全部", "小学", "初中", "高中"],
        "help": "留空表示全学段",
    },
}

render_chat_interface(agent, PolicyInsightInput, input_fields)
