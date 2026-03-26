@echo off
REM 八爪鱼（Octopus）启动脚本 - Windows

echo ========================================
echo 八爪鱼（Octopus）v0.1.0 MVP
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查虚拟环境
if not exist "venv" (
    echo 创建虚拟环境...
    python -m venv venv
    if errorlevel 1 (
        echo 错误：创建虚拟环境失败
        pause
        exit /b 1
    )
)

REM 激活虚拟环境
call venv\Scripts\activate.bat

REM 安装依赖
echo 安装依赖...
pip install -r requirements.txt -q
if errorlevel 1 (
    echo 错误：安装依赖失败
    pause
    exit /b 1
)

REM 运行程序
echo.
echo 启动八爪鱼...
echo.
python src/main.py

REM 退出虚拟环境
deactivate

pause
