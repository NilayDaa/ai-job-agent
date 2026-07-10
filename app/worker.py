import os

from redis import Redis
from rq import Worker, Queue


def get_redis_connection():

    redis_url = os.getenv("REDIS_URL")

    if redis_url:
        return Redis.from_url(
            redis_url
        )

    return Redis(
        host=os.getenv(
            "REDIS_HOST",
            "localhost"
        ),
        port=int(
            os.getenv(
                "REDIS_PORT",
                6379
            )
        ),
        password=os.getenv(
            "REDIS_PASSWORD"
        )
    )


redis_conn = get_redis_connection()


queues = [
    Queue(
        "scraper",
        connection=redis_conn
    )
]


if __name__ == "__main__":

    print(
        "Worker started..."
    )

    worker = Worker(
        queues,
        connection=redis_conn
    )

    worker.work()