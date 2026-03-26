@echo off
chcp 65001 >nul
echo ========================================
echo Octopus - Web UI Startup Script
echo ========================================
echo.

REM Check Python environment
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found, please install Python 3.9+
    pause
    exit /b 1
)

REM Add project root to Python path
set PYTHONPATH=%cd%;%cd%\src

REM Start access service
echo [INFO] Starting access service...
echo [INFO] Web UI will be available at http://localhost:8000
echo.
echo Press Ctrl+C to stop the service
echo.

python src/services/access/app.py
