/**
 * Frontend Configuration.
 * Handles environment-specific API endpoints and defaults.
 */

// Auto-detect backend API host:
// - When running Vite dev server on port 3000 -> proxy or direct http://localhost:8000
// - When running unified Python server -> relative ""
// - When deployed to Netlify -> relative or custom VITE_API_BASE_URL
export const API_BASE_URL = 
  (typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL) ||
  (typeof window !== 'undefined' && (window.location.port === '3000' || window.location.port === '5173')
    ? 'http://localhost:8000'
    : '');

export const APP_CONFIG = {
  appName: 'Johnson Electric 3D Drawing AI Extractor',
  version: '1.0.0',
  defaultSessionId: 'sample',
  maxUploadBytes: 50 * 1024 * 1024,
  allowedMimeTypes: ['application/pdf'],
};
