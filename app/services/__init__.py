"""
Business logic services

Package chứa các service modules để xử lý business logic
và tích hợp với các services từ desktop application gốc.

Modules:
- geometry_service_adapter.py: Adapter để bridge FastAPI với GeometryService cũ
- geometry/: Package chứa GeometryService và related services từ project gốc
- excel/: Package chứa Excel processing services
- utils/: Common utilities cho services

Các service adapter chịu trách nhiệm:
- Chuyển đổi request/response format
- Handle async operations
- Error handling và logging
- Integration với các services cũ
"""

# TODO: Import các service adapters khi đã implement
# from .geometry_service_adapter import GeometryServiceAdapter
# from .excel_service_adapter import ExcelServiceAdapter

__all__ = [
    # "GeometryServiceAdapter",
    # "ExcelServiceAdapter"
]
