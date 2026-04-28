#!/usr/bin/env python
"""Final verification that everything is ready"""

print("=" * 60)
print("FINAL VERIFICATION - AI Hadith Authenticator")
print("=" * 60)
print()

try:
    # Test 1: Import app
    import app
    print("✅ app.py imports successfully")
    
    # Test 2: Check Quran surahs
    from complete_surahs import COMPLETE_SURAHS
    print(f"✅ Quran: {len(COMPLETE_SURAHS)} surahs loaded")
    
    # Test 3: Check Deobandi guidelines
    from deobandi_guidelines import get_primary_sources, get_core_texts
    sources = get_primary_sources()
    texts = get_core_texts()
    print(f"✅ Deobandi: {len(sources)} primary sources")
    print(f"✅ Core texts: {len(texts)} categories")
    
    # Test 4: Check routes
    from flask import url_for
    with app.app.test_request_context():
        collections_url = url_for('collections')
        quran_url = url_for('quran')
        guidelines_url = url_for('islamic_guidelines')
        print(f"✅ Collections route: {collections_url}")
        print(f"✅ Quran route: {quran_url}")
        print(f"✅ Guidelines route: {guidelines_url}")
    
    print()
    print("=" * 60)
    print("ALL SYSTEMS READY!")
    print("=" * 60)
    print()
    print("🚨 ACTION REQUIRED: Restart Flask server")
    print()
    print("   Stop Flask (Ctrl+C), then run:")
    print("   python app.py")
    print()
    print("🎉 Then everything will work perfectly!")
    print()
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
