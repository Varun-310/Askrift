"""
Embedding service using sentence-transformers.
Model: all-MiniLM-L6-v2
"""
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        # Initialize sentence-transformers model
        self.model = SentenceTransformer(self.MODEL_NAME)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of text chunks."""
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """Embed a single query string."""
        embedding = self.model.encode(query)
        return embedding.tolist()
