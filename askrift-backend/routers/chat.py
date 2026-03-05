from fastapi import APIRouter
from models.schemas import ChatQuery

router = APIRouter()


@router.post("/query")
async def query_documents(query: ChatQuery):
    """
    RAG query: embed question → retrieve chunks → LLM → stream response via SSE.
    Returns Server-Sent Events stream.
    """
    # TODO: Phase 4 implementation
    pass
