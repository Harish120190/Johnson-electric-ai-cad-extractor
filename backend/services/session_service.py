"""
Session management service for drawing extractions.
Provides in-memory session registry and file-system backed persistence.
"""

import os
import json
import uuid
import base64
from backend.config import UPLOADS_DIR, OUTPUT_DIR, SAMPLE_PDF

class SessionService:
    _sessions = {}

    @classmethod
    def initialize(cls):
        """Preload sample session if existing output is present on disk."""
        sample_json_path = os.path.join(OUTPUT_DIR, "extracted_drawing_data.json")
        if os.path.exists(sample_json_path):
            try:
                with open(sample_json_path, "r", encoding="utf-8") as f:
                    cls._sessions["sample"] = {
                        "result": json.load(f),
                        "output_dir": OUTPUT_DIR,
                        "pdf_name": "3D Drawing Example.pdf"
                    }
            except Exception as e:
                print(f"Warning: Failed to preload sample output: {e}")

    @classmethod
    def get_all_sessions(cls):
        return cls._sessions

    @classmethod
    def get_session(cls, session_id):
        return cls._sessions.get(session_id)

    @classmethod
    def store_session(cls, session_id, result_dict, output_dir, pdf_name):
        cls._sessions[session_id] = {
            "result": result_dict,
            "output_dir": output_dir,
            "pdf_name": pdf_name
        }

    @classmethod
    def create_upload_session(cls, filename, pdf_bytes):
        """Creates a unique session directory and writes uploaded bytes."""
        session_id = str(uuid.uuid4())[:8]
        session_dir = os.path.join(UPLOADS_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        pdf_path = os.path.join(session_dir, filename)
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)
        return session_id, session_dir, pdf_path

    @classmethod
    def get_drawing_image_base64(cls, output_dir):
        """Retrieves normalized or rasterized drawing image as Base64 string."""
        norm_img_path = os.path.join(output_dir, "drawing_normalized.png")
        if not os.path.exists(norm_img_path):
            norm_img_path = os.path.join(output_dir, "rasterized_highres.png")
        if not os.path.exists(norm_img_path):
            norm_img_path = os.path.join(output_dir, "rasterized_raw.png")

        if os.path.exists(norm_img_path):
            with open(norm_img_path, "rb") as img_f:
                return base64.b64encode(img_f.read()).decode("utf-8")
        return ""

# Initialize sample cache on import
SessionService.initialize()

