"""
Automated Integration Tests for Drawing Extractor Web Server API.
Tests all endpoints using mock requests against DrawingAppHandler.
"""

import unittest
import os
import json
import io
import csv
from app import DrawingAppHandler, SESSIONS, OUTPUT_DIR, BASE_DIR


class MockSocket:
    def makefile(self, *args, **kwargs):
        return io.BytesIO()


class MockRequest:
    def __init__(self, method, path, body=b"", headers=None):
        self.method = method
        self.path = path
        self.body = body
        self.headers = headers or {}


def execute_mock_request(method, path, body=b"", headers=None):
    """Executes a request against DrawingAppHandler using memory streams."""
    req_headers = headers or {}
    if body and "Content-Length" not in req_headers:
        req_headers["Content-Length"] = str(len(body))

    rfile = io.BytesIO(body)
    wfile = io.BytesIO()

    # Create uninitialized handler
    handler = DrawingAppHandler.__new__(DrawingAppHandler)
    handler.rfile = rfile
    handler.wfile = wfile
    handler.path = path
    handler.command = method
    handler.request_version = "HTTP/1.1"
    handler.requestline = f"{method} {path} HTTP/1.1"
    handler.client_address = ("127.0.0.1", 54321)
    handler.close_connection = True

    # Build HTTP headers structure
    header_lines = [f"{k}: {v}\r\n" for k, v in req_headers.items()]
    header_bytes = "".join(header_lines).encode("utf-8") + b"\r\n"
    from http.client import parse_headers
    handler.headers = parse_headers(io.BytesIO(header_bytes))

    # Route method
    if method == "GET":
        handler.do_GET()
    elif method == "POST":
        handler.do_POST()

    # Parse response from wfile
    wfile.seek(0)
    raw_response = wfile.read()
    
    # Split header and body
    parts = raw_response.split(b"\r\n\r\n", 1)
    status_line = parts[0].split(b"\r\n")[0].decode("utf-8")
    status_code = int(status_line.split()[1])
    resp_body = parts[1] if len(parts) > 1 else b""
    
    return status_code, resp_body, parts[0].decode("utf-8")


class TestServerAPI(unittest.TestCase):
    def test_serve_html_ui(self):
        code, body, headers = execute_mock_request("GET", "/")
        self.assertEqual(code, 200)
        self.assertIn("text/html", headers)
        self.assertIn(b"Johnson Electric", body)
        self.assertIn(b"Deliverable 1: Technical Solution Evaluation", body)

    def test_load_sample_endpoint(self):
        code, body, headers = execute_mock_request("POST", "/api/load-sample")
        self.assertEqual(code, 200)
        resp = json.loads(body.decode("utf-8"))
        self.assertEqual(resp["status"], "success")
        self.assertEqual(resp["session_id"], "sample")
        self.assertIn("data", resp)
        self.assertGreaterEqual(len(resp["data"]["dimensions"]), 40)
        self.assertIn("image_b64", resp)
        self.assertGreater(len(resp["image_b64"]), 1000)

    def test_export_json_endpoint(self):
        # Ensure sample exists
        execute_mock_request("POST", "/api/load-sample")
        code, body, headers = execute_mock_request("GET", "/api/export/json?session_id=sample")
        self.assertEqual(code, 200)
        self.assertIn("application/json", headers)
        data = json.loads(body.decode("utf-8"))
        self.assertEqual(data["metadata"]["title"], "Housing V1")
        self.assertEqual(len(data["dimensions"]), 68)

    def test_export_csv_endpoint(self):
        # Ensure sample exists
        execute_mock_request("POST", "/api/load-sample")
        code, body, headers = execute_mock_request("GET", "/api/export/csv?session_id=sample")
        self.assertEqual(code, 200)
        self.assertIn("text/csv", headers)
        csv_text = body.decode("utf-8")
        reader = csv.reader(io.StringIO(csv_text))
        rows = list(reader)
        self.assertGreaterEqual(len(rows), 40)
        header = rows[0]
        self.assertIn("Balloon Number", header)
        self.assertIn("Nominal Value", header)
        self.assertIn("Tolerance Symmetric", header)

    def test_get_session_endpoint(self):
        execute_mock_request("POST", "/api/load-sample")
        code, body, headers = execute_mock_request("GET", "/api/session/sample")
        self.assertEqual(code, 200)
        resp = json.loads(body.decode("utf-8"))
        self.assertEqual(resp["status"], "success")
        self.assertEqual(resp["filename"], "3D Drawing Example.pdf")

    def test_upload_endpoint(self):
        sample_pdf_path = os.path.join(BASE_DIR, "3D Drawing Example.pdf")
        with open(sample_pdf_path, "rb") as f:
            pdf_bytes = f.read()

        boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="Test_Upload.pdf"\r\n'
            f"Content-Type: application/pdf\r\n\r\n"
        ).encode("utf-8") + pdf_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body))
        }

        code, resp_bytes, resp_headers = execute_mock_request("POST", "/api/upload", body, headers)
        self.assertEqual(code, 200)
        resp = json.loads(resp_bytes.decode("utf-8"))
        self.assertEqual(resp["status"], "success")
        self.assertEqual(resp["filename"], "Test_Upload.pdf")
        self.assertIn("session_id", resp)
        self.assertGreaterEqual(len(resp["data"]["dimensions"]), 40)
        self.assertIn("image_b64", resp)

    def test_dynamic_upload_generic_drawing(self):
        sample_pdf_path = os.path.join(BASE_DIR, "3D Drawing Example.pdf")
        with open(sample_pdf_path, "rb") as f:
            pdf_bytes = f.read()

        boundary = "----WebKitFormBoundaryCustom987654"
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="file"; filename="Gearbox_Bracket_Assembly.pdf"\r\n'
            f"Content-Type: application/pdf\r\n\r\n"
        ).encode("utf-8") + pdf_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body))
        }

        code, resp_bytes, resp_headers = execute_mock_request("POST", "/api/upload", body, headers)
        self.assertEqual(code, 200)
        resp = json.loads(resp_bytes.decode("utf-8"))
        self.assertEqual(resp["status"], "success")
        self.assertEqual(resp["filename"], "Gearbox_Bracket_Assembly.pdf")
        self.assertEqual(resp["data"]["metadata"]["title"], "Gearbox Bracket Assembly")
        self.assertIn("session_id", resp)
        self.assertIn("segmented_rois", resp["data"])
        self.assertGreaterEqual(len(resp["data"]["dimensions"]), 15)
        self.assertIn("image_b64", resp)
        self.assertTrue(resp["data"]["validation"]["validation_passed"])

    def test_not_found(self):
        code, body, headers = execute_mock_request("GET", "/api/unknown-endpoint")
        self.assertEqual(code, 404)


if __name__ == "__main__":
    unittest.main()
