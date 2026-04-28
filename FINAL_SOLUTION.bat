@echo off
cls
echo ============================================
echo AI HADITH AUTHENTICATOR - FINAL SOLUTION
echo ============================================
echo.
echo Stopping all Python processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
timeout /t 2 /nobreak >nul
echo.
echo Starting Flask with ALL routes loaded...
echo.
python run_fixed.py
