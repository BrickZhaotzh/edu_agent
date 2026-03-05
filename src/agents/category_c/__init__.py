"""C类 教研量产智能体集合

核心管线: C1.1(问题链) → C1.3(逐字稿) → C1.4(分镜脚本)
"""

from src.agents.category_c.class_exercise import ClassExerciseAgent
from src.agents.category_c.code_example import CodeExampleAgent
from src.agents.category_c.experiment_prd import ExperimentPRDAgent
from src.agents.category_c.homework import HomeworkAgent
from src.agents.category_c.knowledge_graph import KnowledgeGraphAgent
from src.agents.category_c.micro_lesson_review import MicroLessonReviewAgent
from src.agents.category_c.pinyin_annotator import PinyinAnnotatorAgent
from src.agents.category_c.proposal_draft import ProposalDraftAgent
from src.agents.category_c.question_chain import QuestionChainAgent
from src.agents.category_c.resource_upload import ResourceUploadAgent
from src.agents.category_c.rubric import RubricAgent
from src.agents.category_c.script_gen import ScriptGenAgent
from src.agents.category_c.slideshow import SlideshowAgent
from src.agents.category_c.standard_analysis import StandardAnalysisAgent
from src.agents.category_c.storyboard import StoryboardAgent
from src.agents.category_c.student_manual import StudentManualAgent
from src.agents.category_c.teacher_manual import TeacherManualAgent
from src.agents.category_c.teaching_design import TeachingDesignAgent
from src.agents.category_c.teaching_review import TeachingReviewAgent

__all__ = [
    # C1.x 教研内容生产
    "QuestionChainAgent",       # C1.1  问题链设计 (P0)
    "ProposalDraftAgent",       # C1.2  方案稿撰写 (P1)
    "ScriptGenAgent",           # C1.3  逐字稿生成 (P0)
    "StoryboardAgent",          # C1.4  分镜脚本 (P0)
    "SlideshowAgent",           # C1.5  课件生成 (P1)
    "TeachingDesignAgent",      # C1.6  教学设计 (P1)
    "StudentManualAgent",       # C1.7  学生手册 (P1)
    "TeacherManualAgent",       # C1.8  教师手册 (P1)
    "HomeworkAgent",            # C1.9  课后作业 (P1)
    "RubricAgent",              # C1.10 评价量规 (P1)
    # C2.x 实验与编程
    "ExperimentPRDAgent",       # C2.1  实验PRD (P1)
    "CodeExampleAgent",         # C2.2  编程样例 (P1)
    # C3.x 辅助工具
    "PinyinAnnotatorAgent",     # C3.1  拼音标注 (P1)
    "TeachingReviewAgent",      # C3.2  教学审核 (P1)
    "ClassExerciseAgent",       # C3.3  随堂练习 (P1)
    "MicroLessonReviewAgent",   # C3.4  微课评审 (P2)
    # C4.x 资源管理
    "ResourceUploadAgent",      # C4.1  资源上传 (P3)
    # C5.x 知识与标准
    "KnowledgeGraphAgent",      # C5.1  知识图谱 (P2)
    "StandardAnalysisAgent",    # C5.2  课标分析 (P1)
]
