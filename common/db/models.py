import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, String, DateTime, Integer, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from common.db.base import Base

class CommonAttributes:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    app_id = Column(String, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class ActionItemModel(CommonAttributes, Base):
    __tablename__ = "action_items"
    
    task_description = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False, nullable=False)
    assigned_to = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)

class AnalysisResultModel(CommonAttributes, Base):
    __tablename__ = "analysis_results"

    source_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    result_type = Column(String, nullable=False)
    analysis_data = Column(JSON, nullable=False)

class StudyRequestModel(CommonAttributes, Base):
    __tablename__ = "study_requests"

    topic_description = Column(String, nullable=False)
    duration_days = Column(Integer, nullable=False)
    target_date = Column(DateTime, nullable=False)
    subject = Column(String, nullable=False)
    
    study_plans = relationship("StudyPlanModel", back_populates="request", uselist=True)

class StudyPlanModel(CommonAttributes, Base):
    __tablename__ = "study_plans"
    
    goal_title = Column(String, nullable=False)
    target_date = Column(DateTime, nullable=False)
    subject = Column(String, nullable=False)
    status = Column(String, default="Active", nullable=False)
    priority = Column(Integer, default=1, nullable=False)
    required_resources = Column(JSON, nullable=False, default=[])

    study_request_id = Column(UUID(as_uuid=True), ForeignKey("study_requests.id"))
    request = relationship("StudyRequestModel", back_populates="study_plans")
    sessions = relationship("StudySessionModel", back_populates="plan", uselist=True)

class StudySessionModel(CommonAttributes, Base):
    __tablename__ = "study_sessions"
    
    topic = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    summary_generated = Column(String, nullable=True)
    key_concepts = Column(JSON, nullable=False, default=[])
    confidence_rating = Column(Integer, nullable=True)

    study_plan_id = Column(UUID(as_uuid=True), ForeignKey("study_plans.id"))
    plan = relationship("StudyPlanModel", back_populates="sessions")

class MeetingModel(CommonAttributes, Base):
    __tablename__ = "meetings"

    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    raw_transcript = Column(String, nullable=False)
