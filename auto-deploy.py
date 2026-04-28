#!/usr/bin/env python3
"""
AUTOMATED PYTHONANYWHERE DEPLOYMENT
Run this script on PythonAnywhere Bash console
"""

import os
import subprocess
import sys

def run_cmd(cmd, description):
    """Run a command and print output"""
    print(f"\n{'='*70}")
    print(f"🔧 {description}")
    print(f"{'='*70}")
    print(f"Command: {cmd}\n")

    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("="*70)
    print("🚀 AI HADITH AUTHENTICATOR - AUTOMATED DEPLOYMENT")
    print("   PythonAnywhere")
    print("="*70)

    USERNAME = "zaheerabbaspattan"
    PROJECT_DIR = f"/home/{USERNAME}/ai-hadith-authentication"
    REPO_URL = "https://github.com/ZaheerAbbasOrakzai/ai-hadith-authentication.git"

    print(f"\n📋 Configuration:")
    print(f"   Username: {USERNAME}")
    print(f"   Project: {PROJECT_DIR}")
    print(f"   Repository: {REPO_URL}")

    # Step 1: Remove old installation
    if not run_cmd(f"rm -rf {PROJECT_DIR}", "Removing old installation"):
        return False

    # Step 2: Clone repository
    if not run_cmd(f"cd /home/{USERNAME} && git clone {REPO_URL}", "Cloning repository"):
        return False

    # Step 3: Create virtual environment
    if not run_cmd(f"cd {PROJECT_DIR} && python3 -m venv venv", "Creating virtual environment"):
        return False

    # Step 4: Install dependencies
    if not run_cmd(f"cd {PROJECT_DIR} && source venv/bin/activate && pip install --upgrade pip", "Upgrading pip"):
        return False

    if not run_cmd(f"cd {PROJECT_DIR} && source venv/bin/activate && pip install -r requirements-pythonanywhere.txt", "Installing dependencies"):
        return False

    # Step 5: Create directories
    if not run_cmd(f"cd {PROJECT_DIR} && mkdir -p uploads temp sessions", "Creating directories"):
        return False

    # Step 6: Create WSGI file
    wsgi_content = '''import sys
import os

project_home = "/home/zaheerabbaspattan/ai-hadith-authentication"
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from app import app as application
application.config['DEBUG'] = False
'''

    wsgi_file = f"{PROJECT_DIR}/ai_hadith_wsgi.py"
    with open(wsgi_file, 'w') as f:
        f.write(wsgi_content)
    print(f"\n✅ WSGI file created: {wsgi_file}")

    # Step 7: Print configuration for web app
    print("\n" + "="*70)
    print("✅ DEPLOYMENT COMPLETE!")
    print("="*70)
    print("\n📝 NOW CONFIGURE YOUR WEB APP:")
    print("\n1. Go to the 'Web' tab on PythonAnywhere")
    print("2. Update these settings:")
    print(f"   Source code: {PROJECT_DIR}")
    print(f"   Working directory: {PROJECT_DIR}")
    print(f"   WSGI file: {PROJECT_DIR}/ai_hadith_wsgi.py")
    print(f"   Virtualenv: {PROJECT_DIR}/venv")
    print("\n3. Add environment variables:")
    print("   FLASK_ENV=production")
    print("   SECRET_KEY=ai-hadith-auth-secret-key-2025-production")
    print("   MONGODB_URI=mongodb://localhost:27017/hadith_db")
    print("\n4. Click the green 'Reload' button")
    print("\n🌐 Your app will be live at:")
    print(f"   https://{USERNAME}.pythonanywhere.com")
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
