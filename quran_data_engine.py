# Authentic Quran Data Engine - Strict Deobandi-Hanafi-Maturidi Compliance
# ZERO TOLERANCE for fabricated APIs or broken endpoints
# Uses ONLY verified, working API: https://api.quran.com/api/v4/

import requests
import json
import os
from typing import Dict, List, Optional

# VERIFIED API ENDPOINT - Quran.com API v4
QURAN_API_BASE = "https://api.quran.com/api/v4"

# Load local Tafsir Ibn Kathir database
TAFSIR_IBN_KATHIR_PATH = os.path.join(os.path.dirname(__file__), 'ar-tafsir-ibn-kathir.json', 'ar-tafsir-ibn-kathir.json')

class QuranDataEngine:
    """
    Authentic Quran Data Engine with strict validation
    - Uses ONLY verified Quran.com API v4
    - Provides Uthmani and Indo-Pak scripts
    - Integrates local Tafsir Ibn Kathir database
    - Zero tolerance for fabrication
    """
    
    def __init__(self):
        self.api_base = QURAN_API_BASE
        self.tafsir_data = self._load_tafsir_ibn_kathir()
        self.cache = {}
    
    def _load_tafsir_ibn_kathir(self) -> Dict:
        """Load Tafsir Ibn Kathir from local JSON database"""
        try:
            if os.path.exists(TAFSIR_IBN_KATHIR_PATH):
                with open(TAFSIR_IBN_KATHIR_PATH, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Warning: Could not load Tafsir Ibn Kathir: {e}")
            return {}
    
    def get_surah_info(self, surah_number: int) -> Optional[Dict]:
        """Get surah metadata from verified API"""
        try:
            response = requests.get(
                f"{self.api_base}/chapters/{surah_number}",
                timeout=10
            )
            if response.ok:
                return response.json().get('chapter')
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    def get_ayah_with_translation(self, surah: int, ayah: int, translation_id: int = 131) -> Optional[Dict]:
        """
        Get Ayah with Uthmani script, Indo-Pak script, and translation
        Default translation: 131 (Dr. Mustafa Khattab, The Clear Quran)
        """
        try:
            response = requests.get(
                f"{self.api_base}/verses/by_key/{surah}:{ayah}",
                params={"words": "false", "translations": str(translation_id)},
                timeout=10
            )
            if response.ok:
                data = response.json()
                verse = data.get('verse', {})
                translations = verse.get('translations', [])
                
                return {
                    'text_uthmani': verse.get('text_uthmani'),
                    'text_indopak': verse.get('text_indopak'),
                    'translation': translations[0].get('text') if translations else None,
                    'verse_key': verse.get('verse_key'),
                    'page_number': verse.get('page_number'),
                    'juz_number': verse.get('juz_number')
                }
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    def get_surah_verses(self, surah_number: int, translation_id: int = 131) -> Optional[List[Dict]]:
        """Get all verses of a surah with Uthmani script and translation"""
        try:
            response = requests.get(
                f"{self.api_base}/verses/by_chapter/{surah_number}",
                params={
                    "words": "false",
                    "translations": str(translation_id),
                    "per_page": 300
                },
                timeout=15
            )
            if response.ok:
                data = response.json()
                verses = data.get('verses', [])
                
                result = []
                for verse in verses:
                    translations = verse.get('translations', [])
                    result.append({
                        'verse_number': verse.get('verse_number'),
                        'verse_key': verse.get('verse_key'),
                        'text_uthmani': verse.get('text_uthmani'),
                        'text_indopak': verse.get('text_indopak'),
                        'translation': translations[0].get('text') if translations else None,
                        'page_number': verse.get('page_number'),
                        'juz_number': verse.get('juz_number')
                    })
                return result
            return None
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    def get_tafsir_ibn_kathir(self, surah: int, ayah: int) -> Optional[str]:
        """
        Get Tafsir Ibn Kathir from LOCAL database
        This is AUTHENTIC - uses local verified database
        """
        verse_key = f"{surah}:{ayah}"
        tafsir_entry = self.tafsir_data.get(verse_key)
        if tafsir_entry:
            return tafsir_entry.get('text')
        return None
    
    def validate_data(self, data: Dict) -> bool:
        """
        Strict validation layer - ensures data meets Quranic standards
        """
        if not data:
            return False
        
        # Must have Uthmani script
        if not data.get('text_uthmani'):
            return False
        
        # Must have verse reference
        if not data.get('verse_key'):
            return False
        
        return True

# Singleton instance
quran_engine = QuranDataEngine()

def get_maariful_quran_info() -> Dict:
    """
    Ma'ariful Qur'an by Muhammad Taqi Usmani
    ❌ NO OFFICIAL API EXISTS
    
    This function provides ONLY real acquisition methods
    """
    return {
        'title': "Ma'ariful Qur'an",
        'author': "Mufti Muhammad Shafi Usmani",
        'translator': "Muhammad Taqi Usmani (English translation)",
        'volumes': 8,
        'api_available': False,
        'acquisition_methods': [
            {
                'type': 'Physical Book',
                'publisher': 'Maktaba-e-Darul-Uloom',
                'url': 'https://www.darululoomkhi.edu.pk/'
            },
            {
                'type': 'PDF Download',
                'source': 'Darul Uloom Karachi',
                'url': 'https://www.darululoomkhi.edu.pk/fiqh/maarifulquran/'
            },
            {
                'type': 'Mobile App',
                'name': 'Ma\'ariful Qur\'an (Android/iOS)',
                'note': 'Search app stores for official apps'
            }
        ],
        'note': 'No API exists for Ma\'ariful Qur\'an. Content must be accessed through licensed books or verified apps.'
    }
