from app.repositories.jobs_repository import get_all_jobs
from app.services.embeddings import create_embedding
from app.services.vector_store import VectorStore


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
        query_embedding = create_embedding(query)
        return self.vector_store.search(query_embedding, k)


semantic_search = SemanticSearchService()