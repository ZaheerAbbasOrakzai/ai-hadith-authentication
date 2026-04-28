"""
Tafsir Ibn Kathir Engine
Provides access to authentic Tafsir Ibn Kathir from local database
"""

import json
import sqlite3
import os
from typing import Dict, List, Optional

class TafsirEngine:
    def __init__(self):
        self.json_path = 'ar-tafsir-ibn-kathir.json/ar-tafsir-ibn-kathir.json'
        self.db_path = 'ar-tafsir-ibn-kathir.db'
        self.tafsir_data = None
        self.db_conn = None
        self._load_data()
    
    def _load_data(self):
        """Load tafsir data from JSON or database"""
        # Try JSON first
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    self.tafsir_data = json.load(f)
                print(f"✅ Tafsir Ibn Kathir loaded from JSON: {len(self.tafsir_data)} entries")
            except Exception as e:
                print(f"⚠️ Failed to load JSON: {e}")
        
        # Try SQLite database
        if os.path.exists(self.db_path):
            try:
                self.db_conn = sqlite3.connect(self.db_path, check_same_thread=False)
                print(f"✅ Tafsir Ibn Kathir database connected")
            except Exception as e:
                print(f"⚠️ Failed to connect to database: {e}")
    
    def get_tafsir(self, surah: int, ayah: int) -> Optional[Dict]:
        """
        Get tafsir for specific ayah
        
        Args:
            surah: Surah number (1-114)
            ayah: Ayah number
            
        Returns:
            Dictionary with tafsir text or None
        """
        key = f"{surah}:{ayah}"
        
        # Try JSON data first
        if self.tafsir_data and key in self.tafsir_data:
            value = self.tafsir_data[key]
            # Handle both dict and string values
            if isinstance(value, dict):
                text = value.get('text', '')
            elif isinstance(value, str):
                text = value
            else:
                text = str(value)
            
            return {
                'surah': surah,
                'ayah': ayah,
                'text': text,
                'source': 'Tafsir Ibn Kathir (Local JSON)'
            }
        
        # Try database
        if self.db_conn:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute(
                    "SELECT text FROM tafsir WHERE surah = ? AND ayah = ?",
                    (surah, ayah)
                )
                result = cursor.fetchone()
                if result:
                    return {
                        'surah': surah,
                        'ayah': ayah,
                        'text': result[0],
                        'source': 'Tafsir Ibn Kathir (Local DB)'
                    }
            except Exception as e:
                print(f"Database query error: {e}")
        
        return None
    
    def get_surah_tafsir(self, surah: int) -> List[Dict]:
        """
        Get all tafsir entries for a surah
        
        Args:
            surah: Surah number (1-114)
            
        Returns:
            List of tafsir entries
        """
        results = []
        
        # Try JSON data
        if self.tafsir_data:
            for key, value in self.tafsir_data.items():
                if key.startswith(f"{surah}:"):
                    parts = key.split(':')
                    # Handle both dict and string values
                    if isinstance(value, dict):
                        text = value.get('text', '')
                    elif isinstance(value, str):
                        text = value
                    else:
                        text = str(value)
                    
                    results.append({
                        'surah': int(parts[0]),
                        'ayah': int(parts[1]),
                        'text': text,
                        'source': 'Tafsir Ibn Kathir (Local JSON)'
                    })
        
        # Try database if no JSON results
        if not results and self.db_conn:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute(
                    "SELECT ayah, text FROM tafsir WHERE surah = ? ORDER BY ayah",
                    (surah,)
                )
                for row in cursor.fetchall():
                    results.append({
                        'surah': surah,
                        'ayah': row[0],
                        'text': row[1],
                        'source': 'Tafsir Ibn Kathir (Local DB)'
                    })
            except Exception as e:
                print(f"Database query error: {e}")
        
        return results
    
    def search_tafsir(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search tafsir by text content
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of matching tafsir entries
        """
        results = []
        query_lower = query.lower()
        
        # Search JSON data
        if self.tafsir_data:
            for key, value in self.tafsir_data.items():
                # Handle both dict and string values
                if isinstance(value, dict):
                    text = value.get('text', '')
                elif isinstance(value, str):
                    text = value
                else:
                    continue
                
                if query_lower in text.lower():
                    parts = key.split(':')
                    results.append({
                        'surah': int(parts[0]),
                        'ayah': int(parts[1]),
                        'text': text,
                        'source': 'Tafsir Ibn Kathir (Local JSON)'
                    })
                    if len(results) >= limit:
                        break
        
        return results
    
    def get_stats(self) -> Dict:
        """Get statistics about tafsir data"""
        stats = {
            'total_entries': 0,
            'source': 'None',
            'available': False
        }
        
        if self.tafsir_data:
            stats['total_entries'] = len(self.tafsir_data)
            stats['source'] = 'JSON'
            stats['available'] = True
        elif self.db_conn:
            try:
                cursor = self.db_conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM tafsir")
                count = cursor.fetchone()[0]
                stats['total_entries'] = count
                stats['source'] = 'SQLite'
                stats['available'] = True
            except:
                pass
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.db_conn:
            self.db_conn.close()


# Global instance
tafsir_engine = TafsirEngine()


def get_tafsir_for_ayah(surah: int, ayah: int) -> Optional[Dict]:
    """Convenience function to get tafsir"""
    return tafsir_engine.get_tafsir(surah, ayah)


def get_tafsir_stats() -> Dict:
    """Get tafsir engine statistics"""
    return tafsir_engine.get_stats()
