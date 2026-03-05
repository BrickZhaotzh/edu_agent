"""B类 Agent — 课程设计与开发

核心管线: B1.2 → B1.3 → B1.4 → B1.5 → B2.1
"""

from .course_planning import CoursePlanningAgent
from .demo_delivery import DemoDeliveryAgent
from .lesson_design import LessonDesignAgent
from .outline_integration import OutlineIntegrationAgent
from .standard_matching import StandardMatchingAgent
from .unit_detail import UnitDetailAgent
from .unit_theme import UnitThemeAgent

__all__ = [
    "CoursePlanningAgent",
    "StandardMatchingAgent",
    "UnitThemeAgent",
    "UnitDetailAgent",
    "OutlineIntegrationAgent",
    "LessonDesignAgent",
    "DemoDeliveryAgent",
]
