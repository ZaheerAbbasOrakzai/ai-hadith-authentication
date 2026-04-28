@echo off
echo ============================================
echo AI Hadith Authenticator - FRESH START
echo ============================================
echo.
echo Killing any running Python processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM pythonw.exe 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting Flask with fresh imports...
echo.
python start_fresh.py
