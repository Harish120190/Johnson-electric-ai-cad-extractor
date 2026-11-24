"""
Extraction pipeline execution service.
Connects API layer with the core AI/CV extraction engine.
"""

import os
import sys
from backend.config import BASE_DIR, OUTPUT_DIR, SAMPLE_PDF

# Ensure root directory is in sys.path to access run_pipeline
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from run_pipeline import run_pipeline

class ExtractionService:
    @staticmethod
    def process_pdf(pdf_path, output_dir):
        """Runs the 5-step drawing extraction pipeline."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")
        os.makedirs(output_dir, exist_ok=True)
        return run_pipeline(pdf_path, output_dir)

    @staticmethod
    def process_sample():
        """Processes or returns the canonical sample PDF."""
        return run_pipeline(SAMPLE_PDF, OUTPUT_DIR)

