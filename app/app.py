"""科创课程AI智能体平台 — Streamlit 多页面应用主入口"""

import sys
from pathlib import Path

import streamlit as st

# 确保项目根目录在 sys.path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.core.chat_storage import ChatStorage

st.set_page_config(
    page_title="科创课程AI智能体平台",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 对话计数（用于导航标题气泡）
_conv_counts = ChatStorage().count_all()


def _t(name: str, agent_id: str) -> str:
    """导航标题：有对话时追加计数"""
    n = _conv_counts.get(agent_id, 0)
    return f"{name} ({n})" if n else name


# ============ 页面注册 ============

# 首页
home = st.Page("pages/home.py", title="首页仪表盘", icon="🏠", default=True)

# A类 — 课程产品方案
a_pages = [
    st.Page("pages/category_a/a1_1_policy_insight.py", title=_t("A1.1 政策洞察分析", "A1.1"), icon="📋"),
    st.Page("pages/category_a/a2_1_competitor_research.py", title=_t("A2.1 行业竞品调研", "A2.1"), icon="🔍"),
    st.Page("pages/category_a/a2_2_user_pain_point.py", title=_t("A2.2 用户痛点分析", "A2.2"), icon="👥"),
    st.Page("pages/category_a/a3_1_course_proposal.py", title=_t("A3.1 课程立项书", "A3.1"), icon="📝"),
    st.Page("pages/category_a/a4_1_demo_design.py", title=_t("A4.1 Demo课设计", "A4.1"), icon="🎯"),
    st.Page("pages/category_a/a5_1_demo_scoring.py", title=_t("A5.1 Demo评分模型", "A5.1"), icon="⭐"),
    st.Page("pages/category_a/a6_1_resource_assessment.py", title=_t("A6.1 生态资源评估", "A6.1"), icon="📦"),
]

# B类 — 课程方案
b_pages = [
    st.Page("pages/category_b/b1_1_course_planning.py", title=_t("B1.1 课程整体规划", "B1.1"), icon="📐"),
    st.Page("pages/category_b/b1_2_standard_matching.py", title=_t("B1.2 课标教材匹配", "B1.2"), icon="🔗"),
    st.Page("pages/category_b/b1_3_unit_theme.py", title=_t("B1.3 单元主题架构", "B1.3"), icon="🏗️"),
    st.Page("pages/category_b/b1_4_unit_detail.py", title=_t("B1.4 单元细化主题", "B1.4"), icon="🔬"),
    st.Page("pages/category_b/b1_5_outline_integration.py", title=_t("B1.5 大纲整合输出", "B1.5"), icon="📄"),
    st.Page("pages/category_b/b2_1_lesson_design.py", title=_t("B2.1 单节课时设计", "B2.1"), icon="📅"),
    st.Page("pages/category_b/b2_2_demo_delivery.py", title=_t("B2.2 Demo课交付", "B2.2"), icon="🎁"),
]

# C类 — 教研量产
c_pages = [
    st.Page("pages/category_c/c1_1_question_chain.py", title=_t("C1.1 问题链设计", "C1.1"), icon="❓"),
    st.Page("pages/category_c/c1_2_proposal_draft.py", title=_t("C1.2 方案稿撰写", "C1.2"), icon="📃"),
    st.Page("pages/category_c/c1_3_script_gen.py", title=_t("C1.3 逐字稿生成", "C1.3"), icon="📜"),
    st.Page("pages/category_c/c1_4_storyboard.py", title=_t("C1.4 分镜脚本", "C1.4"), icon="🎬"),
    st.Page("pages/category_c/c1_5_slideshow.py", title=_t("C1.5 课件生成", "C1.5"), icon="📊"),
    st.Page("pages/category_c/c1_6_teaching_design.py", title=_t("C1.6 教学设计", "C1.6"), icon="✏️"),
    st.Page("pages/category_c/c1_7_student_manual.py", title=_t("C1.7 学生手册", "C1.7"), icon="📘"),
    st.Page("pages/category_c/c1_8_teacher_manual.py", title=_t("C1.8 教师手册", "C1.8"), icon="📕"),
    st.Page("pages/category_c/c1_9_homework.py", title=_t("C1.9 课后作业", "C1.9"), icon="📝"),
    st.Page("pages/category_c/c1_10_rubric.py", title=_t("C1.10 评价量规", "C1.10"), icon="📏"),
    st.Page("pages/category_c/c2_1_experiment_prd.py", title=_t("C2.1 实验PRD", "C2.1"), icon="🧪"),
    st.Page("pages/category_c/c2_2_code_example.py", title=_t("C2.2 编程样例", "C2.2"), icon="💻"),
    st.Page("pages/category_c/c3_1_pinyin.py", title=_t("C3.1 拼音标注", "C3.1"), icon="🔤"),
    st.Page("pages/category_c/c3_2_teaching_review.py", title=_t("C3.2 教学审核", "C3.2"), icon="✅"),
    st.Page("pages/category_c/c3_3_class_exercise.py", title=_t("C3.3 随堂练习", "C3.3"), icon="🏋️"),
    st.Page("pages/category_c/c3_4_micro_lesson_review.py", title=_t("C3.4 微课评审", "C3.4"), icon="🎥"),
    st.Page("pages/category_c/c4_1_resource_upload.py", title=_t("C4.1 资源上传", "C4.1"), icon="📤"),
    st.Page("pages/category_c/c5_1_knowledge_graph.py", title=_t("C5.1 知识图谱", "C5.1"), icon="🕸️"),
    st.Page("pages/category_c/c5_2_standard_analysis.py", title=_t("C5.2 课标分析", "C5.2"), icon="📑"),
]

# D类 — 学具制作
d_pages = [
    st.Page("pages/category_d/d1_1_supply_list.py", title=_t("D1.1 教具需求清单", "D1.1"), icon="📋"),
    st.Page("pages/category_d/d1_2_supply_diagram.py", title=_t("D1.2 教具示意图", "D1.2"), icon="🖼️"),
    st.Page("pages/category_d/d1_5_requirement_spec.py", title=_t("D1.5 需求规格说明书", "D1.5"), icon="📄"),
    st.Page("pages/category_d/d2_1_supply_sourcing.py", title=_t("D2.1 学具寻源", "D2.1"), icon="🔎"),
]

# E类 — 视频制作
e_pages = [
    st.Page("pages/category_e/e1_1_lecture_video.py", title=_t("E1.1 说课视频", "E1.1"), icon="🎤"),
    st.Page("pages/category_e/e1_2_outsource_video.py", title=_t("E1.2 外包视频制作", "E1.2"), icon="🎞️"),
    st.Page("pages/category_e/e1_3_assembly_video.py", title=_t("E1.3 学具搭建视频", "E1.3"), icon="🔧"),
    st.Page("pages/category_e/e1_4_tts_gen.py", title=_t("E1.4 语音合成", "E1.4"), icon="🔊"),
]

# F类 — 课程运营
f_pages = [
    st.Page("pages/category_f/f1_1_poster_copy.py", title=_t("F1.1 宣传海报文案", "F1.1"), icon="🖼️"),
    st.Page("pages/category_f/f1_2_course_intro.py", title=_t("F1.2 课程介绍页", "F1.2"), icon="📰"),
    st.Page("pages/category_f/f1_3_training_material.py", title=_t("F1.3 培训材料", "F1.3"), icon="📚"),
    st.Page("pages/category_f/f1_4_operation_copy.py", title=_t("F1.4 运营文案", "F1.4"), icon="✍️"),
    st.Page("pages/category_f/f2_1_satisfaction_survey.py", title=_t("F2.1 满意度调研", "F2.1"), icon="📊"),
    st.Page("pages/category_f/f3_1_faq_bot.py", title=_t("F3.1 FAQ智能答疑", "F3.1"), icon="💬"),
]

# 工作流编排
workflow_pages = [
    st.Page("pages/workflow_builder.py", title="工作流编排器", icon="🔀"),
]

# 管理页面
admin_pages = [
    st.Page("pages/admin_knowledge.py", title="云端知识库管理", icon="☁️"),
]

# ============ 导航 ============

pg = st.navigation(
    {
        "概览": [home],
        "工作流": workflow_pages,
        "A 课程产品方案": a_pages,
        "B 课程方案": b_pages,
        "C 教研量产": c_pages,
        "D 学具制作": d_pages,
        "E 视频制作": e_pages,
        "F 课程运营": f_pages,
        "管理": admin_pages,
    }
)

pg.run()
