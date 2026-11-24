import React from 'react';

export default function GdtCards({ gdtFrames = [] }) {
  if (!gdtFrames || gdtFrames.length === 0) {
    return null;
  }

  const getSymbolIcon = (sym) => {
    switch (sym?.toUpperCase()) {
      case 'POSITION':
        return '⌖';
      case 'FLATNESS':
        return '⏥';
      case 'CYLINDRICITY':
        return '⌭';
      case 'PERPENDICULARITY':
        return '⟂';
      case 'PARALLELISM':
        return '∥';
      case 'RUNOUT':
        return '↗';
      default:
        return '⌖';
    }
  };

  return (
    <div className="gdt-section">
      <div className="section-title">ASME Y14.5 GD&T Feature Control Frames</div>
      <div className="gdt-grid">
        {gdtFrames.map((f, idx) => (
          <div key={f.frame_id || idx} className="gdt-card">
            <div className="fcf-box">
              <div className="fcf-cell fcf-sym" title={f.symbol}>
                {getSymbolIcon(f.symbol)}
              </div>
              <div className="fcf-cell fcf-tol">
                Ø{f.tolerance_value?.toFixed(2) || f.tolerance_value}
              </div>
              {f.datums && f.datums.length > 0 ? (
                f.datums.map((d, dIdx) => (
                  <div key={dIdx} className="fcf-cell fcf-datum">
                    {d}
                  </div>
                ))
              ) : (
                <div className="fcf-cell fcf-form">Form</div>
              )}
            </div>
            <div className="gdt-meta">
              <span className="gdt-name">{f.symbol}</span>
              <span className="gdt-view">{f.associated_view || 'Main Drawing'}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

