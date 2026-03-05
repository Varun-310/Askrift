"""
Embedding service using sentence-transformers.
Model: all-MiniLM-L6-v2
"""


class EmbeddingService:
    MODEL_NAME = "all-MiniLM-L6-v2"

    def __init__(self):
        # TODO: Phase 3 - initialize sentence-transformers model
        self.model = None

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed a list of text chunks."""
        # TODO: Phase 3 implementation
        pass

    def embed_query(self, query: str) -> list[float]:
        """Embed a single query string."""
        # TODO: Phase 3 implementation
        pass
