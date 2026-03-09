"""
Groq LLM service.
Model: llama-3.1-8b-instant
Handles context assembly, streaming, and citation extraction.
"""
import json
from groq import AsyncGroq
from models.schemas import Citation

SYSTEM_PROMPT = """You are Askrift, a precise document intelligence assistant.
Answer the user's question using ONLY the provided document context.
Be concise and direct. If the context doesn't contain the answer, say so clearly.
Do not invent information. Do not reference external knowledge.
Context: {chunks}"""


class LLMService:
    MODEL = "llama-3.1-8b-instant"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = AsyncGroq(api_key=self.api_key)

    async def stream_response(self, question: str, context_chunks: list[dict], conversation_history: list[dict]):
        """
        Stream LLM response token by token.
        Yields text tokens, then a final citation metadata event.
        Returns JSON dumped strings to be sent via SSE.
        """
        # Prepare context
        context_str = "\n\n".join([f"--- Chunk {i+1} ---\n{c['text']}" for i, c in enumerate(context_chunks)])
        sys_prompt = SYSTEM_PROMPT.format(chunks=context_str)
        
        messages = [{"role": "system", "content": sys_prompt}]
        
        for msg in conversation_history:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})
            
        messages.append({"role": "user", "content": question})
        
        stream = await self.client.chat.completions.create(
            messages=messages,
            model=self.MODEL,
            temperature=0.0,
            stream=True
        )
        
        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield json.dumps({
                    "type": "text",
                    "content": content
                })
                
        # Yield citations at the end
        citations = []
        for c in context_chunks:
            citations.append(Citation(
                doc_name=c["doc_name"],
                doc_id=c["doc_id"],
                page_number=c["page_number"],
                chunk_index=c["chunk_index"],
                relevance_score=c["relevance_score"]
            ).model_dump())
            
        yield json.dumps({
            "type": "citations",
            "content": citations
        })
