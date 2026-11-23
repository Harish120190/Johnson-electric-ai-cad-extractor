"""
Engineering Rule Verification & Consistency Validator.
Applies mechanical engineering rules, tolerance checks, and coordinate arithmetic validations.
"""

from typing import List, Dict, Any
from .models import DrawingExtractionResult


class EngineeringDrawingValidator:
    def __init__(self):
        pass

    def validate_extraction(self, result: DrawingExtractionResult) -> Dict[str, Any]:
        """
        Executes engineering domain checks and validation rules.
        """
        checks_passed = []
        warnings = []

        # 1. Pilot vs Counterbore Hole Geometry Check
        dim_pilot = next((d for d in result.dimensions if d.balloon_number == 770), None)
        dim_cbore = next((d for d in result.dimensions if d.balloon_number == 774), None)
        if dim_pilot and dim_cbore:
            if dim_pilot.nominal_value < dim_cbore.nominal_value:
                checks_passed.append(
                    f"Hole Geometry Valid: Pilot bore Ø{dim_pilot.nominal_value}mm is strictly smaller than counterbore Ø{dim_cbore.nominal_value}mm"
                )
            else:
                warnings.append(
                    f"Hole Geometry Violation: Pilot bore Ø{dim_pilot.nominal_value}mm >= counterbore Ø{dim_cbore.nominal_value}mm"
                )

        # 2. Connector Pin Pitch Symmetry Check
        p1 = next((d for d in result.dimensions if d.balloon_number == 501), None)
        p5 = next((d for d in result.dimensions if d.balloon_number == 502), None)
        p2 = next((d for d in result.dimensions if d.balloon_number == 504), None)
        p4 = next((d for d in result.dimensions if d.balloon_number == 503), None)

        if p1 and p5 and p2 and p4:
            if abs(p1.nominal_value - p5.nominal_value) < 1e-4 and abs(p2.nominal_value - p4.nominal_value) < 1e-4:
                checks_passed.append(
                    f"Pin Pitch Symmetry Valid: Outer pins symmetric at {p1.nominal_value}mm, inner pins symmetric at {p2.nominal_value}mm from Datum Y2"
                )
                if abs(p1.nominal_value - 2 * p2.nominal_value) < 1e-4:
                    checks_passed.append(
                        f"Pin Grid Pitch Consistency Valid: Outer pitch ({p1.nominal_value}mm) is exactly 2x inner pitch ({p2.nominal_value}mm)"
                    )

        # 3. GD&T Feature Control Frame Syntax Check
        form_tolerances = {"flatness", "straightness", "circularity", "cylindricity"}
        for gdt in result.gdt_controls:
            char_name = gdt.characteristic.value.lower() if hasattr(gdt.characteristic, "value") else str(gdt.characteristic).lower()
            is_form = char_name in form_tolerances
            if gdt.tolerance_value > 0 and (is_form or len(gdt.datum_references) > 0):
                datums_str = f"Datums: {', '.join(gdt.datum_references)}" if gdt.datum_references else "Form Standard (No Datum Required)"
                checks_passed.append(
                    f"GD&T Frame Valid: [{gdt.characteristic.upper()} | {gdt.tolerance_value}mm | {datums_str}]"
                )
            else:
                warnings.append(f"GD&T Syntax Incomplete: Frame {gdt.id}")

        # 4. Snap-fit Clearance Check
        snap_h = next((d for d in result.dimensions if d.balloon_number == 760), None)
        snap_z = next((d for d in result.dimensions if d.balloon_number == 750), None)
        if snap_h and snap_z:
            if snap_h.nominal_value > snap_z.nominal_value:
                checks_passed.append(
                    f"Snap Latch Retention Clearance Valid: Snap window height ({snap_h.nominal_value}mm) accommodates latch height ({snap_z.nominal_value}mm)"
                )

        # 5. Tolerance Sanity Check
        invalid_tolerances = []
        for dim in result.dimensions:
            if dim.tolerance_symmetric is not None and dim.tolerance_symmetric <= 0:
                invalid_tolerances.append(dim.balloon_number)
        if not invalid_tolerances:
            checks_passed.append("All dimension tolerance bounds are positive and geometrically valid.")
        else:
            warnings.append(f"Invalid non-positive tolerances found on balloons: {invalid_tolerances}")

        overall_passed = len(warnings) == 0
        confidence_score = max(0.0, 1.0 - (len(warnings) * 0.1))

        return {
            "validation_passed": overall_passed,
            "overall_confidence": round(confidence_score, 3),
            "checks_passed_count": len(checks_passed),
            "warnings_count": len(warnings),
            "checks_passed": checks_passed,
            "warnings": warnings
        }

