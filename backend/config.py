import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()


class Config:
    """Application configuration."""
    
    # Base directory of the application
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max upload
    
    # Server configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'ekp-secret-key-dev')
    HOST = os.environ.get('HOST', '0.0.0.0')
    # Render provides PORT env variable
    PORT = int(os.environ.get('PORT', 5000))
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # CORS configuration - allow frontend URL in production
    _cors_origins = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173')
    CORS_ORIGINS = [origin.strip() for origin in _cors_origins.split(',')]
    
    # ChromaDB configuration
    CHROMA_PERSIST_DIR = os.path.join(BASE_DIR, 'chroma_db')
    COLLECTION_NAME = 'enterprise_knowledge_platform'
    
    # Text processing configuration
    CHUNK_SIZE = int(os.environ.get('CHUNK_SIZE', '1000'))
    CHUNK_OVERLAP = int(os.environ.get('CHUNK_OVERLAP', '200'))
    
    # Embedding model
    EMBEDDING_MODEL = 'all-MiniLM-L6-v2'
    
    # Ollama configuration
    OLLAMA_BASE_URL = os.environ.get('OLLAMA_BASE_URL', 'http://localhost:11434')
    OLLAMA_MODEL = os.environ.get('OLLAMA_MODEL', 'gemma3:latest')
    OLLAMA_TIMEOUT = int(os.environ.get('OLLAMA_TIMEOUT', '60'))
    OLLAMA_NUM_PREDICT = int(os.environ.get('OLLAMA_NUM_PREDICT', '512'))
    OLLAMA_TEMPERATURE = float(os.environ.get('OLLAMA_TEMPERATURE', '0.1'))
    OLLAMA_TOP_P = float(os.environ.get('OLLAMA_TOP_P', '0.9'))
    
    # Chat configuration
    MAX_HISTORY_LENGTH = int(os.environ.get('MAX_HISTORY_LENGTH', '10'))
    RAG_N_RESULTS = int(os.environ.get('RAG_N_RESULTS', '5'))

