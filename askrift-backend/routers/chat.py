from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from models.schemas import ChatQuery
from dependencies import get_current_user
from services.embedder import EmbeddingService
from services.vectorstore import VectorStoreService
from services.llm import LLMService
from config import get_settings

router = APIRouter()
settings = get_settings()

embedder = EmbeddingService()
vectorstore = VectorStoreService(persist_path=settings.CHROMA_PERSIST_PATH)
llm_service = LLMService(api_key=settings.GROQ_API_KEY)


@router.post("/query")
async def query_documents(query: ChatQuery, current_user = Depends(get_current_user)):
    """
    RAG query: embed question → retrieve chunks → LLM → stream response via SSE.
    Returns Server-Sent Events stream.
    """
    if not query.question.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    if not settings.GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="LLM API key (GROQ_API_KEY) not configured")

    # 1. Embed query
    try:
        query_emb = embedder.embed_query(query.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate query embedding: {str(e)}")

    # 2. Retrieve relevant chunks
    try:
        chunks = vectorstore.query(
            user_id=current_user.id,
            query_embedding=query_emb,
            top_k=5,
            doc_ids=query.active_doc_ids if query.active_doc_ids else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve contexts: {str(e)}")

    # 3. Stream Response generator for SSE
    async def sse_generator():
        try:
            async for chunk in llm_service.stream_response(
                question=query.question,
                context_chunks=chunks,
                conversation_history=query.conversation_history
            ):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            # Yield error event
            import json
            yield f"data: {json.dumps({'type': 'error', 'content': str(e)})}\n\n"

    return StreamingResponse(sse_generator(), media_type="text/event-stream")
