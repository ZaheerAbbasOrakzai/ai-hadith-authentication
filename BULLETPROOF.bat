@echo off
setlocal EnableDelayedExpansion

echo ========================================
echo   AI Hadith Authenticator - BULLETPROOF
echo ========================================
echo.

REM Clear ALL problematic environment variables
for %%v in (WERKZEUG_SERVER_FD WERKZEUG_RUN_MAIN FLASK_RUN_FROM_CLI FLASK_ENV FLASK_DEBUG PYTHONPATH) do (
    set "%%v="
)

REM Set minimal safe environment
set "FLASK_ENV=development"
set "PYTHONUNBUFFERED=1"

echo 🧹 Environment cleaned
echo 🚀 Starting server...
echo.

REM Use Python to run the app with completely fresh environment
python -c "
import os
import sys

# Double-clean environment
for key in list(os.environ.keys()):
    if 'WERKZEUG' in key or 'FLASK_RUN' in key:
        del os.environ[key]

os.environ['FLASK_ENV'] = 'development'

from app import app
print('🕌 Server starting on http://127.0.0.1:5000')
app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False, threaded=False)
"

pause
