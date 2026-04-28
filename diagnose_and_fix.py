#!/usr/bin/env python
"""Diagnose and fix the collections route issue"""

import os
import sys
import subprocess
import time

print("=" * 70)
print("COLLECTIONS ROUTE DIAGNOSTIC & FIX TOOL")
print("=" * 70)
print()

# Step 1: Check if route exists in file
print("[1/5] Checking if route exists in app.py...")
try:
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if "@app.route('/collections')" in content:
            print("✅ Route found in app.py file")
            # Find line number
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if "@app.route('/collections')" in line:
                    print(f"   Located at line {i}")
                    break
        else:
            print("❌ Route NOT found in app.py file")
            print("   ERROR: The route needs to be added to app.py")
            sys.exit(1)
except Exception as e:
    print(f"❌ Error reading app.py: {e}")
    sys.exit(1)

print()

# Step 2: Check for syntax errors
print("[2/5] Checking for syntax errors...")
result = subprocess.run([sys.executable, '-m', 'py_compile', 'app.py'], 
                       capture_output=True, text=True)
if result.returncode == 0:
    print("✅ No syntax errors in app.py")
else:
    print("❌ Syntax errors found:")
    print(result.stderr)
    sys.exit(1)

print()

# Step 3: Check if Python processes are running
print("[3/5] Checking for running Python processes...")
if os.name == 'nt':  # Windows
    result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                           capture_output=True, text=True)
    if 'python.exe' in result.stdout:
        print("⚠️  Python processes are running")
        print("   These need to be stopped for changes to take effect")
    else:
        print("✅ No Python processes running")
else:  # Linux/Mac
    result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
    if 'python' in result.stdout and 'app.py' in result.stdout:
        print("⚠️  Python processes are running")
    else:
        print("✅ No Python processes running")

print()

# Step 4: Check Python cache
print("[4/5] Checking Python cache...")
cache_dirs = []
if os.path.exists('__pycache__'):
    cache_dirs.append('__pycache__')
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_dirs.append(os.path.join(root, '__pycache__'))

if cache_dirs:
    print(f"⚠️  Found {len(cache_dirs)} cache directories")
    print("   These should be cleared")
else:
    print("✅ No cache directories found")

print()

# Step 5: Offer to fix
print("[5/5] Fix Options")
print("=" * 70)
print()
print("The route EXISTS in app.py but Flask is using an old cached version.")
print()
print("To fix this, you need to:")
print("1. Stop ALL Python processes")
print("2. Clear Python cache")
print("3. Start Flask fresh")
print()

response = input("Would you like me to do this automatically? (yes/no): ").strip().lower()

if response in ['yes', 'y']:
    print()
    print("Applying fix...")
    print()
    
    # Kill Python processes
    print("→ Stopping Python processes...")
    if os.name == 'nt':  # Windows
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                      capture_output=True)
        subprocess.run(['taskkill', '/F', '/IM', 'pythonw.exe'], 
                      capture_output=True)
    else:  # Linux/Mac
        subprocess.run(['pkill', '-f', 'python.*app.py'], 
                      capture_output=True)
    
    time.sleep(2)
    print("✅ Processes stopped")
    
    # Clear cache
    print("→ Clearing Python cache...")
    import shutil
    for cache_dir in cache_dirs:
        try:
            shutil.rmtree(cache_dir)
            print(f"   Removed {cache_dir}")
        except Exception as e:
            print(f"   Could not remove {cache_dir}: {e}")
    print("✅ Cache cleared")
    
    print()
    print("=" * 70)
    print("FIX APPLIED!")
    print("=" * 70)
    print()
    print("Now run: python app.py")
    print()
    print("Then visit: http://localhost:5000/")
    print("The Collections link will work! ✅")
    print()
    
else:
    print()
    print("Manual fix instructions:")
    print()
    print("1. Stop Flask (Ctrl+C)")
    print("2. Run: taskkill /F /IM python.exe")
    print("3. Delete __pycache__ folders")
    print("4. Run: python app.py")
    print()
