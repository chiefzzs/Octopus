@echo off
REM Octopus Services Startup Script - Windows

echo ========================================
echo Octopus v0.4.0 RC
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found, please install Python 3.8+
    pause
    exit /b 1
)

REM Check virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Starting Octopus Services...
echo.

REM Start Access Service
echo Starting Access Service on port 8000...
start "Octopus - Access Service" cmd /k "venv\Scripts\activate.bat && python src/services/access/app.py"
timeout /t 2 /nobreak >nul

REM Start Control Service
echo Starting Control Service on port 8001...
start "Octopus - Control Service" cmd /k "venv\Scripts\activate.bat && python src/services/control/app.py"
timeout /t 2 /nobreak >nul

REM Start Realtime Service
echo Starting Realtime Service on port 8002...
start "Octopus - Realtime Service" cmd /k "venv\Scripts\activate.bat && python src/services/realtime/app.py"
timeout /t 2 /nobreak >nul

REM Start Execution Service
echo Starting Execution Service on port 8003...
start "Octopus - Execution Service" cmd /k "venv\Scripts\activate.bat && python src/services/execution/app.py"
timeout /t 2 /nobreak >nul

REM Start Capability Service
echo Starting Capability Service on port 8004...
start "Octopus - Capability Service" cmd /k "venv\Scripts\activate.bat && python src/services/capability/app.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo All services started successfully!
echo ========================================
echo.
echo Services:
echo   - Access Service:    http://localhost:8000
echo   - Control Service:   http://localhost:8001
echo   - Realtime Service:  http://localhost:8002
echo   - Execution Service: http://localhost:8003
echo   - Capability Service: http://localhost:8004
echo.
echo Press any key to exit...
pause >nul
