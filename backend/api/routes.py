"""
Backend API HTTP request router and dispatcher.
Maps RESTful routes to their corresponding controller methods.
"""

import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from backend.api.controllers import (
    HealthController,
    UploadController,
    SampleController,
    SessionController,
    ExportController,
    StaticController
)
from backend.config import BASE_DIR, OUTPUT_DIR, FRONTEND_DIR, CORS_ORIGIN, ALLOWED_METHODS, ALLOWED_HEADERS

class BackendApiHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Structured server request log
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))

    def address_string(self):
        if hasattr(self, 'client_address') and self.client_address:
            return str(self.client_address[0])
        return "127.0.0.1"

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", CORS_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", ALLOWED_METHODS)
        self.send_header("Access-Control-Allow-Headers", ALLOWED_HEADERS)
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        # API Endpoints
        if path == "/api/health":
            HealthController.get_health(self)
        elif path == "/api/sample":
            SampleController.handle_sample(self)
        elif path.startswith("/api/session/"):
            session_id = path[len("/api/session/"):]
            SessionController.handle_get_session(self, session_id)
        elif path == "/api/export/json":
            session_id = query.get("session_id", ["sample"])[0]
            ExportController.export_json(self, session_id)
        elif path == "/api/export/csv":
            session_id = query.get("session_id", ["sample"])[0]
            ExportController.export_csv(self, session_id)

        # Static Assets & Frontend Integration
        elif path in ("/", "/index.html"):
            StaticController.serve_frontend(self)
        elif path == "/demo.html":
            StaticController.serve_static_file(
                self, os.path.join(FRONTEND_DIR, "demo.html"), "text/html; charset=utf-8"
            )
        elif path == "/favicon.ico":
            self.send_response(204)
            self.end_headers()
        elif path == "/drawing_normalized.png":
            StaticController.serve_static_file(
                self, os.path.join(OUTPUT_DIR, "drawing_normalized.png"), "image/png"
            )
        elif path == "/extracted_drawing_data.json":
            StaticController.serve_static_file(
                self, os.path.join(OUTPUT_DIR, "extracted_drawing_data.json"), "application/json"
            )
        elif path.startswith("/images/"):
            rel_img = path[len("/images/"):]
            StaticController.serve_image(self, rel_img)
        else:
            self.send_error(404, "Endpoint Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/upload":
            UploadController.handle_upload(self)
        elif path == "/api/load-sample":
            SampleController.handle_sample(self)
        else:
            self.send_error(404, "Endpoint Not Found")
