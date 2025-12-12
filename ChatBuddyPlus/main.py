from fastapi import FastAPI
from ChatBuddyPlus.api.routes import router as api_router

app = FastAPI(
    title="ChatBuddy+ Agent Lobe",
    version="v1.0",
    description="Personal AI chat assistant with advanced memory capabilities."
)

app.include_router(api_router, prefix="/api/v1/chatbuddy")

@app.get("/")
async def root():
    return {"message": "ChatBuddy+ API is running."}