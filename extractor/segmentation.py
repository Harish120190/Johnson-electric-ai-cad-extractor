"""
Layout Analysis & Region of Interest (ROI) Segmentation.
Divides technical drawing into semantic functional zones:
- Title Block & Document Metadata
- Detail Views (L, N)
- Section Views (M-M, W-W, T-T)
- Orthographic Housing Views (Coordinates 600-699)
- 3D Isometric Visualization
"""

import os
import subprocess
from typing import Dict, List, Any


class LayoutSegmenter:
    def __init__(self, output_dir: str):
        self.crops_dir = os.path.join(output_dir, "roi_crops")
        os.makedirs(self.crops_dir, exist_ok=True)

    def get_image_size(self, image_path: str) -> tuple:
        cmd = ["sips", "-g", "pixelWidth", "-g", "pixelHeight", image_path]
        res = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        w, h = 0, 0
        for line in res.stdout.splitlines():
            if "pixelWidth" in line:
                w = int(line.split(":")[-1].strip())
            elif "pixelHeight" in line:
                h = int(line.split(":")[-1].strip())
        return w, h

    def segment_drawing(self, image_path: str) -> Dict[str, Dict[str, Any]]:
        """
        Calculates normalized bounding boxes and crops semantic ROIs.
        Normalized coordinates: [x_min, y_min, x_max, y_max] from 0.0 to 1.0.
        """
        img_w, img_h = self.get_image_size(image_path)

        roi_definitions = {
            "title_block": {
                "description": "Drawing Title Block, Revision, Scale, and Material Table",
                "norm_bbox": [0.77, 0.84, 0.99, 0.99],
                "category": "metadata"
            },
            "detail_L_connector": {
                "description": "Detail L (10:1): 5-Pin Connector, Pitch, Chamfers, and GD&T",
                "norm_bbox": [0.33, 0.06, 0.67, 0.38],
                "category": "detail_view"
            },
            "section_M_M": {
                "description": "Section M-M (10:1): Connector Longitudinal Cross-Section",
                "norm_bbox": [0.67, 0.08, 0.95, 0.40],
                "category": "section_view"
            },
            "detail_N_and_WW": {
                "description": "Detail N (10:1) & Section W-W (5:1): Snap-fit Latches & Screw Bosses",
                "norm_bbox": [0.48, 0.38, 0.82, 0.65],
                "category": "detail_and_section"
            },
            "isometric_3d": {
                "description": "Isometric 3D View of Actuator Housing with Saia-Burgess Branding",
                "norm_bbox": [0.55, 0.64, 0.78, 0.88],
                "category": "3d_visualization"
            },
            "section_T_T": {
                "description": "Section T-T (5:1): Main Housing Transverse Cross-Section",
                "norm_bbox": [0.12, 0.74, 0.42, 0.96],
                "category": "section_view"
            },
            "top_elevation_view": {
                "description": "Top Connector Elevation & Datum Z Reference",
                "norm_bbox": [0.06, 0.08, 0.45, 0.28],
                "category": "elevation_view"
            },
            "main_housing_coordinates": {
                "description": "Main Top View (5:1) with Coordinate Rails 600-699, Bores 1-3, Snaps 1-4",
                "norm_bbox": [0.04, 0.24, 0.52, 0.78],
                "category": "main_view"
            }
        }

        segmented_crops = {}

        for roi_id, defn in roi_definitions.items():
            norm_box = defn["norm_bbox"]
            x_min_px = int(norm_box[0] * img_w)
            y_min_px = int(norm_box[1] * img_h)
            x_max_px = int(norm_box[2] * img_w)
            y_max_px = int(norm_box[3] * img_h)

            crop_w = max(10, x_max_px - x_min_px)
            crop_h = max(10, y_max_px - y_min_px)

            crop_filename = f"{roi_id}.png"
            crop_path = os.path.join(self.crops_dir, crop_filename)

            # Sips command: --cropToHeightWidth pixelsH pixelsW --cropOffset offsetY offsetX
            cmd = [
                "sips",
                "--cropToHeightWidth", str(crop_h), str(crop_w),
                "--cropOffset", str(y_min_px), str(x_min_px),
                image_path,
                "--out", crop_path
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            segmented_crops[roi_id] = {
                "roi_id": roi_id,
                "crop_path": crop_path,
                "description": defn["description"],
                "category": defn["category"],
                "norm_bbox": norm_box,
                "pixel_bbox": [x_min_px, y_min_px, x_max_px, y_max_px],
                "crop_dimensions": [crop_w, crop_h]
            }

        return segmented_crops

