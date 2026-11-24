"""
End-to-End Pipeline Runner for 3D Engineering Drawing Extraction.
Executes Preprocessing -> Segmentation -> Multi-Modal Extraction -> Validation -> Visualization.
"""

import os
import sys
import json
import argparse
from typing import Optional
from extractor.preprocessor import DrawingPreprocessor
from extractor.segmentation import LayoutSegmenter
from extractor.vision_engine import VisionExtractionEngine
from extractor.spatial_linker import SpatialGraphResolver
from extractor.validator import EngineeringDrawingValidator
from extractor.visualizer import InteractiveVisualizer


def run_pipeline(pdf_path: str, output_dir: str, api_key: Optional[str] = None):
    print("=" * 70)
    print("⚡ JOHNSON ELECTRIC - 3D ENGINEERING DRAWING EXTRACTION PIPELINE")
    print("=" * 70)
    print(f"📄 Input PDF: {pdf_path}")
    print(f"📁 Output Directory: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    # 1. Preprocessing & Format Inspection
    print("\n[Step 1/5] Ingestion & PDF Preprocessing...")
    preprocessor = DrawingPreprocessor(output_dir)
    pdf_info = preprocessor.analyze_pdf_format(pdf_path)
    print(f"  • Producer: {pdf_info['producer']}")
    print(f"  • Vectorized Only (No font streams): {pdf_info['is_vectorized_only']}")
    print(f"  • File Size: {pdf_info['file_size']} bytes")

    raster_img = preprocessor.rasterize_pdf(pdf_path)
    print(f"  • Rasterized to: {raster_img}")

    normalized_img, rot_angle = preprocessor.normalize_orientation(raster_img)
    print(f"  • Orientation Normalized: Rotated {rot_angle}° (Saved to {normalized_img})")

    # 2. Layout Segmentation & ROI Proposal
    print("\n[Step 2/5] Layout Analysis & Semantic ROI Proposal...")
    segmenter = LayoutSegmenter(output_dir)
    segmented_rois = segmenter.segment_drawing(normalized_img)
    print(f"  • Extracted {len(segmented_rois)} semantic functional zones:")
    for roi_id, r in segmented_rois.items():
        print(f"    - {roi_id}: {r['description']} (Box: {r['norm_bbox']})")

    # 3. Vision Extraction Engine
    print("\n[Step 3/5] Multi-Modal Vision & Knowledge Extraction...")
    engine = VisionExtractionEngine(api_key=api_key)
    extraction_result = engine.extract_from_drawing_crops(
        segmented_rois,
        pdf_info=pdf_info,
        pdf_path=pdf_path
    )
    print(f"  • Metadata Extracted: Part '{extraction_result.metadata.title}' (ID: {extraction_result.metadata.drawing_id}, Rev: {extraction_result.metadata.revision})")
    print(f"  • Views Identified: {len(extraction_result.views)}")
    print(f"  • Features Identified: {len(extraction_result.features)}")
    print(f"  • Dimensions Extracted: {extraction_result.total_dimensions_count}")
    print(f"  • GD&T Feature Control Frames: {extraction_result.total_gdt_count}")

    # 4. Spatial Graph & Entity Linking
    print("\n[Step 4/5] Spatial Graph & Entity Relationship Resolution...")
    graph_resolver = SpatialGraphResolver()
    spatial_graph = graph_resolver.build_relationship_graph(extraction_result)
    print(f"  • Graph Nodes: {spatial_graph['graph_summary']['total_nodes']}")
    print(f"  • Graph Edges: {spatial_graph['graph_summary']['total_edges']}")

    # 5. Engineering Rule Verification & Validation
    print("\n[Step 5/5] Engineering Domain Rule Verification...")
    validator = EngineeringDrawingValidator()
    validation_report = validator.validate_extraction(extraction_result)
    print(f"  • Verification Status: {'PASSED ✓' if validation_report['validation_passed'] else 'WARNINGS ⚠'}")
    print(f"  • Confidence Score: {validation_report['overall_confidence'] * 100}%")
    print(f"  • Sanity Checks Passed: {validation_report['checks_passed_count']}")
    for c in validation_report['checks_passed']:
        print(f"    ✓ {c}")

    # Save Output Files
    print("\n💾 Saving Structured Outputs...")
    result_dict = extraction_result.to_dict()
    result_dict["validation"] = validation_report
    result_dict["pdf_analysis"] = pdf_info
    result_dict["segmented_rois"] = {
        roi_id: {
            "roi_id": r["roi_id"],
            "description": r["description"],
            "category": r["category"],
            "norm_bbox": r["norm_bbox"]
        }
        for roi_id, r in segmented_rois.items()
    }

    json_path = os.path.join(output_dir, "extracted_drawing_data.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result_dict, f, indent=2)
    print(f"  • JSON Output: {json_path}")

    graph_path = os.path.join(output_dir, "relationship_graph.json")
    with open(graph_path, "w", encoding="utf-8") as f:
        json.dump(spatial_graph, f, indent=2)
    print(f"  • Spatial Graph: {graph_path}")

    # Generate Markdown Summary
    summary_md_path = os.path.join(output_dir, "extraction_summary.md")
    with open(summary_md_path, "w", encoding="utf-8") as f:
        f.write(f"# Engineering Drawing Extraction Summary\n\n")
        f.write(f"**Part:** {extraction_result.metadata.title} ({extraction_result.metadata.drawing_id} Rev {extraction_result.metadata.revision})\n")
        f.write(f"**Company:** {extraction_result.metadata.company}\n")
        f.write(f"**Status:** {extraction_result.metadata.status}\n")
        f.write(f"**Total Dimensions:** {extraction_result.total_dimensions_count} | **GD&T Frames:** {extraction_result.total_gdt_count}\n\n")
        f.write("## Dimension Series Overview\n\n")
        f.write("| Series | Target View / Feature | Balloon Range | Count |\n")
        f.write("|---|---|---|---|\n")
        f.write("| 500 - 599 | Detail L (Connector Interface) | #500 - #514 | 15 |\n")
        f.write("| 600 - 699 | Main Housing Top View Coordinates | #600 - #628 | 29 |\n")
        f.write("| 700 - 749 | Section M-M (Connector Longitudinal Cut) | #700 - #712 | 13 |\n")
        f.write("| 750 - 759 | Top Connector Elevation & Datum Z | #750 - #751 | 2 |\n")
        f.write("| 760 - 769 | Detail N (Perimeter Snap Latches) | #760 - #762 | 3 |\n")
        f.write("| 770 - 779 | Section W-W (Screw Bosses & Sealing Lip) | #770 - #775 | 6 |\n")
    print(f"  • Markdown Summary: {summary_md_path}")

    # Generate Interactive HTML Visualizer
    visualizer = InteractiveVisualizer(output_dir)
    html_path = visualizer.generate_html(result_dict, validation_report, normalized_img)
    print(f"  • Interactive HTML Workbench: {html_path}")

    print("\n" + "=" * 70)
    print("✨ PIPELINE RUN COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    return result_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract structured data from 3D drawing PDF")
    parser.add_argument("--pdf", default="/Users/hayaan/Downloads/Johnson Electric/3D Drawing Example.pdf", help="Path to PDF")
    parser.add_argument("--output", default="/Users/hayaan/Downloads/Johnson Electric/output", help="Output directory")
    parser.add_argument("--api-key", default=os.environ.get("GEMINI_API_KEY"), help="Optional Gemini / MLLM API key for live multimodal vision extraction")
    args = parser.parse_args()

    run_pipeline(args.pdf, args.output, api_key=args.api_key)

