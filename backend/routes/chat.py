"""
Chat Route - Handles RAG-powered chat interactions.
Provides endpoints for multi-turn conversations with the LLM.
"""

import uuid
import logging
from flask import Blueprint, request, jsonify

from services.rag_service import rag_service

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat', methods=['POST'])
def chat():
    """
    Process a chat message through the RAG pipeline.
    
    Accepts JSON with a 'question' field and optional 'session_id'.
    Returns the AI-generated answer with source references.
    
    Request body:
        {
            "question": "What is the refund policy?",
            "session_id": "optional-existing-session-id"
        }
    
    Returns:
        200: RAG response with answer and sources
        400: Missing or invalid question
        500: Internal pipeline error
    """
    try:
        data = request.get_json(silent=True)
        
        # Validate request body
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing "question" in request body',
                'answer': None,
                'sources': [],
                'session_id': None,
            }), 400
        
        question = data['question']
        session_id = data.get('session_id', None)
        
        # Validate question is not empty
        if not question or not question.strip():
            return jsonify({
                'success': False,
                'error': 'Question cannot be empty',
                'answer': None,
                'sources': [],
                'session_id': session_id,
            }), 400
        
        question = question.strip()
        
        # Execute RAG pipeline
        result = rag_service.query(
            question=question,
            session_id=session_id,
            n_results=None,  # Use default from config
        )
        
        status_code = 200 if result['success'] else 500
        
        # Build response
        response = {
            'success': result['success'],
            'answer': result.get('answer'),
            'sources': result.get('sources', []),
            'session_id': result.get('session_id'),
            'has_context': result.get('has_context', False),
        }
        
        if result.get('error'):
            response['error'] = result['error']
        
        return jsonify(response), status_code
        
    except Exception as e:
        logger.error(f'Unexpected error in chat endpoint: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'error': f'An internal error occurred: {str(e)}',
            'answer': None,
            'sources': [],
            'session_id': session_id if 'session_id' in locals() else None,
        }), 500


@chat_bp.route('/chat/clear', methods=['POST'])
def clear_chat():
    """
    Clear chat history for a session.
    
    Request body:
        {
            "session_id": "session-id-to-clear"
        }
    
    Returns:
        200: History cleared successfully
        400: Missing session_id
    """
    try:
        data = request.get_json(silent=True)
        
        if not data or 'session_id' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing "session_id" in request body',
            }), 400
        
        session_id = data['session_id']
        
        if not session_id:
            return jsonify({
                'success': False,
                'message': 'session_id cannot be empty',
            }), 400
        
        cleared = rag_service.clear_history(session_id)
        
        if cleared:
            return jsonify({
                'success': True,
                'message': 'Chat history cleared successfully',
                'session_id': session_id,
            }), 200
        else:
            return jsonify({
                'success': True,
                'message': 'Session not found, new history will start fresh',
                'session_id': session_id,
            }), 200
        
    except Exception as e:
        logger.error(f'Error clearing chat history: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error clearing chat history: {str(e)}',
        }), 500


@chat_bp.route('/chat/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """
    Get the chat history for a specific session.
    
    Args:
        session_id: The session identifier from URL path
    
    Returns:
        200: Chat history with messages
        400: Missing session_id
    """
    try:
        if not session_id:
            return jsonify({
                'success': False,
                'message': 'session_id is required',
                'messages': [],
            }), 400
        
        history = rag_service.get_history(session_id)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'messages': history,
            'message_count': len(history),
        }), 200
        
    except Exception as e:
        logger.error(f'Error getting chat history: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error getting chat history: {str(e)}',
            'messages': [],
        }), 500


@chat_bp.route('/chat/status', methods=['GET'])
def get_chat_status():
    """
    Get the status of the chat system.
    
    Returns:
        200: System status including Ollama and model availability
    """
    try:
        status = rag_service.get_status()
        
        return jsonify({
            'success': True,
            'status': status,
        }), 200
        
    except Exception as e:
        logger.error(f'Error getting chat status: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error getting chat status: {str(e)}',
            'status': None,
        }), 500


@chat_bp.route('/chat/new-session', methods=['POST'])
def create_new_session():
    """
    Create a new chat session.
    
    Returns:
        200: New session ID
    """
    try:
        session_id = rag_service.session_manager.create_session()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'New chat session created',
        }), 200
        
    except Exception as e:
        logger.error(f'Error creating new session: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': f'Error creating new session: {str(e)}',
            'session_id': None,
        }), 500

