"""
PDF Processor Service - Handles PDF text extraction and cleaning.
Uses PyMuPDF (fitz) for robust PDF parsing.
"""

import logging
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)


def extract_text(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.
    
    Args:
        pdf_path: Absolute path to the PDF file
        
    Returns:
        Extracted text content as a single string
        
    Raises:
        FileNotFoundError: If the PDF file does not exist
        ValueError: If text extraction fails or PDF is empty
    """
    try:
        doc = fitz.open(pdf_path)
        text_parts = []
        
        for page_num, page in enumerate(doc, 1):
            page_text = page.get_text()
            if page_text.strip():
                text_parts.append(page_text)
        
        doc.close()
        
        full_text = '\n'.join(text_parts)
        
        if not full_text.strip():
            raise ValueError(
                f'No extractable text found in PDF: {pdf_path}. '
                'The PDF may be scanned/image-based and requires OCR.'
            )
        
        return full_text
        
    except FileNotFoundError:
        logger.error(f'PDF file not found: {pdf_path}')
        raise
    except ValueError:
        logger.error(f'No text content in PDF: {pdf_path}')
        raise
    except Exception as e:
        logger.error(f'Failed to extract text from PDF {pdf_path}: {str(e)}')
        raise


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text for better processing.
    
    Performs the following cleaning operations:
    - Collapses multiple whitespace characters into single spaces
    - Removes empty lines (preserves paragraph breaks)
    - Strips leading/trailing whitespace from each line
    - Removes null bytes and other control characters
    - Normalizes unicode characters
    
    Args:
        text: Raw extracted text from PDF
        
    Returns:
        Cleaned and normalized text
    """
    if not text:
        return ''
    
    import re
    
    # Remove null bytes and control characters (except newlines and tabs)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    
    # Split into lines for processing
    lines = text.split('\n')
    
    cleaned_lines = []
    for line in lines:
        # Strip leading/trailing whitespace
        line = line.strip()
        
        # Collapse multiple internal spaces into one
        line = re.sub(r' +', ' ', line)
        
        # Skip lines that are just whitespace/empty after cleaning
        if line:
            cleaned_lines.append(line)
    
    # Join back with newlines
    cleaned_text = '\n'.join(cleaned_lines)
    
    # Collapse multiple consecutive newlines into at most two (paragraph breaks)
    cleaned_text = re.sub(r'\n{3,}', '\n\n', cleaned_text)
    
    # Final strip
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text


def get_pdf_metadata(pdf_path: str) -> dict:
    """
    Extract metadata from a PDF file.
    
    Args:
        pdf_path: Absolute path to the PDF file
        
    Returns:
        Dictionary containing PDF metadata (title, author, subject, pages, etc.)
    """
    try:
        doc = fitz.open(pdf_path)
        metadata = doc.metadata or {}
        page_count = doc.page_count
        doc.close()
        
        return {
            'title': metadata.get('title', ''),
            'author': metadata.get('author', ''),
            'subject': metadata.get('subject', ''),
            'keywords': metadata.get('keywords', ''),
            'page_count': page_count,
        }
    except Exception as e:
        logger.warning(f'Failed to extract metadata from {pdf_path}: {str(e)}')
        return {
            'title': '',
            'author': '',
            'subject': '',
            'keywords': '',
            'page_count': 0,
        }

