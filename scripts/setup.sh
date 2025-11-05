#!/bin/bash
# setup.sh - Script tự động setup project

echo "🚀 Setting up Geometry Calculator API project..."

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed."
    exit 1
fi

# Tạo cấu trúc thư mục
echo "📁 Creating project structure..."
mkdir -p uploads outputs config logs tests
mkdir -p nginx/ssl

# Tạo virtual environment
echo "🐍 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found, installing basic dependencies..."
    pip install fastapi uvicorn pandas openpyxl pydantic psutil
fi

# Tạo .env file
echo "⚙️ Creating .env file..."
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# API Settings
DEBUG=true
HOST=0.0.0.0
PORT=8000

# File Processing
MAX_FILE_SIZE=104857600
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
LARGE_FILE_THRESHOLD=52428800

# Security
ALLOWED_ORIGINS=["*"]
ALLOWED_FILE_TYPES=[".xlsx", ".xls"]

# Processing
CHUNK_SIZE=1000
MAX_BACKGROUND_TASKS=5
CLEANUP_INTERVAL_HOURS=24

# Geometry Service
DEFAULT_CALCULATOR_VERSION=fx799
SUPPORTED_VERSIONS=["fx799", "fx991", "fx570", "fx880", "fx801"]

# Database (optional)
DATABASE_URL=sqlite:///./geometry_api.db
EOF
fi

# Tạo run script
echo "🏃 Creating run script..."
cat > run.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Geometry Calculator API..."

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Create directories if not exist
mkdir -p uploads outputs logs

# Run the API
echo "API will be available at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo ""
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
EOF

chmod +x run.sh

# Tạo test script
echo "🧪 Creating test script..."
cat > test_api.py << 'EOF'
#!/usr/bin/env python3
"""
Test script cho Geometry Calculator API
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        print()

def test_root():
    """Test root endpoint"""
    print("🏠 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"App: {data.get('message', 'Unknown')}")
            print(f"Version: {data.get('version', 'Unknown')}")
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        print()

def test_geometry_shapes():
    """Test geometry shapes endpoint"""
    print("📜 Testing geometry shapes...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/geometry/shapes")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        print()

if __name__ == "__main__":
    print("🧪 Testing Geometry Calculator API...\n")
    
    tests = [test_health, test_root, test_geometry_shapes]
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📈 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Make sure API is running on localhost:8000")
        sys.exit(1)
EOF

chmod +x test_api.py

# Tạo .gitignore
echo "🙅 Creating .gitignore..."
if [ ! -f ".gitignore" ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
venv/
env/
.env
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project specific
uploads/
outputs/
logs/
*.db
*.sqlite
*.sqlite3

# OS
.DS_Store
Thumbs.db

# Docker
.dockerignore
EOF
fi

echo "✅ Project setup completed!"
echo ""
echo "📆 Next steps:"
echo "1. Copy your geometry services from original project to app/services/geometry/"
echo "2. Implement the actual models and routers (replace placeholders)"
echo "3. Start the API: ./run.sh"
echo "4. Test the API: python test_api.py"
echo "5. View documentation: http://localhost:8000/docs"
echo ""
echo "🐳 For Docker deployment:"
echo "1. docker-compose up --build"
echo "2. Access API at http://localhost:8000"
