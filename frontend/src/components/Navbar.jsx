import React from 'react';

export default function Navbar({
  metadata,
  onOpenUpload,
  onLoadSample,
  onExportJson,
  onExportCsv,
  isProcessing,
  activeTab,
  setActiveTab
}) {
  return (
    <header className="navbar">
      <div className="nav-brand">
        <div className="brand-logo">⚡</div>
        <div className="brand-text">
          <div className="brand-title">Johnson Electric</div>
          <div className="brand-subtitle">3D Engineering Drawing AI Extractor</div>
        </div>
      </div>

      <div className="nav-tabs">
        <button
          className={`tab-btn ${activeTab === 'prototype' ? 'active' : ''}`}
          onClick={() => setActiveTab('prototype')}
        >
          🚀 AI Extractor Prototype
        </button>
        <button
          className={`tab-btn ${activeTab === 'evaluation' ? 'active' : ''}`}
          onClick={() => setActiveTab('evaluation')}
        >
          📋 Solution Evaluation (Deliv. 1)
        </button>
        <button
          className={`tab-btn ${activeTab === 'architecture' ? 'active' : ''}`}
          onClick={() => setActiveTab('architecture')}
        >
          🏗️ Architecture (Deliv. 2)
        </button>
      </div>

      <div className="nav-actions">
        {metadata?.drawing_id && (
          <span className="part-badge">
            Part: <strong>{metadata.part_name || 'Housing V1'}</strong> ({metadata.drawing_id})
          </span>
        )}

        <button
          className="btn btn-secondary"
          onClick={onLoadSample}
          disabled={isProcessing}
          title="Reload the canonical 3D Drawing Example PDF"
        >
          🔄 Sample
        </button>

        <button
          className="btn btn-primary"
          onClick={onOpenUpload}
          disabled={isProcessing}
        >
          ⬆ Upload PDF
        </button>

        <div className="dropdown">
          <button className="btn btn-secondary" disabled={isProcessing}>
            💾 Export ▾
          </button>
          <div className="dropdown-menu">
            <button onClick={onExportJson}>Export Structured JSON</button>
            <button onClick={onExportCsv}>Export Dimensions CSV</button>
          </div>
        </div>
      </div>
    </header>
  );
}
