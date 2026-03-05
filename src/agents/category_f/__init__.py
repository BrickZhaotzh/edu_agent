"""F类 — 课程运营 智能体"""

from src.agents.category_f.course_intro import CourseIntroAgent
from src.agents.category_f.faq_bot import FAQBotAgent
from src.agents.category_f.operation_copy import OperationCopyAgent
from src.agents.category_f.poster_copy import PosterCopyAgent
from src.agents.category_f.satisfaction_survey import SatisfactionSurveyAgent
from src.agents.category_f.training_material import TrainingMaterialAgent

__all__ = [
    "FAQBotAgent",
    "OperationCopyAgent",
    "SatisfactionSurveyAgent",
    "PosterCopyAgent",
    "CourseIntroAgent",
    "TrainingMaterialAgent",
]
