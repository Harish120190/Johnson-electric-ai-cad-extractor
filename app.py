"""
Root Entrypoint for Johnson Electric 3D Drawing AI Extractor.
Delegates cleanly to the modular backend package while maintaining full
backward compatibility for existing scripts, tests, and runners.
"""

import sys
from backend.config import BASE_DIR, OUTPUT_DIR, UPLOADS_DIR, SAMPLE_PDF, DEFAULT_PORT
from backend.services.session_service import SessionService
from backend.api.routes import BackendApiHandler
from backend.server import run_server, ThreadedApiServer

# Backward-compatible aliases for tests and external scripts
DrawingAppHandler = BackendApiHandler
ThreadedHTTPServer = ThreadedApiServer
SESSIONS = SessionService.get_all_sessions()

if __name__ == "__main__":
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port=port)
