import dramatiq
import os
import asyncio
from typing import Optional
from dramatiq.brokers.redis import RedisBroker
from common.db.postgres import save_analysis_result
from common.schemas import AgentState
from common.agent_sdk.agent_core import build_insightmate_graph

redis_host = os.environ.get("REDIS_HOST", "localhost")
redis_port = int(os.environ.get("REDIS_PORT", 6379))

broker = RedisBroker(host=redis_host, port=redis_port)
dramatiq.set_broker(broker)

INSIGHTMATE_GRAPH = build_insightmate_graph()


@dramatiq.actor
def process_transcript_analysis(title: str, transcript_text: str, user_id: str):
    
    initial_state = AgentState(
        transcript=transcript_text,
        analysis_result=None,
        next_step="summarize"
    )
    
    final_state = asyncio.run(_run_graph_agent(initial_state))

    if final_state and final_state.analysis_result:
        try:
            asyncio.run(save_analysis_result(
                title=title,
                transcript=transcript_text,
                analysis=final_state.analysis_result,
                user_id=user_id
            ))
        except Exception as e:
            pass
            
    else:
        pass

    return f"Analysis complete for session {title}"

async def _run_graph_agent(initial_state: AgentState) -> Optional[AgentState]:
    
    graph_input = initial_state.model_dump()
    
    try:
        result = await INSIGHTMATE_GRAPH.ainvoke(graph_input)
        
        return AgentState(**result)
    except Exception as e:
        return None