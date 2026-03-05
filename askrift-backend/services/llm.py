"""
Groq LLM service.
Model: llama-3.1-8b-instant
Handles context assembly, streaming, and citation extraction.
"""


SYSTEM_PROMPT = """You are Askrift, a precise document intelligence assistant.
Answer the user's question using ONLY the provided document context.
Be concise and direct. If the context doesn't contain the answer, say so clearly.
Do not invent information. Do not reference external knowledge.
Context: {chunks}"""


class LLMService:
    MODEL = "llama-3.1-8b-instant"

    def __init__(self, api_key: str):
        # TODO: Phase 4 - initialize Groq client
        self.api_key = api_key
        self.client = None

    async def stream_response(self, question: str, context_chunks: list[dict], conversation_history: list[dict]):
        """
        Stream LLM response token by token.
        Yields text tokens, then a final citation metadata event.
        """
        # TODO: Phase 4 implementation
        pass
