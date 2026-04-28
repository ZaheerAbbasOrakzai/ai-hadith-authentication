#!/usr/bin/env python3
"""
AI Hadith Authenticator - Fixed Runner
Ensures all routes are loaded before starting
"""

import os
import sys

# Disable bytecode to avoid cache issues
sys.dont_write_bytecode = True
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

print("=" * 70)
print("AI HADITH AUTHENTICATOR")
print("=" * 70)
print()

# Import the complete app (this loads ALL routes)
print("Loading application...")
from app import app

# Verify collections route is available
print("Verifying routes...")
with app.test_request_context():
    from flask import url_for
    try:
        collections_url = url_for('collections')
        print(f"✅ Collections route: {collections_url}")
    except Exception as e:
        print(f"❌ Collections route ERROR: {e}")
        print("\nAvailable routes:")
        for rule in app.url_map.iter_rules():
            if 'collection' in rule.endpoint.lower():
                print(f"  - {rule.endpoint} -> {rule.rule}")

print()
print("=" * 70)
print("Starting server...")
print("=" * 70)
print()
print("🌐 URL: http://127.0.0.1:5000/")
print("🛑 Press CTRL+C to stop")
print()

if __name__ == '__main__':
    try:
        app.run(
            host='127.0.0.1',
            port=5000,
            debug=True,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
