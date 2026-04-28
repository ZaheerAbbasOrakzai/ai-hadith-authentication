#!/usr/bin/env python
"""Verify the collections route is available RIGHT NOW"""

import sys
import os

# Force fresh import
if 'app' in sys.modules:
    del sys.modules['app']
if 'complete_surahs' in sys.modules:
    del sys.modules['complete_surahs']
if 'deobandi_guidelines' in sys.modules:
    del sys.modules['deobandi_guidelines']

print("Importing app.py fresh...")
import app

print("\nChecking routes...")
with app.app.test_request_context():
    from flask import url_for
    
    try:
        collections_url = url_for('collections')
        print(f"✅ SUCCESS: url_for('collections') = {collections_url}")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        print("\nAvailable routes:")
        for rule in app.app.url_map.iter_rules():
            if 'collection' in rule.endpoint.lower():
                print(f"  - {rule.endpoint} -> {rule.rule}")
        sys.exit(1)

print("\n✅ The route IS available!")
print("Now start Flask with: python app.py")
