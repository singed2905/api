"""
FastAPI routers for different API endpoints

Package chứa các router modules để tổ chức API endpoints.

Modules:
- geometry.py: API endpoints cho geometry calculations
- excel.py: API endpoints cho Excel processing
- health.py: Health check và monitoring endpoints

Mỗi router module sử dụng FastAPI APIRouter để define
các endpoint và được include vào main FastAPI app.
"""

from .geometry import router as geometry_router
# from .excel import router as excel_router
# from .health import router as health_router

__all__ = [
    "geometry_router",
    # "excel_router", 
    # "health_router"
]
