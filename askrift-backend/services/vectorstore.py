"""
ChromaDB vector store operations.
Per-user collections: user_{user_id}
"""


class VectorStoreService:
    def __init__(self, persist_path: str = "./chroma_data"):
        # TODO: Phase 3 - initialize ChromaDB client
        self.persist_path = persist_path
        self.client = None

    def add_chunks(self, user_id: str, doc_id: str, chunks: list[dict], embeddings: list[list[float]]):
        """Add document chunks to user's ChromaDB collection."""
        # TODO: Phase 3 implementation
        pass

    def query(self, user_id: str, query_embedding: list[float], top_k: int = 5, doc_ids: list[str] = None) -> list[dict]:
        """Query top-k relevant chunks from user's collection."""
        # TODO: Phase 4 implementation
        pass

    def delete_document(self, user_id: str, doc_id: str):
        """Delete all chunks for a document from user's collection."""
        # TODO: Phase 3 implementation
        pass
