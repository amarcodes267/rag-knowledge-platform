import { useState, useRef, useCallback, useEffect } from 'react';
import { uploadFile } from '../../services/uploadService';
import UploadProgress from './UploadProgress';
import FilePreview from './FilePreview';

/**
 * Upload box component with drag-and-drop and file selection.
 * Handles file validation and upload flow.
 */
function UploadBox() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [status, setStatus] = useState({ type: '', message: '' });
  const fileInputRef = useRef(null);

  /**
   * Validate the selected file.
   * @param {File} file - File to validate
   * @returns {boolean} Whether the file is valid
   */
  const validateFile = useCallback((file) => {
    if (!file) {
      setStatus({ type: 'error', message: 'No file selected.' });
      return false;
    }
    if (file.type !== 'application/pdf') {
      setStatus({ type: 'error', message: 'Only PDF files are allowed.' });
      return false;
    }
    if (file.size === 0) {
      setStatus({ type: 'error', message: 'The selected file is empty.' });
      return false;
    }
    return true;
  }, []);

  /**
   * Handle file selection from input or drag-and-drop.
   * @param {File} file - The selected file
   */
  const handleFileSelect = useCallback((file) => {
    setStatus({ type: '', message: '' });
    if (validateFile(file)) {
      setSelectedFile(file);
    } else {
      setSelectedFile(null);
    }
  }, [validateFile]);

  /**
   * Handle drag over event.
   */
  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  /**
   * Handle drag leave event.
   */
  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  /**
   * Handle drop event.
   */
  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  }, [handleFileSelect]);

  /**
   * Handle file input change.
   */
  const handleInputChange = useCallback((e) => {
    const file = e.target.files[0];
    if (file) {
      handleFileSelect(file);
    }
  }, [handleFileSelect]);

  /**
   * Handle remove selected file.
   */
  const handleRemoveFile = useCallback(() => {
    setSelectedFile(null);
    setStatus({ type: '', message: '' });
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, []);

  /**
   * Handle upload button click.
   */
  const progressIntervalRef = useRef(null);

  const handleUpload = useCallback(async () => {
    if (!selectedFile) {
      setStatus({ type: 'error', message: 'Please select a file first.' });
      return;
    }

    setIsUploading(true);
    setUploadProgress(0);
    setStatus({ type: '', message: '' });

    // Simulate progress for better UX
    progressIntervalRef.current = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressIntervalRef.current);
          return 90;
        }
        return prev + 10;
      });
    }, 300);

    try {
      const result = await uploadFile(selectedFile);
      clearInterval(progressIntervalRef.current);
      setUploadProgress(100);
      
      if (result.success) {
        setStatus({
          type: 'success',
          message: `File "${result.filename}" uploaded successfully!`,
        });
        // Clear the form after successful upload
        setTimeout(() => {
          handleRemoveFile();
          setUploadProgress(0);
        }, 2000);
      }
    } catch (error) {
      clearInterval(progressIntervalRef.current);
      setUploadProgress(0);
      setStatus({
        type: 'error',
        message: error.message || 'Upload failed. Please try again.',
      });
    } finally {
      setIsUploading(false);
    }
  }, [selectedFile, handleRemoveFile]);

  // Cleanup interval on unmount
  useEffect(() => {
    return () => {
      if (progressIntervalRef.current) {
        clearInterval(progressIntervalRef.current);
      }
    };
  }, []);

  return (
    <div className="upload-box">
      {/* Drag and drop zone */}
      <div
        className={`upload-box__dropzone ${isDragging ? 'upload-box__dropzone--active' : ''} ${selectedFile ? 'upload-box__dropzone--has-file' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !selectedFile && fileInputRef.current?.click()}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,application/pdf"
          onChange={handleInputChange}
          className="upload-box__input"
          id="file-upload"
        />
        
        {!selectedFile ? (
          <div className="upload-box__placeholder">
            <div className="upload-box__icon">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
                <polyline points="17 8 12 3 7 8" />
                <line x1="12" y1="3" x2="12" y2="15" />
              </svg>
            </div>
            <p className="upload-box__text">
              <span className="upload-box__text-bold">Click to upload</span> or drag and drop
            </p>
            <p className="upload-box__hint">PDF files only (max 50MB)</p>
          </div>
        ) : (
          <div className="upload-box__selected" onClick={(e) => e.stopPropagation()}>
            <FilePreview file={selectedFile} onRemove={handleRemoveFile} />
          </div>
        )}
      </div>

      {/* Upload progress */}
      {isUploading && (
        <UploadProgress progress={uploadProgress} />
      )}

      {/* Upload button */}
      {selectedFile && !isUploading && (
        <button className="upload-box__submit btn btn--primary btn--lg" onClick={handleUpload}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
          Upload File
        </button>
      )}

      {/* Status alerts */}
      {status.message && (
        <div className={`upload-box__alert alert alert--${status.type}`}>
          <p>{status.message}</p>
        </div>
      )}
    </div>
  );
}

export default UploadBox;

