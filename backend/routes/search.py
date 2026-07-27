"""
Search Route - Handles semantic search queries against the vector store.
Provides endpoints for searching indexed documents.
"""

import logging
from flask import Blueprint, request, jsonify

from services.search_service import search_documents, get_search_stats

logger = logging.getLogger(__name__)

search_bp = Blueprint('search', __name__)


@search_bp.route('/search', methods=['POST'])
def search():
    """
    Perform semantic search across indexed documents.
    
    Accepts JSON with query parameters and returns relevant document chunks
    ranked by semantic similarity.
    
    Request body:
        {
            "query": "What is the refund policy?",
            "n_results": 5,
            "filename": "optional_filter.pdf"
        }
    
    Returns:
        200: Search results with scored matches
        400: Missing or invalid query
        500: Search error
    """
    try:
        data = request.get_json(silent=True)
        
        # Validate request body
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing "query" in request body'
            }), 400
        
        query = data['query']
        n_results = data.get('n_results', 5)
        filename = data.get('filename', None)
        
        # Validate query is not empty
        if not query or not query.strip():
            return jsonify({
                'success': False,
                'message': 'Search query cannot be empty'
            }), 400
        
        # Perform search
        result = search_documents(
            query=query,
            n_results=n_results,
            filename=filename,
        )
        
        return jsonify(result), 200
        
    except ValueError as e:
        logger.error(f'Search validation error: {str(e)}')
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f'Internal search error: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': f'An internal error occurred during search: {str(e)}'
        }), 500


@search_bp.route('/search/index-stats', methods=['GET'])
def index_stats():
    """
    Get statistics about the search index.
    
    Returns:
        200: Index statistics including document count
    """
    try:
        stats = get_search_stats()
        return jsonify({
            'success': True,
            'stats': stats,
        }), 200
    except Exception as e:
        logger.error(f'Error getting index stats: {str(e)}')
        return jsonify({
            'success': False,
            'message': f'Error getting index statistics: {str(e)}'
        }), 500

