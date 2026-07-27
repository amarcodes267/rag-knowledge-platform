import os
import json
import logging
import pickle
import uuid
import numpy as np
from typing import List, Optional, Dict, Any

import faiss

from config import Config
from services.embeddings import embedding_service

logger = logging.getLogger(__name__)


class VectorStoreService:
    """
    Service for managing vector embeddings using FAISS with persistent storage.
    
    Provides persistent storage with metadata support using:
    - FAISS: Efficient similarity search (cosine similarity via inner product on normalized vectors)
    - Pickle: Persistent metadata and document storage
    """
    
    _instance = None
    _index = None
    _documents = []  # List of dicts: {id, content, metadata, embedding}
    _id_to_index = {}  # Map document ID to index position
    _persist_path = None
    _metadata_path = None
    
    EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 dimension
    
    def __new__(cls):
        """Singleton pattern for the vector store."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _get_paths(self):
        """Get persistence file paths."""
        persist_dir = getattr(Config, 'CHROMA_PERSIST_DIR', './chroma_db')
        os.makedirs(persist_dir, exist_ok=True)
        self._persist_path = os.path.join(persist_dir, 'faiss_index.bin')
        self._metadata_path = os.path.join(persist_dir, 'documents.pkl')
    
    def _ensure_initialized(self):
        """Lazy-initialize the FAISS index and load persisted data."""
        if self._index is not None:
            return
        
        self._get_paths()
        
        # Try to load existing index and metadata
        if os.path.exists(self._persist_path) and os.path.exists(self._metadata_path):
            try:
                self._index = faiss.read_index(self._persist_path)
                with open(self._metadata_path, 'rb') as f:
                    data = pickle.load(f)
                    self._documents = data.get('documents', [])
                    self._id_to_index = data.get('id_to_index', {})
                logger.info(
                    f'Loaded existing FAISS index with {len(self._documents)} documents'
                )
                return
            except Exception as e:
                logger.warning(f'Failed to load existing index, creating new: {e}')
        
        # Create new index (Inner Product on normalized vectors = cosine similarity)
        self._index = faiss.IndexIDMap(
            faiss.IndexFlatIP(self.EMBEDDING_DIM)
        )
        self._documents = []
        self._id_to_index = {}
        logger.info('Created new FAISS index')
    
    def _persist(self):
        """Save the FAISS index and metadata to disk."""
        try:
            faiss.write_index(self._index, self._persist_path)
            with open(self._metadata_path, 'wb') as f:
                pickle.dump({
                    'documents': self._documents,
                    'id_to_index': self._id_to_index,
                }, f)
        except Exception as e:
            logger.error(f'Failed to persist vector store: {e}')
    
    def add_documents(self, chunks: List[dict]) -> int:
        """
        Add chunked documents with embeddings to the vector store.
        
        Args:
            chunks: List of chunk dicts with 'content' and 'metadata' keys
                    (as produced by text_splitter.split_text)
            
        Returns:
            Number of documents successfully added
            
        Raises:
            ValueError: If chunks list is empty or invalid
        """
        if not chunks:
            raise ValueError('No chunks to add to vector store')
        
        self._ensure_initialized()
        
        # Extract texts and metadata
        texts = [chunk['content'] for chunk in chunks]
        
        # Generate embeddings using our service
        embeddings = embedding_service.encode(texts)
        embeddings_array = np.array(embeddings).astype(np.float32)
        
        # Generate unique IDs
        ids = [str(uuid.uuid4()) for _ in chunks]
        id_array = np.array([hash(id_) % (2**63) for id_ in ids]).astype(np.int64)
        
        # Add to FAISS index (IDs must be int64, 1D array for faiss >= 1.9.0)
        self._index.add_with_ids(embeddings_array, id_array)
        
        # Store documents with metadata
        for i, chunk in enumerate(chunks):
            doc_entry = {
                'id': ids[i],
                'faiss_id': int(id_array[i]),
                'content': texts[i],
                'metadata': chunk.get('metadata', {}).copy(),
                'embedding': embeddings[i],
            }
            self._documents.append(doc_entry)
            self._id_to_index[ids[i]] = len(self._documents) - 1
        
        # Persist to disk
        self._persist()
        
        logger.info(f'Added {len(chunks)} chunks to vector store')
        
        return len(chunks)
    
    def search(
        self,
        query: str,
        n_results: Optional[int] = 5,
        filter_criteria: Optional[Dict[str, Any]] = None,
    ) -> List[dict]:
        """
        Perform semantic search on the vector store.
        
        Args:
            query: Natural language query string
            n_results: Maximum number of results to return
            filter_criteria: Optional metadata filter (e.g., {'filename': 'doc.pdf'})
            
        Returns:
            List of result dicts, each containing:
                - 'content': The matched text chunk
                - 'metadata': Associated metadata
                - 'score': Similarity score (0-1, higher is more similar)
        """
        if not query or not query.strip():
            raise ValueError('Search query cannot be empty')
        
        self._ensure_initialized()
        
        if len(self._documents) == 0:
            logger.warning('Search attempted on empty vector store')
            return []
        
        # Handle None n_results
        if n_results is None:
            n_results = 5
        
        # Generate embedding for the query
        query_embedding = embedding_service.encode_single(query.strip())
        query_array = np.array([query_embedding]).astype(np.float32)
        
        # Search in FAISS
        k = min(n_results, len(self._documents))
        distances, indices = self._index.search(query_array, k)
        
        # Format results
        formatted_results = []
        
        for idx in range(len(indices[0])):
            faiss_idx = int(indices[0][idx])
            if faiss_idx == -1:
                continue
            
            # Find the document by faiss_id
            doc = None
            for d in self._documents:
                if d['faiss_id'] == faiss_idx:
                    doc = d
                    break
            
            if doc is None:
                continue
            
            # FAISS returns inner product score for normalized vectors = cosine similarity
            score = float(distances[0][idx])
            # Clamp to [0, 1] range
            score = max(0.0, min(1.0, score))
            
            # Apply metadata filter if specified
            if filter_criteria:
                match = True
                for key, value in filter_criteria.items():
                    if doc['metadata'].get(key) != value:
                        match = False
                        break
                if not match:
                    continue
            
            formatted_results.append({
                'content': doc['content'],
                'metadata': doc['metadata'],
                'score': round(score, 4),
            })
        
        # Sort by score descending
        formatted_results.sort(key=lambda x: x['score'], reverse=True)
        
        logger.info(f'Search for "{query[:50]}..." returned {len(formatted_results)} results')
        
        return formatted_results
    
    def get_collection_stats(self) -> dict:
        """
        Get statistics about the vector store collection.
        
        Returns:
            Dict with count, and optionally other stats
        """
        self._ensure_initialized()
        
        return {
            'total_documents': len(self._documents),
            'collection_name': getattr(Config, 'COLLECTION_NAME', 'enterprise_knowledge_platform'),
            'embedding_dimension': self.EMBEDDING_DIM,
        }
    
    def delete_document(self, filename: str) -> int:
        """
        Delete all chunks associated with a specific filename.
        
        Args:
            filename: The filename to delete from the vector store
            
        Returns:
            Number of chunks deleted
        """
        self._ensure_initialized()
        
        # Find documents to delete
        docs_to_delete = [
            doc for doc in self._documents
            if doc['metadata'].get('filename') == filename
        ]
        
        if not docs_to_delete:
            logger.warning(f'No chunks found for file: {filename}')
            return 0
        
        # Remove from FAISS by IDs
        faiss_ids = np.array([doc['faiss_id'] for doc in docs_to_delete]).astype(np.int64)
        self._index.remove_ids(faiss_ids)
        
        # Remove from document list
        ids_to_remove = {doc['id'] for doc in docs_to_delete}
        self._documents = [d for d in self._documents if d['id'] not in ids_to_remove]
        for doc_id in ids_to_remove:
            self._id_to_index.pop(doc_id, None)
        
        # Rebuild id_to_index mapping
        self._id_to_index = {}
        for idx, doc in enumerate(self._documents):
            self._id_to_index[doc['id']] = idx
        
        # Persist
        self._persist()
        
        count = len(docs_to_delete)
        logger.info(f'Deleted {count} chunks for file: {filename}')
        return count


# Global singleton instance
vector_store = VectorStoreService()
