"""
Pydantic models cho Geometry API

Complete implementation của tất cả models cần thiết cho
Geometry Calculator API với full validation và type checking.

Models bao gồm:
- Enums: Dynamic loading từ JSON configs
- Data models: PointData, LineData, PlaneData, CircleData, SphereData
- Request/Response models: GeometryCalculationRequest/Response
- Error models: ErrorResponse, ValidationErrorResponse
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any, Union
from enum import Enum
import re
from datetime import datetime

# =================================================================
# ENUMS - Based on JSON configurations
# =================================================================

class ShapeType(str, Enum):
    """Supported geometry shapes"""
    POINT = "Điểm"
    LINE = "Đường thẳng"
    PLANE = "Mặt phẳng"
    CIRCLE = "Đường tròn"
    SPHERE = "Mặt cầu"

class OperationType(str, Enum):
    """Supported geometry operations"""
    INTERSECTION = "Tương giao"
    DISTANCE = "Khoảng cách"
    AREA = "Diện tích"
    VOLUME = "Thể tích"
    LINE_EQUATION = "PT đường thẳng"

class DimensionType(str, Enum):
    """Coordinate system dimensions"""
    TWO_D = "2"
    THREE_D = "3"

class CalculatorVersion(str, Enum):
    """Supported calculator versions"""
    FX799 = "fx799"
    FX880 = "fx880"
    FX991 = "fx991"
    FX570 = "fx570"
    FX801 = "fx801"
    FX802 = "fx802"
    FX803 = "fx803"

# =================================================================
# SHAPE DATA MODELS
# =================================================================

class PointData(BaseModel):
    """Point geometry data model"""
    coordinates: str = Field(
        ..., 
        example="1,2,3",
        description="Tọa độ điểm (x,y cho 2D hoặc x,y,z cho 3D)"
    )
    
    @validator('coordinates')
    def validate_coordinates(cls, v):
        if not v or not v.strip():
            raise ValueError("Tọa độ không được để trống")
        
        # Clean and validate format
        clean_coords = v.strip().replace(" ", "")
        
        # Check for valid coordinate format (numbers separated by commas)
        pattern = r'^-?\d+(\.\d+)?(,-?\d+(\.\d+)?){1,2}$'
        if not re.match(pattern, clean_coords):
            raise ValueError("Format tọa độ không hợp lệ. Ví dụ: '1,2' hoặc '1,2,3'")
        
        return clean_coords

class LineData(BaseModel):
    """Line geometry data model"""
    point: str = Field(
        ...,
        example="1,2,3",
        description="Điểm thuộc đường thẳng (x,y,z)"
    )
    direction_vector: str = Field(
        ...,
        example="1,0,1", 
        description="Vector chỉ phương của đường thẳng"
    )
    
    @validator('point', 'direction_vector')
    def validate_vector_format(cls, v):
        if not v or not v.strip():
            raise ValueError("Vector/điểm không được để trống")
        
        clean_v = v.strip().replace(" ", "")
        pattern = r'^-?\d+(\.\d+)?(,-?\d+(\.\d+)?){1,2}$'
        
        if not re.match(pattern, clean_v):
            raise ValueError("Format vector không hợp lệ. Ví dụ: '1,0,1'")
        
        return clean_v

class PlaneData(BaseModel):
    """Plane geometry data model"""
    a: str = Field(..., example="1", description="Hệ số a trong ax+by+cz+d=0")
    b: str = Field(..., example="2", description="Hệ số b trong ax+by+cz+d=0")
    c: str = Field(..., example="3", description="Hệ số c trong ax+by+cz+d=0")
    d: str = Field(..., example="4", description="Hệ số d trong ax+by+cz+d=0")
    
    @validator('a', 'b', 'c', 'd')
    def validate_coefficient(cls, v):
        if not v or not v.strip():
            raise ValueError("Hệ số không được để trống")
        
        clean_v = v.strip()
        try:
            float(clean_v)
            return clean_v
        except ValueError:
            raise ValueError(f"Hệ số phải là số: '{v}'")

class CircleData(BaseModel):
    """Circle geometry data model"""
    center: str = Field(
        ...,
        example="0,0",
        description="Tọa độ tâm đường tròn (x,y)"
    )
    radius: str = Field(
        ...,
        example="5",
        description="Bán kính đường tròn"
    )
    
    @validator('center')
    def validate_center(cls, v):
        if not v or not v.strip():
            raise ValueError("Tọa độ tâm không được để trống")
        
        clean_v = v.strip().replace(" ", "")
        pattern = r'^-?\d+(\.\d+)?,-?\d+(\.\d+)?$'
        
        if not re.match(pattern, clean_v):
            raise ValueError("Format tọa độ tâm không hợp lệ. Ví dụ: '0,0'")
        
        return clean_v
    
    @validator('radius')
    def validate_radius(cls, v):
        if not v or not v.strip():
            raise ValueError("Bán kính không được để trống")
        
        try:
            radius_val = float(v.strip())
            if radius_val <= 0:
                raise ValueError("Bán kính phải là số dương")
            return str(radius_val)
        except ValueError:
            raise ValueError("Bán kính phải là số hợp lệ")

class SphereData(BaseModel):
    """Sphere geometry data model"""
    center: str = Field(
        ...,
        example="0,0,0",
        description="Tọa độ tâm mặt cầu (x,y,z)"
    )
    radius: str = Field(
        ...,
        example="3",
        description="Bán kính mặt cầu"
    )
    
    @validator('center')
    def validate_center(cls, v):
        if not v or not v.strip():
            raise ValueError("Tọa độ tâm không được để trống")
        
        clean_v = v.strip().replace(" ", "")
        pattern = r'^-?\d+(\.\d+)?(,-?\d+(\.\d+)?){2}$'
        
        if not re.match(pattern, clean_v):
            raise ValueError("Format tọa độ tâm không hợp lệ. Ví dụ: '0,0,0'")
        
        return clean_v
    
    @validator('radius')
    def validate_radius(cls, v):
        if not v or not v.strip():
            raise ValueError("Bán kính không được để trống")
        
        try:
            radius_val = float(v.strip())
            if radius_val <= 0:
                raise ValueError("Bán kính phải là số dương")
            return str(radius_val)
        except ValueError:
            raise ValueError("Bán kính phải là số hợp lệ")

# =================================================================
# REQUEST/RESPONSE MODELS
# =================================================================

class GeometryCalculationRequest(BaseModel):
    """
    Main request model for geometry calculations
    
    Supports all geometry operations with appropriate shape data
    based on the selected operation and shapes.
    """
    
    operation: OperationType
    shape_a: ShapeType
    shape_b: Optional[ShapeType] = None
    dimension_a: DimensionType
    dimension_b: Optional[DimensionType] = None
    calculator_version: CalculatorVersion = CalculatorVersion.FX799
    
    # Shape data - conditional based on selected shapes
    point_a: Optional[PointData] = None
    point_b: Optional[PointData] = None
    line_a: Optional[LineData] = None
    line_b: Optional[LineData] = None
    plane_a: Optional[PlaneData] = None
    plane_b: Optional[PlaneData] = None
    circle_a: Optional[CircleData] = None
    circle_b: Optional[CircleData] = None
    sphere_a: Optional[SphereData] = None
    sphere_b: Optional[SphereData] = None
    
    # Processing options
    include_raw_calculation: bool = Field(default=True, description="Bao gồm raw calculation data")
    include_steps: bool = Field(default=False, description="Bao gồm các bước tính toán")
    
    class Config:
        json_schema_extra = {
            "examples": {
                "point_distance_3d": {
                    "summary": "Khoảng cách 2 điểm 3D",
                    "description": "Tính khoảng cách giữa 2 điểm trong không gian 3 chiều",
                    "value": {
                        "operation": "Khoảng cách",
                        "shape_a": "Điểm",
                        "shape_b": "Điểm",
                        "dimension_a": "3",
                        "dimension_b": "3",
                        "calculator_version": "fx799",
                        "point_a": {"coordinates": "1,2,3"},
                        "point_b": {"coordinates": "4,5,6"}
                    }
                },
                "circle_area": {
                    "summary": "Diện tích đường tròn",
                    "description": "Tính diện tích của đường tròn 2D",
                    "value": {
                        "operation": "Diện tích",
                        "shape_a": "Đường tròn",
                        "dimension_a": "2",
                        "calculator_version": "fx799",
                        "circle_a": {
                            "center": "0,0",
                            "radius": "5"
                        }
                    }
                }
            }
        }

class GeometryCalculationResponse(BaseModel):
    """Response model for geometry calculations"""
    
    success: bool
    operation: str
    shape_a: str
    shape_b: Optional[str] = None
    dimension_a: str
    dimension_b: Optional[str] = None
    calculator_version: str
    
    # Results
    encoded_keylog: str = Field(..., description="Keylog đã mã hóa cho máy tính Casio")
    raw_calculation: Dict[str, Any] = Field(..., description="Kết quả tính toán raw")
    
    # Metadata
    processing_time: float = Field(..., description="Thời gian xử lý (giây)")
    timestamp: str = Field(..., description="Thời gian tạo response")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Thông tin bổ sung")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "operation": "Khoảng cách",
                "shape_a": "Điểm",
                "shape_b": "Điểm",
                "dimension_a": "3",
                "dimension_b": "3",
                "calculator_version": "fx799",
                "encoded_keylog": "wj113=2=3=qT11T1224=5=6=CqT3T1RT2=",
                "raw_calculation": {
                    "result_a": ["1", "2", "3"],
                    "result_b": ["4", "5", "6"],
                    "summary": {
                        "distance": 5.196152422706632
                    }
                },
                "processing_time": 0.045,
                "timestamp": "2025-11-05T02:30:00Z"
            }
        }

# =================================================================
# ERROR MODELS
# =================================================================

class ErrorResponse(BaseModel):
    """Standard error response model"""
    success: bool = False
    error: str
    details: Optional[str] = None
    timestamp: str
    error_code: Optional[str] = None
    suggestions: Optional[List[str]] = None

class ValidationErrorResponse(BaseModel):
    """Validation error response model"""
    success: bool = False
    error: str = "Validation Error"
    details: List[Dict[str, Any]]
    timestamp: str
    invalid_fields: Optional[List[str]] = None

# =================================================================
# UTILITY MODELS
# =================================================================

class HealthCheckResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]
    system: Dict[str, str]
    directories: Optional[Dict[str, Any]] = None
    settings: Optional[Dict[str, Any]] = None

class ShapeCompatibilityResponse(BaseModel):
    """Response model for operation-shape compatibility"""
    operation: str
    compatible_shapes: List[str]
    combinations: List[Dict[str, str]]
    examples: Optional[List[Dict[str, Any]]] = None

class ConfigInfoResponse(BaseModel):
    """Configuration information response"""
    geometry_operations: Dict[str, Any]
    supported_versions: List[str] 
    supported_shapes: List[str]
    encoding_rules_count: int
    keylog_patterns_count: int
    timestamp: str

# =================================================================
# VALIDATION REQUEST MODELS
# =================================================================

class ValidationRequest(BaseModel):
    """Request model for input validation only"""
    request_data: GeometryCalculationRequest
    validate_operation_combination: bool = True
    validate_shape_data: bool = True
    check_calculator_support: bool = True

class ValidationResponse(BaseModel):
    """Response model for validation results"""
    valid: bool
    message: str
    issues: List[str] = []
    suggestions: List[str] = []
    estimated_processing_time: Optional[str] = None
    timestamp: str
