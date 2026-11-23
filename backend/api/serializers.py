"""
Data serializers for JSON and CSV exports.
"""

import json
import csv
import io

class Serializer:
    @staticmethod
    def to_json_bytes(data, indent=2):
        return json.dumps(data, indent=indent).encode("utf-8")

    @staticmethod
    def dimensions_to_csv_bytes(dimensions):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Balloon Number",
            "Nominal Value",
            "Tolerance Symmetric",
            "Tolerance Upper",
            "Tolerance Lower",
            "Unit",
            "Dimension Type",
            "Series Category",
            "Associated View",
            "Associated Feature",
            "Measurement Note",
            "Raw Callout String"
        ])
        for d in dimensions:
            writer.writerow([
                d.get("balloon_number"),
                d.get("nominal_value"),
                d.get("tolerance_symmetric") or "",
                d.get("tolerance_upper") or "",
                d.get("tolerance_lower") or "",
                d.get("unit"),
                d.get("dimension_type"),
                d.get("dimension_range_category"),
                d.get("associated_view"),
                d.get("associated_feature") or "",
                d.get("measurement_note") or "",
                d.get("raw_string")
            ])
        return output.getvalue().encode("utf-8")
