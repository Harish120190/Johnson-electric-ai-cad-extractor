"""
Backend API Configuration.
Defines server paths, directory paths, and environment settings.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAMPLE_PDF = os.path.join(BASE_DIR, "3D Drawing Example.pdf")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DIST_DIR = os.path.join(BASE_DIR, "dist")

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEFAULT_PORT = 8000
DEFAULT_HOST = "0.0.0.0"
CORS_ORIGIN = "*"
ALLOWED_METHODS = "GET, POST, OPTIONS, PUT, DELETE"
ALLOWED_HEADERS = "Content-Type, Authorization, X-Requested-With, Accept"
MAX_UPLOAD_SIZE = 50 * 1024 * 1024  # 50MB

