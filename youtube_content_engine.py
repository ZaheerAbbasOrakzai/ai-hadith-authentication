"""
YouTube Content Engine
Curated Islamic content from verified scholars and channels
"""

from typing import Dict, List
from datetime import datetime

class YouTubeContentEngine:
    def __init__(self):
        # Approved scholars and channels (verified and active)
        self.approved_scholars = {
            'zakir_naik': {
                'name': 'Dr. Zakir Naik',
                'youtube_url': 'https://www.youtube.com/@DrZakirNaik',
                'description': 'Islamic scholar and public speaker',
                'category': 'Scholar',
                'verified': True
            },
            'mufti_tariq_masood': {
                'name': 'Mufti Tariq Masood',
                'youtube_url': 'https://www.youtube.com/@MuftiTariqMasoodSpeeches',
                'description': 'Pakistani Islamic scholar',
                'category': 'Scholar',
                'verified': True
            },
            'nouman_ali_khan': {
                'name': 'Nouman Ali Khan',
                'youtube_url': 'https://www.youtube.com/@bayyinah',
                'description': 'Quran teacher and Arabic instructor',
                'category': 'Scholar',
                'verified': True
            },
            'omar_suleiman': {
                'name': 'Omar Suleiman',
                'youtube_url': 'https://www.youtube.com/@yaqeeninstitute',
                'description': 'Islamic scholar and civil rights activist',
                'category': 'Scholar',
                'verified': True
            },
            'tariq_jameel': {
                'name': 'Maulana Tariq Jameel',
                'youtube_url': 'https://youtu.be/2E8X4-KVjlY',
                'description': 'Pakistani Islamic scholar',
                'category': 'Scholar',
                'verified': True
            },
            'assim_al_hakeem': {
                'name': 'Sheikh Assim Al-Hakeem',
                'youtube_url': 'https://www.youtube.com/@assimalhakeem',
                'description': 'Saudi Islamic scholar',
                'category': 'Scholar',
                'verified': True
            },
            'mufti_manzoor_mengal': {
                'name': 'Mufti Manzoor Mengal',
                'youtube_url': 'https://www.youtube.com/@YaqeenMedia',
                'description': 'Pakistani Islamic scholar',
                'category': 'Scholar',
                'verified': True
            }
        }
        
        self.approved_channels = {
            'islamic_teacher': {
                'name': 'Islamic Teacher',
                'youtube_url': 'https://www.youtube.com/@IslamicTeacherOfficial',
                'description': 'Islamic teachings and lectures',
                'category': 'Educational',
                'verified': True
            },
            'merciful_servant': {
                'name': 'MercifulServant',
                'youtube_url': 'https://www.youtube.com/@MercifulServant',
                'description': 'Islamic reminders and stories',
                'category': 'Reminders',
                'verified': True
            },
            'one_islam': {
                'name': 'One Islam Productions',
                'youtube_url': 'https://www.youtube.com/@OneIslamProductions',
                'description': 'High-quality Islamic content',
                'category': 'Educational',
                'verified': True
            },
            'free_quran_education': {
                'name': 'FreeQuranEducation',
                'youtube_url': 'https://www.youtube.com/@FreeQuranEducation',
                'description': 'Free Quran learning resources',
                'category': 'Educational',
                'verified': True
            },
            'the_deen_show': {
                'name': 'The Deen Show',
                'youtube_url': 'https://www.youtube.com/@TheDeenShow',
                'description': 'Islamic talk show and interviews',
                'category': 'Talk Show',
                'verified': True
            }
        }
        
        # EXCLUDED: Channels with aqida concerns
        self.excluded_channels = [
            'Engineer Muhammad Ali Mirza'
        ]
    
    def get_all_approved_content(self) -> List[Dict]:
        """Get all approved scholars and channels"""
        content = []
        
        # Add scholars
        for key, scholar in self.approved_scholars.items():
            content.append({
                'id': key,
                'type': 'scholar',
                **scholar
            })
        
        # Add channels
        for key, channel in self.approved_channels.items():
            content.append({
                'id': key,
                'type': 'channel',
                **channel
            })
        
        return content
    
    def get_scholars(self) -> List[Dict]:
        """Get approved scholars only"""
        return [
            {
                'id': key,
                **scholar
            }
            for key, scholar in self.approved_scholars.items()
        ]
    
    def get_channels(self) -> List[Dict]:
        """Get approved channels only"""
        return [
            {
                'id': key,
                **channel
            }
            for key, channel in self.approved_channels.items()
        ]
    
    def get_by_category(self, category: str) -> List[Dict]:
        """Get content by category"""
        content = self.get_all_approved_content()
        return [item for item in content if item.get('category') == category]
    
    def is_approved(self, channel_name: str) -> bool:
        """Check if a channel/scholar is approved"""
        # Check excluded list first
        if channel_name in self.excluded_channels:
            return False
        
        # Check approved lists
        for scholar in self.approved_scholars.values():
            if channel_name.lower() == scholar['name'].lower():
                return True
        
        for channel in self.approved_channels.values():
            if channel_name.lower() == channel['name'].lower():
                return True
        
        return False
    
    def get_content_guidelines(self) -> Dict:
        """Get content filtering guidelines"""
        return {
            'approved_scholars_count': len(self.approved_scholars),
            'approved_channels_count': len(self.approved_channels),
            'excluded_count': len(self.excluded_channels),
            'guidelines': [
                'Only verified scholars from approved list',
                'Strict aqida compliance required',
                'No controversial or deviant content',
                'Hanafi-Maturidi tradition preferred',
                'Educational and authentic sources only'
            ]
        }


# Global instance
youtube_engine = YouTubeContentEngine()


def get_approved_youtube_content() -> List[Dict]:
    """Convenience function to get all approved content"""
    return youtube_engine.get_all_approved_content()


def get_approved_scholars() -> List[Dict]:
    """Convenience function to get approved scholars"""
    return youtube_engine.get_scholars()


def get_approved_channels() -> List[Dict]:
    """Convenience function to get approved channels"""
    return youtube_engine.get_channels()
