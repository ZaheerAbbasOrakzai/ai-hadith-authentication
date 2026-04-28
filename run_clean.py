#!/usr/bin/env python
"""
Clean Flask startup - bypasses all caching issues
"""

import sys
import os

# Disable bytecode generation
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

# Clear any cached modules
for module in list(sys.modules.keys()):
    if module.startswith('app') or module.startswith('complete_') or module.startswith('deobandi_'):
        del sys.modules[module]

print("=" * 70)
print("AI HADITH AUTHENTICATOR - CLEAN START")
print("=" * 70)
print()
print("Importing app with NO cache...")

# Import app fresh
from app import app

print()
print("Verifying routes...")
with app.test_request_context():
    from flask import url_for
    try:
        url = url_for('collections')
        print(f"✅ Collections route: {url}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("\nDEBUG: Available routes:")
        for rule in app.url_map.iter_rules():
            print(f"  {rule.endpoint} -> {rule.rule}")
        sys.exit(1)

print()
print("=" * 70)
print("Starting Flask server...")
print("=" * 70)
print()
print("Visit: http://127.0.0.1:5000/")
print()

# Run Flask
if __name__ == '__main__':
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True,
        use_reloader=False
    )
