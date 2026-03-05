from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import DocumentMeta, DocumentListResponse

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document (PDF/DOCX/TXT), parse, chunk, embed, and store."""
    # TODO: Phase 3 implementation
    pass


@router.get("/list", response_model=DocumentListResponse)
async def list_documents():
    """List all documents for the authenticated user."""
    # TODO: Phase 3 implementation
    pass


@router.delete("/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document from ChromaDB, Supabase, and Storage."""
    # TODO: Phase 3 implementation
    pass
