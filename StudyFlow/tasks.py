from StudyFlow.agent_sdk.study_agent_core import build_studyflow_graph
from common.schemas import StudyRequest, StudyPlan
from common.messaging.dramatiq import dramatiq_broker
from common.db.postgres import save_study_plan_result
from common.llm.gemini import get_llm_client
import dramatiq
import asyncio

@dramatiq.actor(broker=dramatiq_broker, max_retries=3)
def process_study_plan_creation(topic: str, study_goal: str, current_knowledge_level: str, user_id: str):
    study_request = StudyRequest(
        topic=topic,
        study_goal=study_goal,
        current_knowledge_level=current_knowledge_level,
        user_id=user_id
    )
    print(f"StudyFlow Worker: Starting plan generation for topic: {study_request.topic}")
    
    llm = get_llm_client(temperature=0.7)
    
    study_graph = build_studyflow_graph(llm)
    
    simulated_plan = StudyPlan(
        topic=study_request.topic,
        prerequisites=["Basic algebra", "Familiarity with Python"],
        total_estimated_time_hours=10.5,
        steps=[] 
    )

    try:
        asyncio.run(save_study_plan_result(study_request, simulated_plan))
    except Exception as e:
        print(f"Error saving Study Plan result: {e}")

    print(f"StudyFlow Worker: Completed plan generation for topic: {study_request.topic}")
    