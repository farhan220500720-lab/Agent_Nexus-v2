from dramatiq import Broker
from dramatiq.brokers.redis import RedisBroker
import os
import dramatiq

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_broker = RedisBroker(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB
)

dramatiq.set_broker(redis_broker)