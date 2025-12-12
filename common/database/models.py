from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class BaseMixin:
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

class UserModel(Base, BaseMixin):
    __tablename__ = 'users'

    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)

    personalization_data = Column(JSON, default={}, nullable=False)
    
    tasks = relationship("AgentTaskModel", back_populates="user")

class AgentTaskModel(Base, BaseMixin):
    __tablename__ = 'agent_tasks'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    
    task_type = Column(String(50), nullable=False)
    status = Column(String(50), default='PENDING', nullable=False)
    
    input_data = Column(JSON, nullable=False)
    output_data = Column(JSON, default={}, nullable=True)
    
    user = relationship("UserModel", back_populates="tasks")
    