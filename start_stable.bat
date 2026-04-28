@echo off
title AI Hadith Authenticator - Stable Server
color 0B
echo.
echo ========================================
echo   AI Hadith Authenticator
echo   Stable Server Runner
echo   (Fixes Windows Threading Issues)
echo ========================================
echo.

:: Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\activate
    echo Then: pip install -r requirements.txt
    echo.
    echo 💡 For Windows threading fix, also run: pip install waitress
    pause
    exit /b 1
)

:: Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

:: Check if waitress is installed (recommended for Windows)
python -c "import waitress" 2>nul
if errorlevel 1 (
    echo ⚠️ Waitress not found (recommended for Windows)
    echo Installing Waitress for better stability...
    pip install waitress
    echo.
)

:: Check if requirements are installed
echo 📦 Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ❌ Flask not installed! Installing requirements...
    pip install -r requirements.txt
)

:: Start the stable server
echo.
echo 🚀 Starting Stable Server...
echo 📍 Server will be available at: http://localhost:5000
echo 🛡️ Using Windows-compatible server configuration
echo 🛑 Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

:: Run the stable server
python run_stable.py

:: Handle server shutdown
echo.
echo 👋 Server stopped
echo 💡 If issues persist, try: python run_stable.py
pause
