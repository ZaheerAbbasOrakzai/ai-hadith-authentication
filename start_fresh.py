#!/usr/bin/env python
"""Start Flask with absolutely fresh imports - no cache"""

import sys
import os
import shutil

print("=" * 70)
print("STARTING FLASK WITH FRESH IMPORTS")
print("=" * 70)
print()

# Step 1: Clear Python cache
print("[1/3] Clearing Python cache...")
cache_cleared = 0
for root, dirs, files in os.walk('.'):
    if '__pycache__' in dirs:
        cache_dir = os.path.join(root, '__pycache__')
        try:
            shutil.rmtree(cache_dir)
            cache_cleared += 1
        except:
            pass

for file in os.listdir('.'):
    if file.endswith('.pyc'):
        try:
            os.remove(file)
            cache_cleared += 1
        except:
            pass

print(f"   Cleared {cache_cleared} cache items")
print()

# Step 2: Force Python to not use bytecode
print("[2/3] Disabling bytecode generation...")
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
print("   Bytecode disabled")
print()

# Step 3: Import and run Flask
print("[3/3] Starting Flask...")
print()

# Import app fresh
import app

# Run the Flask app
if __name__ == '__main__':
    app.app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=False,  # Disable reloader to avoid cache issues
        threaded=True
    )
