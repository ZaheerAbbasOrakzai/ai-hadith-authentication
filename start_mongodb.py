#!/usr/bin/env python3
"""
MongoDB Service Starter for AI Hadith Authenticator
This script helps ensure MongoDB is running before starting the Flask app
"""

import subprocess
import sys
import time
import requests
from pathlib import Path

def check_mongodb_running():
    """Check if MongoDB is running on localhost:27017"""
    try:
        response = requests.get('http://localhost:27017', timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        return False
    except Exception:
        return False

def start_mongodb_service():
    """Attempt to start MongoDB service"""
    print("🔄 Attempting to start MongoDB service...")
    
    # Try different MongoDB service commands
    commands = [
        ['net', 'start', 'MongoDB'],
        ['sc', 'start', 'MongoDB'],
        ['mongod', '--dbpath', 'C:/data/db'],
        ['mongod']
    ]
    
    for cmd in commands:
        try:
            print(f"🔧 Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ MongoDB service started successfully")
                return True
            else:
                print(f"⚠️ Command failed: {result.stderr}")
        except subprocess.TimeoutExpired:
            print("⏰ Command timed out, trying next...")
        except FileNotFoundError:
            print(f"❌ Command not found: {cmd[0]}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False

def main():
    """Main function to check and start MongoDB"""
    print("🔍 Checking MongoDB service status...")
    
    if check_mongodb_running():
        print("✅ MongoDB is already running")
        return True
    
    print("❌ MongoDB is not running")
    
    if start_mongodb_service():
        # Give MongoDB time to start
        print("⏳ Waiting for MongoDB to initialize...")
        time.sleep(5)
        
        if check_mongodb_running():
            print("✅ MongoDB is now running")
            return True
        else:
            print("❌ MongoDB failed to start properly")
            return False
    else:
        print("❌ Failed to start MongoDB service")
        print("\n💡 Manual steps:")
        print("1. Install MongoDB from: https://www.mongodb.com/try/download/community")
        print("2. Run MongoDB as a service or start manually with: mongod")
        print("3. Or continue with SQLite fallback (recommended for development)")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
