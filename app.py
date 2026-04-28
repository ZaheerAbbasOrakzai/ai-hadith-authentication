from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from pymongo import MongoClient
import os
import re
import json
import requests
import random
import string
import tempfile
import sqlite3
from datetime import datetime, timedelta
from dotenv import load_dotenv
from huggingface_hub import snapshot_download
import logging
import warnings
from complete_surahs import COMPLETE_SURAHS
from deobandi_guidelines import (
    get_deobandi_guidelines,
    get_primary_sources,
    get_core_texts,
    get_recognized_scholars,
    get_fiqh_terminology,
    format_islamic_response
)
from quran_data_engine import quran_engine, get_maariful_quran_info
warnings.filterwarnings('ignore')

try:
    import torch
except ImportError:
    torch = None

try:
    from google import genai as google_genai
    _genai_available = True
except ImportError:
    google_genai = None
    _genai_available = False

# Load environment variables
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_DB_PATH = os.path.join(BASE_DIR, 'users.db')
HADITH_DATA_PATH = os.path.join(BASE_DIR, 'kutub_al_sittah_with_search_text.json')
ISLAMICITY_HADITH_SEARCH_URL = 'https://www.islamicity.org/hadith/search/'

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'ai_hadith_authenticator_secret_key_2025_secure')
app.config['TEMPLATES_AUTO_RELOAD'] = True

# HuggingFace Space API Configuration
HF_SPACE_NAME = "abbasorakzai777/ai-hadith-authentication"

# Global client for HF Space (initialized lazily)
_hf_client = None

def get_hf_client():
    """Get or create HF Space client"""
    global _hf_client
    if _hf_client is None:
        try:
            from gradio_client import Client
            _hf_client = Client(HF_SPACE_NAME)
        except Exception as e:
            print(f"Failed to initialize HF client: {e}")
            return None
    return _hf_client

def call_hf_space_api(lang_mode, text, image_path=None, audio_path=None):
    """Call the HuggingFace Space API for hadith analysis using Gradio Client"""
    client = get_hf_client()
    if not client:
        return {
            'success': False,
            'error': 'Failed to connect to analysis service. Please try again later.'
        }

    try:
        # Prepare inputs for the predict function
        # Based on reference: lang_mode, text, image, audio
        inputs = [
            lang_mode,
            text or "",
            image_path if image_path and os.path.exists(image_path) else None,
            audio_path if audio_path and os.path.exists(audio_path) else None
        ]

        # Call the predict function
        result = client.predict(
            *inputs,
            api_name="/predict"
        )

        # Parse the response: [grade, confidence, warning, isnad, source]
        if result and len(result) >= 5:
            return {
                'success': True,
                'grade': result[0],
                'confidence': result[1],
                'warning': result[2],
                'isnad': result[3],
                'source': result[4]
            }
        else:
            return {
                'success': False,
                'error': 'Invalid response from analysis service'
            }

    except Exception as e:
        print(f"HF Space API error: {e}")
        return {
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }

# Initialize extensions
bcrypt = Bcrypt(app)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
mail = Mail(app)

# Make functions available to templates
@app.template_global()
def is_logged_in():
    return 'user_id' in session

@app.template_global()
def get_current_user():
    if 'user_id' in session:
        return session.get('name', 'User')
    return None

@app.template_global()
def url_for_static(filename):
    return url_for('static', filename=filename)

# Database Configuration
# Initialize global variables
client = None
db = None
users_collection = None
conn = None
sqlite_conn = None

try:
    # Try MongoDB first
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/hadith_auth'), serverSelectionTimeoutMS=2000, connectTimeoutMS=2000)
    db = client.hadith_auth
    users_collection = db.users
    conn = "MongoDB"
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using SQLite as fallback database (this is normal for development)")
    conn = "SQLite"

# Always initialize SQLite as backup (even if MongoDB is primary)
try:
    db_dir = os.path.dirname(USERS_DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print(f"Created database directory: {db_dir}")

    sqlite_conn = sqlite3.connect(USERS_DB_PATH, check_same_thread=False)
    sqlite_conn.execute('''CREATE TABLE IF NOT EXISTS users
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          name TEXT NOT NULL,
                          email TEXT UNIQUE NOT NULL,
                          password TEXT NOT NULL,
                          created_at TEXT NOT NULL,
                          is_verified INTEGER DEFAULT 0,
                          verification_token TEXT)''')
    sqlite_conn.commit()
    print(f"SQLite database ready at: {USERS_DB_PATH}")
except Exception as sqlite_e:
    print(f"SQLite initialization failed: {sqlite_e}")
    import traceback
    traceback.print_exc()

# Hugging Face Configuration
HF_SPACE_ID = os.getenv('HF_SPACE_ID', 'abbasorakzai777/ai-hadith-authentication')
HF_TOKEN = os.getenv('HF_TOKEN', '')  # Set in environment variables
HF_SPACE_URL = os.getenv('HF_SPACE_URL', 'https://abbasorakzai777-ai-hadith-authentication.hf.space')
HF_MODEL_SUBDIR = os.getenv('HF_MODEL_SUBDIR', 'final_model')
HF_MODEL_CACHE_DIR = os.getenv('HF_MODEL_CACHE_DIR', os.path.join(os.path.dirname(__file__), '.hf-cache'))
SUNNAH_API_KEY = os.getenv('SUNNAH_API_KEY', '')  # Set in environment variables

HADITH_COLLECTIONS = [
    {
        'alias': 'bukhari',
        'name': 'Sahih al-Bukhari',
        'book_names': ['bukhari', 'sahih bukhari', 'sahih al-bukhari'],
        'category': 'Kutub al-Sittah',
        'description': 'Widely regarded as the most authentic hadith collection after the Quran.',
        'accent': 'green'
    },
    {
        'alias': 'muslim',
        'name': 'Sahih Muslim',
        'book_names': ['muslim', 'sahih muslim'],
        'category': 'Kutub al-Sittah',
        'description': 'A foundational sahih collection known for rigorous narration standards.',
        'accent': 'blue'
    },
    {
        'alias': 'abudawud',
        'name': 'Sunan Abi Dawud',
        'book_names': ['abu dawud', 'abi dawud', 'abudawud', 'sunan abu dawud', 'sunan abi dawud'],
        'category': 'Kutub al-Sittah',
        'description': 'A major source for hadith related to rulings, worship, and daily life.',
        'accent': 'purple'
    },
    {
        'alias': 'tirmidhi',
        'name': "Jami' at-Tirmidhi",
        'book_names': ['tirmidhi', "jami' at-tirmidhi", 'jami at tirmidhi'],
        'category': 'Kutub al-Sittah',
        'description': 'Known for combining hadith transmission with grading and scholarly insight.',
        'accent': 'rose'
    },
    {
        'alias': 'nasai',
        'name': "Sunan an-Nasa'i",
        'book_names': ["nasa'i", 'nasai', "sunan an-nasa'i", 'sunan an nasai'],
        'category': 'Kutub al-Sittah',
        'description': 'A carefully curated collection valued for precision and strong narrations.',
        'accent': 'amber'
    },
    {
        'alias': 'ibnmajah',
        'name': 'Sunan Ibn Majah',
        'book_names': ['ibn majah', 'ibnmajah', 'sunan ibn majah'],
        'category': 'Kutub al-Sittah',
        'description': 'A major canonical collection that complements the other six books.',
        'accent': 'yellow'
    },
    {
        'alias': 'muwatta',
        'name': "Muwatta' Malik",
        'book_names': ["muwatta", "muwatta' malik", 'malik'],
        'category': 'Classical Collection',
        'description': 'An early hadith and fiqh collection associated with Imam Malik.',
        'accent': 'emerald'
    },
    {
        'alias': 'riyadussalihin',
        'name': 'Riyad as-Salihin',
        'book_names': ['riyad as-salihin', 'riyad us salihin', 'riyadussalihin'],
        'category': 'Ethics & Spirituality',
        'description': 'A widely read selection of hadith focused on character, worship, and manners.',
        'accent': 'indigo'
    },
    {
        'alias': 'nawawi40',
        'name': "Imam Nawawi's Forty Hadith",
        'book_names': ["nawawi's forty hadith", 'forty hadith nawawi', 'nawawi 40', 'nawawi40'],
        'category': 'Core Essentials',
        'description': 'A concise foundational set of hadith covering major principles of Islam.',
        'accent': 'pink'
    }
]

THEME_MODES = {'light', 'dark', 'system'}
THEME_ACCENTS = {'emerald', 'indigo', 'rose', 'amber'}
DEFAULT_THEME_MODE = 'system'
DEFAULT_THEME_ACCENT = 'emerald'

# Gemini AI Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
gemini_client = None

if GEMINI_API_KEY and _genai_available:
    try:
        gemini_client = google_genai.Client(api_key=GEMINI_API_KEY)
        print("[OK] Gemini API configured successfully (google-genai SDK, gemini-2.5-flash)")
    except Exception as _ge:
        print(f"[WARN] Gemini init failed: {_ge}")
        gemini_client = None
elif not GEMINI_API_KEY:
    print("[WARN] Gemini API key not configured")
elif not _genai_available:
    print("[WARN] google-genai package not installed")

# Keep gemini_model as alias so rest of code works
gemini_model = gemini_client

# Direct Model Import Class
class DirectHadithModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cpu"  # Use CPU for compatibility
        self.loaded = False
        self.model_path = None
        self.label_mapping = {
            0: "Sahih",
            1: "Hasan",
            2: "Da'if"
        }
        
    def load_model(self):
        if not torch:
            self.loaded = False
            return False
        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
            snapshot_dir = snapshot_download(
                repo_id=HF_SPACE_ID,
                repo_type="space",
                allow_patterns=[f"{HF_MODEL_SUBDIR}/*"],
                token=HF_TOKEN or None,
                local_dir=HF_MODEL_CACHE_DIR
            )
            model_path = os.path.join(snapshot_dir, HF_MODEL_SUBDIR)
            if not os.path.isdir(model_path):
                # Try to load from Hugging Face Hub
                model_name = "abbasorakzai777/ai-hadith-authentication/final_model"
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
                self.model.eval()
                self.model_path = model_path
                self.loaded = True
                config = getattr(self.model, "config", None)
                if config and getattr(config, "id2label", None):
                    raw_labels = {int(k): v for k, v in config.id2label.items()}
                    if set(raw_labels.values()) != {"LABEL_0", "LABEL_1", "LABEL_2"}:
                        self.label_mapping = raw_labels
                raw_labels = {int(k): v for k, v in config.id2label.items()}
                if set(raw_labels.values()) != {"LABEL_0", "LABEL_1", "LABEL_2"}:
                    self.label_mapping = raw_labels
            return True
        except Exception as e:
            print(f"Direct model loading failed: {e}")
            self.loaded = False
            return False
    
    def predict(self, text, lang_mode="auto"):
        """Make prediction using the loaded model"""
        if not torch or not self.loaded or not self.model or not self.tokenizer:
            return None
            
        try:
            # Simple prediction logic
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
            predicted_class = torch.argmax(predictions, dim=-1).item()
            confidence = torch.max(predictions, dim=-1)[0].item()
            grade = self.label_mapping.get(predicted_class, f"Label {predicted_class}")
            return [grade, f"{confidence*100:.1f}%", "", "Model classification only", f"HF final_model ({os.path.basename(self.model_path or HF_MODEL_SUBDIR)})"]
            
        except Exception as e:
            print(f"Direct model prediction failed: {e}")
            return None

# Global variables
_hf_client = None
_hf_text_cache = {}
hadith_data = []
direct_model = DirectHadithModel()
_local_fallback_predictor = None
_local_fallback_load_attempted = False

# Initialize Hugging Face client
try:
    from gradio_client import Client
except ImportError:
    Client = None

# Initialize Hugging Face client
_hf_client = None
handle_file = None
target = os.getenv('HF_SPACE_URL', 'https://abbasorakzai777-ai-hadith-authentication.hf.space')

if target and Client:
    try:
        _hf_client = Client(target)
        print("Hugging Face client initialized successfully")
    except Exception as e:
        print(f"Could not initialize Hugging Face client: {e}")
        print("Direct model will be used as fallback (this is normal)")
        print(f"Error details: {type(e).__name__}: {str(e)}")
        _hf_client = None
        handle_file = None
else:
    print("Gradio client not available or no target URL")
    _hf_client = None
    handle_file = None

# Load Hadith Data
try:
    with open(HADITH_DATA_PATH, 'r', encoding='utf-8') as f:
        hadith_data = json.load(f)
    print("Hadith database loaded successfully")
except Exception as e:
    print(f"Could not load hadith database: {e}")
    hadith_data = []

def get_hf_client():
    return _hf_client

def _normalize_collection_value(value):
    normalized = (value or '').strip().lower()
    normalized = re.sub(r'[^a-z0-9]+', ' ', normalized)
    return ' '.join(normalized.split())

def _get_local_collection_aliases():
    local_aliases = set()
    for hadith in hadith_data:
        book_name = _normalize_collection_value(hadith.get('book') or hadith.get('source') or hadith.get('source_book'))
        for collection in HADITH_COLLECTIONS:
            if book_name and book_name in {_normalize_collection_value(name) for name in collection['book_names']}:
                local_aliases.add(collection['alias'])
                break
    return local_aliases

def get_hadith_collections():
    local_aliases = _get_local_collection_aliases()
    collections = []
    for collection in HADITH_COLLECTIONS:
        collection_data = dict(collection)
        collection_data['local_available'] = collection['alias'] in local_aliases
        collection_data['external_url'] = ISLAMICITY_HADITH_SEARCH_URL
        collections.append(collection_data)
    return collections

def _extract_collection_filter(query_text, collection_value):
    selected_collection = _normalize_collection_value(collection_value)
    cleaned_query = (query_text or '').strip()
    if cleaned_query.lower().startswith('collection:'):
        _, _, collection_part = cleaned_query.partition(':')
        selected_collection = _normalize_collection_value(collection_part)
        cleaned_query = ''
    return cleaned_query, selected_collection

def _resolve_collection_alias(collection_value):
    normalized_value = _normalize_collection_value(collection_value)
    if not normalized_value:
        return None
    for collection in HADITH_COLLECTIONS:
        known_names = {_normalize_collection_value(collection['alias']), _normalize_collection_value(collection['name'])}
        known_names.update(_normalize_collection_value(name) for name in collection['book_names'])
        if normalized_value in known_names:
            return collection['alias']
    return None

def _match_collection_alias(book_name):
    normalized_book = _normalize_collection_value(book_name)
    if not normalized_book:
        return None
    for collection in HADITH_COLLECTIONS:
        if normalized_book in {_normalize_collection_value(name) for name in collection['book_names']}:
            return collection['alias']
    return None

def _save_uploaded_file(uploaded_file):
    if not uploaded_file or not uploaded_file.filename:
        return None
    suffix = os.path.splitext(uploaded_file.filename)[1]
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    uploaded_file.save(temp_file.name)
    temp_file.close()
    return temp_file.name

def _hf_file_arg(path):
    if not path:
        return None
    if handle_file:
        return handle_file(path)
    return path

def predict_with_hf_space(lang_mode, text, image_path=None, audio_path=None):
    client = get_hf_client()
    if not client:
        return None
    image_arg = _hf_file_arg(image_path)
    audio_arg = _hf_file_arg(audio_path)
    attempts = [
        lambda: client.predict(lang_mode, text, image_arg, audio_arg, api_name="/predict"),
        lambda: client.predict(lang_mode, text, image_arg, audio_arg)
    ]
    for attempt in attempts:
        try:
            result = attempt()
            if isinstance(result, (list, tuple)) and len(result) >= 5:
                return {
                    'grade': result[0],
                    'confidence': result[1],
                    'warning': result[2],
                    'isnad': result[3],
                    'source': result[4]
                }
        except Exception as e:
            print(f"Hugging Face Space prediction failed: {e}")
    return None

def _get_local_fallback_predictor():
    global _local_fallback_predictor, _local_fallback_load_attempted
    if _local_fallback_load_attempted:
        return _local_fallback_predictor
    _local_fallback_load_attempted = True
    try:
        from hadith_classifier import predict_hadith
        _local_fallback_predictor = predict_hadith
    except Exception as e:
        print(f"Local multimodal fallback unavailable: {e}")
        _local_fallback_predictor = None
    return _local_fallback_predictor

def predict_with_local_fallback(lang_mode, text, image_path=None, audio_path=None):
    predictor = _get_local_fallback_predictor()
    if not predictor:
        return None
    try:
        result = predictor(lang_mode, text, image_path, audio_path)
        if isinstance(result, (list, tuple)) and len(result) >= 5:
            return {
                'grade': result[0],
                'confidence': result[1],
                'warning': result[2],
                'isnad': result[3],
                'source': result[4]
            }
    except Exception as e:
        print(f"Local multimodal fallback failed: {e}")
    return None

def build_manual_media_response():
    return {
        'grade': 'Not classified',
        'confidence': '0%',
        'warning': 'Could not extract text from the uploaded image/audio because OCR or ASR is unavailable and the remote model could not be reached. Paste the hadith text manually or install the local OCR/ASR dependencies.',
        'isnad': 'No extracted text available for chain verification',
        'source': 'Manual text input required'
    }

def build_unverified_analysis_response():
    return {
        'grade': 'Not classified',
        'confidence': '0%',
        'warning': 'Could not verify authenticity because the model services are unavailable. No heuristic grade was assigned.',
        'isnad': 'Chain verification unavailable while model services are offline',
        'source': 'Verification unavailable'
    }

def get_user_by_email(email):
    # Try MongoDB first with proper error handling
    if users_collection is not None:
        try:
            user = users_collection.find_one({'email': email})
            return user
        except Exception as e:
            print(f"MongoDB lookup failed, falling back to SQLite: {e}")
            # Don't return here, continue to SQLite fallback
    
    # SQLite fallback
    if sqlite_conn is not None:
        try:
            cursor = sqlite_conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return {
                    '_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'password': row[3],
                    'created_at': row[4],
                    'is_verified': bool(row[5]),
                    'verification_token': row[6]
                }
        except Exception as e:
            print(f"SQLite lookup failed: {e}")
    
    return None

def get_theme_preferences():
    mode = session.get('theme_mode', DEFAULT_THEME_MODE)
    accent = session.get('theme_accent', DEFAULT_THEME_ACCENT)
    if mode not in THEME_MODES:
        mode = DEFAULT_THEME_MODE
    if accent not in THEME_ACCENTS:
        accent = DEFAULT_THEME_ACCENT
    return {
        'mode': mode,
        'accent': accent
    }

def set_theme_preferences(mode=None, accent=None):
    preferences = get_theme_preferences()
    if mode in THEME_MODES:
        session['theme_mode'] = mode
        preferences['mode'] = mode
    if accent in THEME_ACCENTS:
        session['theme_accent'] = accent
        preferences['accent'] = accent
    return preferences

def get_current_user_profile():
    fallback_name = session.get('name', 'User')
    fallback_email = session.get('email', '')
    user = get_user_by_email(fallback_email) if fallback_email else None
    name = (user or {}).get('name', fallback_name)
    email = (user or {}).get('email', fallback_email)
    created_at_raw = (user or {}).get('created_at') or session.get('created_at')
    joined_on = 'Recently'
    if created_at_raw:
        try:
            joined_on = datetime.fromisoformat(str(created_at_raw)).strftime('%d %b %Y')
        except ValueError:
            joined_on = str(created_at_raw)[:10]
    initials = ''.join(part[:1].upper() for part in name.split()[:2]) or 'U'
    theme_preferences = get_theme_preferences()
    collections = get_hadith_collections()
    local_collection_count = sum(1 for collection in collections if collection['local_available'])
    return {
        'name': name,
        'email': email,
        'joined_on': joined_on,
        'initials': initials,
        'theme_mode': theme_preferences['mode'],
        'theme_accent': theme_preferences['accent'],
        'collection_count': len(collections),
        'local_collection_count': local_collection_count
    }

def build_page_context(**kwargs):
    profile = get_current_user_profile()
    context = {
        'name': profile['name'],
        'email': profile['email'],
        'user_profile': profile,
        'theme_preferences': get_theme_preferences(),
        'hadith_collections': get_hadith_collections(),
        'islamicity_url': ISLAMICITY_HADITH_SEARCH_URL
    }
    context.update(kwargs)
    return context

def search_hadith_database(query_text):
    """Search real hadith database for matching entries"""
    try:
        query_lower = query_text.lower()
        for hadith in hadith_data[:100]:  # Search through real hadith data
            if 'text' in hadith and 'english' in hadith['text']:
                if any(word in hadith['text']['english'].lower() for word in query_lower.split()[:3]):
                    return {
                        'grade': hadith.get('grade', 'Unknown'),
                        'confidence': 'Reference match',
                        'warning': 'Matched against local source data; scholarly review is still recommended',
                        'isnad': hadith.get('isnad', 'Chain available in original source'),
                        'source': hadith.get('book', 'Unknown source')
                    }
        return {
            'grade': 'Not found in database',
            'confidence': '0%',
            'warning': 'No reliable source match was found; manual verification is required',
            'isnad': 'Chain verification unavailable',
            'source': 'Source verification required'
        }
    except Exception as e:
        print(f"Database search error: {e}")
        return {
            'grade': 'Analysis failed',
            'confidence': '0%',
            'warning': 'Database search error',
            'isnad': 'Not available',
            'source': 'Not available'
        }

def create_user(name, email, password):
    import traceback
    log_file = open('registration_debug.log', 'a')
    log_file.write(f"\n--- Registration attempt: {email} at {datetime.now()} ---\n")

    try:
        user_data = {
            'name': name,
            'email': email,
            'password': bcrypt.generate_password_hash(password).decode('utf-8'),
            'created_at': datetime.now().isoformat(),
            'is_verified': False,
            'verification_token': ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        }

        log_file.write(f"users_collection is None: {users_collection is None}\n")
        log_file.write(f"sqlite_conn is None: {sqlite_conn is None}\n")

        # Try MongoDB first with proper error handling
        if users_collection is not None:
            try:
                log_file.write("Attempting MongoDB insert...\n")
                result = users_collection.insert_one(user_data)
                log_file.write(f"MongoDB insert SUCCESS, id: {result.inserted_id}\n")
                user_data['_id'] = result.inserted_id
                log_file.close()
                return user_data
            except Exception as e:
                log_file.write(f"MongoDB insert FAILED: {e}\n")
                log_file.write(traceback.format_exc())
                log_file.write("\nFalling back to SQLite...\n")

        # SQLite fallback
        if sqlite_conn is not None:
            try:
                log_file.write("Attempting SQLite insert...\n")
                cursor = sqlite_conn.cursor()
                cursor.execute(
                    "INSERT INTO users (name, email, password, created_at, is_verified, verification_token) VALUES (?, ?, ?, ?, ?, ?)",
                    (name, email, user_data['password'], user_data['created_at'], 0, user_data['verification_token'])
                )
                sqlite_conn.commit()
                user_data['_id'] = cursor.lastrowid
                log_file.write(f"SQLite insert SUCCESS, id: {cursor.lastrowid}\n")
                log_file.close()
                return user_data
            except Exception as e:
                log_file.write(f"SQLite insert FAILED: {e}\n")
                log_file.write(traceback.format_exc())
                log_file.close()
                return None

        log_file.write("ERROR: Both databases unavailable\n")
        log_file.close()
        return None

    except Exception as e:
        log_file.write(f"UNEXPECTED ERROR in create_user: {e}\n")
        log_file.write(traceback.format_exc())
        log_file.close()
        return None

@app.before_request
def require_login():
    if request.endpoint in ['index', 'login', 'signup', 'static', 'health', 'forgot_password', 'reset_password', 'verify_otp', 'collections', 'mushaf', 'tafsir_viewer',
                            'api_prayer_times', 'api_location', 'api_tafsir', 'api_tafsir_surah', 'api_tafsir_search', 'api_tafsir_stats',
                            'api_youtube_approved', 'api_youtube_scholars', 'api_youtube_channels', 'api_youtube_guidelines'] or is_logged_in():
        return
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index_premium.html', **build_page_context())

@app.route('/profile')
def profile():
    if not is_logged_in():
        return redirect(url_for('login'))
    profile_data = get_current_user_profile()
    return render_template(
        'profile.html',
        **build_page_context(
            profile_data=profile_data,
            profile_stats=[
                {'label': 'Supported Collections', 'value': str(profile_data['collection_count'])},
                {'label': 'Local Collections', 'value': str(profile_data['local_collection_count'])},
                {'label': 'Theme Mode', 'value': profile_data['theme_mode'].title()},
                {'label': 'Accent Theme', 'value': profile_data['theme_accent'].title()}
            ]
        )
    )

@app.route('/settings')
def settings():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template(
        'settings.html',
        **build_page_context(
            theme_modes=['system', 'light', 'dark'],
            theme_accents=[
                {'value': 'emerald', 'label': 'Emerald', 'preview': 'from-emerald-500 to-green-600'},
                {'value': 'indigo', 'label': 'Indigo', 'preview': 'from-indigo-500 to-violet-600'},
                {'value': 'rose', 'label': 'Rose', 'preview': 'from-rose-500 to-pink-600'},
                {'value': 'amber', 'label': 'Amber', 'preview': 'from-amber-500 to-orange-600'}
            ]
        )
    )

@app.route('/settings/theme', methods=['POST'])
def update_theme():
    if not is_logged_in():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    payload = request.get_json(silent=True) or request.form
    preferences = set_theme_preferences(
        mode=(payload.get('mode') or '').strip().lower(),
        accent=(payload.get('accent') or '').strip().lower()
    )
    return jsonify({
        'success': True,
        'theme_preferences': preferences
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect already authenticated users to index
    if session.get('user_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if not email or not password:
            flash('Please fill all fields', 'error')
            return render_template('auth_login.html')

        user = get_user_by_email(email)
        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id']) if '_id' in user else 'demo_user'
            session['name'] = user.get('name', 'User')
            session['email'] = user['email']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password. Please check your credentials.', 'error')

    return render_template('auth_login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Redirect already authenticated users to index
    if session.get('user_id'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not all([name, email, password]):
            flash('Please fill all fields', 'error')
            return render_template('auth_signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('auth_signup.html')
        
        existing_user = get_user_by_email(email)
        if existing_user:
            flash('Email already registered', 'error')
            return render_template('auth_signup.html')
        
        user = create_user(name, email, password)
        if user:
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            print(f"DEBUG: Registration failed for {email}")
            print(f"DEBUG: users_collection is None: {users_collection is None}")
            print(f"DEBUG: sqlite_conn is None: {sqlite_conn is None}")
            flash('Registration failed. Database connection error. Please restart the server.', 'error')
    
    return render_template('auth_signup.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        
        if not email:
            flash('Please enter your email address', 'error')
            return render_template('forgot_password.html')
        
        user = get_user_by_email(email)
        if not user:
            flash('Email address not found', 'error')
            return render_template('forgot_password.html')
        
        # Generate and store OTP (simplified for demo)
        import random
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Store OTP in session and user email
        session['reset_email'] = email
        session['otp'] = otp  # In production, store in database with expiry
        
        # Send OTP email (simplified for demo)
        print(f"OTP for {email}: {otp}")  # Debug output
        flash(f'Password reset OTP sent to {email}. For demo: OTP is {otp}', 'success')
        return redirect(url_for('verify_otp'))
    
    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    # Check if user has verified OTP
    if not session.get('otp_verified') or not session.get('reset_email'):
        flash('Access denied. Please complete the OTP verification first.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirmPassword', '').strip()
        
        if not password or not confirm_password:
            flash('Please fill all fields', 'error')
            return render_template('reset_password.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('reset_password.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('reset_password.html')
        
        # Update user password
        reset_email = session.get('reset_email')
        try:
            # Update password in database
            if sqlite_conn:
                cursor = sqlite_conn.cursor()
                cursor.execute("UPDATE users SET password = ? WHERE email = ?", 
                             (bcrypt.generate_password_hash(password).decode('utf-8'), reset_email))
                sqlite_conn.commit()
            
            # Clear session
            session.pop('reset_email', None)
            session.pop('otp', None)
            session.pop('otp_verified', None)
            
            flash('Password reset successful! Please login with your new password.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Password reset failed. Please try again.', 'error')
            print(f"Password reset error: {e}")
    
    return render_template('reset_password.html')

@app.route('/hadith-analyzer')
def hadith_analyzer():
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('hadith_analyzer_new.html', **build_page_context())

@app.route('/analyze-hadith', methods=['POST'])
def analyze_hadith():
    image_path = None
    audio_path = None
    try:
        lang_mode = request.form.get('lang_mode') or request.form.get('language') or 'auto'
        text = request.form.get('text', '').strip()
        image_path = _save_uploaded_file(request.files.get('image'))
        audio_path = _save_uploaded_file(request.files.get('audio'))
        has_uploaded_media = bool(image_path or audio_path)

        if not text and not has_uploaded_media:
            return jsonify({
                'success': False,
                'error': 'Please enter hadith text or upload image/audio'
            }), 400

        # If only media (no text), try to extract text
        if not text:
            hf_result = predict_with_hf_space(lang_mode, text, image_path=image_path, audio_path=audio_path)
            if hf_result:
                return jsonify({'success': True, 'data': hf_result})
            fallback_result = predict_with_local_fallback(lang_mode, text, image_path=image_path, audio_path=audio_path)
            if fallback_result:
                return jsonify({'success': True, 'data': fallback_result})
            return jsonify({
                'success': True,
                'data': build_manual_media_response()
            })

        # If we have text, try multiple methods in order of preference
        
        # 1. Try direct model (fastest, local)
        if text and not image_path and not audio_path and (direct_model.loaded or direct_model.load_model()):
            result = direct_model.predict(text, lang_mode)
            if result:
                return jsonify({
                    'success': True,
                    'data': {
                        'grade': result[0],
                        'confidence': result[1],
                        'warning': result[2],
                        'isnad': result[3],
                        'source': result[4]
                    }
                })

        # 2. Try HuggingFace Space
        hf_result = predict_with_hf_space(lang_mode, text, image_path=image_path, audio_path=audio_path)
        if hf_result:
            return jsonify({'success': True, 'data': hf_result})

        # 3. Try local fallback
        fallback_result = predict_with_local_fallback(lang_mode, text, image_path=image_path, audio_path=audio_path)
        if fallback_result:
            return jsonify({'success': True, 'data': fallback_result})

        # 4. Try database search (best fallback for text)
        if text:
            db_result = search_hadith_database(text)
            if db_result and db_result.get('grade') != 'Not found in database':
                return jsonify({'success': True, 'data': db_result})

        # 5. Last resort - return unverified response
        return jsonify({
            'success': True,
            'data': build_unverified_analysis_response()
        })
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({
            'success': False,
            'error': 'Analysis failed. Please try again.'
        }), 500
    finally:
        for temp_path in (image_path, audio_path):
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

# =============================================
# HADITH CLASSIFIER & AUTHENTICATOR CONFIG
# =============================================
CDN_BASE = "https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions"

I18N = {
    "ar": {
        "title": "مُصَنِّف ومُوَثِّق الأحاديث النبوية",
        "subtitle": "تصنيف آلي + استخراج السند الأصيل من sunnah.com",
        "btn": "تحليل الحديث الآن",
        "input_text": "أدخل نص الحديث أو ارفع صورة / صوت",
        "short": "النص قصير جدًا",
        "weak": "تنبيه: الحديث ضعيف",
        "no_match": "لم يُعثر على مطابقة كافية",
        "ocr_fail": "[فشل استخراج النص من الصورة]",
        "asr_fail": "[فشل تحويل الصوت إلى نص]",
        "model_fail": "[خطأ في التصنيف]"
    },
    "en": {
        "title": "Hadith Classifier & Authenticator",
        "subtitle": "ML Grading + Authentic Isnād from sunnah.com",
        "btn": "Analyze Hadith Now",
        "input_text": "Enter hadith text or upload image / audio",
        "short": "Text too short",
        "weak": "Warning: Weak hadith",
        "no_match": "No sufficient match found",
        "ocr_fail": "[Failed to extract text from image]",
        "asr_fail": "[Failed to transcribe audio]",
        "model_fail": "[Classification model error]"
    }
}

LABELS = {
    0: {"ar": "صحيح", "en": "Sahih"},
    1: {"ar": "حسن",  "en": "Hasan"},
    2: {"ar": "ضعيف", "en": "Da'if"}
}

ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]")

def get_lang(s):
    return "ar" if ARABIC_RE.search(s or "") else "en"

def normalize_text(text, lang):
    text = (text or "").strip().lower()
    if lang == "ar":
        text = re.sub(r"[ًٌٍَُِّْـ]", "", text)
        text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())

def safe_ocr(image_path):
    """Extract text from image using OCR"""
    if not image_path or not os.path.exists(image_path):
        return ""
    try:
        from PIL import Image, ImageOps
        import pytesseract
        pil_img = Image.open(image_path)
        pil_img = ImageOps.grayscale(pil_img)
        pil_img = ImageOps.autocontrast(pil_img)
        text = pytesseract.image_to_string(
            pil_img,
            lang="ara+eng",
            config="--psm 6"
        ).strip()
        return text if text else "[No text found in image]"
    except ImportError as e:
        return f"[OCR library missing: Install pytesseract and Tesseract OCR]"
    except pytesseract.TesseractNotFoundError:
        return f"[Tesseract OCR not installed: Please install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki]"
    except Exception as e:
        return f"[OCR failed: {str(e)[:100]}]"

def safe_asr(audio_path):
    """Extract text from audio using Whisper ASR"""
    if not audio_path or not os.path.exists(audio_path):
        return ""
    try:
        import soundfile as sf
        from transformers import pipeline
        audio, sr = sf.read(audio_path)
        asr = pipeline("automatic-speech-recognition", model="openai/whisper-small", device=-1)
        result = asr({"array": audio, "sampling_rate": sr})
        text = result["text"].strip()
        return text if text else "[No speech detected]"
    except Exception as e:
        return f"[Audio failed: {str(e)[:70]}]"

def safe_pdf_extract(pdf_path):
    """Extract text from PDF file"""
    if not pdf_path or not os.path.exists(pdf_path):
        return ""
    try:
        # Try PyPDF2 first
        try:
            import PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip() if text.strip() else "[No text found in PDF]"
        except ImportError:
            pass
        
        # Fallback to pdfplumber
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text.strip() if text.strip() else "[No text found in PDF]"
        except ImportError:
            pass
        
        # Final fallback - try OCR on PDF pages as images
        try:
            from pdf2image import convert_from_path
            from PIL import Image, ImageOps
            import pytesseract
            
            images = convert_from_path(pdf_path, first_page=1, last_page=5)
            text = ""
            for img in images:
                img = ImageOps.grayscale(img)
                img = ImageOps.autocontrast(img)
                page_text = pytesseract.image_to_string(img, lang='ara+eng', config='--psm 6')
                text += page_text + "\n"
            return text.strip() if text.strip() else "[No text found in PDF]"
        except Exception as e:
            return f"[PDF extraction failed: {str(e)[:70]}]"
            
    except Exception as e:
        return f"[PDF extraction failed: {str(e)[:70]}]"

def find_hadith_lookup(text, lang):
    """Look up hadith on sunnah.com + CDN fallback"""
    if len(text.strip()) < 12:
        return None
    
    query = normalize_text(text, lang)
    
    # sunnah.com - primary source
    try:
        sunnah_key = os.getenv('SUNNAH_API_KEY', 'SqD712P3T216niHek5QM9L')
        r = requests.get(
            f"https://api.sunnah.com/v1/hadiths/search/{query[:110]}",
            headers={"X-API-Key": sunnah_key},
            params={"limit": 1},
            timeout=10
        )
        if r.ok:
            data = r.json()
            if data.get("data"):
                h = data["data"][0]
                isnad = h.get("chain", "") or h["hadith"][0].get("body", "")
                coll = h["collection"]["name"]
                book = h["book"]["bookName"]
                num = h["hadithNumber"]
                grade = h.get("grade", "—")
                return {
                    "isnad": isnad.strip(),
                    "source": f"{coll} → {book} → Hadith {num}",
                    "grade": grade
                }
    except Exception as e:
        print("sunnah.com error:", str(e))
    
    # CDN fallback
    try:
        import difflib
        collections = ["bukhari", "muslim", "tirmidhi"]
        prefix = "ara" if lang == "ar" else "eng"
        for coll in collections:
            url = f"{CDN_BASE}/{prefix}-{coll}.min.json"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                continue
            hadiths = r.json()["hadiths"]
            texts = [normalize_text(h["text"], lang) for h in hadiths]
            matches = difflib.get_close_matches(query, texts, n=1, cutoff=0.42)
            if matches:
                idx = texts.index(matches[0])
                h = hadiths[idx]
                return {
                    "isnad": h.get("header", "—").strip(),
                    "source": f"{coll.title()} - Hadith {h.get('hadithnumber', '—')}",
                    "grade": h.get("grades", [{}])[0].get("grade", "—") if h.get("grades") else "—"
                }
    except Exception as e:
        print("CDN fallback error:", str(e))
    
    return None

def classify_hadith(text, lang):
    """Classify hadith using ML model"""
    T = I18N[lang]
    cleaned = text.strip()
    if len(cleaned) < 15:
        return "—", "0%", T["short"]
    
    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import torch
        model_dir = os.path.join(BASE_DIR, "final_model")
        if os.path.exists(model_dir):
            tokenizer = AutoTokenizer.from_pretrained(model_dir)
            model = AutoModelForSequenceClassification.from_pretrained(model_dir)
            model.eval()
            
            inputs = tokenizer(cleaned[:1500], truncation=True, padding=True, max_length=512, return_tensors="pt")
            with torch.no_grad():
                logits = model(**inputs).logits
                probs = torch.softmax(logits, dim=-1)
                pred = probs.argmax(-1).item()
                conf = probs.max().item() * 100
            
            grade = LABELS[pred][lang]
            confidence = f"{conf:.1f}%"
            warning = T["weak"] if pred == 2 else ""
            return grade, confidence, warning
    except Exception as e:
        print("Classification error:", str(e))
    
    return "—", "0%", T["model_fail"]

@app.route('/analyze-full', methods=['POST'])
def analyze_full():
    """Full hadith analysis with multiple fallback methods"""
    print("=" * 60)
    print("ANALYZE-FULL ROUTE CALLED - NEW VERSION WITH FALLBACKS")
    print("=" * 60)
    
    if not is_logged_in():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    image_path = None
    audio_path = None
    pdf_path = None

    try:
        text = request.form.get('text', '').strip()
        lang_mode = request.form.get('lang', 'auto')
        image_file = request.files.get('image')
        audio_file = request.files.get('audio')
        pdf_file = request.files.get('pdf')

        print(f"Received request - text: {len(text)} chars, image: {image_file.filename if image_file else 'None'}, audio: {audio_file.filename if audio_file else 'None'}, pdf: {pdf_file.filename if pdf_file else 'None'}")

        # Save uploaded files
        if image_file:
            image_path = _save_uploaded_file(image_file)
            print(f"Image saved to: {image_path}")
        if audio_file:
            audio_path = _save_uploaded_file(audio_file)
        if pdf_file:
            pdf_path = _save_uploaded_file(pdf_file)

        # Process PDF if provided (extract text and add to text input)
        if pdf_path:
            pdf_text = safe_pdf_extract(pdf_path)
            if pdf_text and not pdf_text.startswith("["):
                text += "\n\n" + pdf_text
                print(f"PDF extracted: {len(pdf_text)} chars")

        # If we have text, try multiple methods in order of preference
        
        # 1. Try direct model (fastest, local)
        print("Trying method 1: Direct Model...")
        if text and not image_path and not audio_path and (direct_model.loaded or direct_model.load_model()):
            result = direct_model.predict(text, lang_mode)
            if result:
                print("✅ Direct Model SUCCESS")
                return jsonify({
                    'success': True,
                    'grade': result[0],
                    'confidence': result[1],
                    'warning': result[2],
                    'isnad': result[3],
                    'source': result[4]
                })
        print("❌ Direct Model failed or not available")

        # 2. Try HuggingFace Space
        print("Trying method 2: HuggingFace Space...")
        hf_result = predict_with_hf_space(lang_mode, text, image_path=image_path, audio_path=audio_path)
        if hf_result:
            print("✅ HuggingFace Space SUCCESS")
            return jsonify({
                'success': True,
                'grade': hf_result['grade'],
                'confidence': hf_result['confidence'],
                'warning': hf_result['warning'],
                'isnad': hf_result['isnad'],
                'source': hf_result['source']
            })
        print("❌ HuggingFace Space failed")

        # 3. Try local fallback
        print("Trying method 3: Local Fallback...")
        fallback_result = predict_with_local_fallback(lang_mode, text, image_path=image_path, audio_path=audio_path)
        if fallback_result:
            print("✅ Local Fallback SUCCESS")
            return jsonify({
                'success': True,
                'grade': fallback_result['grade'],
                'confidence': fallback_result['confidence'],
                'warning': fallback_result['warning'],
                'isnad': fallback_result['isnad'],
                'source': fallback_result['source']
            })
        print("❌ Local Fallback failed")

        # 4. Try database search (best fallback for text)
        print("Trying method 4: Database Search...")
        if text:
            db_result = search_hadith_database(text)
            if db_result and db_result.get('grade') != 'Not found in database':
                print("✅ Database Search SUCCESS")
                return jsonify({
                    'success': True,
                    'grade': db_result['grade'],
                    'confidence': db_result['confidence'],
                    'warning': db_result['warning'],
                    'isnad': db_result['isnad'],
                    'source': db_result['source']
                })
        print("❌ Database Search failed")

        # 5. Last resort - return unverified response
        print("Using method 5: Unverified Response (last resort)")
        unverified = build_unverified_analysis_response()
        return jsonify({
            'success': True,
            'grade': unverified['grade'],
            'confidence': unverified['confidence'],
            'warning': unverified['warning'],
            'isnad': unverified['isnad'],
            'source': unverified['source']
        })

    except Exception as e:
        print(f"Full analysis error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Analysis failed: {str(e)}'
        }), 500
    finally:
        # Clean up temporary files
        for temp_path in (image_path, audio_path, pdf_path):
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

@app.route('/chat')
def chat_page():
    """Render the AI chat interface page"""
    if not is_logged_in():
        return redirect(url_for('login'))
    return render_template('chat.html', **build_page_context())

def _call_gemini(prompt: str) -> str:
    """
    Try every available Gemini model in order.
    On 429 wait the suggested delay then retry once.
    Returns the response text or raises an exception.
    """
    import time, re as _re

    models = [
        'gemini-2.5-flash',
        'gemini-2.0-flash',
        'gemini-2.0-flash-lite',
        'gemini-flash-latest',
    ]

    last_err = None
    for model in models:
        for attempt in range(2):          # 2 attempts per model (retry after wait)
            try:
                resp = gemini_client.models.generate_content(
                    model=model,
                    contents=prompt
                )
                if resp and resp.text:
                    print(f"[OK] Gemini responded via {model}")
                    return resp.text.strip()
            except Exception as e:
                err_str = str(e)
                last_err = e
                if '429' in err_str or 'RESOURCE_EXHAUSTED' in err_str:
                    # Parse suggested retry delay from error message
                    delay_match = _re.search(r"retryDelay.*?(\d+)s", err_str)
                    wait = int(delay_match.group(1)) if delay_match else 15
                    wait = min(wait, 20)   # cap at 20 s so request doesn't time out
                    print(f"[WARN] {model} rate-limited, waiting {wait}s …")
                    time.sleep(wait)
                    continue              # retry same model after wait
                elif '503' in err_str or 'UNAVAILABLE' in err_str:
                    print(f"[WARN] {model} overloaded, trying next model …")
                    break                 # skip to next model immediately
                else:
                    print(f"[WARN] {model} error: {err_str[:120]}")
                    break                 # non-rate-limit error → try next model
    raise last_err or RuntimeError("All Gemini models failed")


@app.route('/chat/message', methods=['POST'])
def chat_message():
    """Real AI chat powered by Google Gemini — tries all models, retries on rate-limit."""
    if not is_logged_in():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    try:
        data = request.get_json()
        message = (data.get('message') or '').strip()
        if not message:
            return jsonify({'success': False, 'error': 'Please enter a message'}), 400

        if not gemini_client or not GEMINI_API_KEY:
            return jsonify({'success': False, 'error': 'AI service not configured.'}), 500

        # Compact but complete Islamic system prompt
        prompt = (
            "You are Sheikh Ahmad, a knowledgeable and friendly Islamic AI assistant. "
            "Answer ALL questions about Islam (Quran, Hadith, Fiqh, Prayer, Zakat, Hajj, "
            "Ramadan, Islamic history, family, ethics, modern issues) thoroughly and accurately. "
            "Be warm and conversational. Use bullet points and **bold** where helpful. "
            "Cite Quran verses or Hadith when relevant. Never refuse an Islamic question.\n\n"
            f"User: {message}\nSheikh Ahmad:"
        )

        reply = _call_gemini(prompt)

        # Prepend Islamic greeting if user greeted
        greetings = ['hello', 'hi', 'assalam', 'salam', 'aoa', 'hey', 'asalam', 'salaam']
        if any(g in message.lower() for g in greetings):
            if 'السلام' not in reply and 'Assalamu' not in reply:
                reply = (
                    "وعليكم السلام ورحمة الله وبركاته\n"
                    "*(Wa alaykum assalam wa rahmatullahi wa barakatuh)*\n\n"
                ) + reply

        return jsonify({
            'success': True,
            'response': reply,
            'timestamp': datetime.now().strftime('%I:%M %p')
        })

    except Exception as e:
        err = str(e)
        print(f"[ERROR] chat_message final: {err[:200]}")
        if '429' in err or 'RESOURCE_EXHAUSTED' in err:
            return jsonify({
                'success': False,
                'error': (
                    '⚠️ The AI quota is temporarily exhausted on this API key. '
                    'Please go to https://aistudio.google.com/apikey, create a new free API key, '
                    'and update GEMINI_API_KEY in your .env file, then restart the app.'
                )
            }), 429
        return jsonify({'success': False, 'error': f'AI error: {err[:120]}'}), 500


@app.route('/search', methods=['GET'])
def search():
    if not is_logged_in():
        return redirect(url_for('login'))
        
    raw_query = request.args.get('q', '').strip()
    query, requested_collection = _extract_collection_filter(raw_query, request.args.get('collection', ''))
    collection_alias = _resolve_collection_alias(requested_collection)
    
    if not query and not collection_alias:
        return render_template('search.html', results=[], active_collection=None, query='', **build_page_context())
    
    results = []
    query_lower = query.lower()
    
    for hadith in hadith_data:
        english_text = hadith.get('english') or hadith.get('text_en') or hadith.get('text_english') or ''
        arabic_text = hadith.get('arabic') or hadith.get('text_ar') or hadith.get('text_arabic') or hadith.get('text') or ''
        source_text = hadith.get('source') or hadith.get('book') or hadith.get('source_book') or ''
        grade_text = hadith.get('grade') or hadith.get('classification') or 'Unknown'
        hadith_id = hadith.get('id') or hadith.get('hadith_id') or ''
        book_alias = _match_collection_alias(source_text)
        if not book_alias:
            continue
        if collection_alias and book_alias != collection_alias:
            continue
        matches_query = not query or query_lower in english_text.lower() or query_lower in arabic_text.lower() or query_lower in source_text.lower()
        if matches_query:
            results.append({
                'id': hadith_id,
                'text': english_text or arabic_text,
                'english': english_text,
                'arabic': arabic_text,
                'source': source_text,
                'grade': grade_text,
                'number': hadith.get('hadithnumber') or hadith.get('hadith_number') or hadith.get('reference', {}).get('hadith'),
                'collection': book_alias,
                'source_url': hadith.get('source_url') or ISLAMICITY_HADITH_SEARCH_URL
            })
    
    return render_template('search.html', results=results[:20], active_collection=collection_alias, query=query, **build_page_context())

@app.route('/hadith-collections')
def hadith_collections():
    return jsonify({
        'collections': get_hadith_collections(),
        'external_search_url': ISLAMICITY_HADITH_SEARCH_URL
    })

@app.route('/quran')
def quran():
    if not is_logged_in():
        return redirect(url_for('login'))

    # Complete Surah data for the Quran list (all 114 surahs)
    surahs = COMPLETE_SURAHS

    return render_template('quran_list.html', surahs=surahs, **build_page_context())

@app.route('/quran/<int:surah_num>')
def quran_surah(surah_num):
    if not is_logged_in():
        return redirect(url_for('login'))
    
    # Get the surah metadata from COMPLETE_SURAHS
    surah_metadata = None
    for s in COMPLETE_SURAHS:
        if s['number'] == surah_num:
            surah_metadata = s
            break
    
    if not surah_metadata:
        return redirect(url_for('quran'))
    
    # Fetch the actual Quran verses from API
    try:
        import requests
        # Fetch Arabic text
        arabic_response = requests.get(
            f"http://api.alquran.cloud/v1/surah/{surah_num}",
            timeout=10
        )
        # Fetch English translation
        english_response = requests.get(
            f"http://api.alquran.cloud/v1/surah/{surah_num}/en.asad",
            timeout=10
        )
        
        if arabic_response.ok and english_response.ok:
            arabic_data = arabic_response.json()
            english_data = english_response.json()
            
            if arabic_data.get('code') == 200 and english_data.get('code') == 200:
                surah = {
                    'number': surah_metadata['number'],
                    'name': surah_metadata['name'],
                    'englishName': surah_metadata['englishName'],
                    'englishNameTranslation': surah_metadata['englishNameTranslation'],
                    'numberOfAyahs': surah_metadata['numberOfAyahs'],
                    'revelationType': surah_metadata['revelationType'],
                    'ayahs': arabic_data['data']['ayahs']
                }
                english_surah = {
                    'ayahs': english_data['data']['ayahs']
                }
                return render_template('surah_view.html', surah=surah, english_surah=english_surah, bookmarked_ayah=None, **build_page_context())
    except Exception as e:
        print(f"Error fetching Quran data: {e}")
    
    # Fallback: return just metadata if API fails
    return render_template('surah_view.html', surah=surah_metadata, english_surah=None, bookmarked_ayah=None, **build_page_context())

@app.route('/collections')
def collections():
    # Allow access without login for collections page
    from prayer_times_engine import get_auto_location_prayer_times, get_user_location
    from tafsir_engine import get_tafsir_stats
    from youtube_content_engine import get_approved_youtube_content
    
    # Get user location and prayer times automatically
    try:
        prayer_times_data = get_auto_location_prayer_times()
    except Exception as e:
        print(f"Auto location prayer times error: {e}")
        # Fallback to Peshawar
        from prayer_times_engine import get_prayer_times_for_city
        prayer_times_data = get_prayer_times_for_city('Peshawar', 'Pakistan')
    
    # Get tafsir stats
    tafsir_stats = get_tafsir_stats()
    
    # Get YouTube content
    youtube_content = get_approved_youtube_content()
    
    return render_template('collections.html', 
                         prayer_times_data=prayer_times_data,
                         tafsir_stats=tafsir_stats,
                         youtube_content=youtube_content,
                         **build_page_context())

@app.route('/mushaf')
def mushaf():
    """16-line Indo-Pak Mushaf reader"""
    return render_template('mushaf.html')

@app.route('/tafsir')
def tafsir_viewer():
    """Tafsir Ibn Kathir viewer and search"""
    return render_template('tafsir_viewer.html')

@app.route('/islamic-guidelines')
def islamic_guidelines():
    """Display Deobandi (Hanafi-Maturidi) Islamic guidelines and sources"""
    if not is_logged_in():
        return redirect(url_for('login'))
    
    return render_template(
        'islamic_guidelines.html',
        guidelines=get_deobandi_guidelines(),
        primary_sources=get_primary_sources(),
        core_texts=get_core_texts(),
        scholars=get_recognized_scholars(),
        terminology=get_fiqh_terminology(),
        **build_page_context()
    )

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    reset_email = session.get('reset_email')
    stored_otp = session.get('otp')
    
    if not reset_email or not stored_otp:
        flash('Session expired. Please try again.', 'error')
        return redirect(url_for('forgot_password'))
    
    if request.method == 'POST':
        otp = request.form.get('otp', '').strip()
        
        if not otp:
            flash('Please enter the OTP', 'error')
            return render_template('verify_otp.html')
        
        if otp == stored_otp:
            session['otp_verified'] = True
            # Clear the OTP after successful verification
            session.pop('otp', None)
            flash('OTP verified successfully. Please set your new password.', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('Invalid OTP. Please try again.', 'error')
    
    return render_template('verify_otp.html')

# ============================================================================
# COLLECTION SECTION API ROUTES
# ============================================================================

@app.route('/api/prayer-times')
def api_prayer_times():
    """Enhanced prayer times API with location detection"""
    try:
        # Check if specific location requested
        city = request.args.get('city')
        country = request.args.get('country')
        
        if city and country:
            from prayer_times_engine import get_prayer_times_for_city
            prayer_times = get_prayer_times_for_city(city, country)
        else:
            # Auto-detect location and get prayer times
            from prayer_times_engine import get_auto_location_prayer_times
            prayer_times = get_auto_location_prayer_times()
        
        if prayer_times:
            return jsonify({
                'success': True,
                'data': prayer_times,
                'location_detected': not (city and country)
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch prayer times'
            }), 500
            
    except Exception as e:
        print(f"Prayer times API error: {e}")
        return jsonify({
            'success': False,
            'error': 'Prayer times service unavailable'
        }), 500

@app.route('/api/location')
def api_location():
    """API endpoint to get user's detected location"""
    try:
        from prayer_times_engine import get_user_location
        location = get_user_location()
        
        return jsonify({
            'success': True,
            'data': location
        })
        
    except Exception as e:
        print(f"Location API error: {e}")
        return jsonify({
            'success': False,
            'error': 'Location service unavailable'
        }), 500

@app.route('/api/tafsir/<int:surah>/<int:ayah>')
def api_tafsir(surah, ayah):
    """Get Tafsir Ibn Kathir for specific ayah"""
    from tafsir_engine import get_tafsir_for_ayah
    
    tafsir = get_tafsir_for_ayah(surah, ayah)
    
    if tafsir:
        return jsonify({
            'success': True,
            'data': tafsir
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Tafsir not found for this ayah'
        }), 404

@app.route('/api/tafsir/surah/<int:surah>')
def api_tafsir_surah(surah):
    """Get all Tafsir Ibn Kathir entries for a surah"""
    from tafsir_engine import tafsir_engine
    
    tafsir_list = tafsir_engine.get_surah_tafsir(surah)
    
    if tafsir_list:
        return jsonify({
            'success': True,
            'count': len(tafsir_list),
            'data': tafsir_list
        })
    else:
        return jsonify({
            'success': False,
            'error': 'No tafsir found for this surah'
        }), 404

@app.route('/api/tafsir/search')
def api_tafsir_search():
    """Search Tafsir Ibn Kathir"""
    from tafsir_engine import tafsir_engine
    
    query = request.args.get('q', '')
    limit = int(request.args.get('limit', 10))
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query required'
        }), 400
    
    results = tafsir_engine.search_tafsir(query, limit)
    
    return jsonify({
        'success': True,
        'count': len(results),
        'data': results
    })

@app.route('/api/tafsir/stats')
def api_tafsir_stats():
    """Get Tafsir database statistics"""
    from tafsir_engine import get_tafsir_stats
    
    stats = get_tafsir_stats()
    
    return jsonify({
        'success': True,
        'data': stats
    })

@app.route('/api/youtube/approved')
def api_youtube_approved():
    """Get approved YouTube scholars and channels"""
    from youtube_content_engine import get_approved_youtube_content
    
    content = get_approved_youtube_content()
    
    return jsonify({
        'success': True,
        'count': len(content),
        'data': content
    })

@app.route('/api/youtube/scholars')
def api_youtube_scholars():
    """Get approved Islamic scholars"""
    from youtube_content_engine import get_approved_scholars
    
    scholars = get_approved_scholars()
    
    return jsonify({
        'success': True,
        'count': len(scholars),
        'data': scholars
    })

@app.route('/api/youtube/channels')
def api_youtube_channels():
    """Get approved YouTube channels"""
    from youtube_content_engine import get_approved_channels
    
    channels = get_approved_channels()
    
    return jsonify({
        'success': True,
        'count': len(channels),
        'data': channels
    })

@app.route('/api/youtube/guidelines')
def api_youtube_guidelines():
    """Get YouTube content filtering guidelines"""
    from youtube_content_engine import youtube_engine
    
    guidelines = youtube_engine.get_content_guidelines()
    
    return jsonify({
        'success': True,
        'data': guidelines
    })

if __name__ == '__main__':
    import os
    import sys
    
    # CRITICAL: Clear all problematic Werkzeug environment variables immediately
    # This must happen before any Flask imports are used
    problematic_env_vars = [
        'WERKZEUG_SERVER_FD',
        'WERKZEUG_RUN_MAIN',
        'FLASK_RUN_FROM_CLI',
        'FLASK_ENV',
        'FLASK_DEBUG'
    ]
    
    for var in problematic_env_vars:
        if var in os.environ:
            try:
                del os.environ[var]
            except:
                pass
    
    # Set only safe environment variables
    os.environ['FLASK_ENV'] = 'development'
    os.environ['PYTHONUNBUFFERED'] = '1'
    
    print("[START] AI Hadith Authenticator Server")
    print("=" * 50)
    print("[INFO] Environment variables cleaned")
    print("-" * 50)
    
    # Try different server configurations
    server_configs = [
        {
            'name': 'Debug Mode',
            'debug': True,
            'threaded': True,
            'use_reloader': False,
            'host': '127.0.0.1',
            'port': 5000
        },
        {
            'name': 'Development Mode (Safe)',
            'debug': True,
            'threaded': False,
            'use_reloader': False,
            'host': '0.0.0.0',
            'port': 5000
        },
        {
            'name': 'Basic Mode (Minimal)',
            'debug': False,
            'threaded': False,
            'use_reloader': False,
            'host': '127.0.0.1',
            'port': 5000
        }
    ]

    for config in server_configs:
        try:
            print(f"[START] Starting {config['name']}...")
            print(f"[URL] Server: http://{config['host']}:{config['port']}")
            print(f"[CONFIG] Debug: {config['debug']}, Threaded: {config['threaded']}")
            print("-" * 40)

            # Remove 'name' parameter as it's not valid for app.run()
            config_copy = config.copy()
            config_name = config_copy.pop('name')
            app.run(**config_copy)
            break
            
        except OSError as e:
            if "WinError 10038" in str(e) or "not a socket" in str(e):
                print(f"[WARN] Socket error in {config['name']}")
                print("[RETRY] Trying next configuration...")
                continue
            else:
                print(f"[ERROR] Server error: {e}")
                raise
        except KeyboardInterrupt:
            print("\n[STOP] Server stopped gracefully")
            sys.exit(0)
        except KeyError as e:
            if 'WERKZEUG_SERVER_FD' in str(e):
                print(f"[WARN] Werkzeug environment issue in {config['name']}")
                print("[RETRY] Trying next configuration...")
                continue
            else:
                print(f"[ERROR] Critical error in {config['name']}: {e}")
                continue
        except Exception as e:
            print(f"[ERROR] Unexpected error in {config['name']}: {e}")
            continue
    else:
        print("\n[ERROR] All server configurations failed!")
        print("[INFO] Try using the stable server: python run_stable.py")
        print("[INFO] Or install Waitress: pip install waitress")
        sys.exit(1)
