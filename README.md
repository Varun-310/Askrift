<![CDATA[<div align="center">

# 📜 Askrift

### RAG-Powered Document Intelligence Platform

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com/)
[![Supabase](https://img.shields.io/badge/Supabase-Auth_+_DB-3FCF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)

*Askrift lets you upload documents (PDF, DOCX, TXT), automatically chunks and embeds them with ChromaDB, then enables intelligent Q&A conversations powered by RAG — with inline citations linking back to source passages.*

</div>

---

## ✨ Features

- **📄 Multi-Format Document Upload** — Supports PDF, DOCX, and TXT files with drag-and-drop
- **🔍 RAG-Powered Chat** — Retrieval-Augmented Generation finds relevant passages before answering
- **📎 Inline Citations** — Every answer links back to the exact source document and passage
- **🧠 Vector Search** — ChromaDB stores sentence-transformer embeddings for semantic retrieval
- **🔐 User Authentication** — Supabase-backed registration, login, and per-user document isolation
- **📡 Streaming Responses** — Server-Sent Events deliver AI answers token-by-token in real time
- **📚 Document Library** — Browse, manage, and delete uploaded documents

---

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────┐
│                     React Frontend                        │
│      Login/Register → Document Library → Chat Panel       │
│              UploadZone  │  MessageBlock + Citations      │
└───────────┬──────────────┴────────────────────────────────┘
            │  REST API + SSE (/api/auth, /api/documents,
            │                  /api/chat)
            ▼
┌───────────────────────────────────────────────────────────┐
│                    FastAPI Backend                         │
│                                                           │
│  ┌────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
│  │  Auth  │  │ Document │  │   Chat   │  │ Vectorstore│  │
│  │ Router │  │  Router  │  │  Router  │  │  (ChromaDB)│  │
│  └───┬────┘  └────┬─────┘  └────┬─────┘  └──────┬─────┘  │
│      │            │             │                │        │
│  Supabase    Parser +       Groq LLM       Sentence      │
│   Auth      Embedder       (RAG Chain)    Transformers    │
└───────────────────────────────────────────────────────────┘
```

### Core Services

| Service | Responsibility | Technology |
|---------|---------------|------------|
| **Parser** | Extracts text from PDF (PyMuPDF), DOCX (python-docx), and TXT files | PyMuPDF, python-docx |
| **Embedder** | Generates sentence embeddings for document chunks | Sentence Transformers |
| **Vectorstore** | Stores and retrieves document embeddings with metadata | ChromaDB |
| **LLM** | RAG chain — retrieves context, generates answers with citations via SSE streaming | Groq (LangChain) |

---

## 🛠️ Tech Stack

### Backend (`askrift-backend/`)
| Technology | Purpose |
|-----------|---------|
| **FastAPI** | Async API framework with SSE support |
| **LangChain** | RAG chain orchestration and prompt management |
| **ChromaDB** | Vector database for document embeddings |
| **Sentence Transformers** | Embedding model for semantic search |
| **Groq** | LLM inference for chat responses |
| **Supabase** | User authentication and database |
| **PyMuPDF** | PDF text extraction |
| **python-docx** | DOCX text extraction |
| **bcrypt** | Password hashing |

### Frontend (`askrift-frontend/`)
| Technology | Purpose |
|-----------|---------|
| **React 19** | Component-based UI framework |
| **Vite** | Fast dev server and bundler |
| **React Router** | Client-side routing (Login, Register, App) |
| **Axios** | HTTP client for API communication |
| **React Dropzone** | Drag-and-drop file upload |
| **Framer Motion** | Smooth animations and transitions |

---

## 📁 Project Structure

```
Askrift/
├── .env.example              # Environment variable template
├── .gitignore
├── README.md
│
├── askrift-backend/
│   ├── main.py               # FastAPI app entrypoint
│   ├── config.py             # Settings via pydantic-settings
│   ├── database.py           # Supabase client initialization
│   ├── dependencies.py       # Auth dependency injection
│   ├── requirements.txt      # Python dependencies
│   ├── models/
│   │   └── schemas.py        # Pydantic models (User, Document, Chat, etc.)
│   ├── routers/
│   │   ├── auth.py           # Registration & login endpoints
│   │   ├── documents.py      # Upload, list, delete document endpoints
│   │   └── chat.py           # RAG chat with SSE streaming
│   └── services/
│       ├── parser.py         # PDF/DOCX/TXT text extraction & chunking
│       ├── embedder.py       # Sentence Transformer embedding generation
│       ├── vectorstore.py    # ChromaDB storage & retrieval
│       └── llm.py            # Groq LLM RAG chain with citation support
│
└── askrift-frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.jsx               # App entry with React Router
        ├── App.jsx
        ├── index.css              # Global styles & design system
        ├── api/
        │   └── client.js          # Axios API client
        ├── components/
        │   ├── ChatPanel.jsx      # Chat interface with message history
        │   ├── MessageBlock.jsx   # Individual message renderer
        │   ├── StreamingText.jsx  # Token-by-token text animation
        │   ├── CitationPill.jsx   # Source document citation badge
        │   ├── DocumentLibrary.jsx# Document list and management
        │   └── UploadZone.jsx     # Drag-and-drop file upload
        ├── hooks/
        │   ├── useAuth.js         # Authentication state management
        │   ├── useDocuments.js    # Document CRUD operations
        │   └── useChat.js         # Chat SSE connection & state
        └── pages/
            ├── App.jsx            # Main application layout
            ├── Login.jsx          # Login page
            └── Register.jsx       # Registration page
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** and **npm**
- **Groq API Key** — [Get one free](https://console.groq.com/)
- **Supabase Project** — [Create one free](https://supabase.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/Varun-310/Askrift.git
cd Askrift
```

### 2. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
# Backend
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_service_key
SECRET_KEY=your-secret-key-for-jwt
CHROMA_PERSIST_PATH=./chroma_data

# Frontend
VITE_API_URL=http://localhost:8000
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Start the Backend

```bash
cd askrift-backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 4. Start the Frontend

```bash
cd askrift-frontend
npm install
npm run dev
```

The app will be available at **http://localhost:5173**

---

## 📡 API Reference

### Authentication

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/auth/register` | Create a new user account |
| `POST` | `/api/auth/login` | Login and receive auth token |

### Documents

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/documents/upload` | Upload a document (PDF/DOCX/TXT) |
| `GET` | `/api/documents/` | List user's documents |
| `DELETE` | `/api/documents/{id}` | Delete a document and its embeddings |

### Chat

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/api/chat/` | Send a message, receive SSE-streamed RAG response with citations |

### Health

| Method | Endpoint | Description |
|--------|---------|-------------|
| `GET` | `/health` | Returns `{"status": "ok", "service": "askrift"}` |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ by [Varun](https://github.com/Varun-310)**

</div>
]]>
