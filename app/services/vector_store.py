import faiss
import numpy as np
import pickle
from pathlib import Path

from app.services.embeddings import create_job_embedding

INDEX_DIR = Path("data")
INDEX_FILE = INDEX_DIR / "jobs.index"
MAPPING_FILE = INDEX_DIR / "job_mapping.pkl"


class VectorStore:
    def __init__(self):
        self.dimension = 384
        self.index = faiss.IndexFlatIP(self.dimension)
        self.job_mapping = []

    def build_index(self, jobs: list):
        """
        Build a new FAISS index from job data.
        """

        self.index.reset()
        self.job_mapping = []

        vectors = []

        for job in jobs:
            embedding = create_job_embedding(job)

            vectors.append(embedding.astype("float32"))
            self.job_mapping.append(job)

        if vectors:
            matrix = np.vstack(vectors)
            self.index.add(matrix)

    def search(self, query_embedding, k=10):
        """
        Return the k most similar jobs.
        """

        query = np.array([query_embedding]).astype("float32")

        scores, indices = self.index.search(query, k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            job = self.job_mapping[idx].copy()
            job["score"] = float(score)

            results.append(job)

        return results

    def save(self):
        INDEX_DIR.mkdir(exist_ok=True)

        print("Saving index to:", INDEX_FILE.resolve())
        print("Saving mapping to:", MAPPING_FILE.resolve())

        faiss.write_index(self.index, str(INDEX_FILE))

        with open(MAPPING_FILE, "wb") as f:
            pickle.dump(self.job_mapping, f)

        print("Saved", len(self.job_mapping), "jobs")

    def load(self):
        """
        Load index and mapping.
        """

        if not INDEX_FILE.exists():
            return False

        self.index = faiss.read_index(str(INDEX_FILE))

        with open(MAPPING_FILE, "rb") as f:
            self.job_mapping = pickle.load(f)

        return True
    
    def rebuild(self, jobs: list):
        print("========== REBUILD ==========")
        print("Jobs received:", len(jobs))

        if jobs:
            print("First job:", jobs[0])

        self.build_index(jobs)

        print("Vectors in index:", self.index.ntotal)

        self.save()

        print("========== DONE ==========")