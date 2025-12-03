from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Type, TypeVar
from common.db.base import CommonBase
from common.schemas import MeetingBase, MeetingInDB
from common.db.models import Meeting

async def create_meeting(db: AsyncSession, meeting_data: MeetingBase) -> MeetingInDB:
    # Convert Pydantic model to dict and create SQLAlchemy model instance
    db_obj = Meeting(**meeting_data.dict()) 
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return MeetingInDB.from_orm(db_obj)

async def get_all_meetings(db: AsyncSession) -> List[MeetingInDB]:
    result = await db.execute(select(Meeting))
    meetings = result.scalars().all()
    return [MeetingInDB.from_orm(m) for m in meetings]