import UploadBox from '../components/upload/UploadBox';
import '../styles/Upload.css';

/**
 * Upload page with drag-and-drop PDF upload functionality.
 * Connects to Flask backend for file storage.
 */
function Upload() {
  return (
    <div className="upload-page">
      <section className="section">
        <div className="container">
          <div className="page-header">
            <h1 className="page-title">Upload PDF</h1>
            <p className="page-subtitle">
              Securely upload your PDF documents. Drag and drop or click to select files.
            </p>
          </div>

          <div className="upload-page__content">
            <UploadBox />
          </div>

          <div className="upload-page__info">
            <div className="upload-page__info-card">
              <div className="upload-page__info-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="16" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
              </div>
              <div>
                <h3 className="upload-page__info-title">Supported Formats</h3>
                <p className="upload-page__info-text">PDF files only (.pdf)</p>
              </div>
            </div>
            <div className="upload-page__info-card">
              <div className="upload-page__info-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="16" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
              </div>
              <div>
                <h3 className="upload-page__info-title">Maximum File Size</h3>
                <p className="upload-page__info-text">Up to 50MB per file</p>
              </div>
            </div>
            <div className="upload-page__info-card">
              <div className="upload-page__info-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="16" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
              </div>
              <div>
                <h3 className="upload-page__info-title">Secure Upload</h3>
                <p className="upload-page__info-text">Enterprise-grade encryption</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Upload;

