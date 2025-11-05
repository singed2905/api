#!/bin/bash
"""
Geometry Calculator API - Run Script

Script dễ dàng để start API server với tất cả dependencies.

Features:
- Tự động activate virtual environment
- Tạo directories cần thiết
- Check dependencies
- Start FastAPI server với uvicorn
- Display useful URLs
"""

echo "🚀 Starting Geometry Calculator API..."
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "requirements.txt" ] || [ ! -d "app" ]; then
    echo -e "${RED}❌ Error: Please run this script from the project root directory${NC}"
    echo "Expected files: requirements.txt, app/ directory"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3 is required but not installed.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 found${NC}"

# Check virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️ Virtual environment not found. Run setup.sh first.${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    # Install dependencies
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo -e "${GREEN}✅ Virtual environment found${NC}"
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Check if FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo -e "${YELLOW}⚠️ FastAPI not found. Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

echo -e "${GREEN}✅ Dependencies ready${NC}"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p uploads outputs logs config
echo -e "${GREEN}✅ Directories ready${NC}"

# Check config files
echo "⚙️ Checking configuration..."
if [ -f "config/modes.json" ]; then
    echo -e "${GREEN}✅ Config files found${NC}"
else
    echo -e "${YELLOW}⚠️ Some config files may be missing${NC}"
fi

# Copy environment template if .env doesn't exist
if [ ! -f ".env" ] && [ -f ".env.template" ]; then
    echo "📋 Creating .env from template..."
    cp .env.template .env
    echo -e "${GREEN}✅ .env file created${NC}"
fi

echo "================================================"
echo -e "${BLUE}🌍 Starting Geometry Calculator API...${NC}"
echo ""
echo -e "${GREEN}API will be available at:${NC}"
echo "  🔗 Main API: http://localhost:8000"
echo "  📚 Documentation: http://localhost:8000/docs"
echo "  📖 ReDoc: http://localhost:8000/redoc"
echo "  ❤️ Health Check: http://localhost:8000/health"
echo "  🔧 Geometry API: http://localhost:8000/api/v1/geometry/"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo "================================================"
echo ""

# Start the API server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level info

# Cleanup message
echo ""
echo -e "${BLUE}👋 Server stopped. Goodbye!${NC}"
