"""
Preprocessor Module.
Handles PDF rasterization, resolution upscaling, orientation detection, and image normalization.
"""

import os
import subprocess
import json
from typing import Tuple, Dict, Any, Optional


class DrawingPreprocessor:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def analyze_pdf_format(self, pdf_path: str) -> Dict[str, Any]:
        """Inspects PDF to extract document metadata, page geometry, and text stream capabilities."""
        with open(pdf_path, "rb") as f:
            content = f.read()

        import re

        def extract_field(field_name: str) -> Optional[str]:
            match = re.search(rb'/' + field_name.encode() + rb'\s*\(([^)]*)\)', content)
            if match:
                try:
                    return match.group(1).decode('latin1', 'ignore').strip()
                except Exception:
                    return match.group(1).decode('utf-8', 'ignore').strip()
            return None

        producer = extract_field('Producer') or 'Unknown'
        author = extract_field('Author') or 'Engineering CAD Team'
        title = extract_field('Title')
        creation_date = extract_field('CreationDate')

        # Extract MediaBox [x0 y0 x1 y1]
        mb_match = re.search(rb'/MediaBox\s*\[\s*([0-9\.\s\-]+)\s*\]', content)
        mediabox = [float(x) for x in mb_match.group(1).split()] if mb_match else None

        # Determine sheet size from points (72 points = 1 inch)
        sheet_size = "A0"
        if mediabox and len(mediabox) >= 4:
            w_pt = abs(mediabox[2] - mediabox[0])
            h_pt = abs(mediabox[3] - mediabox[1])
            max_pt = max(w_pt, h_pt)
            if max_pt >= 3000:
                sheet_size = "A0"
            elif max_pt >= 2000:
                sheet_size = "A1"
            elif max_pt >= 1400:
                sheet_size = "A2"
            elif max_pt >= 900:
                sheet_size = "A3"
            else:
                sheet_size = "A4"

        # Check font dictionaries and content streams
        has_fonts = b"/Font" in content
        has_text_ops = b"Tj" in content or b"TJ" in content
        is_vectorized_only = not has_fonts and not has_text_ops

        # Count pages
        page_matches = re.findall(rb'/Type\s*/Page[^s]', content)
        page_count = max(1, len(page_matches))

        return {
            "file_size": len(content),
            "producer": producer,
            "author": author,
            "title": title,
            "creation_date": creation_date,
            "sheet_size": sheet_size,
            "mediabox": mediabox,
            "page_count": page_count,
            "has_embedded_fonts": has_fonts,
            "has_native_text_operators": has_text_ops,
            "is_vectorized_only": is_vectorized_only
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

