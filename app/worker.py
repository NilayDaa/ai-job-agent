from redis import Redis
from rq import Worker, Queue

from app.services.cache import REDIS_HOST

redis_conn = Redis(
    host=REDIS_HOST,
    port=6379
)

queues = [
    Queue("scraper", connection=redis_conn)
]

if __name__ == "__main__":
    worker = Worker(
        queues,
        connection=redis_conn
    )

    print("Worker started...")

    worker.work()