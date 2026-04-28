@echo off
title AI Hadith Authenticator - Professional Server
color 0A
echo.
echo ========================================
echo   AI Hadith Authenticator
echo   Professional Server Startup
echo ========================================
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\activate
    echo Then: pip install -r requirements.txt
    pause
    exit /b 1
)

:: Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

:: Check if requirements are installed
echo 📦 Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ❌ Flask not installed! Installing requirements...
    pip install -r requirements.txt
)

:: Start the professional server
echo.
echo 🚀 Starting Professional Server...
echo 📍 Server will be available at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

:: Run the professional server
python run_professional.py

:: Handle server shutdown
echo.
echo 👋 Server stopped
pause
