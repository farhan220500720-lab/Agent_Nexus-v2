# InsightMate/api.py
import os
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from datetime import datetime

from common.logger import get_logger
from common.db.postgres import get_async_session, engine
from common.db.models import Meeting  # SQLAlchemy model we migrated

logger = get_logger("insightmate")
app = FastAPI(title="InsightMate (dev)")

class MeetingCreate(BaseModel):
    title: str
    transcript: str

class MeetingOut(BaseModel):
    id: int
    title: str
    created_at: str

@app.get("/healthz")
async def health():
    # DB connectivity healthcheck
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "now": datetime.utcnow().isoformat() + "Z"}
    except Exception as e:
        logger.exception("health check failed")
        raise HTTPException(status_code=500, detail="db error")

@app.post("/meetings", response_model=MeetingOut, status_code=201)
async def create_meeting(payload: MeetingCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Create a meeting record in Postgres (async).
    This uses SQLAlchemy ORM model Meeting and AsyncSession.
    """
    meeting = Meeting(title=payload.title, transcript=payload.transcript)
    try:
        session.add(meeting)
        await session.commit()
        await session.refresh(meeting)  # populate generated id/created_at
        logger.info("meeting inserted", extra={"id": meeting.id, "title": meeting.title})
        return MeetingOut(id=meeting.id, title=meeting.title, created_at=meeting.created_at.isoformat())
    except Exception as e:
        await session.rollback()
        logger.exception("failed to insert meeting")
        raise HTTPException(status_code=500, detail="insert failed")

@app.get("/meetings")
async def list_meetings(limit: int = 50, session: AsyncSession = Depends(get_async_session)):
    stmt = select(Meeting).order_by(Meeting.id.desc()).limit(limit)
    result = await session.execute(stmt)
    rows = result.scalars().all()
    return [{"id": r.id, "title": r.title, "created_at": r.created_at.isoformat()} for r in rows]
