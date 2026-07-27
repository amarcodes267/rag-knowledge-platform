/**
 * Upload progress bar component.
 * 
 * @param {object} props
 * @param {number} props.progress - Progress percentage (0-100)
 */
function UploadProgress({ progress }) {
  return (
    <div className="upload-progress">
      <div className="upload-progress__info">
        <span className="upload-progress__label">Uploading...</span>
        <span className="upload-progress__percentage">{Math.round(progress)}%</span>
      </div>
      <div className="upload-progress__bar">
        <div
          className="upload-progress__fill"
          style={{ width: `${progress}%` }}
          role="progressbar"
          aria-valuenow={progress}
          aria-valuemin={0}
          aria-valuemax={100}
        ></div>
      </div>
    </div>
  );
}

export default UploadProgress;

