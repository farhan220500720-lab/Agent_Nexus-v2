from pydantic import BaseModel, Field
from typing import Dict, Any

class TaskRequest(BaseModel):
    task_id: str = Field(..., description="Unique ID for the task run.")
    source: str = Field(..., description="The agent or service that initiated the task (e.g., InsightMate).")
    payload: Dict[str, Any] = Field(..., description="The main data required to execute the task.")
    
class SummaryTaskPayload(BaseModel):
    meeting_id: int = Field(..., description="The database ID of the meeting to summarize.")
    transcript: str = Field(..., description="The raw transcript data.")
    target_length: int = Field(250, description="The desired length of the summary.")