"""
Spatial Entity Linker & Relationship Graph Resolver.
Connects dimension balloons, leader lines, datums, and geometric features into a unified spatial graph.
"""

from typing import Dict, List, Any
from .models import DrawingExtractionResult


class SpatialGraphResolver:
    def __init__(self):
        pass

    def build_relationship_graph(self, result: DrawingExtractionResult) -> Dict[str, Any]:
        """
        Builds an engineering knowledge graph representing spatial and hierarchical relationships.
        """
        nodes = []
        edges = []

        # 1. Add View Nodes
        for v in result.views:
            nodes.append({
                "id": v.view_id,
                "label": v.name,
                "type": "view",
                "scale": v.scale,
                "view_type": str(v.view_type)
            })
            if v.parent_view:
                edges.append({
                    "source": v.parent_view,
                    "target": v.view_id,
                    "relation": "cuts_or_details",
                    "label": f"Cut/Detail: {v.cutting_plane or v.name}"
                })

        # 2. Add Feature Nodes
        for feat in result.features:
            nodes.append({
                "id": feat.feature_id,
                "label": feat.name,
                "type": "feature",
                "count": feat.instance_count,
                "feature_type": feat.feature_type
            })

        # 3. Add Dimension Nodes & Edges
        for dim in result.dimensions:
            nodes.append({
                "id": dim.id,
                "label": f"#{dim.balloon_number}: {dim.nominal_value}",
                "type": "dimension",
                "category": dim.dimension_range_category,
                "raw": dim.raw_string
            })

            # Link to view
            matching_view = next((v for v in result.views if v.name in dim.associated_view or dim.associated_view in v.name), None)
            if matching_view:
                edges.append({
                    "source": matching_view.view_id,
                    "target": dim.id,
                    "relation": "contains_dimension"
                })

            # Link to feature
            for feat in result.features:
                if dim.balloon_number in feat.critical_dimensions or (dim.associated_feature and any(k.lower() in dim.associated_feature.lower() for k in feat.name.split())):
                    edges.append({
                        "source": feat.feature_id,
                        "target": dim.id,
                        "relation": "constrained_by_dimension"
                    })

        # 4. Add GD&T Nodes & Edges
        for gdt in result.gdt_controls:
            nodes.append({
                "id": gdt.id,
                "label": f"GD&T: {gdt.characteristic} {gdt.tolerance_value}",
                "type": "gdt_control",
                "datums": gdt.datum_references
            })
            # Link to associated feature
            for feat in result.features:
                if "Pin" in gdt.associated_feature and "pin" in feat.feature_id:
                    edges.append({
                        "source": feat.feature_id,
                        "target": gdt.id,
                        "relation": "controlled_by_gdt"
                    })

        return {
            "graph_summary": {
                "total_nodes": len(nodes),
                "total_edges": len(edges),
                "view_count": len(result.views),
                "feature_count": len(result.features),
                "dimension_count": len(result.dimensions),
                "gdt_count": len(result.gdt_controls)
            },
            "nodes": nodes,
            "edges": edges
        }

