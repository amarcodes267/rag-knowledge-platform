/**
 * API Service - Centralized API communication layer.
 * Handles all HTTP requests to the Flask backend.
 */

const API_BASE_URL = '/api';

/**
 * Make a GET request to the API.
 * @param {string} endpoint - API endpoint path
 * @returns {Promise<object>} Response data
 */
export async function get(endpoint) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || `HTTP error ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API GET ${endpoint} failed:`, error);
    throw error;
  }
}

/**
 * Make a POST request to the API.
 * @param {string} endpoint - API endpoint path
 * @param {object} data - Request body data
 * @returns {Promise<object>} Response data
 */
export async function post(endpoint, data) {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || `HTTP error ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error(`API POST ${endpoint} failed:`, error);
    throw error;
  }
}

/**
 * Check if the backend server is healthy.
 * @returns {Promise<object>} Health status
 */
export async function checkHealth() {
  return get('/health');
}

