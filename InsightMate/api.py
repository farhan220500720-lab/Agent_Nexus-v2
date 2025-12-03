from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List
import uuid

from common.db.postgres import get_async_session, engine
from common.schemas import MeetingBase, MeetingOutput
from common.db import crud
from InsightMate.tasks import generate_summary

app = FastAPI()

@app.get("/healthz")
async def health():
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.post("/meetings", response_model=MeetingOutput, status_code=status.HTTP_202_ACCEPTED)
async def create_meeting_endpoint(meeting: MeetingBase, db: AsyncSession = Depends(get_async_session)):
    # 1. Save the meeting to the relational database (Postgres)
    db_meeting = await crud.create_meeting(db, meeting)
    
    # 2. Enqueue the task for background processing (Agentic work)
    # The API returns immediately, and the worker (in the other terminal) picks it up.
    task_id = str(uuid.uuid4())
    generate_summary.send(
        meeting_id=db_meeting.id, 
        transcript=db_meeting.transcript, 
        target_length=250
    )
    
    # 3. Return the saved object immediately with a 202 Accepted status
    return db_meeting
    

@app.get("/meetings", response_model=List[MeetingOutput])
async def read_meetings(db: AsyncSession = Depends(get_async_session)):
    return await crud.get_all_meetings(db)