#!/usr/bin/env python3
"""
Geometry Calculator API - Comprehensive Test Script

Script test đầy đủ cho tất cả API endpoints với:
- Health checks
- Configuration validation
- Geometry calculations  
- Error handling tests
- Performance measurements
- JSON config verification

Usage:
    python test_api.py
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*50}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text.center(50)}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*50}{Colors.END}")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️ {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}🔍 {text}{Colors.END}")

def test_endpoint(name: str, method: str, url: str, data: Dict = None, expected_status: int = 200) -> bool:
    """
    Test an API endpoint
    
    Args:
        name: Test name
        method: HTTP method
        url: Endpoint URL
        data: Request data (for POST)
        expected_status: Expected HTTP status code
        
    Returns:
        True if test passed
    """
    try:
        start_time = time.time()
        
        if method.upper() == "GET":
            response = requests.get(url, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, timeout=10)
        else:
            print_error(f"Unsupported method: {method}")
            return False
        
        elapsed = (time.time() - start_time) * 1000
        
        print(f"\n{Colors.PURPLE}🧪 {name}{Colors.END}")
        print(f"   URL: {url}")
        print(f"   Status: {response.status_code} (expected: {expected_status})")
        print(f"   Time: {elapsed:.1f}ms")
        
        if response.status_code == expected_status:
            try:
                result = response.json()
                print(f"   Response: {Colors.WHITE}{json.dumps(result, indent=2, ensure_ascii=False)[:200]}...{Colors.END}")
                print_success(f"{name} - PASSED")
                return True
            except json.JSONDecodeError:
                print(f"   Response: {response.text[:200]}...")
                print_success(f"{name} - PASSED (non-JSON response)")
                return True
        else:
            print(f"   Error: {response.text[:200]}")
            print_error(f"{name} - FAILED")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error(f"{name} - CONNECTION ERROR (Is API running?)")
        return False
    except requests.exceptions.Timeout:
        print_error(f"{name} - TIMEOUT")
        return False
    except Exception as e:
        print_error(f"{name} - ERROR: {str(e)}")
        return False

def test_geometry_calculation():
    """Test geometry calculation endpoint with real data"""
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
    
    return test_endpoint(
        "Geometry Calculation - Point Distance",
        "POST",
        f"{BASE_URL}/api/v1/geometry/calculate",
        test_data
    )

def test_circle_area_calculation():
    """Test circle area calculation"""
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
    
    return test_endpoint(
        "Geometry Calculation - Circle Area",
        "POST",
        f"{BASE_URL}/api/v1/geometry/calculate",
        test_data
    )

def test_validation():
    """Test input validation"""
    test_data = {
        "request_data": {
            "operation": "Khoảng cách",
            "shape_a": "Điểm",
            "shape_b": "Điểm",
            "dimension_a": "3",
            "dimension_b": "3",
            "calculator_version": "fx799",
            "point_a": {"coordinates": "1,2,3"},
            "point_b": {"coordinates": "4,5,6"}
        },
        "validate_operation_combination": True,
        "validate_shape_data": True,
        "check_calculator_support": True
    }
    
    return test_endpoint(
        "Input Validation",
        "POST",
        f"{BASE_URL}/api/v1/geometry/validate",
        test_data
    )

def run_all_tests():
    """Run all API tests"""
    print_header("GEOMETRY CALCULATOR API TESTS")
    print(f"{Colors.BLUE}Testing API at: {BASE_URL}{Colors.END}")
    print(f"{Colors.BLUE}Timestamp: {datetime.now().isoformat()}{Colors.END}")
    
    tests = [
        # Basic endpoints
        ("Health Check", "GET", f"{BASE_URL}/health"),
        ("Root Endpoint", "GET", f"{BASE_URL}/"),
        
        # Geometry endpoints
        ("Available Shapes", "GET", f"{BASE_URL}/api/v1/geometry/shapes"),
        ("Geometry Examples", "GET", f"{BASE_URL}/api/v1/geometry/examples"),
        ("Geometry Config", "GET", f"{BASE_URL}/api/v1/geometry/config"),
        ("Geometry Health", "GET", f"{BASE_URL}/api/v1/geometry/health"),
        
        # Operation compatibility
        ("Compatible Shapes - Distance", "GET", f"{BASE_URL}/api/v1/geometry/operations/Khoảng cách/shapes"),
        ("Compatible Shapes - Area", "GET", f"{BASE_URL}/api/v1/geometry/operations/Diện tích/shapes"),
    ]
    
    passed = 0
    total = len(tests)
    
    # Run basic endpoint tests
    for test_name, method, url in tests:
        if test_endpoint(test_name, method, url):
            passed += 1
    
    # Run calculation tests
    print_header("CALCULATION TESTS")
    
    if test_geometry_calculation():
        passed += 1
    total += 1
    
    if test_circle_area_calculation():
        passed += 1
    total += 1
    
    if test_validation():
        passed += 1
    total += 1
    
    # Error handling tests
    print_header("ERROR HANDLING TESTS")
    
    if test_endpoint(
        "Invalid Operation Test",
        "POST", 
        f"{BASE_URL}/api/v1/geometry/calculate",
        {
            "operation": "Invalid Operation",
            "shape_a": "Điểm",
            "dimension_a": "3",
            "calculator_version": "fx799"
        },
        expected_status=422  # Validation error expected
    ):
        passed += 1
    total += 1
    
    # Final results
    print_header("TEST RESULTS")
    print(f"\n{Colors.BOLD}Total Tests: {total}{Colors.END}")
    print(f"{Colors.GREEN}{Colors.BOLD}Passed: {passed}{Colors.END}")
    print(f"{Colors.RED}{Colors.BOLD}Failed: {total - passed}{Colors.END}")
    print(f"{Colors.BLUE}{Colors.BOLD}Success Rate: {(passed/total)*100:.1f}%{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ ALL TESTS PASSED! API is working correctly.{Colors.END}")
        print(f"{Colors.GREEN}\n🎉 Geometry Calculator API is ready to use!{Colors.END}")
        print(f"{Colors.BLUE}\n📚 Visit http://localhost:8000/docs for interactive documentation{Colors.END}")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ Some tests failed. Check API logs for details.{Colors.END}")
        print(f"{Colors.YELLOW}\n📝 Make sure API is running: ./run.sh{Colors.END}")
        return False

if __name__ == "__main__":
    print(f"{Colors.BLUE}{Colors.BOLD}Geometry Calculator API Test Suite{Colors.END}")
    print(f"{Colors.BLUE}Version: 2.1.0{Colors.END}")
    
    success = run_all_tests()
    
    sys.exit(0 if success else 1)
