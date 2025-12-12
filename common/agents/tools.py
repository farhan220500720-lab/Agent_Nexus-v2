from langchain_core.tools import tool
import asyncio
import uuid
import time
from typing import List
from common.schemas.study_schemas import QuizAttempt # Existing import
from common.schemas.chat_schemas import ConversationMessage, UserProfileSummary # New imports
from common.db.postgres import POSTGRES_CLIENT

# --- StudyFlow Tool (Existing) ---
@tool
def save_quiz_attempt_tool(user_id: str, topic_key: str, question: str, user_answer: str, correct_answer: str, score: float) -> str:
    """
    Saves a user's quiz attempt and score to the PostgreSQL database for adaptive learning tracking.
    """
    attempt_data = QuizAttempt(
        quiz_id=str(uuid.uuid4()),
        user_id=user_id,
        topic_key=topic_key,
        question=question,
        user_answer=user_answer,
        correct_answer=correct_answer,
        score=score,
        timestamp=time.time()
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(POSTGRES_CLIENT.save_quiz_attempt(attempt_data))
    return f"Quiz attempt {attempt_data.quiz_id} saved successfully for user {user_id}."

# --- ChatBuddyPlus Tools (New) ---

@tool
def save_conversation_message_tool(user_id: str, session_id: str, message_type: str, content: str) -> str:
    """
    Saves a single message (USER or AI) to the database history for context and retrieval.
    """
    message_data = ConversationMessage(
        user_id=user_id,
        session_id=session_id,
        message_type=message_type,
        content=content,
        timestamp=time.time()
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(POSTGRES_CLIENT.save_conversation_message(message_data))
    return "Message saved to conversation history."

@tool
def get_user_profile_summary_tool(user_id: str) -> str:
    """
    Retrieves the long-term personality and fact summary for a given user_id.
    Returns the profile as a JSON string.
    """
    loop = asyncio.get_event_loop()
    profile_json = loop.run_until_complete(POSTGRES_CLIENT.get_user_profile(user_id))
    return profile_json

@tool
def update_user_profile_tool(user_id: str, name: str, key_interests: List[str], key_facts: List[str]) -> str:
    """
    Updates the user's long-term profile summary in the database with new facts and interests.
    This should be called when the agent learns a new, important, persistent piece of information about the user.
    """
    profile_data = UserProfileSummary(
        user_id=user_id,
        summary_id=str(uuid.uuid4()),
        name=name,
        key_interests=key_interests,
        key_facts=key_facts,
        last_updated=time.time()
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(POSTGRES_CLIENT.update_user_profile(profile_data))
    return "User profile summary updated successfully."