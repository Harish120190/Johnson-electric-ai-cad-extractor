"""
Preprocessor Module.
Handles PDF rasterization, resolution upscaling, orientation detection, and image normalization.
"""

import os
import subprocess
import json
from typing import Tuple, Dict, Any


class DrawingPreprocessor:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def analyze_pdf_format(self, pdf_path: str) -> Dict[str, Any]:
        """Inspects PDF to check if text is vectorized or has font streams."""
        with open(pdf_path, "rb") as f:
            content = f.read()

        has_fonts = b"/Font" in content
        has_text_ops = b"Tj" in content or b"TJ" in content
        is_vectorized_only = not has_fonts and not has_text_ops

        return {
            "file_size": len(content),
            "has_embedded_fonts": has_fonts,
            "has_native_text_operators": has_text_ops,
            "is_vectorized_only": is_vectorized_only,
            "producer": "Microsoft: Print To PDF" if b"Microsoft: Print To PDF" in content else "Unknown"
        }

    def rasterize_pdf(self, pdf_path: str, target_dpi: int = 300) -> str:
        """
        Rasterizes PDF into high-resolution PNG using macOS sips / CoreGraphics.
        """
        raw_png = os.path.join(self.output_dir, "rasterized_raw.png")
        
        # In macOS, sips rasterizes PDF to PNG cleanly
        cmd = ["sips", "-s", "format", "png", pdf_path, "--out", raw_png]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Upscale if needed for OCR / multi-modal resolution
        dims = self.get_image_dimensions(raw_png)
        # Standard A0 at 72dpi is 842x595 or 595x842; upsample to 4x (approx 288 dpi)
        if dims[0] < 2000 and dims[1] < 2000:
            target_w = dims[0] * 4
            target_h = dims[1] * 4
            resampled_png = os.path.join(self.output_dir, "rasterized_highres.png")
            upscale_cmd = ["sips", "--resampleHeightWidth", str(target_h), str(target_w), raw_png, "--out", resampled_png]
            subprocess.run(upscale_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return resampled_png
        return raw_png

    def get_image_dimensions(self, image_path: str) -> Tuple[int, int]:
        """Returns (width, height) of image."""
        cmd = ["sips", "-g", "pixelWidth", "-g", "pixelHeight", image_path]
        res = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        width, height = 0, 0
        for line in res.stdout.splitlines():
            if "pixelWidth" in line:
                width = int(line.split(":")[-1].strip())
            elif "pixelHeight" in line:
                height = int(line.split(":")[-1].strip())
        return width, height

    def normalize_orientation(self, image_path: str) -> Tuple[str, int]:
        """
        Detects if drawing is portrait instead of landscape and rotates it.
        Engineering drawings like A0/A1 are standard landscape.
        """
        w, h = self.get_image_dimensions(image_path)
        normalized_path = os.path.join(self.output_dir, "drawing_normalized.png")

        if h > w:
            # Drawing was printed in portrait; rotate 90 degrees clockwise to restore standard landscape
            cmd = ["sips", "-r", "90", image_path, "--out", normalized_path]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return normalized_path, 90
        else:
            # Already landscape
            import shutil
            shutil.copyfile(image_path, normalized_path)
            return normalized_path, 0

