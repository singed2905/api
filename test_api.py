#!/usr/bin/env python3
"""
Geometry Calculator API - Fixed Test Script

Script test hoạt động với cả pytest và standalone execution.
Chạy trực tiếp: python test_api.py

Features:
- Comprehensive endpoint testing
- Real API call validation
- Performance measurement
- Error scenario testing
- JSON response validation
"""

import requests
import json
import sys
import time
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
REQUEST_TIMEOUT = 10

# Terminal colors
class TestColors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def log_success(message: str):
    """Log success message"""
    print(f"{TestColors.GREEN}✅ {message}{TestColors.END}")

def log_error(message: str): 
    """Log error message"""
    print(f"{TestColors.RED}❌ {message}{TestColors.END}")

def log_info(message: str):
    """Log info message"""
    print(f"{TestColors.BLUE}🔍 {message}{TestColors.END}")

def log_warning(message: str):
    """Log warning message"""
    print(f"{TestColors.YELLOW}⚠️ {message}{TestColors.END}")

def call_api_endpoint(method: str, url: str, data=None):
    """
    Call API endpoint and return response
    
    Args:
        method: HTTP method
        url: Full URL
        data: Request data for POST
        
    Returns:
        tuple: (success: bool, response_data: dict, status_code: int)
    """
    try:
        start_time = time.time()
        
        if method.upper() == "GET":
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=REQUEST_TIMEOUT)
        else:
            return False, {"error": f"Unsupported method: {method}"}, 0
        
        elapsed_ms = (time.time() - start_time) * 1000
        
        try:
            response_data = response.json()
        except json.JSONDecodeError:
            response_data = {"text_response": response.text}
        
        response_data["_meta"] = {
            "status_code": response.status_code,
            "response_time_ms": round(elapsed_ms, 2)
        }
        
        return response.status_code in [200, 201], response_data, response.status_code
        
    except requests.exceptions.ConnectionError:
        return False, {"error": "Connection failed - API not running?"}, 0
    except requests.exceptions.Timeout:
        return False, {"error": f"Timeout after {REQUEST_TIMEOUT}s"}, 0
    except Exception as e:
        return False, {"error": str(e)}, 0

def test_basic_endpoints():
    """Test basic API endpoints"""
    print(f"\n{TestColors.CYAN}{TestColors.BOLD}BASIC ENDPOINT TESTS{TestColors.END}")
    print("=" * 50)
    
    endpoints = [
        ("Root", "GET", f"{API_BASE_URL}/"),
        ("Health", "GET", f"{API_BASE_URL}/health"),
        ("Shapes", "GET", f"{API_BASE_URL}/api/v1/geometry/shapes"),
        ("Examples", "GET", f"{API_BASE_URL}/api/v1/geometry/examples"),
        ("Config", "GET", f"{API_BASE_URL}/api/v1/geometry/config")
    ]
    
    passed = 0
    for name, method, url in endpoints:
        success, data, status = call_api_endpoint(method, url)
        
        print(f"\n🧪 {name} ({method} {url})")
        print(f"   Status: {status}")
        
        if success:
            print(f"   Time: {data.get('_meta', {}).get('response_time_ms', 0):.1f}ms")
            log_success(f"{name} endpoint - OK")
            passed += 1
        else:
            log_error(f"{name} endpoint - FAILED: {data.get('error', 'Unknown error')}")
    
    return passed, len(endpoints)

def test_geometry_calculations():
    """Test geometry calculation endpoints"""
    print(f"\n{TestColors.CYAN}{TestColors.BOLD}GEOMETRY CALCULATION TESTS{TestColors.END}")
    print("=" * 50)
    
    # Test data
    point_distance_request = {
        "operation": "Khoảng cách",
        "shape_a": "Điểm",
        "shape_b": "Điểm",
        "dimension_a": "3",
        "dimension_b": "3",
        "calculator_version": "fx799",
        "point_a": {"coordinates": "1,2,3"},
        "point_b": {"coordinates": "4,5,6"}
    }
    
    circle_area_request = {
        "operation": "Diện tích",
        "shape_a": "Đường tròn",
        "dimension_a": "2",
        "calculator_version": "fx799",
        "circle_a": {
            "center": "0,0",
            "radius": "5"
        }
    }
    
    calculations = [
        ("Point Distance 3D", point_distance_request),
        ("Circle Area 2D", circle_area_request)
    ]
    
    passed = 0
    for name, request_data in calculations:
        success, data, status = call_api_endpoint(
            "POST", 
            f"{API_BASE_URL}/api/v1/geometry/calculate", 
            request_data
        )
        
        print(f"\n📊 {name} Calculation")
        print(f"   Status: {status}")
        
        if success:
            print(f"   Time: {data.get('_meta', {}).get('response_time_ms', 0):.1f}ms")
            if 'encoded_keylog' in data:
                print(f"   Keylog: {data['encoded_keylog'][:50]}...")
            log_success(f"{name} calculation - OK")
            passed += 1
        else:
            log_error(f"{name} calculation - FAILED: {data.get('error', 'Unknown')}")
    
    return passed, len(calculations)

def test_api_comprehensive():
    """Run comprehensive API test suite"""
    print(f"{TestColors.CYAN}{TestColors.BOLD}GEOMETRY CALCULATOR API - COMPREHENSIVE TESTS{TestColors.END}")
    print(f"Testing API at: {API_BASE_URL}")
    print(f"Timestamp: {datetime.now()}\n")
    
    # Check API availability
    log_info("Checking API availability...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            log_error("API health check failed!")
            log_warning("Make sure API is running: ./run.sh")
            return False
    except Exception as e:
        log_error(f"Cannot connect to API: {e}")
        log_warning("Start API first: ./run.sh")
        return False
    
    log_success("API is accessible!")
    
    # Run test suites
    total_passed = 0
    total_tests = 0
    
    # Basic endpoints
    passed, tests = test_basic_endpoints()
    total_passed += passed
    total_tests += tests
    
    # Geometry calculations
    passed, tests = test_geometry_calculations()
    total_passed += passed
    total_tests += tests
    
    # Results summary
    print(f"\n{TestColors.CYAN}{TestColors.BOLD}FINAL RESULTS{TestColors.END}")
    print("=" * 50)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success Rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_passed == total_tests:
        print(f"\n{TestColors.GREEN}{TestColors.BOLD}🎉 ALL TESTS PASSED!{TestColors.END}")
        print(f"{TestColors.GREEN}API is ready for use!{TestColors.END}")
        return True
    else:
        print(f"\n{TestColors.RED}{TestColors.BOLD}❌ {total_tests - total_passed} TEST(S) FAILED{TestColors.END}")
        return False

# For pytest compatibility (if accidentally run with pytest)
def test_api_health():
    """Pytest compatible health test"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        print("✅ Health check passed")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        raise

def test_api_shapes():
    """Pytest compatible shapes test"""
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/geometry/shapes", timeout=5)
        assert response.status_code == 200
        data = response.json()
        assert "shapes" in data
        print("✅ Shapes endpoint passed")
    except Exception as e:
        print(f"❌ Shapes test failed: {e}")
        raise

def test_point_distance():
    """Pytest compatible calculation test"""
    test_data = {
        "operation": "Khoảng cách",
        "shape_a": "Điểm",
        "shape_b": "Điểm",
        "dimension_a": "3",
        "dimension_b": "3",
        "calculator_version": "fx799",
        "point_a": {"coordinates": "1,2,3"},
        "point_b": {"coordinates": "4,5,6"}
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/geometry/calculate",
            json=test_data,
            timeout=REQUEST_TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert "encoded_keylog" in data
        print("✅ Point distance calculation passed")
    except Exception as e:
        print(f"❌ Point distance calculation failed: {e}")
        raise

def test_circle_area():
    """Pytest compatible area calculation test"""
    test_data = {
        "operation": "Diện tích",
        "shape_a": "Đường tròn",
        "dimension_a": "2",
        "calculator_version": "fx799",
        "circle_a": {
            "center": "0,0",
            "radius": "5"
        }
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/v1/geometry/calculate",
            json=test_data,
            timeout=REQUEST_TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert "encoded_keylog" in data
        print("✅ Circle area calculation passed")
    except Exception as e:
        print(f"❌ Circle area calculation failed: {e}")
        raise

if __name__ == "__main__":
    # When run directly (not with pytest)
    print("🚀 Running Geometry Calculator API Tests (Standalone Mode)")
    success = test_api_comprehensive()
    sys.exit(0 if success else 1)
