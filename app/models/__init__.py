"""
Pydantic models for API request/response validation

Package chứa các model để validate dữ liệu đầu vào và đầu ra của API.

Modules:
- geometry.py: Models cho geometry calculations
- excel.py: Models cho Excel processing  
- common.py: Common models và base classes
"""

from .geometry import (
    # Enums
    ShapeType,
    OperationType,
    DimensionType,
    CalculatorVersion,
    
    # Data models
    PointData,
    LineData,
    PlaneData,
    CircleData,
    SphereData,
    
    # Request/Response models
    GeometryCalculationRequest,
    GeometryCalculationResponse,
    ErrorResponse,
    ValidationErrorResponse,
    HealthCheckResponse
)

__all__ = [
    # Enums
    "ShapeType",
    "OperationType", 
    "DimensionType",
    "CalculatorVersion",
    
    # Data models
    "PointData",
    "LineData", 
    "PlaneData",
    "CircleData",
    "SphereData",
    
    # Request/Response models
    "GeometryCalculationRequest",
    "GeometryCalculationResponse",
    "ErrorResponse",
    "ValidationErrorResponse", 
    "HealthCheckResponse"
]
