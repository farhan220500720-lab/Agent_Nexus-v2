import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# --- DEBUG SECTION ---
api_key = os.getenv("OPENAI_API_KEY")
print(f"DEBUG: Key found? {api_key is not None}")
if api_key:
    # Print first 10 chars to verify it's the right key (should start with sk-or-v1)
    print(f"DEBUG: Key starts with: {api_key[:10]}...")
else:
    print("DEBUG: NO KEY FOUND! Check .env file.")
# ---------------------

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

def call_gpt_model(messages: list, tools: list = None) -> any:
    """
    Sends messages to the API. 
    - If tools are provided, it passes them to the model.
    - Returns the full message object (not just text).
    """
    try:
        extra_headers = {
            "HTTP-Referer": "http://localhost:8000", 
            "X-Title": "AutoAgent_Hub",
        }

        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto", 
            extra_headers=extra_headers
        )

        return completion.choices[0].message 

    except Exception as e:
        print(f"API Error: {e}")
        return None