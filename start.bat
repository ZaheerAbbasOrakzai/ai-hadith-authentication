@echo off
echo ========================================================
echo    AI Hadith Authenticator - Professional Version
echo ========================================================
echo.
echo Choose startup option:
echo.
echo 1. Clean Start (Recommended - Fixes Windows Issues)
echo 2. Stable Server
echo 3. MongoDB Helper
echo 4. Original App (with fixes)
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Starting Clean Flask Server...
    echo 🧹 This fixes Windows environment issues
    python start_clean.py
) else if "%choice%"=="2" (
    echo.
    echo 🚀 Starting Stable Server...
    python run_stable.py
) else if "%choice%"=="3" (
    echo.
    echo 🔧 Starting MongoDB Helper...
    python start_mongodb.py
) else if "%choice%"=="4" (
    echo.
    echo � Starting Original App (with fixes)...
    python app.py
) else if "%choice%"=="5" (
    echo.
    echo 👋 Exiting...
    exit /b 0
) else (
    echo.
    echo ❌ Invalid choice. Please try again.
    pause
    start.bat
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM Start the application
echo 🚀 Starting AI Hadith Authenticator...
echo.
echo Login Credentials:
echo   Email: admin@hadith.com
echo   Password: admin123
echo.
echo URLs:
echo   Main App: http://localhost:5000
echo   Hadith Analyzer: http://localhost:5000/hadith-analyzer
echo.
echo Press CTRL+C to stop the server
echo ========================================================
echo.

python app_professional.py

pause
