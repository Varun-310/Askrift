from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# ── Auth ──────────────────────────────────────────────
class UserRegister(BaseModel):
    email: str
    password: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    token: str


# ── Documents ─────────────────────────────────────────
class DocumentMeta(BaseModel):
    id: str
    user_id: str
    name: str
    file_type: str
    size_bytes: int
    page_count: int
    chunk_count: int
    uploaded_at: str


class DocumentListResponse(BaseModel):
    documents: list[DocumentMeta]


# ── Chat ──────────────────────────────────────────────
class ChatQuery(BaseModel):
    question: str
    active_doc_ids: list[str] = []
    conversation_history: list[dict] = []


class Citation(BaseModel):
    doc_name: str
    doc_id: str
    page_number: int
    chunk_index: int
    relevance_score: float


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]
