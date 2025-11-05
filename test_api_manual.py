#!/usr/bin/env python3
"""
Geometry Calculator API - Manual Test Script

Script test thủ công cho tất cả API endpoints.
Chạy độc lập, không cần pytest.

Usage:
    python test_api_manual.py
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

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
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{text.center(60)}{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{'='*60}{Colors.END}")

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

def test_api_endpoint(name: str, method: str, url: str, data: Dict = None, expected_status: int = 200) -> bool:
    """
    Test một API endpoint
    
    Args:
        name: Tên test
        method: HTTP method (GET/POST)
        url: URL endpoint
        data: Request data cho POST
        expected_status: Expected HTTP status code
        
    Returns:
        True nếu test pass
    """
    try:
        print(f"\n{Colors.PURPLE}🧪 Testing: {name}{Colors.END}")
        print(f"   Method: {method.upper()}")
        print(f"   URL: {url}")
        
        start_time = time.time()
        
        if method.upper() == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        elif method.upper() == "POST":
            if data:
                print(f"   Data: {json.dumps(data, indent=2, ensure_ascii=False)[:100]}...")
            response = requests.post(url, json=data, timeout=TIMEOUT)
        else:
            print_error(f"Unsupported method: {method}")
            return False
        
        elapsed = (time.time() - start_time) * 1000
        
        print(f"   Status: {response.status_code} (expected: {expected_status})")
        print(f"   Response time: {elapsed:.1f}ms")
        
        if response.status_code == expected_status:
            try:
                result = response.json()
                print(f"   Response preview: {json.dumps(result, indent=2, ensure_ascii=False)[:150]}...")
                print_success(f"{name} - PASSED ✨")
                return True
            except json.JSONDecodeError:
                print(f"   Response (non-JSON): {response.text[:100]}...")
                print_success(f"{name} - PASSED (non-JSON)")
                return True
        else:
            print(f"   Error response: {response.text[:200]}...")
            print_error(f"{name} - FAILED (Status: {response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error(f"{name} - CONNECTION ERROR")
        print_warning("API chưa chạy? Hãy chạy: ./run.sh")
        return False
    except requests.exceptions.Timeout:
        print_error(f"{name} - TIMEOUT (>{TIMEOUT}s)")
        return False
    except Exception as e:
        print_error(f"{name} - ERROR: {str(e)}")
        return False

def check_api_status():
    """Check if API is running"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def run_basic_tests():
    """Run basic endpoint tests"""
    print_header("BASIC ENDPOINT TESTS")
    
    tests = [
        ("Root Endpoint", "GET", f"{BASE_URL}/"),
        ("Health Check", "GET", f"{BASE_URL}/health"),
        ("Available Shapes", "GET", f"{BASE_URL}/api/v1/geometry/shapes"),
        ("Geometry Examples", "GET", f"{BASE_URL}/api/v1/geometry/examples"),
        ("Geometry Health", "GET", f"{BASE_URL}/api/v1/geometry/health"),
        ("Geometry Config Debug", "GET", f"{BASE_URL}/api/v1/geometry/config"),
    ]
    
    passed = 0
    for test_name, method, url in tests:
        if test_api_endpoint(test_name, method, url):
            passed += 1
    
    return passed, len(tests)

def run_calculation_tests():
    """Run geometry calculation tests"""
    print_header("GEOMETRY CALCULATION TESTS")
    
    # Test 1: Point distance 3D
    point_distance_data = {
        "operation": "Khoảng cách",
        "shape_a": "Điểm",
        "shape_b": "Điểm",
        "dimension_a": "3",
        "dimension_b": "3",
        "calculator_version": "fx799",
        "point_a": {"coordinates": "1,2,3"},
        "point_b": {"coordinates": "4,5,6"}
    }
    
    test1_pass = test_api_endpoint(
        "Point Distance 3D",
        "POST",
        f"{BASE_URL}/api/v1/geometry/calculate",
        point_distance_data
    )
    
    # Test 2: Circle area 2D
    circle_area_data = {
        "operation": "Diện tích",
        "shape_a": "Đường tròn",
        "dimension_a": "2",
        "calculator_version": "fx799",
        "circle_a": {
            "center": "0,0",
            "radius": "5"
        }
    }
    
    test2_pass = test_api_endpoint(
        "Circle Area 2D",
        "POST", 
        f"{BASE_URL}/api/v1/geometry/calculate",
        circle_area_data
    )
    
    return (1 if test1_pass else 0) + (1 if test2_pass else 0), 2

def run_validation_tests():
    """Run input validation tests"""
    print_header("VALIDATION TESTS")
    
    # Valid input test
    valid_data = {
        "request_data": {
            "operation": "Khoảng cách",
            "shape_a": "Điểm", 
            "shape_b": "Điểm",
            "dimension_a": "3",
            "dimension_b": "3",
            "calculator_version": "fx799",
            "point_a": {"coordinates": "1,2,3"},
            "point_b": {"coordinates": "4,5,6"}
        }
    }
    
    test1_pass = test_api_endpoint(
        "Valid Input Validation",
        "POST",
        f"{BASE_URL}/api/v1/geometry/validate",
        valid_data
    )
    
    return 1 if test1_pass else 0, 1

def run_error_tests():
    """Run error handling tests"""
    print_header("ERROR HANDLING TESTS")
    
    # Test invalid operation (should return 422)
    invalid_data = {
        "operation": "Invalid Operation",
        "shape_a": "Điểm",
        "dimension_a": "3",
        "calculator_version": "fx799"
    }
    
    test1_pass = test_api_endpoint(
        "Invalid Operation Test",
        "POST",
        f"{BASE_URL}/api/v1/geometry/calculate",
        invalid_data,
        expected_status=422  # Validation error expected
    )
    
    return 1 if test1_pass else 0, 1

def main():
    """Main test runner"""
    print(f"{Colors.BLUE}{Colors.BOLD}Geometry Calculator API Test Suite{Colors.END}")
    print(f"{Colors.BLUE}Version: 2.1.0{Colors.END}")
    print(f"{Colors.BLUE}Testing API at: {BASE_URL}{Colors.END}")
    print(f"{Colors.BLUE}Timestamp: {datetime.now().isoformat()}{Colors.END}")
    
    # Check if API is running
    print_info("Checking API status...")
    if not check_api_status():
        print_error("API is not running or not accessible!")
        print_warning("Please start the API first:")
        print("   1. cd api")
        print("   2. chmod +x run.sh")
        print("   3. ./run.sh")
        print("   4. Wait for server to start")
        print("   5. Run this test again")
        sys.exit(1)
    
    print_success("API is running!")
    
    # Run all test suites
    total_passed = 0
    total_tests = 0
    
    # Basic tests
    passed, tests = run_basic_tests()
    total_passed += passed
    total_tests += tests
    
    # Calculation tests 
    passed, tests = run_calculation_tests()
    total_passed += passed
    total_tests += tests
    
    # Validation tests
    passed, tests = run_validation_tests()
    total_passed += passed
    total_tests += tests
    
    # Error tests
    passed, tests = run_error_tests()
    total_passed += passed
    total_tests += tests
    
    # Final results
    print_header("FINAL TEST RESULTS")
    print(f"\n{Colors.BOLD}📊 TEST SUMMARY:{Colors.END}")
    print(f"   Total Tests: {total_tests}")
    print(f"   {Colors.GREEN}✅ Passed: {total_passed}{Colors.END}")
    print(f"   {Colors.RED}❌ Failed: {total_tests - total_passed}{Colors.END}")
    print(f"   {Colors.BLUE}📈 Success Rate: {(total_passed/total_tests)*100:.1f}%{Colors.END}")
    
    if total_passed == total_tests:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! 🎉{Colors.END}")
        print(f"{Colors.GREEN}Geometry Calculator API is working correctly!{Colors.END}")
        print(f"\n{Colors.BLUE}🔗 Quick Links:{Colors.END}")
        print(f"   📖 Docs: {BASE_URL}/docs")
        print(f"   🔧 API: {BASE_URL}/api/v1/geometry/")
        print(f"   ❤️ Health: {BASE_URL}/health")
        return True
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.END}")
        print(f"{Colors.YELLOW}Check API logs for details{Colors.END}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
