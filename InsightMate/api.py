from uuid import uuid4
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import JSONResponse
from common.schemas import TranscriptRequest
from InsightMate.tasks import process_transcript_analysis

app = FastAPI(title="InsightMate", version="0.1")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/analyze", status_code=status.HTTP_202_ACCEPTED)
async def submit_analysis(payload: TranscriptRequest, idempotency_key: Optional[str] = Header(None)):
    if not payload.transcript or not payload.transcript.strip():
        raise HTTPException(status_code=400, detail="Transcript is required")
        
    task_id = idempotency_key or str(uuid4())
    task_data = payload.model_dump()
    
    try:
        
        process_transcript_analysis.send(
            title=task_data['title'], 
            transcript=task_data['transcript'], 
            user_id=task_data['user_id']
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to enqueue transcript analysis task.")
        
    headers = {"Location": f"/tasks/{task_id}"}
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"task_id": task_id}, headers=headers)