#!/usr/bin/env python3
"""
Geometry Calculator API - Simple Local Runner

Chỉ cần chạy: python main.py
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_status(message, color=Colors.BLUE):
    print(f"{color}{message}{Colors.END}")

def check_and_install_package(package_name, import_name=None):
    if import_name is None:
        import_name = package_name.replace('-', '_')
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        print_status(f"📦 Installing {package_name}...", Colors.YELLOW)
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package_name])
            return True
        except subprocess.CalledProcessError:
            print_status(f"❌ Failed to install {package_name}", Colors.RED)
            return False

def setup_environment():
    print_status("🔧 Setting up Geometry Calculator API environment...", Colors.BOLD)
    if sys.version_info < (3, 8):
        print_status("❌ Python 3.8+ required", Colors.RED)
        return False
    print_status(f"✅ Python {sys.version.split()[0]} OK")
    for directory in ['uploads', 'outputs', 'logs', 'config']:
        os.makedirs(directory, exist_ok=True)
    print_status("✅ Directories created")
    critical_packages = [
        ('fastapi', 'fastapi'),
        ('uvicorn[standard]', 'uvicorn'),
        ('pydantic', 'pydantic'),
        ('pydantic-settings', 'pydantic_settings'),
        ('psutil', 'psutil'),
        ('requests', 'requests')
    ]
    print_status("📦 Checking dependencies...")
    all_installed = True
    for package, import_name in critical_packages:
        if not check_and_install_package(package, import_name):
            all_installed = False
    if not all_installed:
        print_status("❌ Some packages failed to install", Colors.RED)
        print_status("💡 Try: pip install -r requirements.txt", Colors.YELLOW)
        return False
    print_status("✅ All critical dependencies ready")
    return True

def start_api_server():
    print_status("🚀 Starting Geometry Calculator API Server...", Colors.BOLD)
    print_status("🌐 API will be available at:", Colors.GREEN)
    print_status("   📍 Main API: http://localhost:8000", Colors.BLUE)
    print_status("   📚 Documentation: http://localhost:8000/docs", Colors.BLUE)
    print_status("   📖 ReDoc: http://localhost:8000/redoc", Colors.BLUE)
    print_status("   ❤️  Health Check: http://localhost:8000/health", Colors.BLUE)
    print_status("   🔧 Geometry API: http://localhost:8000/api/v1/geometry/", Colors.BLUE)
    print_status("⚠️  Press Ctrl+C to stop the server", Colors.YELLOW)
    try:
        import uvicorn
        # Use import string so reload works without warning
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except ImportError as e:
        print_status(f"❌ Import error: {e}", Colors.RED)
        print_status("💡 Try: pip install fastapi uvicorn", Colors.YELLOW)
        return False
    except KeyboardInterrupt:
        print_status("\n🛑 Server stopped by user", Colors.YELLOW)
        return True
    except Exception as e:
        print_status(f"❌ Server error: {e}", Colors.RED)
        return False

def main():
    print_status("🎯 Geometry Calculator API - Simple Runner", Colors.BOLD + Colors.GREEN)
    print_status("Version: 2.1.0")
    print_status(f"Directory: {os.getcwd()}")
    print_status(f"Python: {sys.version.split()[0]}")
    if not os.path.exists('app') or not os.path.exists('app/main.py'):
        print_status("❌ Not in API project directory!", Colors.RED)
        print_status("💡 Make sure you're in the 'api' folder with app/ directory", Colors.YELLOW)
        return False
    if not setup_environment():
        return False
    print_status("🎉 Setup completed! Starting server...", Colors.GREEN)
    return start_api_server()

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print_status("\n👋 Goodbye!", Colors.BLUE)
        sys.exit(0)
    except Exception as e:
        print_status(f"❌ Unexpected error: {e}", Colors.RED)
        sys.exit(1)
