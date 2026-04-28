#!/usr/bin/env python3
"""
DEFINITIVE SOLUTION - Uses Waitress WSGI server (Production-grade, no Werkzeug issues)
"""

import os
import sys

# CRITICAL: Must clear environment BEFORE importing anything
for key in list(os.environ.keys()):
    if 'WERKZEUG' in key or 'FLASK' in key:
        try:
            del os.environ[key]
        except:
            pass

# Now safe to import
try:
    from waitress import serve
    HAS_WAITRESS = True
except ImportError:
    HAS_WAITRESS = False
    print("⚠️  Waitress not installed. Run: pip install waitress")
    sys.exit(1)

# Import Flask app
from app import app

if __name__ == '__main__':
    print("🕌 AI Hadith Authenticator - DEFINITIVE SERVER")
    print("=" * 50)
    print("✅ Using Waitress WSGI server (Production-grade)")
    print("✅ No Werkzeug development server issues")
    print("🌐 http://0.0.0.0:5000")
    print("-" * 50)
    
    # Use Waitress - completely bypasses all Werkzeug issues
    serve(
        app,
        host='0.0.0.0',
        port=5000,
        threads=4,
        channel_timeout=120,
        cleanup_interval=10,
        connection_limit=1000
    )
