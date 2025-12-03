from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CoreSchema(BaseModel):
    class Config:
        orm_mode = True 

# --- InsightMate (Meeting) Schemas ---

class MeetingBase(CoreSchema):
    title: str = Field(..., max_length=256)
    transcript: str

class MeetingInDB(MeetingBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class MeetingOutput(MeetingBase):
    id: int
    created_at: datetime
    updated_at: datetime