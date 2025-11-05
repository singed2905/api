"""
FastAPI routers for different API endpoints

Package chứa các router modules để tổ chức API endpoints.

Active Modules:
- geometry.py: ✅ API endpoints cho geometry calculations

Planned Modules:
- excel.py: API endpoints cho Excel processing  
- auth.py: Authentication và authorization
- monitoring.py: Advanced monitoring và metrics

Mỗi router module sử dụng FastAPI APIRouter để define
các endpoint và được include vào main FastAPI app.
"""

# Import working routers
try:
    from .geometry import router as geometry_router
    _geometry_available = True
except ImportError as e:
    print(f"Warning: Could not import geometry router: {e}")
    geometry_router = None
    _geometry_available = False

# Future routers (placeholder)
# from .excel import router as excel_router
# from .auth import router as auth_router
# from .monitoring import router as monitoring_router

# Available routers for export
__all__ = []

if _geometry_available and geometry_router:
    __all__.append("geometry_router")

# Add other routers when implemented
# __all__.extend(["excel_router", "auth_router", "monitoring_router"])

# Router registry for dynamic loading
AVAILABLE_ROUTERS = {
    "geometry": {
        "router": geometry_router,
        "available": _geometry_available,
        "prefix": "/api/v1",
        "tags": ["geometry"]
    }
    # "excel": {
    #     "router": excel_router,
    #     "available": False,
    #     "prefix": "/api/v1", 
    #     "tags": ["excel"]
    # }
}

# Get list of available router names
def get_available_routers() -> list:
    """Return list of available router names"""
    return [name for name, info in AVAILABLE_ROUTERS.items() if info["available"]]

# Router loading status
ROUTER_STATUS = {
    "total_defined": len(AVAILABLE_ROUTERS),
    "available": len([r for r in AVAILABLE_ROUTERS.values() if r["available"]]),
    "geometry_router": _geometry_available
}
