"""
Engineering Drawing Information Extraction Data Models.
Defines strongly-typed schemas for metadata, views, dimensions, GD&T, and features.
Supports both Pydantic (v1/v2) and standard Python dataclasses for zero-dependency execution.
"""

from typing import List, Optional, Dict, Any, Union
from enum import Enum
import json

try:
    from pydantic import BaseModel, Field
    PYDANTIC_AVAILABLE = True
except ImportError:
    from dataclasses import dataclass, field, asdict, is_dataclass
    PYDANTIC_AVAILABLE = False


class DimensionType(str, Enum):
    LINEAR = "linear"
    COORDINATE = "coordinate"
    DIAMETER = "diameter"
    RADIUS = "radius"
    ANGULAR = "angular"
    CHAMFER = "chamfer"
    BASIC = "basic"
    REFERENCE = "reference"


class GDTCategory(str, Enum):
    POSITION = "position"
    CONCENTRICITY = "concentricity"
    PARALLELISM = "parallelism"
    PERPENDICULARITY = "perpendicularity"
    FLATNESS = "flatness"
    CYLINDRICITY = "cylindricity"
    PROFILE_OF_SURFACE = "profile_of_surface"
    PROFILE_OF_LINE = "profile_of_line"
    RUNOUT = "runout"


class ProjectionType(str, Enum):
    FIRST_ANGLE = "first_angle"
    THIRD_ANGLE = "third_angle"
    ISOMETRIC = "isometric"
    SECTION = "section"
    DETAIL = "detail"


if PYDANTIC_AVAILABLE:
    class BoundingBox(BaseModel):
        x_min: float
        y_min: float
        x_max: float
        y_max: float
        normalized: bool = True

    class DocumentMetadata(BaseModel):
        title: str
        drawing_id: str
        revision: str
        company: str
        author: Optional[str] = None
        date_drawn: Optional[str] = None
        date_printed: Optional[str] = None
        status: Optional[str] = "DRAFT"
        sheet_number: str = "2/2"
        sheet_size: str = "A0"
        nominal_scale: str = "5:1"
        material: str = "see table on the drawing"
        general_tolerances: str = "-"
        confidentiality: str = "CONFIDENTIAL"
        projection_method: ProjectionType = ProjectionType.FIRST_ANGLE

    class GDTControl(BaseModel):
        id: str
        characteristic: GDTCategory
        tolerance_value: float
        datum_references: List[str] = []
        material_condition: Optional[str] = None  # MMC, LMC, RFS
        count: int = 1
        associated_feature: Optional[str] = None
        raw_text: Optional[str] = None
        bbox: Optional[BoundingBox] = None
        confidence: float = 1.0

    class DimensionCallout(BaseModel):
        id: str
        balloon_number: int
        dimension_range_category: str  # e.g., "500-599", "600-699", "700-749"
        dimension_type: DimensionType
        nominal_value: float
        tolerance_upper: Optional[float] = None
        tolerance_lower: Optional[float] = None
        tolerance_symmetric: Optional[float] = None
        unit: str = "mm"
        count: int = 1
        is_reference: bool = False
        is_basic: bool = False
        associated_view: str
        associated_feature: Optional[str] = None
        measurement_note: Optional[str] = None
        datums_referenced: List[str] = []
        raw_string: str
        bbox: Optional[BoundingBox] = None
        confidence: float = 1.0

    class EngineeringView(BaseModel):
        view_id: str
        name: str
        view_type: ProjectionType
        scale: Optional[str] = None
        parent_view: Optional[str] = None
        cutting_plane: Optional[str] = None
        description: str
        features_captured: List[str] = []
        bbox: Optional[BoundingBox] = None

    class FeatureDefinition(BaseModel):
        feature_id: str
        name: str
        feature_type: str  # bore, snap, flange, connector, gear_pocket, motor_cavity
        instance_count: int = 1
        description: str
        critical_dimensions: List[int] = []  # Balloon numbers
        location: Optional[str] = None

    class DrawingExtractionResult(BaseModel):
        metadata: DocumentMetadata
        views: List[EngineeringView]
        features: List[FeatureDefinition]
        dimensions: List[DimensionCallout]
        gdt_controls: List[GDTControl]
        total_dimensions_count: int
        total_gdt_count: int
        validation_passed: bool
        validation_warnings: List[str] = []

        def to_dict(self) -> Dict[str, Any]:
            return self.model_dump()

else:
    # Python dataclass fallback
    @dataclass
    class BoundingBox:
        x_min: float
        y_min: float
        x_max: float
        y_max: float
        normalized: bool = True

    @dataclass
    class DocumentMetadata:
        title: str
        drawing_id: str
        revision: str
        company: str
        author: Optional[str] = None
        date_drawn: Optional[str] = None
        date_printed: Optional[str] = None
        status: Optional[str] = "DRAFT"
        sheet_number: str = "2/2"
        sheet_size: str = "A0"
        nominal_scale: str = "5:1"
        material: str = "see table on the drawing"
        general_tolerances: str = "-"
        confidentiality: str = "CONFIDENTIAL"
        projection_method: str = "first_angle"

    @dataclass
    class GDTControl:
        id: str
        characteristic: str
        tolerance_value: float
        datum_references: List[str] = field(default_factory=list)
        material_condition: Optional[str] = None
        count: int = 1
        associated_feature: Optional[str] = None
        raw_text: Optional[str] = None
        bbox: Optional[BoundingBox] = None
        confidence: float = 1.0

    @dataclass
    class DimensionCallout:
        id: str
        balloon_number: int
        dimension_range_category: str
        dimension_type: str
        nominal_value: float
        tolerance_upper: Optional[float] = None
        tolerance_lower: Optional[float] = None
        tolerance_symmetric: Optional[float] = None
        unit: str = "mm"
        count: int = 1
        is_reference: bool = False
        is_basic: bool = False
        associated_view: str = ""
        associated_feature: Optional[str] = None
        measurement_note: Optional[str] = None
        datums_referenced: List[str] = field(default_factory=list)
        raw_string: str = ""
        bbox: Optional[BoundingBox] = None
        confidence: float = 1.0

    @dataclass
    class EngineeringView:
        view_id: str
        name: str
        view_type: str
        scale: Optional[str] = None
        parent_view: Optional[str] = None
        cutting_plane: Optional[str] = None
        description: str = ""
        features_captured: List[str] = field(default_factory=list)
        bbox: Optional[BoundingBox] = None

    @dataclass
    class FeatureDefinition:
        feature_id: str
        name: str
        feature_type: str
        instance_count: int = 1
        description: str = ""
        critical_dimensions: List[int] = field(default_factory=list)
        location: Optional[str] = None

    @dataclass
    class DrawingExtractionResult:
        metadata: DocumentMetadata
        views: List[EngineeringView]
        features: List[FeatureDefinition]
        dimensions: List[DimensionCallout]
        gdt_controls: List[GDTControl]
        total_dimensions_count: int
        total_gdt_count: int
        validation_passed: bool
        validation_warnings: List[str] = field(default_factory=list)

        def to_dict(self) -> Dict[str, Any]:
            def _dict_factory(data):
                d = {}
                for k, v in data:
                    if isinstance(v, Enum):
                        d[k] = v.value
                    elif isinstance(v, list):
                        d[k] = [x.value if isinstance(x, Enum) else x for x in v]
                    else:
                        d[k] = v
                return d
            return asdict(self, dict_factory=_dict_factory)
