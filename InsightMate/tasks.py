import dramatiq
from dramatiq.brokers.redis import RedisBroker
from .summary_agent import run_summary_agent

broker = RedisBroker(host="localhost", port=6379)
dramatiq.set_broker(broker)

@dramatiq.actor(queue_name='meetings')
async def summarize_meeting(title: str, transcript: str):
    print(f"--- Processing Task: {title} ---")
    await run_summary_agent(transcript=transcript, title=title)
    print(f"--- Task Complete: {title} ---")
    