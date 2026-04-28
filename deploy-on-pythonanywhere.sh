#!/bin/bash
# PythonAnywhere Deployment Script
# Run this script in PythonAnywhere Bash console

echo "=========================================="
echo "AI Hadith Authenticator Deployment"
echo "PythonAnywhere"
echo "=========================================="

USERNAME="zaheerabbaspattan"
PROJECT_DIR="/home/$USERNAME/ai-hadith-authentication"
REPO_URL="https://github.com/ZaheerAbbasOrakzai/ai-hadith-authentication.git"

echo "Configuration:"
echo "  Username: $USERNAME"
echo "  Project Dir: $PROJECT_DIR"
echo "  Repository: $REPO_URL"
echo ""

# Step 1: Remove existing directory if it exists
echo "Step 1: Cleaning up existing directory..."
if [ -d "$PROJECT_DIR" ]; then
    rm -rf "$PROJECT_DIR"
    echo "  Removed existing directory"
fi

# Step 2: Clone repository
echo "Step 2: Cloning repository..."
cd /home/$USERNAME
git clone $REPO_URL
echo "  Repository cloned"

# Step 3: Create virtual environment
echo "Step 3: Creating virtual environment..."
cd $PROJECT_DIR
python3 -m venv venv
echo "  Virtual environment created"

# Step 4: Activate virtual environment and install dependencies
echo "Step 4: Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-pythonanywhere.txt
echo "  Dependencies installed"

# Step 5: Create necessary directories
echo "Step 5: Creating necessary directories..."
mkdir -p uploads
mkdir -p temp
mkdir -p sessions
echo "  Directories created"

# Step 6: Display configuration for web app
echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo ""
echo "Now configure your web app on PythonAnywhere:"
echo ""
echo "1. Go to Web tab"
echo "2. Update these settings:"
echo "   - Source code: $PROJECT_DIR"
echo "   - Working directory: $PROJECT_DIR"
echo "   - WSGI configuration file: $PROJECT_DIR/ai_hadith_wsgi.py"
echo "   - Virtualenv: $PROJECT_DIR/venv"
echo ""
echo "3. Add environment variables:"
echo "   - FLASK_ENV=production"
echo "   - SECRET_KEY=ai-hadith-auth-secret-key-2025-production"
echo "   - MONGODB_URI=mongodb://localhost:27017/hadith_db"
echo ""
echo "4. Click Reload button"
echo ""
echo "Your app will be live at:"
echo "https://$USERNAME.pythonanywhere.com"
echo ""
echo "=========================================="
