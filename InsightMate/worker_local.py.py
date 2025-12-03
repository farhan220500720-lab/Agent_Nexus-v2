# InsightMate/worker_local.py
import asyncio
import sys
from common.logger import get_logger
from common.db.postgres import AsyncSessionLocal
from common.db.models import Meeting, Summary

logger = get_logger("insightmate-worker")

async def summarize_text(text: str) -> str:
    # placeholder summarizer — replace with LLM call later
    # simple heuristic: first 300 chars + ellipsis
    clean = text.strip()
    return clean[:300] + ("..." if len(clean) > 300 else "")

async def process_meeting(meeting_id: int):
    async with AsyncSessionLocal() as session:
        meeting = await session.get(Meeting, meeting_id)
        if not meeting:
            logger.error("meeting not found", extra={"id": meeting_id})
            return False
        logger.info("processing meeting", extra={"id": meeting_id, "title": meeting.title})
        summary_text = await summarize_text(meeting.transcript)
        summary = Summary(meeting_id=meeting_id, content=summary_text)
        session.add(summary)
        try:
            await session.commit()
            await session.refresh(summary)
            logger.info("summary saved", extra={"summary_id": summary.id, "meeting_id": meeting_id})
            return True
        except Exception as e:
            await session.rollback()
            logger.exception("failed to save summary")
            return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python worker_local.py <meeting_id>")
        sys.exit(1)
    mid = int(sys.argv[1])
    asyncio.run(process_meeting(mid))
