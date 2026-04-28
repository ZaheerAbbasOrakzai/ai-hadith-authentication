#!/usr/bin/env python3
"""
PythonAnywhere CLI Deployment Script for AI Hadith Authenticator
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and display output"""
    print(f"\n{'='*60}")
    print(f"STEP: {description}")
    print(f"{'='*60}")
    print(f"Running: {command}")
    print()

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False

def main():
    """Main deployment function"""
    print("="*60)
    print("PythonAnywhere CLI Deployment")
    print("AI Hadith Authenticator")
    print("="*60)

    # Configuration
    USERNAME = "zaheerabbaspattan"
    DOMAIN = f"{USERNAME}.pythonanywhere.com"
    REPO_URL = "https://github.com/ZaheerAbbasOrakzai/ai-hadith-authentication.git"
    PROJECT_DIR = f"/home/{USERNAME}/ai-hadith-authentication"
    VENV_DIR = f"{PROJECT_DIR}/venv"
    WSGI_FILE = f"{PROJECT_DIR}/ai_hadith_wsgi.py"

    print(f"\nConfiguration:")
    print(f"  Username: {USERNAME}")
    print(f"  Domain: {DOMAIN}")
    print(f"  Project Dir: {PROJECT_DIR}")
    print(f"  Repository: {REPO_URL}")

    # Step 1: Install pythonanywhere client
    print("\n" + "="*60)
    print("STEP 1: Install PythonAnywhere Client")
    print("="*60)
    print("Please run this command in your local terminal:")
    print(f"pip install pythonanywhere")
    print("\nThen get your API token from:")
    print(f"https://www.pythonanywhere.com/user/{USERNAME}/#api_token")
    print("\nAfter getting the token, run:")
    print(f"pa_configure {USERNAME} --api-token YOUR_TOKEN_HERE")
    print("\nPress Enter to continue after configuring...")
    input()

    # Step 2: Clone repository (This must be done on PythonAnywhere, not locally)
    print("\n" + "="*60)
    print("STEP 2: Clone Repository on PythonAnywhere")
    print("="*60)
    print("SSH into PythonAnywhere or use the Bash console to run:")
    print(f"cd ~")
    print(f"git clone {REPO_URL}")
    print(f"cd ai-hadith-authentication")
    print("\nPress Enter to continue after cloning...")
    input()

    # Step 3: Create virtualenv
    print("\n" + "="*60)
    print("STEP 3: Create Virtual Environment")
    print("="*60)
    print("Run on PythonAnywhere:")
    print(f"cd {PROJECT_DIR}")
    print(f"python3 -m venv venv")
    print(f"source venv/bin/activate")
    print(f"pip install -r requirements-pythonanywhere.txt")
    print("\nPress Enter to continue after installing dependencies...")
    input()

    # Step 4: Configure web app using CLI
    print("\n" + "="*60)
    print("STEP 4: Configure Web App")
    print("="*60)
    print("Run these commands locally (after pa_configure):")

    commands = [
        f"pa_webapp_create {DOMAIN} --python 3.9 --wsgi-file {WSGI_FILE}",
        f"pa_webapp_update {DOMAIN} --source-dir {PROJECT_DIR}",
        f"pa_webapp_update {DOMAIN} --working-dir {PROJECT_DIR}",
        f"pa_webapp_update {DOMAIN} --venv-path {VENV_DIR}",
    ]

    for cmd in commands:
        print(f"  {cmd}")

    print("\nPress Enter to continue after configuring...")
    input()

    # Step 5: Set environment variables
    print("\n" + "="*60)
    print("STEP 5: Set Environment Variables")
    print("="*60)
    print("Run these commands locally:")
    print(f"pa_webapp_update {DOMAIN} --envvar FLASK_ENV=production")
    print(f"pa_webapp_update {DOMAIN} --envvar SECRET_KEY=ai-hadith-auth-secret-key-2025-production")
    print(f"pa_webapp_update {DOMAIN} --envvar MONGODB_URI=mongodb://localhost:27017/hadith_db")
    print("\nPress Enter to continue...")
    input()

    # Step 6: Reload web app
    print("\n" + "="*60)
    print("STEP 6: Reload Web App")
    print("="*60)
    print(f"pa_webapp_reload {DOMAIN}")
    print("\nRun this command locally to reload your app.")
    print("\nYour app will be live at:")
    print(f"https://{DOMAIN}")

    print("\n" + "="*60)
    print("Deployment Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
