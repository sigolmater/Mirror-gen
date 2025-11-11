@echo off
REM Mirror-gen Frontend Start Script for Windows

echo Starting Mirror-gen Frontend...
echo ==================================

cd %~dp0

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing dependencies...
    call npm install
)

REM Start the development server
echo.
echo Frontend server starting on http://localhost:5173
echo Make sure the backend is running on http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ==================================
echo.

call npm run dev
