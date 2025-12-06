from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class ActionItem(BaseModel):
    task_description: str = Field(...)
    assigned_to: str = Field(...)
    due_date: str = Field(...)

class AnalysisResult(BaseModel):
    summary: str = Field(...)
    key_decisions: List[str] = Field(...)
    action_items: List[ActionItem] = Field(...)

class TranscriptRequest(BaseModel):
    title: str = Field(...)
    transcript: str = Field(...)
    user_id: str = Field(...)

class StudyRequest(BaseModel):
    topic: str = Field(...)
    study_goal: str = Field(...)
    current_knowledge_level: str = Field(...)
    user_id: str = Field(...)

class StudyStep(BaseModel):
    step_number: int = Field(...)
    description: str = Field(...)
    estimated_time_minutes: int = Field(...)
    deliverable: str = Field(...)

class StudyPlan(BaseModel):
    topic: str = Field(...)
    prerequisites: List[str] = Field(...)
    total_estimated_time_hours: float = Field(...)
    steps: List[StudyStep] = Field(...)

class AgentState(BaseModel):
    transcript: str
    analysis_result: Optional[AnalysisResult] = None
    next_step: str

class StudyAgentState(BaseModel):
    study_request: StudyRequest
    study_plan: Optional[StudyPlan] = None
    next_step: str
    user_id: str