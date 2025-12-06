import dramatiq
from dramatiq.brokers.redis import RedisBroker
from dramatiq.results import Results
from dramatiq.results.backends import RedisBackend
from common.config import settings

result_backend = RedisBackend(
    url=settings.REDIS_DSN
)

dramatiq_broker = RedisBroker(
    url=settings.REDIS_DSN,
    middleware=[
        Results(backend=result_backend, result_ttl=3600000),
        dramatiq.middleware.Retries(max_retries=3)
    ]
)

dramatiq.set_broker(dramatiq_broker)