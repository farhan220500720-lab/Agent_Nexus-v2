from typing import List, Optional
from datetime import date
from .base import CommonSchema, BaseModel, BaseSchema
from .insightmate import ActionItem, AnalysisResult # Patch to satisfy incorrect import path

class StudyRequest(BaseSchema):
    user_id: str
    topic_description: str
    duration_days: int
    target_date: date
    subject: str

class StudyPlan(CommonSchema):
    user_id: str
    goal_title: str
    target_date: date
    subject: str
    status: str = "Active"
    priority: int = 1
    required_resources: List[str] = []

class StudySession(CommonSchema):
    user_id: str
    study_plan_id: str
    topic: str
    duration_minutes: int
    summary_generated: Optional[str] = None
    key_concepts: List[str] = []
    confidence_rating: Optional[int] = None
