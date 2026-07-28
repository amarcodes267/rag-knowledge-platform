"""
Embeddings Service - Generates vector embeddings using Sentence Transformers.
Uses the all-MiniLM-L6-v2 model for efficient, high-quality embeddings.

OPTIMIZED: SentenceTransformer import is lazy-loaded inside _load_model()
to avoid ~200MB+ memory spike during Flask startup on Render's 512MB plan.
"""

import logging
from typing import List

from config import Config

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Singleton service for generating text embeddings.
    
    Uses Sentence Transformers with all-MiniLM-L6-v2 model.
    Model is lazy-loaded on first use to minimize startup memory.
    """
    
    _instance = None
    _model = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one model instance is loaded."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def _load_model(self):
        """
        Lazy-load the sentence transformer model.
        
        Import is done here (not at module level) to prevent loading
        torch + sentence-transformers (~200MB+) during Flask startup.
        On Render's 512MB plan, deferred loading is critical for passing
        the initial health check before memory is exhausted.
        """
        if self._model is None:
            # Local import: prevents heavy AI library load at module import time
            from sentence_transformers import SentenceTransformer
            
            model_name = getattr(Config, 'EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
            logger.info(f'Loading embedding model: {model_name}')
            self._model = SentenceTransformer(model_name)
            logger.info('Embedding model loaded successfully')
        return self._model
    
    def encode(self, texts: List[str]) -> List[List[float]]:
        """
        Encode a list of texts into vector embeddings.
        
        Args:
            texts: List of text strings to encode
            
        Returns:
            List of embedding vectors (each as a list of floats)
            
        Raises:
            ValueError: If texts list is empty
        """
        if not texts:
            raise ValueError('Cannot encode empty text list')
        
        model = self._load_model()
        
        # Generate embeddings
        embeddings = model.encode(
            texts,
            show_progress_bar=False,
            normalize_embeddings=True,
            batch_size=32,
        )
        
        # Convert numpy arrays to lists for JSON serialization
        return embeddings.tolist()
    
    def encode_single(self, text: str) -> List[float]:
        """
        Encode a single text string into an embedding vector.
        
        Args:
            text: Text string to encode
            
        Returns:
            Embedding vector as a list of floats
        """
        return self.encode([text])[0]
    
    @property
    def embedding_dimension(self) -> int:
        """Get the dimension of the embedding vectors (384 for all-MiniLM-L6-v2)."""
        model = self._load_model()
        return model.get_sentence_embedding_dimension()


# Global singleton instance - note: model is NOT loaded at this point
# Only the lightweight Python object is created (~1KB), NOT ~200MB
embedding_service = EmbeddingService()
