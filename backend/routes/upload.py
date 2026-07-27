"""
Upload Route - Handles PDF file uploads
"""

import os
from flask import Blueprint, request, jsonify, current_app

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

upload_bp = Blueprint('upload', __name__)


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    if not filename or '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle PDF file upload.
    
    Accepts multipart/form-data with a 'file' field.
    Returns JSON response with upload status.
    """
    try:
        # Check if file was provided in the request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No file provided in the request'
            }), 400
        
        file = request.files['file']
        
        # Check if a file was actually selected
        if not file or file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected for upload'
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'message': 'Invalid file type. Only PDF files are allowed.'
            }), 400
        
        # Secure the filename and save (sanitize to prevent path traversal)
        filename = os.path.basename(file.filename)
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Handle duplicate filenames by appending a number
        base_name, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(upload_path):
            filename = f"{base_name}_{counter}{extension}"
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            counter += 1
        
        # Save the file
        file.save(upload_path)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': f'File "{filename}" uploaded successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'An internal error occurred during upload: {str(e)}'
        }), 500

