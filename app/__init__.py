"""
Geometry Calculator API - Main Application Package

Complete FastAPI application cho Geometry Mode calculations.

Main components:
- FastAPI application instance
- API routers và endpoints  
- Pydantic models và validation
- Services và business logic
- Configuration management
- Utilities và helpers

Version: 2.1.0
Author: Đặng Vũ Hưng (singed2905)
Created: 2025-11-05
"""

__version__ = "2.1.0"
__title__ = "Geometry Calculator API"
__description__ = "API chuyển đổi từ Desktop Geometry Mode thành Web Service"
__author__ = "Đặng Vũ Hưng"
__email__ = "support@geometryapi.com"
__license__ = "MIT"
__url__ = "https://github.com/singed2905/api"

# Legacy metadata for compatibility
APP_NAME = "Geometry Calculator API"
APP_DESCRIPTION = "API chuyển đổi từ Desktop Geometry Mode thành Web Service"
APP_VERSION = __version__
API_PREFIX = "/api/v1"
API_TITLE = "Geometry Calculator API"
API_DESCRIPTION = """
API cung cấp đầy đủ chức năng của Geometry Mode từ desktop application,
được thiết kế để tích hợp vào các ứng dụng web hiện đại.

Tính năng chính:
- Tính toán hình học (khoảng cách, tương giao, diện tích, thể tích)
- Xử lý Excel batch với anti-crash system
- Mã hóa keylog cho máy tính Casio
- Memory monitoring và optimization
"""

# Main exports
try:
    from .main import app
    from .config import settings
    
    # Test basic functionality
    if app and settings:
        _app_ready = True
    else:
        _app_ready = False
        
except ImportError as e:
    print(f"Warning: Could not import main components: {e}")
    app = None
    settings = None
    _app_ready = False

__all__ = [
    "app",
    "settings", 
    "__version__",
    "__title__",
    "__description__",
    "APP_NAME",
    "APP_VERSION",
    "API_PREFIX"
]

# Package status info
PACKAGE_STATUS = {
    "ready": _app_ready,
    "version": __version__,
    "components": {
        "fastapi_app": app is not None,
        "settings": settings is not None
    }
}
