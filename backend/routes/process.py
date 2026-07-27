"""
Process Route - Handles PDF document processing.
Extracts text, chunks, generates embeddings, and stores in vector database.
"""

import os
import logging
from flask import Blueprint, request, jsonify, current_app

from services.pdf_processor import extract_text, clean_text
from services.text_splitter import split_text
from services.vector_store import vector_store

logger = logging.getLogger(__name__)

process_bp = Blueprint('process', __name__)


@process_bp.route('/process', methods=['POST'])
def process_document():
    """
    Process an uploaded PDF document.
    
    Accepts JSON with a 'filename' field specifying which uploaded PDF to process.
    Performs: text extraction -> cleaning -> chunking -> embedding -> vector storage.
    
    Request body:
        {
            "filename": "document.pdf"
        }
    
    Returns:
        200: Processing completed successfully with chunk count
        400: Missing filename or file not found
        500: Processing error
    """
    try:
        data = request.get_json(silent=True)
        
        # Validate request body
        if not data or 'filename' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing "filename" in request body'
            }), 400
        
        filename = data['filename']
        
        # Sanitize filename to prevent path traversal
        filename = os.path.basename(filename)
        
        # Build file path
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file_path = os.path.join(upload_folder, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'message': f'File "{filename}" not found in uploads directory'
            }), 404
        
        # Step 1: Extract text from PDF
        logger.info(f'Processing document: {filename}')
        raw_text = extract_text(file_path)
        
        # Step 2: Clean the extracted text
        cleaned_text = clean_text(raw_text)
        
        if not cleaned_text:
            return jsonify({
                'success': False,
                'message': 'No text content could be extracted from the PDF'
            }), 400
        
        # Step 3: Split text into chunks
        chunks = split_text(cleaned_text, filename=filename)
        
        # Step 4: Generate embeddings and store in vector database
        chunk_count = vector_store.add_documents(chunks)
        
        logger.info(
            f'Successfully processed "{filename}": '
            f'{len(raw_text)} chars extracted, {chunk_count} chunks stored'
        )
        
        return jsonify({
            'success': True,
            'filename': filename,
            'characters_extracted': len(raw_text),
            'chunks_created': chunk_count,
            'message': f'Successfully processed "{filename}" with {chunk_count} chunks'
        }), 200
        
    except FileNotFoundError as e:
        logger.error(f'File not found during processing: {str(e)}')
        return jsonify({
            'success': False,
            'message': str(e)
        }), 404
    except ValueError as e:
        logger.error(f'Processing error: {str(e)}')
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400
    except Exception as e:
        logger.error(f'Internal error processing document: {str(e)}', exc_info=True)
        return jsonify({
            'success': False,
            'message': f'An internal error occurred during processing: {str(e)}'
        }), 500


@process_bp.route('/process/status', methods=['GET'])
def get_processing_status():
    """
    Get the current processing and indexing status.
    
    Returns:
        200: Status information with document count
    """
    try:
        stats = vector_store.get_collection_stats()
        return jsonify({
            'success': True,
            'indexed_documents': stats.get('total_documents', 0),
            'status': 'operational',
        }), 200
    except Exception as e:
        logger.error(f'Error getting processing status: {str(e)}')
        return jsonify({
            'success': False,
            'message': f'Error getting status: {str(e)}'
        }), 500

