"""A类智能体 — 战略决策与市场洞察"""

from src.agents.category_a.competitor_research import CompetitorResearchAgent
from src.agents.category_a.course_proposal import CourseProposalAgent
from src.agents.category_a.demo_design import DemoDesignAgent
from src.agents.category_a.demo_scoring import DemoScoringAgent
from src.agents.category_a.policy_insight import PolicyInsightAgent
from src.agents.category_a.resource_assessment import ResourceAssessmentAgent
from src.agents.category_a.user_pain_point import UserPainPointAgent

__all__ = [
    "PolicyInsightAgent",
    "CompetitorResearchAgent",
    "UserPainPointAgent",
    "CourseProposalAgent",
    "DemoDesignAgent",
    "DemoScoringAgent",
    "ResourceAssessmentAgent",
]
