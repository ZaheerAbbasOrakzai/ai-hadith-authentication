#!/bin/bash

# AI Hadith Authenticator - Linux/Mac Startup Script

echo "========================================"
echo "    AI Hadith Authenticator"
echo "========================================"
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run setup.py first to create the environment."
    echo
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found!"
    echo "Please create .env file from .env.example template."
    echo
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment!"
    exit 1
fi

# Set environment variables
export FLASK_ENV=development
export FLASK_APP=run.py

# Check if required files exist
if [ ! -f "app.py" ]; then
    echo "[ERROR] app.py not found!"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "[ERROR] requirements.txt not found!"
    exit 1
fi

# Check if dependencies are installed
echo "[INFO] Checking dependencies..."
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] Flask not installed. Installing dependencies..."
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies!"
        exit 1
    fi
fi

# Create necessary directories
mkdir -p logs uploads backups

# Start the application
echo
echo "========================================"
echo "    Starting AI Hadith Authenticator"
echo "========================================"
echo "[INFO] Application will be available at: http://localhost:5000"
echo "[INFO] Press CTRL+C to stop the server"
echo "========================================"
echo

python run.py --host 127.0.0.1 --port 5000 --debug

# If application exits
echo
echo "[INFO] Application stopped."
