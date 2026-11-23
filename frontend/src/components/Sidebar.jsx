import React from 'react';

export default function Sidebar({
  views = [],
  features = [],
  dimensionsCount = 0,
  gdtCount = 0,
  confidenceScore = 1.0,
  selectedView,
  setSelectedView,
  selectedFeature,
  setSelectedFeature,
  searchQuery,
  setSearchQuery,
  selectedCategory,
  setSelectedCategory
}) {
  const categories = ['All', 'Precision', 'Fine', 'Standard', 'Coarse'];

  return (
    <aside className="sidebar">
      {/* Quick Metrics */}
      <div className="sidebar-section">
        <div className="section-title">Extraction Metrics</div>
        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-val">{dimensionsCount}</div>
            <div className="metric-label">Dimensions</div>
          </div>
          <div className="metric-card">
            <div className="metric-val">{gdtCount}</div>
            <div className="metric-label">GD&T Frames</div>
          </div>
          <div className="metric-card">
            <div className="metric-val">{(confidenceScore * 100).toFixed(0)}%</div>
            <div className="metric-label">Rule Confidence</div>
          </div>
          <div className="metric-card">
            <div className="metric-val">{views.length}</div>
            <div className="metric-label">CAD Views</div>
          </div>
        </div>
      </div>

      {/* Search Input */}
      <div className="sidebar-section">
        <div className="section-title">Search Callouts</div>
        <input
          type="text"
          className="search-input"
          placeholder="Search by value, balloon, feature..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>

      {/* Filter by Drawing View */}
      <div className="sidebar-section">
        <div className="section-title">Filter by CAD View</div>
        <div className="filter-list">
          <button
            className={`filter-chip ${selectedView === 'ALL' ? 'active' : ''}`}
            onClick={() => setSelectedView('ALL')}
          >
            All Views ({views.length})
          </button>
          {views.map((v) => (
            <button
              key={v.view_id}
              className={`filter-chip ${selectedView === v.view_id ? 'active' : ''}`}
              onClick={() => setSelectedView(v.view_id)}
            >
              {v.view_name}
            </button>
          ))}
        </div>
      </div>

      {/* Filter by Semantic Feature */}
      <div className="sidebar-section">
        <div className="section-title">Filter by Feature</div>
        <div className="filter-list">
          <button
            className={`filter-chip ${selectedFeature === 'ALL' ? 'active' : ''}`}
            onClick={() => setSelectedFeature('ALL')}
          >
            All Features
          </button>
          {features.map((f) => (
            <button
              key={f.feature_id}
              className={`filter-chip ${selectedFeature === f.feature_id ? 'active' : ''}`}
              onClick={() => setSelectedFeature(f.feature_id)}
            >
              {f.feature_name}
            </button>
          ))}
        </div>
      </div>

      {/* Filter by Tolerance Category */}
      <div className="sidebar-section">
        <div className="section-title">Tolerance Category</div>
        <div className="filter-chips-row">
          {categories.map((cat) => (
            <button
              key={cat}
              className={`chip-small ${selectedCategory === cat ? 'active' : ''}`}
              onClick={() => setSelectedCategory(cat)}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>
    </aside>
  );
}
