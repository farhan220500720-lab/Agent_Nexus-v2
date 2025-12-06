from uuid import uuid4
from typing import Optional
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.responses import JSONResponse
from common.schemas import StudyRequest
from StudyFlow.tasks import process_study_plan_creation

app = FastAPI(title="StudyFlow", version="0.1")

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/plan", status_code=status.HTTP_202_ACCEPTED)
async def submit_study_request(payload: StudyRequest, idempotency_key: Optional[str] = Header(None)):
    if not payload.topic or not payload.study_goal:
        raise HTTPException(status_code=400, detail="Topic and study goal are required")
        
    task_id = idempotency_key or str(uuid4())
    
    process_study_plan_creation.send(
        payload.topic, 
        payload.study_goal, 
        payload.current_knowledge_level, 
        payload.user_id
    )
        
    headers = {"Location": f"/tasks/{task_id}"}
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"task_id": task_id, "message": "StudyFlow request accepted. Processing plan."}, headers=headers)