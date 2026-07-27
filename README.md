# Enterprise Knowledge Intelligence Platform

A modern, production-ready enterprise knowledge management platform built with React and Flask. Features a complete RAG (Retrieval-Augmented Generation) pipeline powered by Ollama and Llama 3.2 for intelligent document Q&A.

## Architecture

```
enterprise-knowledge-platform/
├── frontend/          # React.js + Vite frontend
├── backend/           # Flask REST API backend
└── README.md
```

## Features

### Part 1 - Foundation
- ✅ Responsive SaaS-style UI
- ✅ React Router navigation (6 pages)
- ✅ PDF upload with drag-and-drop
- ✅ Flask upload API
- ✅ Frontend-backend integration
- ✅ Form validation (Contact page)
- ✅ Chat UI (interface only)
- ✅ Modular component architecture
- ✅ Professional navbar & footer
- ✅ Mobile-responsive design

### Part 2 - Document Processing & Search
- ✅ PDF text extraction (PyMuPDF)
- ✅ Text chunking (LangChain RecursiveCharacterTextSplitter)
- ✅ Embeddings generation (Sentence Transformers - all-MiniLM-L6-v2)
- ✅ Vector storage (FAISS with persistent storage)
- ✅ Semantic search with cosine similarity
- ✅ Metadata filtering (by filename)
- ✅ Chunk-level source tracking

### Part 3 - RAG Chat (Current)
- ✅ Ollama integration with Llama 3.2
- ✅ Complete RAG pipeline:
  - Question → Embedding → Search → Retrieve → Prompt → LLM → Answer
- ✅ Context-grounded prompt engineering (anti-hallucination)
- ✅ Session-based multi-turn chat history
- ✅ Source references with document filename and chunk number
- ✅ Professional chat interface
- ✅ Typing indicator
- ✅ Loading states
- ✅ Clear Chat button
- ✅ Auto-scroll
- ✅ Error handling (Ollama down, model missing, empty DB)
- ✅ System status detection (online/offline)
- ✅ Environment variable configuration
- ✅ Comprehensive logging

## Tech Stack

### Frontend
- React.js
- Vite
- React Router DOM
- CSS3 (with custom properties)

### Backend
- Python
- Flask
- Flask-CORS
- Sentence Transformers (all-MiniLM-L6-v2)
- FAISS (vector similarity search)
- PyMuPDF (PDF processing)
- LangChain Text Splitters
- Ollama (local LLM)
- Llama 3.2 (language model)

## Folder Structure

```
enterprise-knowledge-platform/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/        # Button, Card, Loader, Alert
│   │   │   ├── layout/        # Navbar, Footer, PageContainer
│   │   │   └── upload/        # UploadBox, UploadProgress, FilePreview
│   │   ├── pages/             # Home, About, Features, Upload, Chat, Contact, NotFound
│   │   ├── services/          # api.js, uploadService.js, chatService.js
│   │   ├── styles/            # Component-specific CSS files
│   │   ├── App.jsx            # Main app with routing
│   │   └── main.jsx           # Entry point
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── backend/
│   ├── routes/
│   │   ├── upload.py          # PDF upload endpoint
│   │   ├── process.py         # Document processing pipeline
│   │   ├── search.py          # Semantic search API
│   │   └── chat.py            # RAG chat API (Part 3)
│   ├── services/
│   │   ├── pdf_processor.py   # PDF text extraction
│   │   ├── text_splitter.py   # Text chunking
│   │   ├── embeddings.py      # Embedding generation (singleton)
│   │   ├── vector_store.py    # FAISS vector store (singleton)
│   │   ├── search_service.py  # Search orchestration
│   │   ├── llm_service.py     # Ollama LLM service (Part 3)
│   │   ├── prompt_service.py  # Prompt engineering (Part 3)
│   │   └── rag_service.py     # RAG pipeline orchestration (Part 3)
│   ├── config.py              # Application configuration
│   ├── app.py                 # Flask application factory
│   ├── requirements.txt
│   └── chroma_db/             # Persistent vector store directory
└── README.md
```

## Installation Guide

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

### Backend Setup

```bash
cd backend
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### Frontend Setup

```bash
cd frontend
npm install
```

### Ollama Installation

1. **Download and install Ollama** from [https://ollama.com/download](https://ollama.com/download)

2. **Start Ollama** (it runs as a background service)

3. **Pull the Llama 3.2 model**:
```bash
ollama pull llama3.2
```

4. **Verify Ollama is running**:
```bash
ollama list
```
You should see `llama3.2` in the list of available models.

### Environment Variables

Create a `.env` file in the `backend/` directory (optional - all variables have defaults):

```env
# Server Configuration
SECRET_KEY=your-secret-key-here
HOST=0.0.0.0
PORT=5000
DEBUG=True

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
OLLAMA_TIMEOUT=60
OLLAMA_NUM_PREDICT=512
OLLAMA_TEMPERATURE=0.1
OLLAMA_TOP_P=0.9

# RAG Configuration
MAX_HISTORY_LENGTH=10
RAG_N_RESULTS=5

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

## Running the Project

### 1. Start Ollama

Ensure Ollama is running in the background with Llama 3.2 loaded.

### 2. Start the Backend

```bash
cd backend
python app.py
```

The backend will start on `http://localhost:5000`.

### 3. Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:3000`.

## API Endpoints

### Health Check
```http
GET /api/health
```

### Upload PDF
```http
POST /api/upload
Content-Type: multipart/form-data
Body: file=<pdf_file>
```

### Process Document
```http
POST /api/process
Content-Type: application/json
Body: {"filename": "document.pdf"}
```

### Semantic Search
```http
POST /api/search
Content-Type: application/json
Body: {"query": "What is the refund policy?", "n_results": 5}
```

### Chat (RAG)
```http
POST /api/chat
Content-Type: application/json
Body: {"question": "What is the refund policy?", "session_id": "optional-session-id"}
```

### Clear Chat History
```http
POST /api/chat/clear
Content-Type: application/json
Body: {"session_id": "your-session-id"}
```

### Get Chat History
```http
GET /api/chat/history/<session_id>
```

### Get Chat Status
```http
GET /api/chat/status
```

### Create New Session
```http
POST /api/chat/new-session
```

### Index Stats
```http
GET /api/search/index-stats
```

### Processing Status
```http
GET /api/process/status
```

## Testing

### Backend

```bash
cd backend
python test_api.py
```

### Frontend

```bash
cd frontend
npm run build   # Production build (checks for errors)
npm run dev     # Development server
```

## How RAG Works

1. **Upload**: User uploads PDF documents via the Upload page
2. **Process**: Backend extracts text, splits into chunks, generates embeddings, stores in FAISS
3. **Search**: When user asks a question, backend generates a query embedding and searches FAISS for similar chunks
4. **Prompt**: Retrieved chunks are formatted into a context-grounded prompt with anti-hallucination instructions
5. **Generate**: Prompt is sent to Ollama (Llama 3.2) which generates an answer based ONLY on the provided context
6. **Respond**: Answer and source references are returned to the frontend and displayed in the chat interface

## Project Status

### Completed Features
- ✅ PDF Upload and Processing
- ✅ Text Extraction and Chunking
- ✅ Vector Embeddings and Storage
- ✅ Semantic Search
