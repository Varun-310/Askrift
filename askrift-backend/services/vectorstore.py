"""
ChromaDB vector store operations.
Per-user collections: user_{user_id}
"""
import chromadb

class VectorStoreService:
    def __init__(self, persist_path: str = "./chroma_data"):
        self.persist_path = persist_path
        self.client = chromadb.PersistentClient(path=self.persist_path)

    def _get_collection(self, user_id: str):
        collection_name = f"user_{user_id}"
        # get or create collection
        return self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_chunks(self, user_id: str, doc_id: str, chunks: list[dict], embeddings: list[list[float]]):
        """Add document chunks to user's ChromaDB collection."""
        collection = self._get_collection(user_id)
        
        ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
        metadatas = []
        documents = []
        
        for idx, chunk in enumerate(chunks):
            documents.append(chunk["text"])
            metadatas.append({
                "doc_id": doc_id,
                "doc_name": chunk["doc_name"],
                "page_number": chunk["page_number"],
                "chunk_index": chunk["chunk_index"]
            })
            
        collection.add(
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas,
            documents=documents
        )

    def query(self, user_id: str, query_embedding: list[float], top_k: int = 5, doc_ids: list[str] = None) -> list[dict]:
        """Query top-k relevant chunks from user's collection."""
        collection = self._get_collection(user_id)
        
        where = {}
        if doc_ids and len(doc_ids) > 0:
            if len(doc_ids) == 1:
                where = {"doc_id": doc_ids[0]}
            else:
                where = {"doc_id": {"$in": doc_ids}}
                
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where if where else None,
            include=["documents", "metadatas", "distances"]
        )
        
        out = []
        if not results["ids"] or not results["ids"][0]:
            return out
            
        for i in range(len(results["ids"][0])):
            meta = results["metadatas"][0][i]
            dist = results["distances"][0][i]
            # Convert cosine distance to a relevance score (0 to 1)
            score = 1.0 - (dist / 2.0) if dist <= 2.0 else 0.0
            
            out.append({
                "text": results["documents"][0][i],
                "doc_id": meta["doc_id"],
                "doc_name": meta["doc_name"],
                "page_number": meta["page_number"],
                "chunk_index": meta["chunk_index"],
                "relevance_score": score
            })
            
        return out

    def delete_document(self, user_id: str, doc_id: str):
        """Delete all chunks for a document from user's collection."""
        collection = self._get_collection(user_id)
        collection.delete(where={"doc_id": doc_id})
