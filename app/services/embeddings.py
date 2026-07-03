from sentence_transformers import SentenceTransformer
import numpy as np

# Load the model only once when the application starts
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def create_embedding(text: str) -> np.ndarray:
    """
    Generate an embedding for a piece of text.

    Args:
        text: Input text

    Returns:
        NumPy array containing the embedding vector
    """
    if not text:
        text = ""

    embedding = model.encode(
        text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding


def create_job_text(job: dict) -> str:
    """
    Combine job fields into a single text for embedding.
    """

    return f"""
Title: {job.get('title', '')}
Company: {job.get('company', '')}
Location: {job.get('location', '')}
""".strip()


def create_job_embedding(job: dict) -> np.ndarray:
    """
    Generate an embedding for a job dictionary.
    """

    text = create_job_text(job)

    return create_embedding(text)