"""
LLM Service - Handles communication with Ollama for local LLM inference.
Manages connection to Ollama server, model verification, and response generation.

OPTIMIZED: The `requests` library import is moved inside methods to avoid
a trivial overhead at startup. Ollama is configured as an external service
via environment variables (not run on Render).
"""

import json
import logging
from typing import List, Dict, Optional
from functools import lru_cache

from config import Config

logger = logging.getLogger(__name__)


class LLMService:
    """
    Service for interacting with Ollama's local LLM (Llama 3.2).
    
    Features:
    - Singleton pattern (consistent with existing architecture)
    - Connection health check
    - Model availability detection
    - Prompt-based text generation
    - Proper error handling and logging
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one LLM service instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the LLM service with configuration."""
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.base_url = Config.OLLAMA_BASE_URL.rstrip('/')
        self.model = Config.OLLAMA_MODEL
        self.timeout = Config.OLLAMA_TIMEOUT
        self._initialized = True
        logger.info(
            f'LLM Service initialized with model="{self.model}" at {self.base_url}'
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for Ollama API requests."""
        return {
            'Content-Type': 'application/json',
        }
    
    def is_ollama_running(self) -> bool:
        """
        Check if the Ollama server is running and accessible.
        
        Returns:
            True if Ollama is running, False otherwise
        """
        import requests
        
        try:
            response = requests.get(
                f'{self.base_url}/api/tags',
                headers=self._get_headers(),
                timeout=5,
            )
            if response.status_code == 200:
                logger.info('Ollama server is running')
                return True
            logger.warning(f'Ollama server returned status {response.status_code}')
            return False
        except requests.exceptions.ConnectionError:
            logger.error(
                f'Cannot connect to Ollama at {self.base_url}. '
                'Is Ollama running?'
            )
            return False
        except requests.exceptions.Timeout:
            logger.error('Connection to Ollama timed out')
            return False
        except Exception as e:
            logger.error(f'Error checking Ollama status: {str(e)}')
            return False
    
    def is_model_available(self) -> bool:
        """
        Check if the required model (Llama 3.2) is available in Ollama.
        
        Returns:
            True if the model is available, False otherwise
        """
        import requests
        
        try:
            response = requests.get(
                f'{self.base_url}/api/tags',
                headers=self._get_headers(),
                timeout=10,
            )
            if response.status_code != 200:
                return False
            
            models = response.json().get('models', [])
            available_models = [m.get('name', '') for m in models]
            
            # Check if our model exists (exact match or with :latest)
            model_available = (
                self.model in available_models or
                f'{self.model}:latest' in available_models
            )
            
            if model_available:
                logger.info(f'Model "{self.model}" is available')
            else:
                available = ', '.join(available_models) if available_models else 'none'
                logger.warning(
                    f'Model "{self.model}" not found. Available models: {available}'
                )
            
            return model_available
            
        except requests.exceptions.ConnectionError:
            logger.error('Cannot connect to Ollama to check model availability')
            return False
        except Exception as e:
            logger.error(f'Error checking model availability: {str(e)}')
            return False
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[List[Dict[str, str]]] = None,
    ) -> Dict:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The user's input prompt
            system_prompt: Optional system-level instructions
            context: Optional list of previous conversation messages
                     (for multi-turn context)
        
        Returns:
            Dict with:
                - 'success': True if generation succeeded
                - 'response': The generated text
                - 'model': Model used for generation
                - 'error': Error message if generation failed
        
        Raises:
            ConnectionError: If Ollama is not running
            RuntimeError: If model is not available
        """
        import requests
        
        if not self.is_ollama_running():
            raise ConnectionError(
                'Ollama server is not running. '
                'Please start Ollama and try again.'
            )
        
        if not self.is_model_available():
            raise RuntimeError(
                f'Model "{self.model}" is not available. '
                f'Please run: ollama pull {self.model}'
            )
        
        # Build messages payload for Ollama chat API
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt,
            })
        
        # Add conversation context if provided
        if context:
            for msg in context:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                if role in ('user', 'assistant', 'system'):
                    messages.append({
                        'role': role,
                        'content': content,
                    })
        
        # Add the current user prompt
        messages.append({
            'role': 'user',
            'content': prompt,
        })
        
        # Build request payload
        payload = {
            'model': self.model,
            'messages': messages,
            'stream': False,
            'options': {
                'num_predict': Config.OLLAMA_NUM_PREDICT,
                'temperature': Config.OLLAMA_TEMPERATURE,
                'top_p': Config.OLLAMA_TOP_P,
            },
        }
        
        logger.info(
            f'Sending prompt to Ollama (model={self.model}, '
            f'messages={len(messages)}, '
            f'temperature={Config.OLLAMA_TEMPERATURE})'
        )
        
        try:
            response = requests.post(
                f'{self.base_url}/api/chat',
                headers=self._get_headers(),
                json=payload,
                timeout=self.timeout,
            )
            
            if response.status_code != 200:
                error_msg = f'Ollama returned status {response.status_code}'
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                except (json.JSONDecodeError, ValueError):
                    pass
                
                logger.error(f'Ollama generation failed: {error_msg}')
                return {
                    'success': False,
                    'response': None,
                    'model': self.model,
                    'error': error_msg,
                }
            
            result = response.json()
            generated_text = result.get('message', {}).get('content', '')
            
            logger.info(
                f'Ollama generation successful '
                f'(response_length={len(generated_text)})'
            )
            
            return {
                'success': True,
                'response': generated_text.strip(),
                'model': self.model,
                'error': None,
            }
            
        except requests.exceptions.Timeout:
            error_msg = (
                f'Ollama request timed out after {self.timeout} seconds. '
                'The model may still be loading or the prompt is too complex.'
            )
            logger.error(error_msg)
            return {
                'success': False,
                'response': None,
                'model': self.model,
                'error': error_msg,
            }
        except requests.exceptions.ConnectionError:
            error_msg = (
                f'Cannot connect to Ollama at {self.base_url}. '
                'Please ensure Ollama is running.'
            )
            logger.error(error_msg)
            return {
                'success': False,
                'response': None,
                'model': self.model,
                'error': error_msg,
            }
        except Exception as e:
            error_msg = f'Unexpected error during LLM generation: {str(e)}'
            logger.error(error_msg, exc_info=True)
            return {
                'success': False,
                'response': None,
                'model': self.model,
                'error': error_msg,
            }
    
    def get_status(self) -> Dict:
        """
        Get the complete status of the LLM service.
        
        Returns:
            Dict with ollama_status, model_available, and config info
        """
        ollama_running = self.is_ollama_running()
        model_available = self.is_model_available() if ollama_running else False
        
        return {
            'ollama_running': ollama_running,
            'model_available': model_available,
            'model': self.model,
            'base_url': self.base_url,
        }


# Global singleton instance
llm_service = LLMService()
