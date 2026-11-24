"""
Controllers for API endpoints.
Encapsulates HTTP business logic and decouples from transport layer.
"""

import os
import email
import email.policy
import traceback
import mimetypes
from backend.services.session_service import SessionService
from backend.services.extraction_service import ExtractionService
from backend.api.serializers import Serializer
from backend.config import BASE_DIR, FRONTEND_DIR, DIST_DIR, OUTPUT_DIR, UPLOADS_DIR

class BaseController:
    @staticmethod
    def send_json(handler, data, status_code=200):
        body = Serializer.to_json_bytes(data)
        handler.send_response(status_code)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Access-Control-Allow-Origin", "*")
        handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        handler.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With, Accept")
        handler.send_header("Content-Length", str(len(body)))
        handler.end_headers()
        handler.wfile.write(body)

    @staticmethod
    def send_binary(handler, data_bytes, content_type, filename=None, status_code=200):
        handler.send_response(status_code)
        handler.send_header("Content-Type", content_type)
        handler.send_header("Access-Control-Allow-Origin", "*")
        if filename:
            handler.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        handler.send_header("Content-Length", str(len(data_bytes)))
        handler.end_headers()
        handler.wfile.write(data_bytes)


class HealthController(BaseController):
    @classmethod
    def get_health(cls, handler):
        cls.send_json(handler, {
            "status": "healthy",
            "service": "johnson-electric-3d-drawing-extractor-api",
            "version": "1.0.0",
            "active_sessions": len(SessionService.get_all_sessions())
        })


class UploadController(BaseController):
    @classmethod
    def handle_upload(cls, handler):
        content_type = handler.headers.get("Content-Type", "")
        if "multipart/form-data" not in content_type:
            cls.send_json(handler, {"error": "Expected multipart/form-data"}, 400)
            return

        try:
            content_length = int(handler.headers.get("Content-Length", 0))
            body = handler.rfile.read(content_length)

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
                for part in msg.iter_parts():
                    payload = part.get_payload(decode=True)
                    if payload and payload.startswith(b"%PDF"):
                        pdf_bytes = payload
                        filename = part.get_filename() or "uploaded_drawing.pdf"
                        break

            if not pdf_bytes:
                cls.send_json(handler, {"error": "No valid PDF file found in upload payload."}, 400)
                return

            session_id, session_dir, pdf_path = SessionService.create_upload_session(filename, pdf_bytes)
            print(f"📥 Received PDF upload: {filename} ({len(pdf_bytes)} bytes) -> Session {session_id}")

            result_dict = ExtractionService.process_pdf(pdf_path, session_dir)
            SessionService.store_session(session_id, result_dict, session_dir, filename)

            image_b64 = SessionService.get_drawing_image_base64(session_dir)

            cls.send_json(handler, {
                "status": "success",
                "session_id": session_id,
                "filename": filename,
                "data": result_dict,
                "image_b64": image_b64
            })

        except Exception as e:
            traceback.print_exc()
            cls.send_json(handler, {"error": f"Extraction failed: {str(e)}"}, 500)


class SampleController(BaseController):
    @classmethod
    def handle_sample(cls, handler):
        try:
            sample_session = SessionService.get_session("sample")
            sample_json_path = os.path.join(OUTPUT_DIR, "extracted_drawing_data.json")

            if not sample_session or not os.path.exists(sample_json_path):
                print("⚡ Running pipeline on sample PDF...")
                result_dict = ExtractionService.process_sample()
                SessionService.store_session("sample", result_dict, OUTPUT_DIR, "3D Drawing Example.pdf")
            else:
                result_dict = sample_session["result"]

            image_b64 = SessionService.get_drawing_image_base64(OUTPUT_DIR)

            cls.send_json(handler, {
                "status": "success",
                "session_id": "sample",
                "filename": "3D Drawing Example.pdf",
                "data": result_dict,
                "image_b64": image_b64
            })
        except Exception as e:
            traceback.print_exc()
            cls.send_json(handler, {"error": f"Failed to load sample: {str(e)}"}, 500)


class SessionController(BaseController):
    @classmethod
    def handle_get_session(cls, handler, session_id):
        session = SessionService.get_session(session_id)
        if not session:
            cls.send_json(handler, {"error": "Session not found"}, 404)
            return

        image_b64 = SessionService.get_drawing_image_base64(session["output_dir"])
        cls.send_json(handler, {
            "status": "success",
            "session_id": session_id,
            "filename": session["pdf_name"],
            "data": session["result"],
            "image_b64": image_b64
        })


class ExportController(BaseController):
    @classmethod
    def export_json(cls, handler, session_id):
        session = SessionService.get_session(session_id)
        if not session:
            handler.send_error(404, "Session not found")
            return
        json_bytes = Serializer.to_json_bytes(session["result"])
        cls.send_binary(handler, json_bytes, "application/json", filename=f"extracted_{session_id}.json")

    @classmethod
    def export_csv(cls, handler, session_id):
        session = SessionService.get_session(session_id)
        if not session:
            handler.send_error(404, "Session not found")
            return
        csv_bytes = Serializer.dimensions_to_csv_bytes(session["result"].get("dimensions", []))
        cls.send_binary(handler, csv_bytes, "text/csv", filename=f"dimensions_{session_id}.csv")


class StaticController(BaseController):
    @classmethod
    def serve_frontend(cls, handler):
        html_file = os.path.join(FRONTEND_DIR, "index.html")
        if not os.path.exists(html_file):
            handler.send_error(404, "Frontend file not found")
            return
        with open(html_file, "rb") as f:
            data = f.read()
        cls.send_binary(handler, data, "text/html; charset=utf-8")

    @classmethod
    def serve_static_file(cls, handler, filepath, content_type):
        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            handler.send_error(404, "File Not Found")
            return
        with open(filepath, "rb") as f:
            data = f.read()
        cls.send_binary(handler, data, content_type)

    @classmethod
    def serve_frontend_asset(cls, handler, rel_path):
        """Safely serve frontend static assets (JS, CSS, fonts) with proper MIME headers."""
        target_path = os.path.abspath(os.path.join(FRONTEND_DIR, rel_path))
        if not target_path.startswith(os.path.abspath(FRONTEND_DIR)) or not os.path.isfile(target_path):
            target_path = os.path.abspath(os.path.join(DIST_DIR, rel_path))
            if not target_path.startswith(os.path.abspath(DIST_DIR)) or not os.path.isfile(target_path):
                handler.send_error(404, "Asset Not Found")
                return

        mime_type, _ = mimetypes.guess_type(target_path)
        if target_path.endswith(".js"):
            mime_type = "application/javascript; charset=utf-8"
        elif target_path.endswith(".css"):
            mime_type = "text/css; charset=utf-8"
        elif target_path.endswith(".json"):
            mime_type = "application/json; charset=utf-8"
        mime_type = mime_type or "application/octet-stream"

        with open(target_path, "rb") as f:
            data = f.read()
        cls.send_binary(handler, data, mime_type)

    @classmethod
    def serve_image(cls, handler, rel_path):
        full_path = os.path.join(OUTPUT_DIR, rel_path)
        if not os.path.exists(full_path):
            full_path = os.path.join(UPLOADS_DIR, rel_path)
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            handler.send_error(404, "Image Not Found")
            return
        mime_type, _ = mimetypes.guess_type(full_path)
        mime_type = mime_type or "image/png"
        with open(full_path, "rb") as f:
            data = f.read()
        cls.send_binary(handler, data, mime_type)

