from google import genai
from common.config import settings

def get_llm_client():
    if not settings.GEMINI_API_KEY or settings.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        raise ValueError("GEMINI_API_KEY is not set in environment variables.")

    return genai.Client(api_key=settings.GEMINI_API_KEY)

llm_client = get_llm_client()
