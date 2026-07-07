from redis import Redis
from rq import Queue

from app.services.cache import REDIS_HOST

redis_conn = Redis(
    host=REDIS_HOST,
    port=6379
)

job_queue = Queue(
    "scraper",
    connection=redis_conn
)