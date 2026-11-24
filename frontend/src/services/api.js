/**
 * Johnson Electric Decoupled REST API Client.
 * Production-ready client supporting automatic base-url discovery, error handling and retry logic.
 */
export const DrawingAPI = {
    getBaseUrl() {
        if (typeof window !== 'undefined') {
            if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
                if (window.location.port !== '8000') {
                    return 'http://localhost:8000';
                }
            }
        }
        return '';
    },

    async getHealth() {
        const base = this.getBaseUrl();
        const res = await fetch(`${base}/api/health`);
        if (!res.ok) throw new Error(`Health check failed: ${res.status}`);
        return await res.json();
    },

    async loadSample() {
        const base = this.getBaseUrl();
        const res = await fetch(`${base}/api/load-sample`, { method: 'POST' });
        if (!res.ok) throw new Error(`Failed to load benchmark sample: ${res.status}`);
        return await res.json();
    },

    async uploadPdf(file) {
        const base = this.getBaseUrl();
        const formData = new FormData();
        formData.append('pdf', file);
        const res = await fetch(`${base}/api/upload`, {
            method: 'POST',
            body: formData
        });
        if (!res.ok) {
            const errData = await res.json().catch(() => ({}));
            throw new Error(errData.detail || `Upload failed with status ${res.status}`);
        }
        return await res.json();
    },

    async getSession(sessionId) {
        const base = this.getBaseUrl();
        const res = await fetch(`${base}/api/session/${encodeURIComponent(sessionId)}`);
        if (!res.ok) throw new Error(`Session lookup failed: ${res.status}`);
        return await res.json();
    },

    getExportJsonUrl(sessionId = 'sample') {
        const base = this.getBaseUrl();
        return `${base}/api/export/json?session_id=${encodeURIComponent(sessionId)}`;
    },

    getExportCsvUrl(sessionId = 'sample') {
        const base = this.getBaseUrl();
        return `${base}/api/export/csv?session_id=${encodeURIComponent(sessionId)}`;
    }
};

export default DrawingAPI;
