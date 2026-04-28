"""
AI Hadith Authenticator - Utility Functions
Common utility functions used across the application
"""

import os
import re
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from flask import request, session
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_token(length: int = 32) -> str:
    """Generate secure random token"""
    return secrets.token_urlsafe(length)


def hash_password(password: str) -> str:
    """Hash password using SHA-256 (for additional security)"""
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> Dict[str, Any]:
    """Validate password strength"""
    result = {
        'valid': True,
        'errors': [],
        'score': 0
    }
    
    # Length check
    if len(password) < 8:
        result['valid'] = False
        result['errors'].append('Password must be at least 8 characters long')
    else:
        result['score'] += 1
    
    # Uppercase check
    if re.search(r'[A-Z]', password):
        result['score'] += 1
    else:
        result['errors'].append('Password should contain at least one uppercase letter')
    
    # Lowercase check
    if re.search(r'[a-z]', password):
        result['score'] += 1
    else:
        result['errors'].append('Password should contain at least one lowercase letter')
    
    # Number check
    if re.search(r'\d', password):
        result['score'] += 1
    else:
        result['errors'].append('Password should contain at least one number')
    
    # Special character check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        result['score'] += 1
    else:
        result['errors'].append('Password should contain at least one special character')
    
    # Common passwords check
    common_passwords = ['password', '123456', 'qwerty', 'admin', 'letmein']
    if password.lower() in common_passwords:
        result['valid'] = False
        result['errors'].append('Password is too common. Please choose a stronger password.')
        result['score'] = 0
    
    return result


def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS"""
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', 'javascript:', 'vbscript:', 'onload=', 'onerror=']
    for char in dangerous_chars:
        text = text.replace(char, '')
    
    return text.strip()


def format_date(date_string: str, format_type: str = 'readable') -> str:
    """Format date string"""
    try:
        if not date_string:
            return ""
        
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        
        if format_type == 'readable':
            return date_obj.strftime('%B %d, %Y at %I:%M %p')
        elif format_type == 'short':
            return date_obj.strftime('%m/%d/%Y')
        elif format_type == 'time':
            return date_obj.strftime('%I:%M %p')
        elif format_type == 'iso':
            return date_obj.isoformat()
        else:
            return str(date_obj)
    except Exception:
        return date_string


def get_client_ip() -> str:
    """Get client IP address"""
    if request.environ.get('HTTP_X_FORWARDED_FOR'):
        return request.environ.get('HTTP_X_FORWARDED_FOR')
    elif request.environ.get('HTTP_X_REAL_IP'):
        return request.environ.get('HTTP_X_REAL_IP')
    else:
        return request.environ.get('REMOTE_ADDR', 'unknown')


def is_logged_in() -> bool:
    """Check if user is logged in"""
    return 'user_id' in session and session['user_id']


def get_current_user() -> Optional[Dict[str, Any]]:
    """Get current user from session"""
    if is_logged_in():
        return {
            'id': session.get('user_id'),
            'email': session.get('user_email'),
            'name': session.get('user_name'),
            'last_login': session.get('last_login')
        }
    return None


def paginate_results(items: List[Any], page: int, per_page: int) -> Dict[str, Any]:
    """Paginate results"""
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'items': items[start:end],
        'total': len(items),
        'page': page,
        'per_page': per_page,
        'pages': (len(items) + per_page - 1) // per_page,
        'has_next': end < len(items),
        'has_prev': page > 1
    }


def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_names) - 1:
        size /= 1024.0
        i += 1
    
    return f"{size:.1f} {size_names[i]}"


def is_valid_file(file_obj, allowed_extensions: List[str]) -> bool:
    """Check if uploaded file is valid"""
    if not file_obj or not file_obj.filename:
        return False
    
    filename = file_obj.filename.lower()
    return any(filename.endswith('.' + ext) for ext in allowed_extensions)


def create_directory_if_not_exists(directory: str) -> bool:
    """Create directory if it doesn't exist"""
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {directory}: {e}")
        return False


def save_uploaded_file(file_obj, upload_folder: str) -> Optional[str]:
    """Save uploaded file and return path"""
    try:
        if not file_obj or not file_obj.filename:
            return None
        
        # Create upload directory if it doesn't exist
        create_directory_if_not_exists(upload_folder)
        
        # Generate secure filename
        filename = file_obj.filename
        file_extension = os.path.splitext(filename)[1]
        secure_filename = f"{generate_token(16)}{file_extension}"
        
        # Save file
        file_path = os.path.join(upload_folder, secure_filename)
        file_obj.save(file_path)
        
        logger.info(f"Saved uploaded file: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Failed to save uploaded file: {e}")
        return None


def cleanup_old_files(directory: str, max_age_days: int = 7) -> int:
    """Clean up old files in directory"""
    try:
        if not os.path.exists(directory):
            return 0
        
        current_time = datetime.now()
        deleted_count = 0
        
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                age_days = (current_time - file_time).days
                
                if age_days > max_age_days:
                    os.remove(file_path)
                    deleted_count += 1
                    logger.info(f"Deleted old file: {file_path}")
        
        return deleted_count
    except Exception as e:
        logger.error(f"Failed to cleanup old files: {e}")
        return 0


def extract_text_from_image(image_path: str) -> Optional[str]:
    """Extract text from image using OCR (placeholder)"""
    try:
        # This would integrate with OCR library like pytesseract
        # For now, return placeholder
        logger.info(f"OCR extraction requested for: {image_path}")
        return "OCR feature coming soon - text extraction from images"
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        return None


def extract_text_from_audio(audio_path: str) -> Optional[str]:
    """Extract text from audio using speech recognition (placeholder)"""
    try:
        # This would integrate with speech recognition library
        # For now, return placeholder
        logger.info(f"Audio transcription requested for: {audio_path}")
        return "Audio transcription feature coming soon - speech to text conversion"
    except Exception as e:
        logger.error(f"Audio transcription failed: {e}")
        return None


def analyze_hadith_keywords(text: str) -> Dict[str, Any]:
    """Analyze hadith text for keywords and patterns"""
    if not text:
        return {'grade': 'Not classified', 'confidence': 0, 'warnings': ['No text provided']}
    
    text_lower = text.lower()
    
    # Check for prophet references
    prophet_keywords = ['prophet', 'messenger', 'rasool', 'muhammad', 'pbuh', 'peace be upon him']
    has_prophet = any(keyword in text_lower for keyword in prophet_keywords)
    
    # Check for narration indicators
    narration_keywords = ['said', 'narrated', 'reported', 'told', 'mentioned', 'qala', 'rawwa']
    has_narration = any(keyword in text_lower for keyword in narration_keywords)
    
    # Check for Islamic content
    islamic_keywords = ['allah', 'god', 'islam', 'muslim', 'prayer', 'salah', 'quran', 'hadith']
    has_islamic = any(keyword in text_lower for keyword in islamic_keywords)
    
    # Check for weak indicators
    weak_keywords = ['weak', 'daif', 'mawdu', 'fabricated', 'false', 'inauthentic']
    has_weak = any(keyword in text_lower for keyword in weak_keywords)
    
    # Determine grade based on patterns
    if has_prophet and has_narration and has_islamic and not has_weak:
        grade = 'Hasan'
        confidence = 75
        warnings = []
    elif has_prophet and has_islamic:
        grade = 'Da\'if'
        confidence = 50
        warnings = ['Limited evidence - needs further verification']
    elif has_islamic:
        grade = 'Not classified'
        confidence = 25
        warnings = ['Insufficient information for classification']
    else:
        grade = 'Not classified'
        confidence = 15
        warnings = ['Non-Islamic content detected']
    
    return {
        'grade': grade,
        'confidence': confidence,
        'warnings': warnings,
        'isnad': 'Chain verification needed - AI model unavailable',
        'source': 'Keyword-based analysis - Please verify with authentic sources',
        'analysis_type': 'keyword_fallback'
    }


def format_hadith_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Format hadith analysis result for display"""
    confidence = result.get('confidence', 0)
    
    # Determine confidence color
    if confidence >= 80:
        confidence_color = 'success'
        confidence_text = 'High'
    elif confidence >= 60:
        confidence_color = 'warning'
        confidence_text = 'Medium'
    else:
        confidence_color = 'error'
        confidence_text = 'Low'
    
    # Determine grade color
    grade = result.get('grade', 'Unknown')
    if grade == 'Sahih':
        grade_color = 'success'
    elif grade == 'Hasan':
        grade_color = 'warning'
    elif grade == 'Da\'if':
        grade_color = 'error'
    else:
        grade_color = 'secondary'
    
    return {
        **result,
        'confidence_color': confidence_color,
        'confidence_text': confidence_text,
        'grade_color': grade_color,
        'formatted_confidence': f"{confidence}%",
        'formatted_grade': grade
    }


def cache_result(cache_key: str, data: Any, timeout_minutes: int = 5) -> None:
    """Cache result in session"""
    cache_data = {
        'data': data,
        'timestamp': datetime.now().isoformat(),
        'timeout_minutes': timeout_minutes
    }
    session[f'cache_{cache_key}'] = cache_data


def get_cached_result(cache_key: str) -> Optional[Any]:
    """Get cached result from session"""
    cache_key_full = f'cache_{cache_key}'
    
    if cache_key_full not in session:
        return None
    
    cache_data = session[cache_key_full]
    cache_time = datetime.fromisoformat(cache_data['timestamp'])
    timeout = timedelta(minutes=cache_data['timeout_minutes'])
    
    if datetime.now() - cache_time > timeout:
        # Cache expired
        session.pop(cache_key_full, None)
        return None
    
    return cache_data['data']


def clear_cache(cache_key: str = None) -> None:
    """Clear cache"""
    if cache_key:
        cache_key_full = f'cache_{cache_key}'
        session.pop(cache_key_full, None)
    else:
        # Clear all cache
        keys_to_remove = [key for key in session.keys() if key.startswith('cache_')]
        for key in keys_to_remove:
            session.pop(key, None)


def log_user_activity(activity: str, details: Dict[str, Any] = None) -> None:
    """Log user activity"""
    try:
        user = get_current_user()
        if user:
            log_entry = {
                'user_id': user['id'],
                'user_email': user['email'],
                'activity': activity,
                'details': details or {},
                'timestamp': datetime.now().isoformat(),
                'ip_address': get_client_ip()
            }
            
            # Log to file (in production, this would go to a proper logging system)
            logger.info(f"User activity: {json.dumps(log_entry)}")
    except Exception as e:
        logger.error(f"Failed to log user activity: {e}")


def get_system_stats() -> Dict[str, Any]:
    """Get system statistics"""
    try:
        stats = {
            'timestamp': datetime.now().isoformat(),
            'uptime': 'N/A',  # Would calculate from process start time
            'memory_usage': 'N/A',  # Would use psutil or similar
            'disk_usage': 'N/A',  # Would check disk space
            'database_status': 'healthy'
        }
        
        # Check if database is accessible
        try:
            from database import check_database_health
            db_health = check_database_health()
            stats['database_status'] = db_health['status']
            stats['database_type'] = db_health.get('database_type', 'Unknown')
        except Exception:
            stats['database_status'] = 'error'
            stats['database_type'] = 'Unknown'
        
        return stats
    except Exception as e:
        logger.error(f"Failed to get system stats: {e}")
        return {
            'timestamp': datetime.now().isoformat(),
            'status': 'error',
            'error': str(e)
        }


def create_response(success: bool, data: Any = None, error: str = None, message: str = None) -> Dict[str, Any]:
    """Create standardized API response"""
    response = {
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if success:
        if data is not None:
            response['data'] = data
        if message:
            response['message'] = message
    else:
        if error:
            response['error'] = error
        if message:
            response['message'] = message
    
    return response


def validate_api_key(api_key: str, expected_key: str) -> bool:
    """Validate API key"""
    if not api_key or not expected_key:
        return False
    
    # Use constant-time comparison to prevent timing attacks
    return secrets.compare_digest(api_key.encode(), expected_key.encode())


def rate_limit_check(identifier: str, limit: int, window_minutes: int = 60) -> Dict[str, Any]:
    """Check rate limit (placeholder - would use Redis or similar in production)"""
    # This is a simplified version - in production, use a proper rate limiting system
    cache_key = f"rate_limit_{identifier}"
    cached_data = get_cached_result(cache_key)
    
    if cached_data:
        request_count = cached_data.get('count', 0)
        last_request = cached_data.get('last_request')
        
        if last_request:
            last_time = datetime.fromisoformat(last_request)
            time_diff = datetime.now() - last_time
            
            if time_diff.total_seconds() < window_minutes * 60:
                if request_count >= limit:
                    return {
                        'allowed': False,
                        'remaining': 0,
                        'reset_time': (last_time + timedelta(minutes=window_minutes)).isoformat()
                    }
                else:
                    # Update count
                    new_data = {
                        'count': request_count + 1,
                        'last_request': datetime.now().isoformat()
                    }
                    cache_result(cache_key, new_data, window_minutes)
                    return {
                        'allowed': True,
                        'remaining': limit - request_count - 1,
                        'reset_time': (last_time + timedelta(minutes=window_minutes)).isoformat()
                    }
    
    # First request or window expired
    cache_result(cache_key, {
        'count': 1,
        'last_request': datetime.now().isoformat()
    }, window_minutes)
    
    return {
        'allowed': True,
        'remaining': limit - 1,
        'reset_time': (datetime.now() + timedelta(minutes=window_minutes)).isoformat()
    }


def generate_csrf_token() -> str:
    """Generate CSRF token"""
    return generate_token(32)


def validate_csrf_token(token: str) -> bool:
    """Validate CSRF token"""
    if 'csrf_token' not in session:
        return False
    
    return secrets.compare_digest(token.encode(), session['csrf_token'].encode())


# Error handling utilities
class AppError(Exception):
    """Base application error"""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(AppError):
    """Validation error"""
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, 'VALIDATION_ERROR')


class AuthenticationError(AppError):
    """Authentication error"""
    def __init__(self, message: str):
        super().__init__(message, 'AUTHENTICATION_ERROR')


class AuthorizationError(AppError):
    """Authorization error"""
    def __init__(self, message: str):
        super().__init__(message, 'AUTHORIZATION_ERROR')


class DatabaseError(AppError):
    """Database error"""
    def __init__(self, message: str):
        super().__init__(message, 'DATABASE_ERROR')


class ExternalServiceError(AppError):
    """External service error"""
    def __init__(self, message: str, service: str = None):
        self.service = service
        super().__init__(message, 'EXTERNAL_SERVICE_ERROR')
