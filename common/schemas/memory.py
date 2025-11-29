# memory.py
from pydantic import BaseModel, Field
from typing import Literal, List

class AgentMemoryItem(BaseModel):
    content: str = Field(..., min_length=1)
    source_agent: Literal["InsightMate", "StudyFlow", "ChatBuddy", "AutoAgent"]
    importance_score: float = Field(0.5, ge=0.0, le=1.0)
    tags: List[str] = []
