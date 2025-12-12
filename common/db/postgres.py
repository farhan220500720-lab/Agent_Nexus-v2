import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from common.config import settings
from common.db.study_models import QuizAttemptModel
from common.schemas.study_schemas import QuizAttempt

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

POSTGRES_CLIENT = PostgresClient()