@echo off
echo ============================================
echo FORCE RESTART - AI Hadith Authenticator
echo ============================================
echo.
echo Step 1: Killing ALL Python processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
echo.
echo Step 2: Waiting for processes to close...
timeout /t 3 /nobreak >nul
echo.
echo Step 3: Clearing Python cache...
if exist __pycache__ rmdir /s /q __pycache__
if exist .pytest_cache rmdir /s /q .pytest_cache
for /d %%i in (*) do (
    if exist "%%i\__pycache__" rmdir /s /q "%%i\__pycache__"
)
echo.
echo Step 4: Starting fresh Flask server...
echo.
python app.py
