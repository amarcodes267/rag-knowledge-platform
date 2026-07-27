"""
Search Service - Orchestrates semantic search across the vector store.
Provides high-level search functionality with result formatting.
"""

import logging
from typing import List, Optional, Dict, Any

from services.vector_store import vector_store

logger = logging.getLogger(__name__)


def search_documents(
    query: str,
    n_results: int = 5,
    filename: Optional[str] = None,
) -> dict:
    """
    Perform semantic search across indexed documents.
    
    This is the main entry point for search operations. It:
    1. Validates the query
    2. Runs semantic search against the vector store
    3. Formats results for API consumption
    
    Args:
        query: Natural language search query
        n_results: Maximum number of results (1-50, default 5)
        filename: Optional filter to search within a specific document
        
    Returns:
        Dict with:
            - 'success': True if search completed
            - 'query': The original query
            - 'results': List of result dicts
            - 'total_results': Number of results returned
    
    Raises:
        ValueError: If query is empty or n_results is out of range
    """
    # Validate query
    if not query or not query.strip():
        raise ValueError('Search query cannot be empty')
    
    # Validate n_results
    if n_results < 1:
        n_results = 1
    elif n_results > 50:
        n_results = 50
    
    # Build optional filter
    filter_criteria = None
    if filename:
        filter_criteria = {'filename': filename}
    
    # Execute search
    results = vector_store.search(
        query=query.strip(),
        n_results=n_results,
        filter_criteria=filter_criteria,
    )
    
    return {
        'success': True,
        'query': query.strip(),
        'results': results,
        'total_results': len(results),
    }


def get_search_stats() -> dict:
    """
    Get statistics about the search index.
    
    Returns:
        Dict with index statistics
    """
    return vector_store.get_collection_stats()

