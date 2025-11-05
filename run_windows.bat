@echo off
REM =============================================================================
REM Geometry Calculator API - Windows Startup Script
REM =============================================================================
REM Chỉ cần double-click hoặc chạy: run_windows.bat
REM 
REM Script này sẽ:
REM 1. Tự động tạo virtual environment
REM 2. Cài đặt dependencies
REM 3. Tạo thư mục cần thiết
REM 4. Start API server
REM =============================================================================

echo.
echo ================================================================
echo          GEOMETRY CALCULATOR API - WINDOWS LAUNCHER
echo ================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo [OK] Python is installed

REM Check if we're in the right directory
if not exist "app\main.py" (
    echo [ERROR] app\main.py not found!
    echo Make sure you're running this from the API project root
    pause
    exit /b 1
)

echo [OK] Project structure found

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [SETUP] Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo [SETUP] Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install/upgrade critical dependencies
echo [SETUP] Installing critical dependencies...
pip install fastapi uvicorn[standard] pydantic pydantic-settings psutil --quiet

REM Try to install from requirements.txt (optional)
if exist "requirements.txt" (
    echo [SETUP] Installing additional dependencies from requirements.txt...
    pip install -r requirements.txt --quiet
)

REM Create necessary directories
echo [SETUP] Creating directories...
if not exist "uploads" mkdir uploads
if not exist "outputs" mkdir outputs  
if not exist "logs" mkdir logs
echo [OK] Directories ready

REM Check if config files exist
if not exist "config\modes.json" (
    echo [WARNING] Some config files may be missing
    echo [INFO] API will still work with default configurations
)

echo.
echo ================================================================
echo                    STARTING API SERVER
echo ================================================================
echo.
echo API will be available at:
echo   ^> Main API: http://localhost:8000
echo   ^> Documentation: http://localhost:8000/docs
echo   ^> Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo ================================================================
echo.

REM Start the API server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

REM Cleanup message
echo.
echo ================================================================
echo Server stopped. Press any key to exit...
pause >nul
