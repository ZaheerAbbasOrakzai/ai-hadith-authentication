#!/usr/bin/env python3
"""
AI Hadith Authenticator - Setup Script
Initial setup and configuration for the application
"""

import os
import sys
import subprocess
import json
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment():
    """Create or activate virtual environment"""
    venv_path = Path("venv")
    
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✅ Virtual environment created")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create virtual environment: {e}")
            return False
    else:
        print("✅ Virtual environment already exists")
    
    return True


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Determine pip command based on OS
    pip_command = "pip" if os.name == "nt" else "pip3"
    
    # Install requirements
    try:
        subprocess.run([
            f"{os.path.join('venv', 'Scripts' if os.name == 'nt' else 'bin')}",
            pip_command,
            "install",
            "-r",
            "requirements.txt"
        ], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    return True


def create_directories():
    """Create necessary directories"""
    directories = [
        "uploads",
        "logs",
        "backups",
        "static/uploads",
        "static/images",
        "static/css",
        "static/js",
        "templates"
    ]
    
    for directory in directories:
        dir_path = Path(directory)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")


def create_env_file():
    """Create .env file from template"""
    env_path = Path(".env")
    env_example_path = Path(".env.example")
    
    if not env_path.exists() and env_example_path.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example_path, 'r') as example_file:
                with open(env_path, 'w') as env_file:
                    env_file.write(example_file.read())
            print("✅ .env file created")
            print("⚠️ Please update .env with your actual configuration values")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    elif env_path.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️ .env.example file not found")
    
    return True


def download_hadith_data():
    """Download hadith database (placeholder)"""
    print("📚 Hadith database setup...")
    
    # Create a simple hadith database for demo
    hadith_data = [
        {
            "id": 1,
            "english": "Actions are judged by intentions.",
            "arabic": "إنما الأعمال بالنيات",
            "grade": "Sahih",
            "source": "Sahih Bukhari 1",
            "narrator": "Umar ibn al-Khattab"
        },
        {
            "id": 2,
            "english": "The best among you are those who learn the Quran and teach it.",
            "arabic": "خيركم من تعلم القرآن وعلمه",
            "grade": "Hasan",
            "source": "Sahih Bukhari 6",
            "narrator": "Uthman ibn Affan"
        },
        {
            "id": 3,
            "english": "None of you truly believes until he loves for his brother what he loves for himself.",
            "arabic": "لا يؤمن أحدكم حتى يحب لأخيه ما يحب لنفسه",
            "grade": "Sahih",
            "source": "Sahih Bukhari 13",
            "narrator": "Anas ibn Malik"
        }
    ]
    
    try:
        with open('kutub_al_sittah_with_search_text.json', 'w', encoding='utf-8') as f:
            json.dump(hadith_data, f, indent=2, ensure_ascii=False)
        print("✅ Hadith database created")
    except Exception as e:
        print(f"❌ Failed to create hadith database: {e}")
        return False
    
    return True


def setup_git():
    """Initialize git repository"""
    if not Path(".git").exists():
        print("🔧 Initializing git repository...")
        try:
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)
            print("✅ Git repository initialized")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize git: {e}")
            return False
    else:
        print("✅ Git repository already exists")
    
    return True


def create_startup_script():
    """Create startup script for easy running"""
    script_content = """@echo off
echo 🕌 AI Hadith Authenticator Starting...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup.py first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\\Scripts\\activate.bat

REM Set environment
set FLASK_ENV=development

REM Run the application
python run.py --host 127.0.0.1 --port 5000

pause
"""
    
    try:
        with open("start.bat", "w") as f:
            f.write(script_content)
        print("✅ Startup script created: start.bat")
    except Exception as e:
        print(f"❌ Failed to create startup script: {e}")


def create_linux_startup_script():
    """Create startup script for Linux/Mac"""
    script_content = """#!/bin/bash
echo "🕌 AI Hadith Authenticator Starting..."
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup.py first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Set environment
export FLASK_ENV=development

# Run the application
python run.py --host 127.0.0.1 --port 5000
"""
    
    try:
        with open("start.sh", "w") as f:
            f.write(script_content)
        os.chmod("start.sh", 0o755)
        print("✅ Startup script created: start.sh")
    except Exception as e:
        print(f"❌ Failed to create startup script: {e}")


def run_tests():
    """Run application tests"""
    print("🧪 Running tests...")
    
    try:
        # Activate virtual environment and run tests
        venv_python = os.path.join("venv", "Scripts", "python") if os.name == "nt" else os.path.join("venv", "bin", "python")
        
        subprocess.run([
            venv_python,
            "-m",
            "pytest",
            "tests/",
            "-v"
        ], check=True)
        print("✅ Tests completed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed: {e}")
        return False
    
    return True


def main():
    """Main setup function"""
    print("""
🕌 AI Hadith Authenticator - Setup Script
========================================

This script will:
1. Check Python version
2. Create virtual environment
3. Install dependencies
4. Create necessary directories
5. Setup environment file
6. Download hadith data
7. Initialize git repository
8. Create startup scripts
    """)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create environment file
    create_env_file()
    
    # Download hadith data
    download_hadith_data()
    
    # Setup git
    setup_git()
    
    # Create startup scripts
    if os.name == "nt":
        create_startup_script()
    else:
        create_linux_startup_script()
    
    print("""
✅ Setup completed successfully!

🚀 Next Steps:
1. Update .env file with your configuration
2. Run 'start.bat' (Windows) or './start.sh' (Linux/Mac)
3. Open http://localhost:5000 in your browser

📚 Documentation:
- Read README.md for detailed instructions
- Check config.py for configuration options

🧪 Testing:
- Run tests with: python -m pytest tests/ -v

🔧 Development:
- Activate virtual environment: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)
- Run in debug mode: python run.py --debug

🕌 Happy coding with AI Hadith Authenticator!
    """)


if __name__ == "__main__":
    main()
