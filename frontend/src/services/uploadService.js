/**
 * Upload Service - Handles file upload operations.
 * Provides methods for uploading PDF files to the backend.
 */

const API_BASE_URL = '/api';

/**
 * Upload a PDF file to the backend.
 * @param {File} file - The PDF file to upload
 * @returns {Promise<object>} Upload response with success status and filename
 */
export async function uploadFile(file) {
  // Validate file type
  if (!file || file.type !== 'application/pdf') {
    throw new Error('Only PDF files are allowed');
  }

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.message || `Upload failed with status ${response.status}`);
    }

    return data;
  } catch (error) {
    if (error.name === 'TypeError' && error.message === 'Failed to fetch') {
      throw new Error('Unable to connect to the server. Please ensure the backend is running.');
    }
    throw error;
  }
}

