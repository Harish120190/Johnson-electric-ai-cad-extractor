import React, { useRef, useState, useEffect } from 'react';

export default function DrawingCanvas({
  imageSrc,
  views = [],
  selectedView,
  onSelectView,
  highlightedBalloon,
  dimensions = []
}) {
  const containerRef = useRef(null);
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [showRoiBoxes, setShowRoiBoxes] = useState(true);

  // Reset view
  const handleReset = () => {
    setScale(1);
    setPosition({ x: 0, y: 0 });
  };

  const handleZoom = (factor) => {
    setScale((prev) => Math.min(Math.max(0.4, prev * factor), 4.5));
  };

  const handleMouseDown = (e) => {
    if (e.button !== 0) return; // Left click only
    setIsPanning(true);
    setDragStart({ x: e.clientX - position.x, y: e.clientY - position.y });
  };

  const handleMouseMove = (e) => {
    if (!isPanning) return;
    setPosition({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y
    });
  };

  const handleMouseUp = () => setIsPanning(false);

  return (
    <div className="canvas-wrapper">
      {/* Canvas Controls Toolbar */}
      <div className="canvas-toolbar">
        <button className="tool-btn" onClick={() => handleZoom(1.2)} title="Zoom In">🔍 +</button>
        <button className="tool-btn" onClick={() => handleZoom(0.8)} title="Zoom Out">🔍 -</button>
        <button className="tool-btn" onClick={handleReset} title="Fit to Screen">🔄 Reset</button>
        <button
          className={`tool-btn ${showRoiBoxes ? 'active' : ''}`}
          onClick={() => setShowRoiBoxes(!showRoiBoxes)}
          title="Toggle Semantic ROI Boxes"
        >
          🔲 {showRoiBoxes ? 'Hide ROIs' : 'Show ROIs'}
        </button>
        <span className="zoom-indicator">{Math.round(scale * 100)}%</span>
      </div>

      {/* Main Interactive Viewport */}
      <div
        className="canvas-viewport"
        ref={containerRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        style={{ cursor: isPanning ? 'grabbing' : 'grab' }}
      >
        <div
          className="canvas-content"
          style={{
            transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
            transformOrigin: 'top left'
          }}
        >
          {imageSrc ? (
            <img
              src={imageSrc}
              alt="Engineering Drawing"
              className="drawing-image"
              draggable={false}
            />
          ) : (
            <div className="canvas-placeholder">
              <div className="placeholder-icon">📐</div>
              <div className="placeholder-text">No Drawing Loaded</div>
            </div>
          )}

          {/* Semantic Functional ROI Overlays */}
          {showRoiBoxes && views.map((v) => {
            if (!v.bounding_box_norm || v.bounding_box_norm.length < 4) return null;
            const [ymin, xmin, ymax, xmax] = v.bounding_box_norm;
            const isSelected = selectedView === v.view_id;

            return (
              <div
                key={v.view_id}
                className={`roi-overlay ${isSelected ? 'selected' : ''}`}
                style={{
                  top: `${ymin * 100}%`,
                  left: `${xmin * 100}%`,
                  height: `${(ymax - ymin) * 100}%`,
                  width: `${(xmax - xmin) * 100}%`,
                }}
                onClick={(e) => {
                  e.stopPropagation();
                  onSelectView(v.view_id);
                }}
              >
                <span className="roi-tag">{v.view_name}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}

