@echo off
echo ========================================
echo AI Hadith Authenticator - Server Restart
echo ========================================
echo.
echo Stopping any running Flask processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting Flask server...
echo.
python app.py
