import React, { useState } from 'react';

export default function DimensionsTable({
  dimensions = [],
  highlightedBalloon,
  onHighlightBalloon
}) {
  const [sortField, setSortField] = useState('balloon_number');
  const [sortAsc, setSortAsc] = useState(true);

  const handleSort = (field) => {
    if (sortField === field) {
      setSortAsc(!sortAsc);
    } else {
      setSortField(field);
      setSortAsc(true);
    }
  };

  const sorted = [...dimensions].sort((a, b) => {
    let valA = a[sortField];
    let valB = b[sortField];

    if (valA === undefined || valA === null) valA = '';
    if (valB === undefined || valB === null) valB = '';

    if (typeof valA === 'number' && typeof valB === 'number') {
      return sortAsc ? valA - valB : valB - valA;
    }
    return sortAsc
      ? String(valA).localeCompare(String(valB))
      : String(valB).localeCompare(String(valA));
  });

  const formatTolerance = (d) => {
    if (d.tolerance_symmetric !== null && d.tolerance_symmetric !== undefined) {
      return `±${d.tolerance_symmetric}`;
    }
    if (d.tolerance_upper !== undefined && d.tolerance_lower !== undefined) {
      const up = d.tolerance_upper >= 0 ? `+${d.tolerance_upper}` : `${d.tolerance_upper}`;
      const lo = d.tolerance_lower > 0 ? `+${d.tolerance_lower}` : `${d.tolerance_lower}`;
      return `${up} / ${lo}`;
    }
    return '—';
  };

  return (
    <div className="table-wrapper">
      <div className="table-header-info">
        <span className="count-badge">Showing {dimensions.length} Dimensions</span>
      </div>

      <div className="table-scroll">
        <table className="dimensions-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('balloon_number')}>
                # Balloon {sortField === 'balloon_number' ? (sortAsc ? '▲' : '▼') : ''}
              </th>
              <th onClick={() => handleSort('nominal_value')}>
                Nominal {sortField === 'nominal_value' ? (sortAsc ? '▲' : '▼') : ''}
              </th>
              <th>Tolerance</th>
              <th>Unit</th>
              <th onClick={() => handleSort('dimension_type')}>
                Type {sortField === 'dimension_type' ? (sortAsc ? '▲' : '▼') : ''}
              </th>
              <th onClick={() => handleSort('associated_feature')}>
                Feature {sortField === 'associated_feature' ? (sortAsc ? '▲' : '▼') : ''}
              </th>
              <th>View Reference</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((dim) => {
              const isSelected = highlightedBalloon === dim.balloon_number;
              return (
                <tr
                  key={dim.balloon_number}
                  className={isSelected ? 'selected-row' : ''}
                  onClick={() => onHighlightBalloon(dim.balloon_number)}
                >
                  <td>
                    <span className="balloon-bubble">{dim.balloon_number}</span>
                  </td>
                  <td className="nominal-val">{dim.nominal_value.toFixed(2)}</td>
                  <td className="tol-val">{formatTolerance(dim)}</td>
                  <td>{dim.unit || 'mm'}</td>
                  <td>
                    <span className={`type-badge badge-${dim.dimension_type || 'linear'}`}>
                      {dim.dimension_type}
                    </span>
                  </td>
                  <td>{dim.associated_feature || 'General Housing'}</td>
                  <td className="view-ref">{dim.associated_view}</td>
                </tr>
              );
            })}
            {sorted.length === 0 && (
              <tr>
                <td colSpan={7} className="no-data">
                  No dimensions match current filters.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

