/**
 * Chat Service - Handles all chat API communication with the backend.
 * Provides methods for sending messages, managing sessions, and checking status.
 */

const API_BASE_URL = '/api';

/**
 * Generate a unique session ID for chat conversations.
 * Uses crypto API if available, falls back to Date.now() + random.
 * @returns {string} Unique session identifier
 */
function generateSessionId() {
  if (window.crypto && window.crypto.randomUUID) {
    return window.crypto.randomUUID();
  }
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Retrieve the current session ID from sessionStorage, or create a new one.
 * @returns {string} Session ID
 */
export function getSessionId() {
  let sessionId = sessionStorage.getItem('ekp_chat_session_id');
  if (!sessionId) {
    sessionId = generateSessionId();
    sessionStorage.setItem('ekp_chat_session_id', sessionId);
  }
  return sessionId;
}

/**
 * Reset the session ID (for starting a new conversation).
 */
export function resetSessionId() {
  const newId = generateSessionId();
  sessionStorage.setItem('ekp_chat_session_id', newId);
  return newId;
}

/**
 * Send a chat message to the RAG backend.
 * 
 * @param {string} question - The user's question
 * @param {string} [sessionId] - Optional session ID for multi-turn conversation
 * @returns {Promise<object>} Response with answer and sources
 */
export async function sendMessage(question, sessionId = null) {
  if (!question || !question.trim()) {
    throw new Error('Question cannot be empty');
  }

  const sid = sessionId || getSessionId();
  const payload = {
    question: question.trim(),
    session_id: sid,
  };

  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      // Handle specific error cases
      if (response.status === 400) {
        throw new Error(data.error || 'Invalid request. Please check your input.');
      }
      if (response.status === 503) {
        throw new Error(
          'The AI service is currently unavailable. ' +
          'Please ensure Ollama is running and the Llama 3.2 model is installed.'
        );
      }
      throw new Error(data.error || `Server error (${response.status})`);
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error(
        'Unable to connect to the server. Please ensure the backend is running.'
      );
    }
    throw error;
  }
}

/**
 * Clear chat history for the current session.
 * 
 * @param {string} [sessionId] - Optional session ID
 * @returns {Promise<object>} Response confirmation
 */
export async function clearChat(sessionId = null) {
  const sid = sessionId || getSessionId();

  try {
    const response = await fetch(`${API_BASE_URL}/chat/clear`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ session_id: sid }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Failed to clear chat history');
    }

    // Reset the session ID for a fresh start
    resetSessionId();

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error(
        'Unable to connect to the server. Please ensure the backend is running.'
      );
    }
    throw error;
  }
}

/**
 * Get the chat history for a session.
 * 
 * @param {string} [sessionId] - Optional session ID
 * @returns {Promise<object>} Chat history with messages
 */
export async function getChatHistory(sessionId = null) {
  const sid = sessionId || getSessionId();

  try {
    const response = await fetch(`${API_BASE_URL}/chat/history/${sid}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Failed to retrieve chat history');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error(
        'Unable to connect to the server. Please ensure the backend is running.'
      );
    }
    throw error;
  }
}

/**
 * Check the status of the chat system (Ollama, model, etc.).
 * 
 * @returns {Promise<object>} System status
 */
export async function getChatStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Failed to get chat status');
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error(
        'Unable to connect to the server. Please ensure the backend is running.'
      );
    }
    throw error;
  }
}

/**
 * Create a new chat session on the server.
 * 
 * @returns {Promise<object>} New session ID
 */
export async function createNewSession() {
  try {
    const response = await fetch(`${API_BASE_URL}/chat/new-session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || 'Failed to create new session');
    }

    if (data.session_id) {
      sessionStorage.setItem('ekp_chat_session_id', data.session_id);
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error(
        'Unable to connect to the server. Please ensure the backend is running.'
      );
    }
    throw error;
  }
}

