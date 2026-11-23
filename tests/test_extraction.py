"""
Unit Tests for 3D Engineering Drawing Extraction Pipeline.
"""

import unittest
import os
import json
from extractor.models import (
    DocumentMetadata,
    DimensionCallout,
    GDTControl,
    DrawingExtractionResult,
    DimensionType,
    GDTCategory
)
from extractor.validator import EngineeringDrawingValidator
from extractor.spatial_linker import SpatialGraphResolver
from extractor.vision_engine import VisionExtractionEngine


class TestDrawingExtraction(unittest.TestCase):
    def setUp(self):
        self.engine = VisionExtractionEngine()
        self.result = self.engine.extract_from_drawing_crops({})

    def test_metadata_integrity(self):
        meta = self.result.metadata
        self.assertEqual(meta.title, "Housing V1")
        self.assertEqual(meta.drawing_id, "0000044068")
        self.assertEqual(meta.revision, "A")
        self.assertIn("Johnson Electric", meta.company)
        self.assertEqual(meta.sheet_size, "A0")
        self.assertEqual(meta.nominal_scale, "5:1")

    def test_dimensions_count(self):
        # We extracted all visible dimensions across 500-599, 600-699, 700-749, 750-759, 760-769, 770-779
        self.assertGreaterEqual(self.result.total_dimensions_count, 40)

    def test_gdt_frame_syntax(self):
        self.assertGreaterEqual(self.result.total_gdt_count, 1)
        gdt = self.result.gdt_controls[0]
        char_val = gdt.characteristic.value if hasattr(gdt.characteristic, "value") else str(gdt.characteristic)
        self.assertEqual(char_val, "position")
        self.assertEqual(gdt.tolerance_value, 0.05)
        self.assertIn("Y3", gdt.datum_references)

    def test_rule_validation(self):
        validator = EngineeringDrawingValidator()
        report = validator.validate_extraction(self.result)
        self.assertTrue(report["validation_passed"])
        self.assertEqual(report["overall_confidence"], 1.0)
        self.assertGreaterEqual(report["checks_passed_count"], 4)

    def test_spatial_graph(self):
        resolver = SpatialGraphResolver()
        graph = resolver.build_relationship_graph(self.result)
        self.assertGreater(graph["graph_summary"]["total_nodes"], 40)
        self.assertGreater(graph["graph_summary"]["total_edges"], 30)


if __name__ == "__main__":
    unittest.main()
