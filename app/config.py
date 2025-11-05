"""
Application configuration settings

Defines các configuration settings cho FastAPI application
sử dụng Pydantic BaseSettings để load từ environment variables.

Configuration sections:
- API settings: app name, version, debug mode
- Server settings: host, port
- File processing: upload limits, directories
- Security: CORS, allowed origins
- Geometry service: calculator versions, processing limits

Các settings có thể được override thông qua .env file.
"""

# TODO: Import và implement Pydantic settings
# from pydantic_settings import BaseSettings
# from typing import List
# import os

class MockSettings:
    """Placeholder settings class"""
    
    def __init__(self):
        # API Settings
        self.app_name = "Geometry Calculator API"
        self.app_version = "2.1.0"
        self.debug = True
        
        # Server Settings
        self.host = "0.0.0.0"
        self.port = 8000
        
        # File Processing
        self.max_file_size = 100 * 1024 * 1024  # 100MB
        self.upload_dir = "uploads"
        self.output_dir = "outputs"
        self.large_file_threshold = 50 * 1024 * 1024  # 50MB
        
        # Security
        self.allowed_origins = ["*"]
        self.allowed_file_types = [".xlsx", ".xls"]
        
        # Processing
        self.chunk_size = 1000
        self.max_background_tasks = 5
        self.cleanup_interval_hours = 24
        
        # Geometry Service
        self.default_calculator_version = "fx799"
        self.supported_versions = ["fx799", "fx991", "fx570", "fx880", "fx801"]
        
        # Database (optional)
        self.database_url = "sqlite:///./geometry_api.db"

# Placeholder settings instance
settings = MockSettings()

# TODO: Replace với actual Pydantic BaseSettings implementation
