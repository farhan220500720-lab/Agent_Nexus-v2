import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from common.config import settings
from common.db import QuizAttemptModel, ConversationMessageModel, UserProfileSummaryModel
from common.schemas.study_schemas import QuizAttempt
from common.schemas.chat_schemas import ConversationMessage, UserProfileSummary
from sqlalchemy import select
import json

class PostgresClient:
    _instance = None

    def __new__(cls, database_url: str = None):
        if cls._instance is None:
            cls._instance = super(PostgresClient, cls).__new__(cls)
            cls._instance.database_url = database_url or settings().DATABASE_URL
            cls._instance.engine = create_async_engine(cls._instance.database_url)
            cls._instance.AsyncSessionLocal = sessionmaker(
                cls._instance.engine, class_=AsyncSession, expire_on_commit=False
            )
        return cls._instance

    @asynccontextmanager
    async def get_session(self):
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise

    async def save_quiz_attempt(self, attempt_data: QuizAttempt):
        async with self.get_session() as session:
            new_attempt = QuizAttemptModel(
                quiz_id=attempt_data.quiz_id,
                user_id=attempt_data.user_id,
                topic_key=attempt_data.topic_key,
                question=attempt_data.question,
                user_answer=attempt_data.user_answer,
                correct_answer=attempt_data.correct_answer,
                score=attempt_data.score
            )
            session.add(new_attempt)
    
    async def save_conversation_message(self, message_data: ConversationMessage):
        async with self.get_session() as session:
            new_message = ConversationMessageModel(
                id=str(message_data.timestamp),
                user_id=message_data.user_id,
                session_id=message_data.session_id,
                message_type=message_data.message_type,
                content=message_data.content,
                timestamp=message_data.timestamp
            )
            session.add(new_message)

    async def get_user_profile(self, user_id: str) -> str:
        async with self.get_session() as session:
            stmt = select(UserProfileSummaryModel).where(UserProfileSummaryModel.user_id == user_id)
            result = await session.execute(stmt)
            profile = result.scalars().first()
            
            if profile:
                return json.dumps({
                    "name": profile.name,
                    "key_interests": json.loads(profile.key_interests),
                    "key_facts": json.loads(profile.key_facts),
                    "last_updated": profile.last_updated
                })
            return "No profile found."

    async def update_user_profile(self, profile_data: UserProfileSummary):
        async with self.get_session() as session:
            stmt = select(UserProfileSummaryModel).where(UserProfileSummaryModel.user_id == profile_data.user_id)
            result = await session.execute(stmt)
            existing_profile = result.scalars().first()

            interests_json = json.dumps(profile_data.key_interests)
            facts_json = json.dumps(profile_data.key_facts)
            
            if existing_profile:
                existing_profile.name = profile_data.name
                existing_profile.key_interests = interests_json
                existing_profile.key_facts = facts_json
                existing_profile.last_updated = profile_data.last_updated
            else:
                new_profile = UserProfileSummaryModel(
                    user_id=profile_data.user_id,
                    summary_id=profile_data.summary_id,
                    name=profile_data.name,
                    key_interests=interests_json,
                    key_facts=facts_json,
                    last_updated=profile_data.last_updated
                )
                session.add(new_profile)

POSTGRES_CLIENT = PostgresClient()