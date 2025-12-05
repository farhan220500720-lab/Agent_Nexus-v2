from fastapi import FastAPI
from pydantic import BaseModel, Field
from InsightMate.tasks import summarize_meeting

app = FastAPI(
    title="InsightMate API",
    description="API for asynchronous meeting summary and action item extraction.",
    version="1.0.0"
)

class MeetingPayload(BaseModel):
    title: str = Field(..., example="Q3 Strategy Review")
    transcript: str = Field(..., example="Joe: We missed the Q3 revenue target by 10%. Jane: I will prepare a detailed post-mortem report by end of week. Decision: Postpone the new marketing campaign until the report is reviewed.")

@app.post("/meetings", status_code=202)
def submit_meeting_summary_task(payload: MeetingPayload):
    summarize_meeting.send(
        title=payload.title,
        transcript=payload.transcript
    )

    return {
        "status": "Task accepted",
        "message": f"Summary task for '{payload.title}' queued successfully.",
        "task_name": "summarize_meeting"
    }