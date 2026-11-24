"""
Unit and Integration Tests for backend/ package modules.
Tests Config, Serializers, SessionService, ExtractionService, and Controllers.
"""

import unittest
import os
import json
import io
from backend.config import BASE_DIR, OUTPUT_DIR, UPLOADS_DIR
from backend.services.session_service import SessionService
from backend.api.serializers import Serializer
from backend.api.routes import BackendApiHandler


class MockRequest:
    def __init__(self, method, path, body=b"", headers=None):
        self.method = method
        self.path = path
        self.body = body
        self.headers = headers or {}


def execute_backend_request(method, path, body=b"", headers=None):
    req_headers = headers or {}
    if body and "Content-Length" not in req_headers:
        req_headers["Content-Length"] = str(len(body))

    rfile = io.BytesIO(body)
    wfile = io.BytesIO()

    handler = BackendApiHandler.__new__(BackendApiHandler)
    handler.rfile = rfile
    handler.wfile = wfile
    handler.path = path
    handler.command = method
    handler.request_version = "HTTP/1.1"
    handler.requestline = f"{method} {path} HTTP/1.1"
    handler.client_address = ("127.0.0.1", 54321)
    handler.close_connection = True

    header_lines = [f"{k}: {v}\r\n" for k, v in req_headers.items()]
    header_bytes = "".join(header_lines).encode("utf-8") + b"\r\n"
    from http.client import parse_headers
    handler.headers = parse_headers(io.BytesIO(header_bytes))

    if method == "GET":
        handler.do_GET()
    elif method == "POST":
        handler.do_POST()
    elif method == "OPTIONS":
        handler.do_OPTIONS()

    wfile.seek(0)
    raw = wfile.read()
    parts = raw.split(b"\r\n\r\n", 1)
    status_line = parts[0].split(b"\r\n")[0].decode("utf-8")
    status_code = int(status_line.split()[1])
    resp_body = parts[1] if len(parts) > 1 else b""
    return status_code, resp_body, parts[0].decode("utf-8")


class TestBackendPackage(unittest.TestCase):
    def test_health_endpoint(self):
        code, body, headers = execute_backend_request("GET", "/api/health")
        self.assertEqual(code, 200)
        self.assertIn("application/json", headers)
        data = json.loads(body.decode("utf-8"))
        self.assertEqual(data["status"], "healthy")
        self.assertIn("johnson-electric", data["service"])
        self.assertEqual(data["version"], "1.0.0")

    def test_cors_options_preflight(self):
        code, body, headers = execute_backend_request("OPTIONS", "/api/upload")
        self.assertEqual(code, 200)
        self.assertIn("Access-Control-Allow-Origin: *", headers)
        self.assertIn("Access-Control-Allow-Methods", headers)

    def test_serializers_json(self):
        test_obj = {"key": "value", "count": 42}
        b = Serializer.to_json_bytes(test_obj)
        self.assertIsInstance(b, bytes)
        self.assertEqual(json.loads(b.decode("utf-8")), test_obj)

    def test_serializers_csv(self):
        test_dims = [{
            "balloon_number": 1,
            "nominal_value": 25.4,
            "tolerance_symmetric": 0.1,
            "tolerance_upper": 0.1,
            "tolerance_lower": -0.1,
            "unit": "mm",
            "dimension_type": "linear",
            "dimension_range_category": "Standard",
            "associated_view": "top_view",
            "associated_feature": "Slot",
            "measurement_note": "",
            "raw_string": "25.4 ± 0.1"
        }]
        csv_b = Serializer.dimensions_to_csv_bytes(test_dims)
        text = csv_b.decode("utf-8")
        self.assertIn("Balloon Number", text)
        self.assertIn("25.4", text)

    def test_session_service_cache(self):
        SessionService.store_session("test_sess", {"mock": True}, "/tmp", "test.pdf")
        retrieved = SessionService.get_session("test_sess")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["pdf_name"], "test.pdf")

    def test_frontend_static_serving(self):
        code, body, headers = execute_backend_request("GET", "/")
        self.assertEqual(code, 200)
        self.assertIn("text/html", headers)
        self.assertIn(b"app.bundle.js", body)

    def test_demo_html_serving(self):
        code, body, headers = execute_backend_request("GET", "/demo.html")
        self.assertEqual(code, 200)
        self.assertIn("text/html", headers)
        self.assertIn(b"Johnson Electric", body)
        self.assertIn(b"Record 1080p WebM", body)

    def test_bundle_asset_serving(self):
        code, body, headers = execute_backend_request("GET", "/app.bundle.js")
        self.assertEqual(code, 200)
        self.assertIn("application/javascript", headers)
        self.assertTrue(len(body) > 10000)

    def test_stylesheet_asset_serving(self):
        code, body, headers = execute_backend_request("GET", "/styles/app.css")
        self.assertEqual(code, 200)
        self.assertIn("text/css", headers)
        self.assertIn(b"--bg-base", body)

    def test_path_traversal_protection(self):
        code, body, headers = execute_backend_request("GET", "/styles/../../backend/server.py")
        self.assertIn(code, (403, 404))


if __name__ == "__main__":
    unittest.main()

