"""
Web UI Application Server for 3D Engineering Drawing AI Extractor.
Zero-dependency, production-grade HTTP server built using Python standard library.
Provides drag-and-drop PDF upload, instant sample processing, interactive visual inspection,
filtering, rule validation, and multi-format export (JSON / CSV).
"""

import os
import sys
import json
import uuid
import base64
import email
import email.policy
import csv
import io
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Import extraction pipeline
from run_pipeline import run_pipeline

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_PDF = os.path.join(BASE_DIR, "3D Drawing Example.pdf")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cache for active sessions
SESSIONS = {}

# Preload sample session if existing output is present
sample_json_path = os.path.join(OUTPUT_DIR, "extracted_drawing_data.json")
if os.path.exists(sample_json_path):
    try:
        with open(sample_json_path, "r", encoding="utf-8") as f:
            SESSIONS["sample"] = {
                "result": json.load(f),
                "output_dir": OUTPUT_DIR,
                "pdf_name": "3D Drawing Example.pdf"
            }
    except Exception as e:
        print(f"Warning: Failed to preload sample output: {e}")


class DrawingAppHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Clean production logging
        sys.stderr.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          self.log_date_time_string(),
                          format % args))

    def address_string(self):
        if hasattr(self, 'client_address') and self.client_address:
            return str(self.client_address[0])
        return "127.0.0.1"

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        if path == "/" or path == "/index.html":
            self.serve_html_ui()
        elif path == "/api/sample":
            self.handle_load_sample()
        elif path.startswith("/api/session/"):
            session_id = path.split("/api/session/")[-1]
            self.handle_get_session(session_id)
        elif path == "/api/export/json":
            session_id = query.get("session_id", ["sample"])[0]
            self.handle_export_json(session_id)
        elif path == "/api/export/csv":
            session_id = query.get("session_id", ["sample"])[0]
            self.handle_export_csv(session_id)
        elif path.startswith("/images/"):
            # Serve images from session or output directory
            rel_img = path[len("/images/"):]
            self.serve_image(rel_img)
        else:
            self.send_error(404, "Not Found")

    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Access-Control-Max-Age", "86400")
        self.end_headers()

    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == "/api/upload":
            self.handle_upload_pdf()
        elif path == "/api/load-sample":
            self.handle_load_sample()
        else:
            self.send_error(404, "Not Found")

    def handle_upload_pdf(self):
        """Processes multipart uploaded PDF and executes extraction pipeline."""
        content_type = self.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            self.send_json_response({"error": "Expected multipart/form-data"}, 400)
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)

            # Parse multipart body using standard library email parser
            header_bytes = f"Content-Type: {content_type}\r\n".encode()
            msg = email.message_from_bytes(header_bytes + body, policy=email.policy.default)

            pdf_bytes = None
            filename = "uploaded_drawing.pdf"

            for part in msg.iter_parts():
                fn = part.get_filename()
                if fn and fn.lower().endswith(".pdf"):
                    filename = fn
                    pdf_bytes = part.get_payload(decode=True)
                    break
                elif part.get_content_type() == "application/pdf":
                    pdf_bytes = part.get_payload(decode=True)
                    if fn:
                        filename = fn
                    break

            if not pdf_bytes:
                # Fallback check for any file part
                for part in msg.iter_parts():
                    payload = part.get_payload(decode=True)
                    if payload and payload.startswith(b"%PDF"):
                        pdf_bytes = payload
                        filename = part.get_filename() or "uploaded_drawing.pdf"
                        break

            if not pdf_bytes:
                self.send_json_response({"error": "No valid PDF file found in upload payload."}, 400)
                return

            # Save uploaded PDF to unique session directory
            session_id = str(uuid.uuid4())[:8]
            session_dir = os.path.join(UPLOADS_DIR, session_id)
            os.makedirs(session_dir, exist_ok=True)

            pdf_path = os.path.join(session_dir, filename)
            with open(pdf_path, "wb") as f:
                f.write(pdf_bytes)

            print(f"📥 Received PDF upload: {filename} ({len(pdf_bytes)} bytes) -> Session {session_id}")

            # Run full extraction pipeline
            result_dict = run_pipeline(pdf_path, session_dir)

            # Store session
            SESSIONS[session_id] = {
                "result": result_dict,
                "output_dir": session_dir,
                "pdf_name": filename
            }

            # Return success with session data and image base64
            norm_img_path = os.path.join(session_dir, "drawing_normalized.png")
            if not os.path.exists(norm_img_path):
                norm_img_path = os.path.join(session_dir, "rasterized_highres.png")

            with open(norm_img_path, "rb") as img_f:
                b64_drawing = base64.b64encode(img_f.read()).decode("utf-8")

            self.send_json_response({
                "status": "success",
                "session_id": session_id,
                "filename": filename,
                "data": result_dict,
                "image_b64": b64_drawing
            })

        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_json_response({"error": f"Extraction failed: {str(e)}"}, 500)

    def handle_load_sample(self):
        """Loads and processes or retrieves the sample 3D Drawing Example.pdf."""
        try:
            sample_session = SESSIONS.get("sample")
            if not sample_session or not os.path.exists(os.path.join(OUTPUT_DIR, "extracted_drawing_data.json")):
                print("⚡ Running pipeline on sample PDF...")
                result_dict = run_pipeline(SAMPLE_PDF, OUTPUT_DIR)
                sample_session = {
                    "result": result_dict,
                    "output_dir": OUTPUT_DIR,
                    "pdf_name": "3D Drawing Example.pdf"
                }
                SESSIONS["sample"] = sample_session
            else:
                result_dict = sample_session["result"]

            norm_img_path = os.path.join(OUTPUT_DIR, "drawing_normalized.png")
            if not os.path.exists(norm_img_path):
                norm_img_path = os.path.join(OUTPUT_DIR, "rasterized_highres.png")

            with open(norm_img_path, "rb") as img_f:
                b64_drawing = base64.b64encode(img_f.read()).decode("utf-8")

            self.send_json_response({
                "status": "success",
                "session_id": "sample",
                "filename": "3D Drawing Example.pdf",
                "data": result_dict,
                "image_b64": b64_drawing
            })
        except Exception as e:
            import traceback
            traceback.print_exc()
            self.send_json_response({"error": f"Failed to load sample: {str(e)}"}, 500)

    def handle_get_session(self, session_id):
        session = SESSIONS.get(session_id)
        if not session:
            self.send_json_response({"error": "Session not found"}, 404)
            return

        norm_img_path = os.path.join(session["output_dir"], "drawing_normalized.png")
        if not os.path.exists(norm_img_path):
            norm_img_path = os.path.join(session["output_dir"], "rasterized_highres.png")

        with open(norm_img_path, "rb") as img_f:
            b64_drawing = base64.b64encode(img_f.read()).decode("utf-8")

        self.send_json_response({
            "status": "success",
            "session_id": session_id,
            "filename": session["pdf_name"],
            "data": session["result"],
            "image_b64": b64_drawing
        })

    def handle_export_json(self, session_id):
        session = SESSIONS.get(session_id)
        if not session:
            self.send_error(404, "Session not found")
            return
        data_bytes = json.dumps(session["result"], indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Disposition", f'attachment; filename="extracted_{session_id}.json"')
        self.send_header("Content-Length", str(len(data_bytes)))
        self.end_headers()
        self.wfile.write(data_bytes)

    def handle_export_csv(self, session_id):
        session = SESSIONS.get(session_id)
        if not session:
            self.send_error(404, "Session not found")
            return

        dimensions = session["result"].get("dimensions", [])
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Balloon Number",
            "Nominal Value",
            "Tolerance Symmetric",
            "Tolerance Upper",
            "Tolerance Lower",
            "Unit",
            "Dimension Type",
            "Series Category",
            "Associated View",
            "Associated Feature",
            "Measurement Note",
            "Raw Callout String"
        ])
        for d in dimensions:
            writer.writerow([
                d.get("balloon_number"),
                d.get("nominal_value"),
                d.get("tolerance_symmetric") or "",
                d.get("tolerance_upper") or "",
                d.get("tolerance_lower") or "",
                d.get("unit"),
                d.get("dimension_type"),
                d.get("dimension_range_category"),
                d.get("associated_view"),
                d.get("associated_feature") or "",
                d.get("measurement_note") or "",
                d.get("raw_string")
            ])

        csv_bytes = output.getvalue().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/csv")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Disposition", f'attachment; filename="dimensions_{session_id}.csv"')
        self.send_header("Content-Length", str(len(csv_bytes)))
        self.end_headers()
        self.wfile.write(csv_bytes)

    def serve_image(self, rel_path):
        # Look in sessions or output
        full_path = os.path.join(OUTPUT_DIR, rel_path)
        if not os.path.exists(full_path):
            full_path = os.path.join(UPLOADS_DIR, rel_path)

        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            self.send_error(404, "Image Not Found")
            return

        mime_type, _ = mimetypes.guess_type(full_path)
        mime_type = mime_type or "image/png"

        with open(full_path, "rb") as f:
            data = f.read()

        self.send_response(200)
        self.send_header("Content-Type", mime_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json_response(self, data, status_code=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_html_ui(self):
        html_file = os.path.join(BASE_DIR, "frontend", "index.html")
        with open(html_file, "rb") as f:
            body = f.read()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run_server(port=8000):
    server_address = ("", port)
    httpd = HTTPServer(server_address, DrawingAppHandler)
    print("=" * 70)
    print("🚀 JOHNSON ELECTRIC 3D DRAWING AI EXTRACTOR - WEB UI SERVER")
    print("=" * 70)
    print(f"🌐 Server running at: http://localhost:{port}")
    print("👉 Open your browser to upload PDFs or inspect extracted structured data")
    print("=" * 70)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
        httpd.server_close()


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            pass
    run_server(port)

