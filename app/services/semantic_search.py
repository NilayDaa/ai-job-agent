from app.repositories.jobs_repository import get_all_jobs
from app.services.embeddings import create_embedding
from app.services.vector_store import VectorStore
import json

from app.services.cache import cache

class SemanticSearchService:
    def __init__(self):
        self.vector_store = VectorStore()

        # Try loading an existing index
        if not self.vector_store.load():
            print("No existing vector index found. Building a new one...")

            rows = get_all_jobs()

            jobs = []

            for row in rows:
                jobs.append({
                    "id": row[0],
                    "title": row[1],
                    "company": row[2],
                    "location": row[3],
                    "link": row[4],
                })

            self.vector_store.build_index(jobs)
            self.vector_store.save()

            print(f"Indexed {len(jobs)} jobs.")

    def search(self, query: str, k: int = 10):

        cache_key = f"search:{query}:{k}"

        cached = cache.get(cache_key)

        if cached:
            print("Cache HIT")
            return json.loads(cached)

        print("Cache MISS")

        query_embedding = create_embedding(query)

        results = self.vector_store.search(query_embedding, k)

        cache.setex(
            cache_key,
            3600,
            json.dumps(results)
        )

        return results

semantic_search = SemanticSearchService()