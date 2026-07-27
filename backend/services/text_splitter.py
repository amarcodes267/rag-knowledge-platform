"""
Text Splitter Service - Chunks text using LangChain's RecursiveCharacterTextSplitter.
Splits text into manageable chunks for embedding and search.
"""

import logging
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import Config

logger = logging.getLogger(__name__)


def split_text(text: str, filename: str = '') -> List[dict]:
    """
    Split text into overlapping chunks with metadata.
    
    Uses RecursiveCharacterTextSplitter with the following separators
    (in order of priority):
    - Double newlines (paragraph breaks)
    - Single newlines
    - Spaces (as last resort)
    
    Args:
        text: Cleaned text content to split
        filename: Source filename for metadata tracking
        
    Returns:
        List of dictionaries, each containing:
            - 'content': The chunk text
            - 'metadata': Dict with filename, chunk_index, total_chunks
    
    Raises:
        ValueError: If text is empty after cleaning
    """
    if not text or not text.strip():
        raise ValueError('Cannot split empty text')
    
    chunk_size = getattr(Config, 'CHUNK_SIZE', 1000)
    chunk_overlap = getattr(Config, 'CHUNK_OVERLAP', 200)
    
    # Validate configuration
    if chunk_overlap >= chunk_size:
        chunk_overlap = chunk_size // 5
        logger.warning(
            f'Chunk overlap ({chunk_overlap}) adjusted to be less than chunk size ({chunk_size})'
        )
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=['\n\n', '\n', ' ', ''],
    )
    
    # Split the text
    chunks = text_splitter.split_text(text)
    
    if not chunks:
        raise ValueError('Text splitting produced no chunks')
    
    # Build chunk documents with metadata
    chunk_docs = []
    total_chunks = len(chunks)
    
    for idx, chunk_content in enumerate(chunks):
        chunk_doc = {
            'content': chunk_content,
            'metadata': {
                'filename': filename,
                'chunk_index': idx,
                'total_chunks': total_chunks,
            }
        }
        chunk_docs.append(chunk_doc)
    
    logger.info(
        f'Split text into {total_chunks} chunks '
        f'(size={chunk_size}, overlap={chunk_overlap})'
    )
    
    return chunk_docs

