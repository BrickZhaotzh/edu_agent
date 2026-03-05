"""Pydantic 基础模型 — 所有 Agent 的输入/输出基类"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class Priority(str, Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class AgentInput(BaseModel):
    """Agent 通用输入基类"""
    query: str = Field(..., description="用户输入的核心问题或需求")
    context: dict[str, Any] = Field(default_factory=dict, description="附加上下文信息")
    knowledge_ids: list[str] = Field(default_factory=list, description="需要加载的知识库ID列表")
    upstream_output: dict[str, Any] | None = Field(None, description="上游管线Agent的输出（用于顺序管线）")
    file_content: str | None = Field(None, description="用户上传的附件内容（文本）")
    file_name: str | None = Field(None, description="用户上传的附件文件名")


class AgentOutput(BaseModel):
    """Agent 通用输出基类"""
    agent_id: str = Field(..., description="智能体ID")
    agent_name: str = Field(..., description="智能体名称")
    content: str = Field(..., description="主要输出内容（Markdown格式）")
    structured_data: dict[str, Any] = Field(default_factory=dict, description="结构化数据（表格、评分等）")
    metadata: dict[str, Any] = Field(default_factory=dict, description="元数据")
    created_at: datetime = Field(default_factory=datetime.now)
    success: bool = True
    error_message: str = ""


# ============ A类 专用模型 ============

class PolicyInsightInput(AgentInput):
    """A1.1 政策洞察分析 输入"""
    province: str = Field("", description="目标省份（空表示全国）")
    subject: str = Field("人工智能", description="学科方向")
    grade_range: str = Field("", description="学段范围，如 '小学3-6年级'")


class PolicyInsightOutput(AgentOutput):
    """A1.1 政策洞察分析 输出"""
    policy_summary: list[dict] = Field(default_factory=list, description="政策要点摘要列表")
    curriculum_mapping: list[dict] = Field(default_factory=list, description="课标映射关系")
    adaptation_suggestions: list[str] = Field(default_factory=list, description="课程适配建议")


class CompetitorResearchInput(AgentInput):
    """A2.1 行业竞品调研 输入"""
    target: str = Field(..., description="调研目标（机构名/赛道方向）")
    dimensions: list[str] = Field(default_factory=lambda: ["产品", "课程", "商业", "政策"], description="调研维度")


class CompetitorResearchOutput(AgentOutput):
    """A2.1 行业竞品调研 输出"""
    competitors: list[dict] = Field(default_factory=list, description="竞品信息列表")
    comparison_matrix: dict = Field(default_factory=dict, description="对比矩阵")
    differentiators: list[str] = Field(default_factory=list, description="差异化要点")


class UserPainPointInput(AgentInput):
    """A2.2 用户痛点分析 输入"""
    target_user: str = Field("教师", description="目标用户类型")
    scenario: str = Field("", description="使用场景")


class UserPainPointOutput(AgentOutput):
    """A2.2 用户痛点分析 输出"""
    questionnaire: str = Field("", description="调研问卷内容")
    pain_points: list[dict] = Field(default_factory=list, description="痛点列表")
    user_personas: list[dict] = Field(default_factory=list, description="用户画像")


class CourseProposalInput(AgentInput):
    """A3.1 课程立项书 输入"""
    course_name: str = Field(..., description="课程名称")
    target_grade: str = Field(..., description="目标学段")
    subject_area: str = Field("人工智能", description="学科领域")


class CourseProposalOutput(AgentOutput):
    """A3.1 课程立项书 输出"""
    business_model: dict = Field(default_factory=dict, description="商业模式分析")
    feasibility: dict = Field(default_factory=dict, description="可行性分析")
    plans: list[dict] = Field(default_factory=list, description="多方案推演")


class DemoDesignInput(AgentInput):
    """A4.1 Demo课设计 输入"""
    course_topic: str = Field(..., description="课程主题")
    target_grade: str = Field(..., description="目标学段")
    duration_minutes: int = Field(45, description="课时长度（分钟）")


class DemoDesignOutput(AgentOutput):
    """A4.1 Demo课设计 输出"""
    lesson_plan: dict = Field(default_factory=dict, description="教学设计方案")
    activities: list[dict] = Field(default_factory=list, description="教学活动列表")


class DemoScoringInput(AgentInput):
    """A5.1 Demo评分模型 输入"""
    demo_content: str = Field(..., description="Demo课内容（文本）")
    scoring_dimensions: list[str] = Field(
        default_factory=lambda: ["内容质量", "教学设计", "互动性", "技术准确性", "趣味性"],
        description="评分维度"
    )


class DemoScoringOutput(AgentOutput):
    """A5.1 Demo评分模型 输出"""
    scores: dict[str, float] = Field(default_factory=dict, description="各维度评分")
    total_score: float = Field(0.0, description="总分")
    review_comments: list[str] = Field(default_factory=list, description="评审意见")


class ResourceAssessmentInput(AgentInput):
    """A6.1 生态资源评估 输入"""
    resource_name: str = Field(..., description="资源名称")
    resource_type: str = Field("", description="资源类型")
    resource_description: str = Field("", description="资源描述")


class ResourceAssessmentOutput(AgentOutput):
    """A6.1 生态资源评估 输出"""
    classification: dict = Field(default_factory=dict, description="分类标签")
    reusability_score: float = Field(0.0, description="复用性评分")
    recommendations: list[str] = Field(default_factory=list, description="使用建议")


# ============ B类 专用模型 ============

class StandardMatchingInput(AgentInput):
    """B1.2 课标教材匹配 输入"""
    subject: str = Field(..., description="学科")
    grade: str = Field(..., description="年级")
    textbook_version: str = Field("", description="教材版本")


class StandardMatchingOutput(AgentOutput):
    """B1.2 课标教材匹配 输出"""
    matches: list[dict] = Field(default_factory=list, description="匹配结果")


class UnitThemeInput(AgentInput):
    """B1.3 单元主题架构 输入"""
    course_name: str = Field(..., description="课程名称")
    total_units: int = Field(8, description="单元总数")
    standard_mapping: dict = Field(default_factory=dict, description="课标映射（来自B1.2）")


class UnitThemeOutput(AgentOutput):
    """B1.3 单元主题架构 输出"""
    units: list[dict] = Field(default_factory=list, description="单元列表")


class LessonDesignInput(AgentInput):
    """B2.1 单节课时设计 输入"""
    unit_name: str = Field(..., description="单元名称")
    lesson_topic: str = Field(..., description="课时主题")
    lesson_number: int = Field(1, description="第几课时")
    duration_minutes: int = Field(45, description="时长")


class LessonDesignOutput(AgentOutput):
    """B2.1 单节课时设计 输出"""
    objectives: list[str] = Field(default_factory=list, description="教学目标")
    activities: list[dict] = Field(default_factory=list, description="教学环节")
    assessment: dict = Field(default_factory=dict, description="评价方式")


# ============ C类 核心模型 ============

class QuestionChainInput(AgentInput):
    """C1.1 问题链设计 输入"""
    lesson_topic: str = Field(..., description="课时主题")
    teaching_objectives: list[str] = Field(default_factory=list, description="教学目标")


class QuestionChainOutput(AgentOutput):
    """C1.1 问题链设计 输出"""
    questions: list[dict] = Field(default_factory=list, description="问题链")


class ScriptGenInput(AgentInput):
    """C1.3 逐字稿生成 输入"""
    lesson_topic: str = Field(..., description="课时主题")
    question_chain: list[dict] = Field(default_factory=list, description="问题链（来自C1.1）")
    duration_minutes: int = Field(45, description="时长")


class ScriptGenOutput(AgentOutput):
    """C1.3 逐字稿生成 输出"""
    script_sections: list[dict] = Field(default_factory=list, description="逐字稿分段")
    total_word_count: int = Field(0, description="总字数")


class StoryboardInput(AgentInput):
    """C1.4 分镜脚本 输入"""
    script_content: str = Field(..., description="逐字稿内容（来自C1.3）")
    video_style: str = Field("讲解+演示", description="视频风格")


class StoryboardOutput(AgentOutput):
    """C1.4 分镜脚本 输出"""
    scenes: list[dict] = Field(default_factory=list, description="分镜列表")
