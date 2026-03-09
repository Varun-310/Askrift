import uuid
from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from models.schemas import DocumentMeta, DocumentListResponse
from dependencies import get_current_user
from services.parser import DocumentParser
from services.embedder import EmbeddingService
from services.vectorstore import VectorStoreService
from config import get_settings
from database import supabase

router = APIRouter()
settings = get_settings()

embedder = EmbeddingService()
vectorstore = VectorStoreService(persist_path=settings.CHROMA_PERSIST_PATH)

@router.post("/upload", response_model=DocumentMeta)
async def upload_document(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    """Upload a document (PDF/DOCX/TXT), parse, chunk, embed, and store."""
    valid_extensions = ["pdf", "docx", "txt", "md"]
    ext = file.filename.lower().split('.')[-1]
    if ext not in valid_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")
        
    file_bytes = await file.read()
    size_bytes = len(file_bytes)
    if size_bytes > 20 * 1024 * 1024:  # 20MB limit
        raise HTTPException(status_code=400, detail="File too large (max 20MB)")
        
    doc_id = str(uuid.uuid4())
    
    # 1. Parse and Chunk
    try:
        chunks = DocumentParser.parse(file_bytes, file.filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse document: {str(e)}")
        
    if not chunks:
        raise HTTPException(status_code=400, detail="Document contains no extractable text")
        
    # 2. Embed
    try:
        texts = [c["text"] for c in chunks]
        embeddings = embedder.embed_texts(texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate embeddings: {str(e)}")
        
    # 3. Store in Vector DB
    try:
        vectorstore.add_chunks(
            user_id=current_user.id,
            doc_id=doc_id,
            chunks=chunks,
            embeddings=embeddings
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store vectors: {str(e)}")
        
    # 4. Store Metadata in Supabase
    page_count = max([c["page_number"] for c in chunks]) if chunks else 1
    chunk_count = len(chunks)
    uploaded_at = datetime.utcnow().isoformat()
    
    doc_meta = {
        "id": doc_id,
        "user_id": current_user.id,
        "name": file.filename,
        "file_type": ext,
        "size_bytes": size_bytes,
        "page_count": page_count,
        "chunk_count": chunk_count,
        "uploaded_at": uploaded_at
    }
    
    try:
        supabase.table("documents").insert(doc_meta).execute()
    except Exception as e:
        # Rollback vectorstore if DB insert fails
        vectorstore.delete_document(current_user.id, doc_id)
        raise HTTPException(status_code=500, detail=f"Failed to save document metadata: {str(e)}")
        
    return DocumentMeta(**doc_meta)


@router.get("/list", response_model=DocumentListResponse)
async def list_documents(current_user = Depends(get_current_user)):
    """List all documents for the authenticated user."""
    try:
        res = supabase.table("documents").select("*").eq("user_id", current_user.id).order('uploaded_at', desc=True).execute()
        return DocumentListResponse(documents=[DocumentMeta(**d) for d in res.data])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{doc_id}")
async def delete_document(doc_id: str, current_user = Depends(get_current_user)):
    """Delete a document from ChromaDB and Supabase metadata."""
    # Delete metadata from Supabase
    try:
        supabase.table("documents").delete().eq("id", doc_id).eq("user_id", current_user.id).execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete metadata: {str(e)}")
        
    # Delete from ChromaDB
    try:
        vectorstore.delete_document(current_user.id, doc_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete vectors: {str(e)}")
        
    return {"status": "success", "doc_id": doc_id}
