import React, { useState, useRef } from 'react';

export default function UploadModal({
  isOpen,
  onClose,
  onUploadFile,
  isProcessing,
  uploadProgress
}) {
  const [isFileDragging, setIsFileDragging] = useState(false);
  const fileInputRef = useRef(null);

  if (!isOpen) return null;

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsFileDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsFileDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsFileDragging(false);
    const files = e.dataTransfer?.files;
    if (files && files.length > 0) {
      onUploadFile(files[0]);
    }
  };

  const handleFileChange = (e) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onUploadFile(files[0]);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">Upload 3D CAD Drawing (PDF)</div>
          <button className="close-btn" onClick={onClose} disabled={isProcessing}>
            ✕
          </button>
        </div>

        <div className="modal-body">
          <p className="modal-desc">
            Upload any engineering drawing PDF. The multi-stage AI pipeline will preprocess,
            propose semantic functional ROIs, extract all dimensions and GD&T tolerances, build a
            spatial relationship graph, and verify engineering domain sanity rules.
          </p>

          <div
            className={`dropzone ${isFileDragging ? 'dragging' : ''}`}
            onClick={() => !isProcessing && fileInputRef.current?.click()}
            onDragOver={handleDragOver}
            onDragEnter={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileChange}
              accept=".pdf,application/pdf"
              style={{ display: 'none' }}
              disabled={isProcessing}
            />

            <div className="dropzone-content">
              <div className="dropzone-icon">📄</div>
              <div className="dropzone-main-text">
                {isFileDragging ? 'Release to upload PDF now' : 'Drag & drop your PDF drawing here'}
              </div>
              <div className="dropzone-sub-text">
                or click anywhere inside this box to browse files
              </div>

              <button
                type="button"
                className="btn btn-primary browse-btn"
                onClick={(e) => {
                  e.stopPropagation();
                  fileInputRef.current?.click();
                }}
                disabled={isProcessing}
              >
                📁 Browse Files on Computer
              </button>

              <div className="dropzone-hints">
                Supported formats: Vector & Raster CAD PDFs (ANSI / ISO / ASME Y14.5M) • Up to 50MB
              </div>
            </div>
          </div>

          {isProcessing && (
            <div className="progress-container">
              <div className="progress-label">
                <span>⚡ Running AI Pipeline...</span>
                <span>{uploadProgress}%</span>
              </div>
              <div className="progress-track">
                <div
                  className="progress-bar-fill"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
              <div className="pipeline-steps-status">
                Ingestion ➔ Layout ROIs ➔ Vision OCR ➔ Spatial Graph ➔ Rule Verification
              </div>
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn btn-secondary" onClick={onClose} disabled={isProcessing}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
