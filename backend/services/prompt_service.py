"""
Prompt Service - Handles prompt engineering for the RAG pipeline.
Builds structured prompts that guide the LLM to answer based only on retrieved context.
"""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class PromptService:
    """
    Service for building and engineering prompts for the RAG pipeline.
    
    Features:
    - Context-grounded prompt construction
    - Anti-hallucination guardrails
    - Multi-turn conversation support
    - Source-aware prompt formatting
    - Configurable system prompts
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern for the prompt service."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the prompt service."""
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        logger.info('Prompt Service initialized')
    
    def build_system_prompt(self) -> str:
        """
        Build the system-level prompt that defines the AI assistant's behavior.
        
        This prompt is sent once at the beginning of the conversation
        and establishes the ground rules for response generation.
        
        Returns:
            System prompt string
        """
        return (
            "You are an intelligent Enterprise Knowledge Assistant. "
            "Your role is to help users find answers from their uploaded documents.\n\n"
            "STRICT RULES - YOU MUST FOLLOW THESE:\n"
            "1. ONLY answer using the provided document context below.\n"
            "2. If the answer is NOT found in the provided context, "
            "clearly state: "
            "'I cannot find this information in the uploaded documents.'\n"
            "3. NEVER make up or hallucinate information.\n"
            "4. NEVER use your pre-training knowledge to answer questions "
            "outside the provided context.\n"
            "5. If the context is partially relevant, answer only what you can "
            "confirm and note what is not covered.\n"
            "6. Be concise and professional.\n"
            "7. When referencing information, mention the source document "
            "filename if available.\n"
            "8. If asked a question that is not related to the documents, "
            "politely explain that you can only answer questions based on "
            "the uploaded documents.\n"
            "9. Do not repeat the user's question in your response.\n"
            "10. Format your response in clear paragraphs for readability."
        )
    
    def build_context_block(self, chunks: List[Dict]) -> str:
        """
        Build a formatted context block from retrieved document chunks.
        
        Args:
            chunks: List of retrieved document chunks, each containing:
                - content: The text content
                - metadata: Dict with filename, chunk_index, etc.
                - score: Similarity score
        
        Returns:
            Formatted context string with source references
        """
        if not chunks:
            return "No relevant documents found."
        
        context_parts = []
        
        for i, chunk in enumerate(chunks, 1):
            content = chunk.get('content', '')
            metadata = chunk.get('metadata', {})
            filename = metadata.get('filename', 'Unknown')
            chunk_index = metadata.get('chunk_index', 0)
            score = chunk.get('score', 0)
            
            context_parts.append(
                f"[Document {i}] From: {filename} (Chunk {chunk_index})\n"
                f"{content}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def build_rag_prompt(
        self,
        question: str,
        chunks: List[Dict],
        conversation_history: Optional[List[Dict]] = None,
    ) -> Dict:
        """
        Build the complete RAG prompt with context and conversation history.
        
        Args:
            question: The user's current question
            chunks: Retrieved document chunks for context
            conversation_history: Optional list of previous messages
                                  [{'role': 'user'/'assistant', 'content': ...}]
        
        Returns:
            Dict with:
                - 'system_prompt': System-level instructions
                - 'context': Formatted context block
                - 'user_prompt': The final user prompt
                - 'has_context': Whether relevant context was found
        """
        system_prompt = self.build_system_prompt()
        context_block = self.build_context_block(chunks)
        
        has_context = len(chunks) > 0 and any(
            chunk.get('content', '').strip()
            for chunk in chunks
        )
        
        if not has_context:
            user_prompt = (
                f"Question: {question}\n\n"
                f"No relevant documents were found in the knowledge base "
                f"that can answer this question.\n\n"
                f"Please inform the user that there are no relevant documents "
                f"in the uploaded PDFs that contain information about this topic."
            )
        else:
            user_prompt = (
                f"Please answer the following question using ONLY the "
                f"provided document context.\n\n"
                f"CONTEXT:\n{context_block}\n\n"
                f"---\n\n"
                f"QUESTION: {question}\n\n"
                f"---\n\n"
                f"IMPORTANT: If the context above does not contain "
                f"the information needed to answer the question, "
                f"say: 'I cannot find this information in the uploaded documents.' "
                f"Do NOT invent or assume any information."
            )
        
        logger.info(
            f'Built RAG prompt for question: "{question[:60]}..." '
            f'(context_chunks={len(chunks)}, has_context={has_context})'
        )
        
        return {
            'system_prompt': system_prompt,
            'context': context_block,
            'user_prompt': user_prompt,
            'has_context': has_context,
        }


# Global singleton instance
prompt_service = PromptService()

