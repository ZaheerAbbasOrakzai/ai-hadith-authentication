"""
Prayer Times Engine with Location Detection
Real-time prayer times based on user location with Hijri calendar
"""

import requests
from datetime import datetime, timedelta
import json
from typing import Dict, Optional, Tuple

class PrayerTimesEngine:
    def __init__(self):
        self.aladhan_api_base = "http://api.aladhan.com/v1"
        self.ipapi_base = "http://ip-api.com/json"
        self.cache = {}
        self.cache_duration = timedelta(hours=1)
        
    def get_user_location(self) -> Dict:
        """Get user location from IP address"""
        try:
            response = requests.get(self.ipapi_base, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        'city': data.get('city', 'Unknown'),
                        'country': data.get('country', 'Unknown'),
                        'latitude': data.get('lat'),
                        'longitude': data.get('lon'),
                        'timezone': data.get('timezone', 'UTC'),
                        'region': data.get('regionName', '')
                    }
        except Exception as e:
            print(f"Location detection error: {e}")
        
        # Fallback to default location (Peshawar, Pakistan)
        return {
            'city': 'Peshawar',
            'country': 'Pakistan',
            'latitude': 34.0151,
            'longitude': 71.5249,
            'timezone': 'Asia/Karachi',
            'region': 'Khyber Pakhtunkhwa'
        }
    
    def get_prayer_times_by_coordinates(self, latitude: float, longitude: float, method: int = 2) -> Optional[Dict]:
        """Get prayer times using coordinates with enhanced data"""
        cache_key = f"coords_{latitude}_{longitude}_{method}_{datetime.now().date()}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data
        
        try:
            # Get current date
            today = datetime.now()
            
            # API call for prayer times
            url = f"{self.aladhan_api_base}/timings/{today.strftime('%d-%m-%Y')}"
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'method': method,  # 2 = ISNA, 4 = Umm al-Qura, 3 = MWL
                'tune': '0,0,0,0,0,0,0,0,0'  # No adjustments
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == 200:
                    timings = data['data']['timings']
                    date_info = data['data']['date']
                    
                    # Get current prayer
                    current_prayer = self._get_current_prayer(timings)
                    
                    # Get next prayer
                    next_prayer = self._get_next_prayer(timings, current_prayer)
                    
                    # Enhanced prayer times data
                    result = {
                        'timings': {
                            'Fajr': timings['Fajr'],
                            'Sunrise': timings['Sunrise'],
                            'Dhuhr': timings['Dhuhr'],
                            'Asr': timings['Asr'],
                            'Maghrib': timings['Maghrib'],
                            'Isha': timings['Isha'],
                            'Midnight': timings['Midnight']
                        },
                        'current_prayer': current_prayer,
                        'next_prayer': next_prayer,
                        'date': {
                            'readable': date_info['readable'],
                            'timestamp': date_info['timestamp'],
                            'hijri': {
                                'date': date_info['hijri']['date'],
                                'format': f"{date_info['hijri']['day']} {date_info['hijri']['month']['en']} {date_info['hijri']['year']}",
                                'month': date_info['hijri']['month']['en'],
                                'year': date_info['hijri']['year'],
                                'weekday': date_info['hijri']['weekday']['en']
                            },
                            'gregorian': {
                                'date': date_info['gregorian']['date'],
                                'format': f"{date_info['gregorian']['day']} {date_info['gregorian']['month']['en']} {date_info['gregorian']['year']}",
                                'month': date_info['gregorian']['month']['en'],
                                'year': date_info['gregorian']['year'],
                                'weekday': date_info['gregorian']['weekday']['en']
                            }
                        },
                        'method': self._get_method_name(method),
                        'coordinates': {
                            'latitude': latitude,
                            'longitude': longitude
                        },
                        'qibla_direction': self._calculate_qibla_direction(latitude, longitude)
                    }
                    
                    # Cache the result
                    self.cache[cache_key] = (result, datetime.now())
                    
                    return result
        except Exception as e:
            print(f"Prayer times API error: {e}")
        
        return None
    
    def get_prayer_times(
        self, 
        city: str = "Peshawar", 
        country: str = "Pakistan", 
        method: int = 2  # Changed to ISNA method
    ) -> Optional[Dict]:
        """
        Get prayer times for a specific city with enhanced data
        """
        cache_key = f"{city}_{country}_{method}_{datetime.now().date()}"
        
        # Check cache
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data
        
        try:
            today = datetime.now()
            url = f"{self.aladhan_api_base}/timingsByCity/{today.strftime('%d-%m-%Y')}"
            params = {
                'city': city,
                'country': country,
                'method': method
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('code') == 200:
                    timings = data['data']['timings']
                    date_info = data['data']['date']
                    meta = data['data']['meta']
                    
                    current_prayer = self._get_current_prayer(timings)
                    next_prayer = self._get_next_prayer(timings, current_prayer)
                    
                    result = {
                        'timings': {
                            'Fajr': timings['Fajr'],
                            'Sunrise': timings['Sunrise'],
                            'Dhuhr': timings['Dhuhr'],
                            'Asr': timings['Asr'],
                            'Maghrib': timings['Maghrib'],
                            'Isha': timings['Isha'],
                            'Midnight': timings['Midnight']
                        },
                        'current_prayer': current_prayer,
                        'next_prayer': next_prayer,
                        'location': {
                            'city': city,
                            'country': country,
                            'latitude': meta.get('latitude'),
                            'longitude': meta.get('longitude'),
                            'timezone': meta.get('timezone')
                        },
                        'date': {
                            'readable': date_info['readable'],
                            'timestamp': date_info['timestamp'],
                            'hijri': {
                                'date': date_info['hijri']['date'],
                                'format': f"{date_info['hijri']['day']} {date_info['hijri']['month']['en']} {date_info['hijri']['year']}",
                                'month': date_info['hijri']['month']['en'],
                                'year': date_info['hijri']['year'],
                                'weekday': date_info['hijri']['weekday']['en']
                            },
                            'gregorian': {
                                'date': date_info['gregorian']['date'],
                                'format': f"{date_info['gregorian']['day']} {date_info['gregorian']['month']['en']} {date_info['gregorian']['year']}",
                                'month': date_info['gregorian']['month']['en'],
                                'year': date_info['gregorian']['year'],
                                'weekday': date_info['gregorian']['weekday']['en']
                            }
                        },
                        'method': self._get_method_name(method),
                        'qibla_direction': self._calculate_qibla_direction(
                            meta.get('latitude', 0), 
                            meta.get('longitude', 0)
                        ),
                        'source': 'Aladhan.com API (Verified)'
                    }
                    
                    # Cache the result
                    self.cache[cache_key] = (result, datetime.now())
                    
                    return result
        except Exception as e:
            print(f"City prayer times error: {e}")
        
        return None
    
    def get_auto_location_prayer_times(self) -> Dict:
        """Get prayer times based on user's detected location"""
        location = self.get_user_location()
        
        if location.get('latitude') and location.get('longitude'):
            prayer_data = self.get_prayer_times_by_coordinates(
                location['latitude'], 
                location['longitude']
            )
            
            if prayer_data:
                prayer_data['location'] = location
                return prayer_data
        
        # Fallback to city-based lookup
        prayer_data = self.get_prayer_times(
            location['city'], 
            location['country']
        )
        
        if prayer_data:
            prayer_data['location'] = location
        
        return prayer_data or self._get_fallback_prayer_times()
    
    def _get_current_prayer(self, timings: Dict) -> str:
        """Determine current prayer based on time"""
        now = datetime.now().time()
        
        prayer_times = {
            'Fajr': datetime.strptime(timings['Fajr'], '%H:%M').time(),
            'Dhuhr': datetime.strptime(timings['Dhuhr'], '%H:%M').time(),
            'Asr': datetime.strptime(timings['Asr'], '%H:%M').time(),
            'Maghrib': datetime.strptime(timings['Maghrib'], '%H:%M').time(),
            'Isha': datetime.strptime(timings['Isha'], '%H:%M').time()
        }
        
        if now >= prayer_times['Isha'] or now < prayer_times['Fajr']:
            return 'Isha'
        elif now >= prayer_times['Maghrib']:
            return 'Maghrib'
        elif now >= prayer_times['Asr']:
            return 'Asr'
        elif now >= prayer_times['Dhuhr']:
            return 'Dhuhr'
        elif now >= prayer_times['Fajr']:
            return 'Fajr'
        
        return 'Fajr'
    
    def _get_next_prayer(self, timings: Dict, current_prayer: str) -> Dict:
        """Get next prayer information"""
        prayers = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha']
        
        try:
            current_index = prayers.index(current_prayer)
            next_index = (current_index + 1) % len(prayers)
            next_prayer_name = prayers[next_index]
            
            # Calculate time remaining
            now = datetime.now()
            next_time = datetime.strptime(timings[next_prayer_name], '%H:%M').time()
            next_datetime = datetime.combine(now.date(), next_time)
            
            # If next prayer is tomorrow
            if next_datetime <= now:
                next_datetime += timedelta(days=1)
            
            time_remaining = next_datetime - now
            hours, remainder = divmod(time_remaining.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            return {
                'name': next_prayer_name,
                'time': timings[next_prayer_name],
                'remaining': f"{hours}h {minutes}m"
            }
        except:
            return {
                'name': 'Fajr',
                'time': timings['Fajr'],
                'remaining': 'Unknown'
            }
    
    def _calculate_qibla_direction(self, latitude: float, longitude: float) -> float:
        """Calculate Qibla direction from given coordinates"""
        import math
        
        # Kaaba coordinates
        kaaba_lat = math.radians(21.4225)
        kaaba_lon = math.radians(39.8262)
        
        # User coordinates
        user_lat = math.radians(latitude)
        user_lon = math.radians(longitude)
        
        # Calculate bearing
        dlon = kaaba_lon - user_lon
        y = math.sin(dlon) * math.cos(kaaba_lat)
        x = math.cos(user_lat) * math.sin(kaaba_lat) - math.sin(user_lat) * math.cos(kaaba_lat) * math.cos(dlon)
        
        bearing = math.atan2(y, x)
        bearing = math.degrees(bearing)
        bearing = (bearing + 360) % 360
        
        return round(bearing, 2)
    
    def _get_fallback_prayer_times(self) -> Dict:
        """Fallback prayer times for Peshawar, Pakistan"""
        return {
            'timings': {
                'Fajr': '05:30',
                'Sunrise': '06:45',
                'Dhuhr': '12:15',
                'Asr': '15:30',
                'Maghrib': '18:00',
                'Isha': '19:30',
                'Midnight': '00:15'
            },
            'current_prayer': 'Dhuhr',
            'next_prayer': {
                'name': 'Asr',
                'time': '15:30',
                'remaining': 'Unknown'
            },
            'location': {
                'city': 'Peshawar',
                'country': 'Pakistan',
                'latitude': 34.0151,
                'longitude': 71.5249
            },
            'date': {
                'readable': datetime.now().strftime('%d %b %Y'),
                'hijri': {
                    'format': 'Hijri date unavailable'
                },
                'gregorian': {
                    'format': datetime.now().strftime('%d %B %Y')
                }
            },
            'method': 'Fallback Times',
            'qibla_direction': 255.5
        }
    
    def _get_method_name(self, method: int) -> str:
        """Get calculation method name"""
        methods = {
            1: "University of Islamic Sciences, Karachi",
            2: "Islamic Society of North America (ISNA)",
            3: "Muslim World League (MWL)",
            4: "Umm Al-Qura University, Makkah",
            5: "Egyptian General Authority of Survey",
            7: "Institute of Geophysics, University of Tehran",
            8: "Gulf Region",
            9: "Kuwait",
            10: "Qatar",
            11: "Majlis Ugama Islam Singapura, Singapore",
            12: "Union Organization islamic de France",
            13: "Diyanet İşleri Başkanlığı, Turkey"
        }
        return methods.get(method, f"Method {method}")
    
    def get_qibla_direction(self, latitude: float, longitude: float) -> Optional[Dict]:
        """
        Get Qibla direction for coordinates
        
        Args:
            latitude: Latitude
            longitude: Longitude
            
        Returns:
            Dictionary with Qibla direction or None
        """
        try:
            response = requests.get(
                f"{self.base_url}/qibla/{latitude}/{longitude}",
                timeout=10
            )
            
            if response.ok:
                data = response.json()
                if data.get('code') == 200:
                    return {
                        'direction': data['data']['direction'],
                        'latitude': latitude,
                        'longitude': longitude,
                        'source': 'Aladhan.com API'
                    }
        except Exception as e:
            print(f"Qibla direction API error: {e}")
        
        return None


# Global instance
prayer_times_engine = PrayerTimesEngine()


def get_prayer_times_for_city(city: str = "Peshawar", country: str = "Pakistan") -> Optional[Dict]:
    """Convenience function to get prayer times for city"""
    return prayer_times_engine.get_prayer_times(city, country)


def get_auto_location_prayer_times() -> Dict:
    """Convenience function to get prayer times based on user location"""
    return prayer_times_engine.get_auto_location_prayer_times()


def get_user_location() -> Dict:
    """Convenience function to get user's detected location"""
    return prayer_times_engine.get_user_location()


def get_current_prayer_name(prayer_times: Dict) -> Optional[str]:
    """Convenience function to get current prayer"""
    return prayer_times.get('current_prayer')
