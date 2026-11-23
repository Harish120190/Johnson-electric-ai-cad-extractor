import React, { useState, useEffect } from 'react';
import { api } from './services/api';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import DrawingCanvas from './components/DrawingCanvas';
import DimensionsTable from './components/DimensionsTable';
import GdtCards from './components/GdtCards';
import UploadModal from './components/UploadModal';
import DeliverablesViewer from './components/DeliverablesViewer';

export default function App() {
  const [activeTab, setActiveTab] = useState('prototype');
  const [drawingData, setDrawingData] = useState(null);
  const [imageSrc, setImageSrc] = useState(null);
  const [sessionId, setSessionId] = useState('sample');
  const [isProcessing, setIsProcessing] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');

  // Filtering states
  const [selectedView, setSelectedView] = useState('ALL');
  const [selectedFeature, setSelectedFeature] = useState('ALL');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [highlightedBalloon, setHighlightedBalloon] = useState(null);

  // Load sample on mount
  useEffect(() => {
    loadSampleData();
  }, []);

  const loadSampleData = async () => {
    setIsProcessing(true);
    setStatusMessage('Loading canonical 3D Drawing sample...');
    try {
      const resp = await api.loadSample();
      if (resp?.data) {
        setDrawingData(resp.data);
        setSessionId(resp.session_id || 'sample');
        if (resp.image_b64) {
          setImageSrc(`data:image/png;base64,${resp.image_b64}`);
        } else {
          setImageSrc('/drawing_normalized.png');
        }
        setStatusMessage('Sample loaded successfully.');
      }
    } catch (err) {
      console.warn('Backend loadSample failed, attempting local fallback:', err);
      try {
        const localResp = await fetch('/extracted_drawing_data.json');
        if (localResp.ok) {
          const data = await localResp.json();
          setDrawingData(data);
          setImageSrc('/drawing_normalized.png');
          setSessionId('sample');
          setStatusMessage('Sample loaded from local cache.');
        }
      } catch (e) {
        setStatusMessage('Error loading drawing data.');
      }
    } finally {
      setIsProcessing(false);
    }
  };

  const handleUploadFile = async (file) => {
    if (!file) return;
    setIsProcessing(true);
    setUploadProgress(15);
    setStatusMessage(`Uploading ${file.name}...`);

    const progressTimer = setInterval(() => {
      setUploadProgress((prev) => (prev < 90 ? prev + 15 : prev));
    }, 400);

    try {
      let resp;
      try {
        resp = await api.uploadDrawing(file);
      } catch (networkErr) {
        console.warn('Backend upload unreachable, executing client fallback:', networkErr);
        resp = await api.processClientSideFallback(file);
      }

      clearInterval(progressTimer);
      setUploadProgress(100);

      if (resp && resp.data) {
        setDrawingData(resp.data);
        setSessionId(resp.session_id);
        if (resp.image_b64) {
          setImageSrc(`data:image/png;base64,${resp.image_b64}`);
        } else {
          setImageSrc('/drawing_normalized.png');
        }
        setStatusMessage(`Successfully extracted ${resp.filename || file.name}`);
        setTimeout(() => {
          setIsUploadOpen(false);
          setUploadProgress(0);
        }, 600);
      }
    } catch (err) {
      clearInterval(progressTimer);
      alert(`Upload failed: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  // Filter dimensions
  const filteredDimensions = (drawingData?.dimensions || []).filter((dim) => {
    if (selectedView !== 'ALL' && dim.associated_view !== selectedView) {
      return false;
    }
    if (selectedFeature !== 'ALL' && dim.associated_feature !== selectedFeature) {
      return false;
    }
    if (selectedCategory !== 'All' && dim.dimension_range_category !== selectedCategory) {
      return false;
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      const matchBalloon = String(dim.balloon_number).includes(q);
      const matchVal = String(dim.nominal_value).includes(q);
      const matchFeature = (dim.associated_feature || '').toLowerCase().includes(q);
      const matchRaw = (dim.raw_string || '').toLowerCase().includes(q);
      if (!matchBalloon && !matchVal && !matchFeature && !matchRaw) return false;
    }
    return true;
  });

  return (
    <div className="app-container">
      <Navbar
        metadata={drawingData?.metadata}
        onOpenUpload={() => setIsUploadOpen(true)}
        onLoadSample={loadSampleData}
        onExportJson={() => api.exportJson(sessionId)}
        onExportCsv={() => api.exportCsv(sessionId)}
        isProcessing={isProcessing}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
      />

      {statusMessage && (
        <div className="status-bar">
          <span>{statusMessage}</span>
          <button className="status-close" onClick={() => setStatusMessage('')}>✕</button>
        </div>
      )}

      {activeTab === 'prototype' ? (
        <main className="main-layout">
          <Sidebar
            views={drawingData?.views || []}
            features={drawingData?.features || []}
            dimensionsCount={filteredDimensions.length}
            gdtCount={drawingData?.gdt_frames?.length || 0}
            confidenceScore={drawingData?.validation?.confidence_score || 1.0}
            selectedView={selectedView}
            setSelectedView={setSelectedView}
            selectedFeature={selectedFeature}
            setSelectedFeature={setSelectedFeature}
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            selectedCategory={selectedCategory}
            setSelectedCategory={setSelectedCategory}
          />

          <section className="workbench-content">
            <div className="canvas-panel">
              <DrawingCanvas
                imageSrc={imageSrc}
                views={drawingData?.views || []}
                selectedView={selectedView}
                onSelectView={setSelectedView}
                highlightedBalloon={highlightedBalloon}
                dimensions={filteredDimensions}
              />
            </div>

            <div className="data-panel">
              <GdtCards gdtFrames={drawingData?.gdt_frames || []} />
              <DimensionsTable
                dimensions={filteredDimensions}
                highlightedBalloon={highlightedBalloon}
                onHighlightBalloon={setHighlightedBalloon}
              />
            </div>
          </section>
        </main>
      ) : (
        <DeliverablesViewer activeTab={activeTab} />
      )}

      <UploadModal
        isOpen={isUploadOpen}
        onClose={() => setIsUploadOpen(false)}
        onUploadFile={handleUploadFile}
        isProcessing={isProcessing}
        uploadProgress={uploadProgress}
      />
    </div>
  );
}
