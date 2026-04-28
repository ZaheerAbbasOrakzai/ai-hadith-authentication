@echo off
cls
echo ============================================
echo AI HADITH AUTHENTICATOR - CLEAN START
echo ============================================
echo.
echo Step 1: Stopping all Python processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
echo Done.
echo.
echo Step 2: Waiting for processes to close...
timeout /t 3 /nobreak >nul
echo Done.
echo.
echo Step 3: Starting Flask with clean imports...
echo.
python run_clean.py
pause
