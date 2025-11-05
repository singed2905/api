"""
FastAPI router cho Geometry API endpoints

Complete implementation của tất cả geometry endpoints với:
- POST /calculate: Tính toán hình học
- GET /shapes: Danh sách hình học và operations
- GET /operations/{operation}/shapes: Compatible shapes
- POST /validate: Validate input
- GET /examples: Ví dụ usage
- GET /config: Debug config info
- GET /health: Geometry service health

Tất cả endpoints sử dụng async/await và comprehensive error handling.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Any, List, Optional
import time
from datetime import datetime
import logging
import json

from ..models.geometry import (
    GeometryCalculationRequest,
    GeometryCalculationResponse,
    ErrorResponse,
    ValidationRequest,
    ValidationResponse,
    ShapeCompatibilityResponse,
    ConfigInfoResponse,
    HealthCheckResponse
)
from ..config import settings

# Setup logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/geometry", tags=["Geometry Calculations"])

# =================================================================
# HELPER FUNCTIONS
# =================================================================

def generate_mock_keylog(request: GeometryCalculationRequest) -> str:
    """
    Generate mock keylog - sẽ replace với actual implementation
    
    Temporary function để generate basic keylog format
    dựa trên patterns từ JSON config.
    """
    try:
        # Get calculator-specific prefix
        version = request.calculator_version.value
        
        # Basic pattern: wj + coordinates + qT + operation
        if request.point_a:
            coords = request.point_a.coordinates.replace(",", "=") + "="
            keylog = f"wj11{coords}qT"
            
            if request.point_b:
                coords_b = request.point_b.coordinates.replace(",", "=") + "="
                keylog += f"1T12{coords_b}CqT3T1RT2="
            
            return keylog
        
        # Default mock keylog
        return f"w9_mock_keylog_{version}_{int(time.time())}"
        
    except Exception as e:
        logger.error(f"Mock keylog generation error: {e}")
        return "w9_mock_keylog_error"

def get_operation_result_summary(request: GeometryCalculationRequest) -> Dict[str, Any]:
    """
    Generate mock calculation summary
    
    Sẽ replace với actual geometry service implementation.
    """
    summary = {
        "operation": request.operation.value,
        "shape_a": request.shape_a.value,
        "calculator_version": request.calculator_version.value,
        "processing_mode": "mock"
    }
    
    if request.shape_b:
        summary["shape_b"] = request.shape_b.value
    
    # Mock results based on operation type
    if request.operation.value == "Khoảng cách" and request.point_a and request.point_b:
        try:
            coords_a = [float(x) for x in request.point_a.coordinates.split(",")]
            coords_b = [float(x) for x in request.point_b.coordinates.split(",")]
            
            # Simple Euclidean distance calculation
            distance = sum((a - b) ** 2 for a, b in zip(coords_a, coords_b)) ** 0.5
            summary["result"] = {
                "distance": round(distance, 6),
                "unit": "units"
            }
        except Exception:
            summary["result"] = {"mock": "Distance calculation placeholder"}
    
    elif request.operation.value == "Diện tích" and request.circle_a:
        try:
            radius = float(request.circle_a.radius)
            area = 3.14159 * radius * radius
            summary["result"] = {
                "area": round(area, 6),
                "unit": "square_units"
            }
        except Exception:
            summary["result"] = {"mock": "Area calculation placeholder"}
    
    else:
        summary["result"] = {"mock": f"Placeholder for {request.operation.value}"}
    
    return summary

# =================================================================
# MAIN ENDPOINTS
# =================================================================

@router.post("/calculate", response_model=GeometryCalculationResponse)
async def calculate_geometry(request: GeometryCalculationRequest):
    """
    Tính toán hình học chính
    
    Xử lý tất cả loại phép toán hình học:
    - Khoảng cách giữa các đối tượng
    - Tương giao giữa hình học
    - Diện tích và thể tích
    - Phương trình đường thẳng
    
    Trả về keylog đã mã hóa cho máy tính Casio.
    """
    
    start_time = time.time()
    
    try:
        logger.info(f"Processing geometry calculation: {request.operation.value} - {request.shape_a.value}")
        
        # Validate operation combination using JSON config
        valid_combo = settings.validate_operation_combination(
            request.operation.value,
            request.shape_a.value, 
            request.shape_b.value if request.shape_b else None
        )
        
        if not valid_combo:
            raise HTTPException(
                status_code=400,
                detail={
                    "success": False,
                    "error": "Invalid Operation Combination",
                    "details": f"Operation '{request.operation.value}' không hỗ trợ cho '{request.shape_a.value}'",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Generate keylog (mock implementation)
        encoded_keylog = generate_mock_keylog(request)
        
        # Get calculation summary
        raw_calculation = get_operation_result_summary(request)
        
        # Calculate processing time
        processing_time = round(time.time() - start_time, 6)
        
        response = GeometryCalculationResponse(
            success=True,
            operation=request.operation.value,
            shape_a=request.shape_a.value,
            shape_b=request.shape_b.value if request.shape_b else None,
            dimension_a=request.dimension_a.value,
            dimension_b=request.dimension_b.value if request.dimension_b else None,
            calculator_version=request.calculator_version.value,
            encoded_keylog=encoded_keylog,
            raw_calculation=raw_calculation,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat(),
            metadata={
                "request_id": f"req_{int(time.time() * 1000)}",
                "processing_node": "geometry_api_v1",
                "cache_used": False
            }
        )
        
        logger.info(f"Calculation completed in {processing_time}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = round(time.time() - start_time, 6)
        logger.error(f"Calculation error after {processing_time}s: {str(e)}")
        
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Calculation Error",
                "details": str(e) if settings.debug else "Lỗi xử lý tính toán",
                "processing_time": processing_time,
                "timestamp": datetime.now().isoformat()
            }
        )

@router.get("/shapes")
async def get_available_shapes():
    """
    Lấy danh sách các hình học và operations được hỗ trợ
    
    Load từ JSON configuration để đảm bảo data luôn updated.
    """
    
    try:
        # Load from JSON config
        operations_config = settings.geometry_operations
        
        if not operations_config:
            raise HTTPException(
                status_code=503,
                detail="Không thể load geometry operations config"
            )
        
        # Extract shapes from coordinate systems
        shapes = set()
        coordinate_systems = operations_config.get("coordinate_systems", {})
        
        for dim, dim_info in coordinate_systems.items():
            shapes.update(dim_info.get("supported_objects", []))
        
        # Extract operations
        operations = list(operations_config.get("operations", {}).keys())
        
        return {
            "shapes": sorted(list(shapes)),
            "operations": operations,
            "coordinate_systems": list(coordinate_systems.keys()),
            "calculator_versions": settings.supported_versions,
            "total_shapes": len(shapes),
            "total_operations": len(operations),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting shapes: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Không thể load danh sách shapes",
                "details": str(e) if settings.debug else "Lỗi config"
            }
        )

@router.get("/operations/{operation}/shapes", response_model=ShapeCompatibilityResponse)
async def get_compatible_shapes(operation: str):
    """
    Lấy danh sách hình học tương thích với operation cụ thể
    
    Args:
        operation: Tên phép toán (Khoảng cách, Tương giao, etc.)
    """
    
    try:
        operations_config = settings.geometry_operations
        operations = operations_config.get("operations", {})
        
        if operation not in operations:
            raise HTTPException(
                status_code=404,
                detail=f"Operation '{operation}' không được hỗ trợ"
            )
        
        op_config = operations[operation]
        compatible_shapes = set()
        combinations = []
        
        # Handle single-shape operations (Area, Volume)
        if "supported_objects" in op_config:
            for obj in op_config["supported_objects"]:
                compatible_shapes.add(obj["type"])
                combinations.append({
                    "shape": obj["type"],
                    "formula": obj.get("formula", "N/A"),
                    "type": "single_shape"
                })
        
        # Handle two-shape operations (Distance, Intersection)
        if "supported_combinations" in op_config:
            for combo in op_config["supported_combinations"]:
                compatible_shapes.add(combo["type1"])
                compatible_shapes.add(combo["type2"])
                combinations.append({
                    "shape_a": combo["type1"],
                    "shape_b": combo["type2"],
                    "result_type": combo["result"],
                    "type": "two_shape"
                })
        
        return ShapeCompatibilityResponse(
            operation=operation,
            compatible_shapes=sorted(list(compatible_shapes)),
            combinations=combinations,
            examples=[
                {
                    "description": f"Ví dụ cho operation {operation}",
                    "shapes_used": list(compatible_shapes)[:2] if len(compatible_shapes) >= 2 else list(compatible_shapes)
                }
            ]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting compatible shapes for {operation}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi xử lý operation {operation}: {str(e)}"
        )

@router.post("/validate", response_model=ValidationResponse)
async def validate_geometry_input(validation_request: ValidationRequest):
    """
    Validate geometry calculation input
    
    Kiểm tra input có hợp lệ trước khi thực hiện calculation.
    """
    
    try:
        request = validation_request.request_data
        issues = []
        suggestions = []
        
        # Validate operation combination
        if validation_request.validate_operation_combination:
            valid_combo = settings.validate_operation_combination(
                request.operation.value,
                request.shape_a.value,
                request.shape_b.value if request.shape_b else None
            )
            
            if not valid_combo:
                issues.append(f"Operation '{request.operation.value}' không tương thích với '{request.shape_a.value}'")
                suggestions.append("Kiểm tra /operations/{operation}/shapes để xem các combinations hỗ trợ")
        
        # Validate calculator version
        if validation_request.check_calculator_support:
            if request.calculator_version.value not in settings.supported_versions:
                issues.append(f"Calculator version '{request.calculator_version.value}' không được hỗ trợ")
                suggestions.append(f"Các version hỗ trợ: {', '.join(settings.supported_versions)}")
        
        # Validate shape data presence
        if validation_request.validate_shape_data:
            if request.shape_a.value == "Điểm" and not request.point_a:
                issues.append("Thiếu dữ liệu point_a")
            if request.shape_b and request.shape_b.value == "Điểm" and not request.point_b:
                issues.append("Thiếu dữ liệu point_b")
            # Add more validations for other shapes...
        
        is_valid = len(issues) == 0
        
        return ValidationResponse(
            valid=is_valid,
            message="Dữ liệu hợp lệ" if is_valid else "Dữ liệu có vấn đề",
            issues=issues,
            suggestions=suggestions,
            estimated_processing_time="< 1s" if is_valid else None,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi validation: {str(e)}"
        )

@router.get("/examples")
async def get_calculation_examples():
    """
    Lấy các ví dụ request cho từng loại calculation
    
    Giúp developers hiểu cách sử dụng API đúng cách.
    """
    
    examples = {
        "point_distance_3d": {
            "description": "Tính khoảng cách giữa 2 điểm trong không gian 3D",
            "method": "POST",
            "endpoint": "/api/v1/geometry/calculate",
            "request_body": {
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
        "circle_area_2d": {
            "description": "Tính diện tích đường tròn 2D",
            "method": "POST", 
            "endpoint": "/api/v1/geometry/calculate",
            "request_body": {
                "operation": "Diện tích",
                "shape_a": "Đường tròn",
                "dimension_a": "2",
                "calculator_version": "fx799",
                "circle_a": {
                    "center": "0,0",
                    "radius": "5"
                }
            }
        },
        "sphere_volume_3d": {
            "description": "Tính thể tích mặt cầu 3D",
            "method": "POST",
            "endpoint": "/api/v1/geometry/calculate", 
            "request_body": {
                "operation": "Thể tích",
                "shape_a": "Mặt cầu",
                "dimension_a": "3",
                "calculator_version": "fx880",
                "sphere_a": {
                    "center": "0,0,0",
                    "radius": "3"
                }
            }
        },
        "line_intersection_3d": {
            "description": "Giao điểm 2 đường thẳng trong không gian 3D",
            "method": "POST",
            "endpoint": "/api/v1/geometry/calculate",
            "request_body": {
                "operation": "Tương giao",
                "shape_a": "Đường thẳng",
                "shape_b": "Đường thẳng",
                "dimension_a": "3",
                "dimension_b": "3",
                "calculator_version": "fx991",
                "line_a": {
                    "point": "1,2,3",
                    "direction_vector": "1,0,1"
                },
                "line_b": {
                    "point": "0,1,2", 
                    "direction_vector": "0,1,0"
                }
            }
        }
    }
    
    return {
        "examples": examples,
        "total_examples": len(examples),
        "usage_instructions": {
            "step1": "Chọn example phù hợp",
            "step2": "Copy request_body",
            "step3": "POST đến endpoint tương ứng",
            "step4": "Nhận keylog đã mã hóa"
        },
        "timestamp": datetime.now().isoformat()
    }

@router.get("/config", response_model=ConfigInfoResponse)
async def get_geometry_config():
    """
    Debug endpoint để xem config đã load
    
    Useful cho development và troubleshooting.
    """
    
    try:
        operations = settings.geometry_operations
        encoding_rules = settings.encoding_rules
        keylog_patterns = settings.keylog_patterns
        
        return ConfigInfoResponse(
            geometry_operations=operations,
            supported_versions=settings.supported_versions,
            supported_shapes=settings.get_supported_shapes(),
            encoding_rules_count=len(encoding_rules.get("latex_to_calculator_mappings", [])),
            keylog_patterns_count=len(keylog_patterns.get("keylog_patterns", {})),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Không thể load config: {str(e)}"
        )

@router.get("/health", response_model=HealthCheckResponse)
async def geometry_health_check():
    """
    Health check cụ thể cho geometry service
    
    Kiểm tra tình trạng của geometry service và các dependencies.
    """
    
    try:
        # Test config loading
        services_status = {}
        
        try:
            operations = settings.geometry_operations
            services_status["geometry_operations"] = "loaded" if operations else "empty"
        except Exception:
            services_status["geometry_operations"] = "error"
        
        try:
            calc_configs = settings.calculator_configs
            services_status["calculator_configs"] = f"loaded_{len(calc_configs)}"
        except Exception:
            services_status["calculator_configs"] = "error"
            
        try:
            encoding_rules = settings.encoding_rules
            services_status["encoding_rules"] = "loaded" if encoding_rules else "empty"
        except Exception:
            services_status["encoding_rules"] = "error"
        
        # System resources
        memory = psutil.virtual_memory()
        
        return HealthCheckResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            version=settings.app_version,
            services=services_status,
            system={
                "memory_usage": f"{memory.percent}%",
                "available_memory": f"{memory.available / (1024**3):.1f}GB",
                "geometry_service": "active"
            }
        )
        
    except Exception as e:
        logger.error(f"Geometry health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "service": "geometry"
            }
        )
