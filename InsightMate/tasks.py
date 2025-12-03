import dramatiq
from common.tasks.broker import redis_broker
from common.tasks import SummaryTaskPayload
import time
import os
import dramatiq

dramatiq.set_broker(redis_broker)

@dramatiq.actor
def generate_summary(meeting_id: int, transcript: str, target_length: int):
    print(f"[{os.getpid()}] Starting summary generation for meeting ID: {meeting_id}...")
    
    time.sleep(5) 
    
    simulated_summary = f"Summary for meeting {meeting_id} (Length {target_length}): This meeting was successfully summarized after 5 seconds of intensive processing. The core topics were Async Queues (Redis/Dramatiq) and the completion of Phase 2 data architecture."
    
    print(f"[{os.getpid()}] Summary generated successfully.")
    
    return simulated_summary