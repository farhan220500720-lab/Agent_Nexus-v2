from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from common.db.models import Base, Meeting
from common.models import AnalysisResult
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://dev:dev@localhost:5432/agentic")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def get_db():
    return AsyncSessionLocal()

async def save_analysis_result(title: str, transcript: str, analysis: AnalysisResult):
    async with AsyncSessionLocal() as session:
        new_meeting = Meeting(
            title=title,
            transcript=transcript,
            summary=analysis.summary,
            action_items=analysis.action_items,
            is_valid=analysis.is_valid
        )
        session.add(new_meeting)
        await session.commit()
        await session.refresh(new_meeting)
        return new_meeting