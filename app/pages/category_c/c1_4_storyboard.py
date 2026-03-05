"""C1.4 分镜脚本 — Streamlit 页面"""
import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.agents.category_c.storyboard import StoryboardAgent
from src.core.models import StoryboardInput
from app.components.chat_interface import render_chat_interface

st.header("C1.4 分镜脚本")
st.caption("将逐字稿转化为视频分镜脚本，管线: C1.1 → C1.3 → C1.4")

agent = StoryboardAgent()

# 上游数据展开区（来自 C1.3 逐字稿生成）
with st.expander("📥 上游数据（来自 C1.3 逐字稿生成）", expanded=False):
    upstream_script = st.text_area(
        "粘贴 C1.3 逐字稿输出",
        value="",
        height=200,
        help="将 C1.3 逐字稿生成的输出粘贴到此处，系统将自动传递给分镜脚本生成",
        key="c1_4_upstream_script",
    )

input_fields = {
    "video_style": {
        "label": "视频风格",
        "type": "select",
        "options": ["讲解+演示", "纯动画", "实拍+动画", "屏幕录制"],
        "help": "选择目标视频的呈现风格",
    },
}

render_chat_interface(agent, StoryboardInput, input_fields)
