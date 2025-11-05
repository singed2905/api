"""
FastAPI main application

Complete implementation của Geometry Calculator API với:
- CORS middleware
- Error handling
- Health checks
- Router inclusion
- System monitoring
- OpenAPI documentation

Production-ready với comprehensive logging và monitoring.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import uvicorn
import os
import logging
from datetime import datetime
import psutil
import traceback
from pathlib import Path

from .config import settings
from .models.geometry import ErrorResponse

# =================================================================
# LOGGING SETUP
# =================================================================
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# =================================================================
# CREATE FASTAPI APP
# =================================================================
app = FastAPI(
    title="Geometry Calculator API",
    description="""
    🔧 **API chuyển đổi từ Desktop Geometry Mode thành Web Service**
    
    API này cung cấp đầy đủ chức năng của **Geometry Mode** từ desktop application,
    được thiết kế để tích hợp vào các ứng dụng web hiện đại.
    
    **Tính năng chính:**
    - Tính toán hình học 2D/3D
    - Xử lý Excel batch processing
    - Mã hóa keylog cho máy tính Casio
    - Memory monitoring và optimization
    """,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# =================================================================
# MIDDLEWARE SETUP
# =================================================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = datetime.now()
    
    try:
        response = await call_next(request)
        processing_time = (datetime.now() - start_time).total_seconds()
        
        logger.info(
            f"{request.method} {request.url.path} - "
            f"Status: {response.status_code} - "
            f"Time: {processing_time:.3f}s"
        )
        
        return response
    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.error(
            f"{request.method} {request.url.path} - "
            f"Error: {str(e)} - "
            f"Time: {processing_time:.3f}s"
        )
        raise

# =================================================================
# EXCEPTION HANDLERS
# =================================================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation Error",
            "details": exc.errors(),
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": "HTTP Error",
            "details": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: Exception):
    """Handle internal server errors"""
    logger.error(f"Internal error on {request.url.path}: {str(exc)}\n{traceback.format_exc()}")
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "details": "Lỗi xử lý nội bộ. Vui lòng thử lại sau." if not settings.debug else str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

# =================================================================
# STARTUP/SHUTDOWN EVENTS
# =================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("Starting Geometry Calculator API...")
    
    # Create necessary directories
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.output_dir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    # Log startup info
    logger.info(f"API Version: {settings.app_version}")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info(f"Config Directory: {settings.config_dir}")
    logger.info(f"Upload Directory: {settings.upload_dir}")
    logger.info(f"Supported Calculators: {settings.supported_versions}")
    
    # Test config loading
    try:
        operations = settings.geometry_operations
        logger.info(f"Loaded {len(operations.get('operations', {}))} geometry operations")
        
        calc_configs = settings.calculator_configs
        logger.info(f"Loaded {len(calc_configs)} calculator configurations")
        
    except Exception as e:
        logger.warning(f"Config loading issues: {e}")
    
    logger.info("✅ Geometry Calculator API startup completed!")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("Shutting down Geometry Calculator API...")
    
    # Cleanup tasks if needed
    # - Close database connections
    # - Cancel background tasks
    # - Clean temporary files
    
    logger.info("✅ Shutdown completed!")

# =================================================================
# ROOT ENDPOINTS
# =================================================================

@app.get("/")
async def root():
    """
    API root endpoint với thông tin cơ bản
    
    Returns basic information about the API, available endpoints,
    và current status.
    """
    return {
        "message": "🔧 Geometry Calculator API",
        "description": "API chuyển đổi từ Desktop Geometry Mode thành Web Service",
        "version": settings.app_version,
        "status": "active",
        "features": [
            "Geometry calculations (2D/3D)",
            "Excel batch processing",
            "Casio keylog encoding",
            "Multi-calculator support",
            "Memory monitoring"
        ],
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "geometry_api": "/api/v1/geometry/",
            "openapi_schema": "/openapi.json"
        },
        "supported_calculators": settings.supported_versions,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """
    Comprehensive health check endpoint
    
    Kiểm tra:
    - Service status
    - System resources
    - Config loading
    - Directory access
    """
    try:
        # System info
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Directory checks
        directories = {
            "upload_dir": {
                "path": settings.upload_dir,
                "exists": os.path.exists(settings.upload_dir),
                "writable": os.access(settings.upload_dir, os.W_OK) if os.path.exists(settings.upload_dir) else False
            },
            "output_dir": {
                "path": settings.output_dir,
                "exists": os.path.exists(settings.output_dir),
                "writable": os.access(settings.output_dir, os.W_OK) if os.path.exists(settings.output_dir) else False
            },
            "config_dir": {
                "path": settings.config_dir,
                "exists": os.path.exists(settings.config_dir),
                "readable": os.access(settings.config_dir, os.R_OK) if os.path.exists(settings.config_dir) else False
            }
        }
        
        # Config loading test
        services_status = {}
        try:
            operations = settings.geometry_operations
            services_status["geometry_operations"] = "active" if operations else "no_config"
        except Exception:
            services_status["geometry_operations"] = "error"
            
        try:
            calc_configs = settings.calculator_configs
            services_status["calculator_configs"] = "active" if calc_configs else "no_config"
        except Exception:
            services_status["calculator_configs"] = "error"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": settings.app_version,
            "services": {
                "geometry_service": "ready",
                "config_loader": "active",
                **services_status
            },
            "system": {
                "memory_usage": f"{memory.percent}%",
                "memory_available": f"{memory.available / (1024**3):.1f}GB",
                "cpu_usage": f"{cpu_percent}%"
            },
            "directories": directories,
            "configuration": {
                "debug_mode": settings.debug,
                "supported_versions": len(settings.supported_versions),
                "config_files_loaded": len(settings.calculator_configs)
            }
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
                "version": settings.app_version
            }
        )

# =================================================================
# INCLUDE ROUTERS
# =================================================================

# Import and include geometry router
try:
    from .routers import geometry
    app.include_router(geometry.router, prefix="/api/v1")
    logger.info("✅ Geometry router included successfully")
except ImportError as e:
    logger.warning(f"⚠️ Could not import geometry router: {e}")

# Future routers will be added here:
# from .routers import excel, auth
# app.include_router(excel.router, prefix="/api/v1")
# app.include_router(auth.router, prefix="/api/v1")

# =================================================================
# DEVELOPMENT SERVER
# =================================================================

if __name__ == "__main__":
    logger.info(f"Starting Geometry Calculator API on {settings.host}:{settings.port}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Documentation: http://{settings.host}:{settings.port}/docs")
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )
