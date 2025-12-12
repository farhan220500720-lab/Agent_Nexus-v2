from typing import List, Optional
from datetime import date
from .base import CommonSchema, BaseSchema

class TranscriptRequest(BaseSchema):
    raw_transcript: str
    meeting_title: str
    
class SummaryResponse(CommonSchema):
    meeting_id: str
    title: str
    summary: str
    action_items: List[str]

class AnalysisResult(CommonSchema):
    source_id: str
    result_type: str
    analysis_data: dict

class ActionItem(BaseSchema):
    task_description: str
    is_completed: bool = False
    assigned_to: Optional[str] = None
    due_date: Optional[date] = None