from langchain_core.tools import tool
import asyncio
import uuid
from common.schemas.study_schemas import QuizAttempt
from common.db.postgres import POSTGRES_CLIENT

@tool
def save_quiz_attempt_tool(user_id: str, topic_key: str, question: str, user_answer: str, correct_answer: str, score: float) -> str:
    """
    Saves a user's quiz attempt and score to the PostgreSQL database for adaptive learning tracking.
    Input requires user_id, topic_key, question, user_answer, correct_answer, and the float score (0.0 to 1.0).
    """
    attempt_data = QuizAttempt(
        quiz_id=str(uuid.uuid4()),
        user_id=user_id,
        topic_key=topic_key,
        question=question,
        user_answer=user_answer,
        correct_answer=correct_answer,
        score=score,
        timestamp=asyncio.get_event_loop().time()
    )
    
    # Run the asynchronous database operation synchronously within the tool wrapper
    loop = asyncio.get_event_loop()
    loop.run_until_complete(POSTGRES_CLIENT.save_quiz_attempt(attempt_data))
    
    return f"Quiz attempt {attempt_data.quiz_id} saved successfully for user {user_id}. Score: {score}."