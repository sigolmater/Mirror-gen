@echo off
REM Mirror-gen Backend Start Script for Windows

echo Starting Mirror-gen Backend Server...
echo ==================================

cd %~dp0

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q -r requirements.txt

REM Start the server
echo.
echo Backend server starting on http://localhost:8000
echo API Documentation available at http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ==================================
echo.

python main.py
