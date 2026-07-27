"""
RAG Service - Orchestrates the complete Retrieval-Augmented Generation pipeline.
Connects the vector store search with LLM generation for context-aware answers.
"""

import logging
import uuid
from typing import List, Dict, Optional
from datetime import datetime

from config import Config
from services.vector_store import vector_store
from services.llm_service import llm_service
from services.prompt_service import prompt_service

logger = logging.getLogger(__name__)


class SessionManager:
    """
    Manages chat session histories for multi-turn conversations.
    
    Features:
    - Per-session message history
    - Configurable max history length (FIFO eviction)
    - Thread-safe session isolation
    """
    
    def __init__(self):
        """Initialize the session manager with empty sessions store."""
        self._sessions: Dict[str, List[Dict]] = {}
        self._max_length = Config.MAX_HISTORY_LENGTH
        logger.info(f'Session Manager initialized (max_history={self._max_length})')
    
    def create_session(self) -> str:
        """
        Create a new chat session.
        
        Returns:
            Unique session ID string
        """
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = []
        logger.info(f'Created new chat session: {session_id[:8]}...')
        return session_id
    
    def get_history(self, session_id: str) -> List[Dict]:
        """
        Get the message history for a session.
        
        Args:
            session_id: The session identifier
            
        Returns:
            List of message dicts with 'role' and 'content' keys
        """
        if session_id not in self._sessions:
            logger.warning(f'Session {session_id[:8]}... not found, creating new')
            self._sessions[session_id] = []
        return self._sessions[session_id]
    
    def add_message(self, session_id: str, role: str, content: str):
        """
        Add a message to the session history.
        Automatically trims history to max_length using FIFO.
        
        Args:
            session_id: The session identifier
            role: 'user' or 'assistant'
            content: The message content
        """
        if session_id not in self._sessions:
            self._sessions[session_id] = []
        
        self._sessions[session_id].append({
            'role': role,
            'content': content,
            'timestamp': datetime.utcnow().isoformat(),
        })
        
        # Trim history to max length (FIFO)
        while len(self._sessions[session_id]) > self._max_length * 2:  # *2 for pairs
            self._sessions[session_id].pop(0)
    
    def clear_history(self, session_id: str) -> bool:
        """
        Clear the chat history for a session.
        
        Args:
            session_id: The session identifier
            
        Returns:
            True if session existed and was cleared, False otherwise
        """
        if session_id in self._sessions:
            self._sessions[session_id] = []
            logger.info(f'Cleared chat history for session {session_id[:8]}...')
            return True
        return False
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session entirely.
        
        Args:
            session_id: The session identifier
            
        Returns:
            True if session existed and was deleted, False otherwise
        """
        if session_id in self._sessions:
            del self._sessions[session_id]
            logger.info(f'Deleted session {session_id[:8]}...')
            return True
        return False


class RAGService:
    """
    Orchestrates the complete RAG pipeline:
    
    Question
    ↓
    Generate Query Embedding
    ↓
    Search Vector Store (FAISS)
    ↓
    Retrieve Relevant Chunks
    ↓
    Build Prompt with Context
    ↓
    Send Prompt to Ollama
    ↓
    Receive Response
    ↓
    Return Answer + Sources
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern for the RAG service."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the RAG service."""
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.session_manager = SessionManager()
        self._initialized = True
        logger.info('RAG Service initialized')
    
    def query(
        self,
        question: str,
        session_id: Optional[str] = None,
        n_results: int = 5,
    ) -> Dict:
        """
        Execute the complete RAG pipeline for a user question.
        
        Args:
            question: The user's natural language question
            session_id: Optional session ID for multi-turn conversation.
                       If not provided, a new session is created.
            n_results: Number of document chunks to retrieve (default: 5)
        
        Returns:
            Dict with:
                - 'success': True if the pipeline completed
                - 'answer': The generated answer text
                - 'sources': List of source references used
                - 'session_id': The session ID (for continued conversation)
                - 'has_context': Whether relevant context was found
                - 'error': Error message if something went wrong
        """
        try:
            # Validate input
            if not question or not question.strip():
                return {
                    'success': False,
                    'answer': None,
                    'sources': [],
                    'session_id': session_id,
                    'has_context': False,
                    'error': 'Question cannot be empty',
                }
            
            question = question.strip()
            
            # Create or use existing session
            if not session_id:
                session_id = self.session_manager.create_session()
            
            logger.info(
                f'RAG query: session={session_id[:8]}..., '
                f'question="{question[:60]}..."'
            )
            
            # Step 1 & 2: Generate query embedding and search vector store
            # (Both happen inside vector_store.search)
            logger.info('Step 1-2: Searching vector store...')
            try:
                search_results = vector_store.search(
                    query=question,
                    n_results=n_results,
                )
            except ValueError as e:
                logger.warning(f'Vector store search failed: {str(e)}')
                search_results = []
            
            retrieved_chunks = len(search_results)
            logger.info(f'Step 3: Retrieved {retrieved_chunks} chunks from vector store')
            
            # Format sources for return
            sources = []
            for result in search_results:
                metadata = result.get('metadata', {})
                sources.append({
                    'filename': metadata.get('filename', 'Unknown'),
                    'chunk_index': metadata.get('chunk_index', 0),
                    'score': result.get('score', 0),
                    'content_preview': result.get('content', '')[:200] + '...'
                    if len(result.get('content', '')) > 200
                    else result.get('content', ''),
                })
            
            # Step 4: Build prompt with context
            logger.info('Step 4: Building prompt with context...')
            conversation_history = self.session_manager.get_history(session_id)
            prompt_data = prompt_service.build_rag_prompt(
                question=question,
                chunks=search_results,
                conversation_history=conversation_history,
            )
            
            # Add user message to history
            self.session_manager.add_message(session_id, 'user', question)
            
            has_context = prompt_data['has_context']
            
            # Step 5 & 6: Send prompt to Ollama and receive response
            logger.info('Step 5-6: Sending prompt to Ollama...')
            llm_response = llm_service.generate(
                prompt=prompt_data['user_prompt'],
                system_prompt=prompt_data['system_prompt'],
                context=conversation_history,
            )
            
            if not llm_response['success']:
                error_msg = llm_response.get('error', 'LLM generation failed')
                logger.error(f'Step 5-6 failed: {error_msg}')
                
                # Still add assistant error to history
                self.session_manager.add_message(
                    session_id, 'assistant',
                    f'I encountered an error: {error_msg}'
                )
                
                return {
                    'success': False,
                    'answer': None,
                    'sources': sources if has_context else [],
                    'session_id': session_id,
                    'has_context': has_context,
                    'error': error_msg,
                }
            
            answer = llm_response['response']
            
            # Step 7: Add assistant response to history
            self.session_manager.add_message(session_id, 'assistant', answer)
            
            logger.info(
                f'Step 7: RAG pipeline complete '
                f'(answer_length={len(answer)}, sources={len(sources)})'
            )
            
            return {
                'success': True,
                'answer': answer,
                'sources': sources if has_context else [],
                'session_id': session_id,
                'has_context': has_context,
                'error': None,
            }
            
        except ConnectionError as e:
            error_msg = str(e)
            logger.error(f'RAG pipeline failed (connection error): {error_msg}')
            return {
                'success': False,
                'answer': None,
                'sources': [],
                'session_id': session_id,
                'has_context': False,
                'error': error_msg,
            }
        except RuntimeError as e:
            error_msg = str(e)
            logger.error(f'RAG pipeline failed (runtime error): {error_msg}')
            return {
                'success': False,
                'answer': None,
                'sources': [],
                'session_id': session_id,
                'has_context': False,
                'error': error_msg,
            }
        except Exception as e:
            error_msg = f'Unexpected RAG pipeline error: {str(e)}'
            logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'answer': None,
                'sources': [],
                'session_id': session_id,
                'has_context': False,
                'error': error_msg,
            }
    
    def clear_history(self, session_id: str) -> bool:
        """
        Clear chat history for a session.
        
        Args:
            session_id: The session to clear
            
        Returns:
            True if cleared successfully
        """
        return self.session_manager.clear_history(session_id)
    
    def get_history(self, session_id: str) -> List[Dict]:
        """
        Get chat history for a session.
        
        Args:
            session_id: The session to retrieve
            
        Returns:
            List of message dicts
        """
        return self.session_manager.get_history(session_id)
    
    def get_status(self) -> Dict:
        """
        Get the overall RAG system status.
        
        Returns:
            Dict with system status information
        """
        llm_status = llm_service.get_status()
        try:
            stats = vector_store.get_collection_stats()
            doc_count = stats.get('total_documents', 0)
        except Exception:
            doc_count = 0
        
        return {
            'ollama_running': llm_status.get('ollama_running', False),
            'model_available': llm_status.get('model_available', False),
            'model': llm_status.get('model', Config.OLLAMA_MODEL),
            'documents_indexed': doc_count,
            'active_sessions': len(self.session_manager._sessions),
        }


# Global singleton instance
rag_service = RAGService()

