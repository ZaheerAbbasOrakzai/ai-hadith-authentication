"""
AI Hadith Authenticator - Database Module
Database operations and models for the application
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from config import get_config, SQLITE_DB_PATH, MONGODB_URI


class DatabaseManager:
    """Database manager with MongoDB primary and SQLite fallback"""
    
    def __init__(self):
        self.config = get_config()
        self.mongodb_client = None
        self.mongodb_db = None
        self.sqlite_conn = None
        self.using_mongodb = False
        
        # Initialize database connections
        self._initialize_connections()
    
    def _initialize_connections(self):
        """Initialize MongoDB and SQLite connections"""
        # Try MongoDB first
        try:
            self.mongodb_client = MongoClient(
                MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            
            # Test connection
            self.mongodb_client.admin.command('ping')
            
            self.mongodb_db = self.mongodb_client.hadith_auth
            self.using_mongodb = True
            print("✅ MongoDB connected successfully")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"⚠️ MongoDB connection failed: {e}")
            print("🔄 Falling back to SQLite...")
            self._initialize_sqlite()
        except Exception as e:
            print(f"❌ Unexpected database error: {e}")
            self._initialize_sqlite()
    
    def _initialize_sqlite(self):
        """Initialize SQLite connection"""
        try:
            self.sqlite_conn = sqlite3.connect(SQLITE_DB_PATH, check_same_thread=False)
            self._create_sqlite_tables()
            self.using_mongodb = False
            print("✅ SQLite initialized successfully")
        except Exception as e:
            print(f"❌ SQLite initialization failed: {e}")
            raise
    
    def _create_sqlite_tables(self):
        """Create SQLite tables if they don't exist"""
        if not self.sqlite_conn:
            return
        
        cursor = self.sqlite_conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL,
                is_verified INTEGER DEFAULT 0,
                verification_token TEXT,
                last_login TEXT,
                login_count INTEGER DEFAULT 0
            )
        ''')
        
        # Hadith analyses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hadith_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                hadith_text TEXT NOT NULL,
                grade TEXT,
                confidence TEXT,
                warning TEXT,
                isnad TEXT,
                source TEXT,
                language TEXT,
                created_at TEXT NOT NULL,
                model_used TEXT
            )
        ''')
        
        # Chat history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                user_message TEXT NOT NULL,
                ai_response TEXT NOT NULL,
                created_at TEXT NOT NULL,
                session_id TEXT
            )
        ''')
        
        # Search history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                search_query TEXT NOT NULL,
                results_count INTEGER,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Quran bookmarks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quran_bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                surah_number INTEGER NOT NULL,
                surah_name TEXT,
                verse_number INTEGER NOT NULL,
                verse_text TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        # User preferences table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                theme TEXT DEFAULT 'dark',
                language TEXT DEFAULT 'en',
                notifications_enabled INTEGER DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        self.sqlite_conn.commit()
        print("✅ SQLite tables created/verified")
    
    def get_connection(self):
        """Get active database connection"""
        if self.using_mongodb:
            return self.mongodb_db
        return self.sqlite_conn
    
    def is_using_mongodb(self):
        """Check if using MongoDB"""
        return self.using_mongodb
    
    def close(self):
        """Close database connections"""
        if self.mongodb_client:
            self.mongodb_client.close()
        if self.sqlite_conn:
            self.sqlite_conn.close()


class UserModel:
    """User model with MongoDB and SQLite support"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager.get_connection()
        self.using_mongodb = db_manager.is_using_mongodb()
    
    def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create a new user"""
        try:
            if self.using_mongodb:
                # MongoDB implementation
                user_data['_id'] = self.db.users.insert_one(user_data).inserted_id
                return user_data
            else:
                # SQLite implementation
                cursor = self.db.cursor()
                cursor.execute('''
                    INSERT INTO users (name, email, password, created_at, is_verified, verification_token)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    user_data['name'],
                    user_data['email'],
                    user_data['password'],
                    user_data['created_at'],
                    user_data.get('is_verified', 0),
                    user_data.get('verification_token')
                ))
                self.db.commit()
                user_data['id'] = cursor.lastrowid
                user_data['_id'] = cursor.lastrowid
                return user_data
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            if self.using_mongodb:
                # MongoDB implementation
                user = self.db.users.find_one({'email': email})
                return user
            else:
                # SQLite implementation
                cursor = self.db.cursor()
                cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
                row = cursor.fetchone()
                if row:
                    return {
                        '_id': row[0],
                        'id': row[0],
                        'name': row[1],
                        'email': row[2],
                        'password': row[3],
                        'created_at': row[4],
                        'is_verified': bool(row[5]),
                        'verification_token': row[6],
                        'last_login': row[7],
                        'login_count': row[8]
                    }
                return None
        except Exception as e:
            print(f"❌ Error getting user by email: {e}")
            return None
    
    def update_user(self, email: str, update_data: Dict[str, Any]) -> bool:
        """Update user data"""
        try:
            if self.using_mongodb:
                # MongoDB implementation
                result = self.db.users.update_one(
                    {'email': email},
                    {'$set': update_data}
                )
                return result.modified_count > 0
            else:
                # SQLite implementation
                cursor = self.db.cursor()
                
                # Build dynamic update query
                set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
                values = list(update_data.values()) + [email]
                
                cursor.execute(f'''
                    UPDATE users SET {set_clause}, updated_at = ?
                    WHERE email = ?
                ''', values)
                self.db.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"❌ Error updating user: {e}")
            return False
    
    def update_login_info(self, email: str) -> bool:
        """Update user login information"""
        update_data = {
            'last_login': datetime.now().isoformat(),
            'login_count': self.db.users.find_one({'email': email}).get('login_count', 0) + 1 if self.using_mongodb else 0
        }
        
        if not self.using_mongodb:
            # For SQLite, get current count first
            cursor = self.db.cursor()
            cursor.execute("SELECT login_count FROM users WHERE email = ?", (email,))
            result = cursor.fetchone()
            if result:
                update_data['login_count'] = result[0] + 1
        
        return self.update_user(email, update_data)


class HadithAnalysisModel:
    """Hadith analysis model"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager.get_connection()
        self.using_mongodb = db_manager.is_using_mongodb()
    
    def save_analysis(self, analysis_data: Dict[str, Any]) -> Optional[str]:
        """Save hadith analysis"""
        try:
            if self.using_mongodb:
                # MongoDB implementation
                result = self.db.hadith_analyses.insert_one(analysis_data)
                return str(result.inserted_id)
            else:
                # SQLite implementation
                cursor = self.db.cursor()
                cursor.execute('''
                    INSERT INTO hadith_analyses 
                    (user_id, hadith_text, grade, confidence, warning, isnad, source, language, created_at, model_used)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    analysis_data.get('user_id'),
                    analysis_data.get('hadith_text'),
                    analysis_data.get('grade'),
                    analysis_data.get('confidence'),
                    analysis_data.get('warning'),
                    analysis_data.get('isnad'),
                    analysis_data.get('source'),
                    analysis_data.get('language'),
                    analysis_data.get('created_at'),
                    analysis_data.get('model_used')
                ))
                self.db.commit()
                return str(cursor.lastrowid)
        except Exception as e:
            print(f"❌ Error saving analysis: {e}")
            return None
    
    def get_user_analyses(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's hadith analyses"""
        try:
            if self.using_mongodb:
                # MongoDB implementation
                analyses = list(self.db.hadith_analyses.find(
                    {'user_id': user_id}
                ).sort('created_at', -1).limit(limit))
                
                # Convert ObjectId to string for JSON serialization
                for analysis in analyses:
                    if '_id' in analysis:
                        analysis['_id'] = str(analysis['_id'])
                
                return analyses
            else:
                # SQLite implementation
                cursor = self.db.cursor()
                cursor.execute('''
                    SELECT * FROM hadith_analyses 
                    WHERE user_id = ? 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (user_id, limit))
                
                analyses = []
                for row in cursor.fetchall():
                    analyses.append({
                        'id': row[0],
                        '_id': row[0],
                        'user_id': row[1],
                        'hadith_text': row[2],
                        'grade': row[3],
                        'confidence': row[4],
                        'warning': row[5],
                        'isnad': row[6],
                        'source': row[7],
                        'language': row[8],
                        'created_at': row[9],
                        'model_used': row[10]
                    })
                
                return analyses
        except Exception as e:
            print(f"❌ Error getting user analyses: {e}")
            return []


class ChatHistoryModel:
    """Chat history model"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager.get_connection()
        self.using_mongodb = db_manager.is_using_mongodb()
    
    def save_message(self, chat_data: Dict[str, Any]) -> Optional[str]:
        """Save chat message"""
        try:
            if self.using_mongodb:
                # MongoDB implementation
                result = self.db.chat_history.insert_one(chat_data)
                return str(result.inserted_id)
            else:
                # SQLite implementation
                cursor = self.db.cursor()
                cursor.execute('''
                    INSERT INTO chat_history 
                    (user_id, user_message, ai_response, created_at, session_id)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    chat_data.get('user_id'),
                    chat_data.get('user_message'),
                    chat_data.get('ai_response'),
                    chat_data.get('created_at'),
                    chat_data.get('session_id')
                ))
                self.db.commit()
                return str(cursor.lastrowid)
        except Exception as e:
            print(f"❌ Error saving chat message: {e}")
            return None
    
    def get_user_chat_history(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's chat history"""
        try:
            if self.using_mongodb:
                # MongoDB implementation
                messages = list(self.db.chat_history.find(
                    {'user_id': user_id}
                ).sort('created_at', -1).limit(limit))
                
                # Convert ObjectId to string
                for message in messages:
                    if '_id' in message:
                        message['_id'] = str(message['_id'])
                
                return messages
            else:
                # SQLite implementation
                cursor = self.db.cursor()
                cursor.execute('''
                    SELECT * FROM chat_history 
                    WHERE user_id = ? 
                    ORDER BY created_at DESC 
                    LIMIT ?
                ''', (user_id, limit))
                
                messages = []
                for row in cursor.fetchall():
                    messages.append({
                        'id': row[0],
                        '_id': row[0],
                        'user_id': row[1],
                        'user_message': row[2],
                        'ai_response': row[3],
                        'created_at': row[4],
                        'session_id': row[5]
                    })
                
                return messages
        except Exception as e:
            print(f"❌ Error getting chat history: {e}")
            return []


class QuranBookmarkModel:
    """Quran bookmarks model"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager.get_connection()
        self.using_mongodb = db_manager.is_using_mongodb()
    
    def save_bookmark(self, bookmark_data: Dict[str, Any]) -> Optional[str]:
        """Save Quran bookmark"""
        try:
            if self.using_mongodb:
                # MongoDB implementation
                result = self.db.quran_bookmarks.insert_one(bookmark_data)
                return str(result.inserted_id)
            else:
                # SQLite implementation
                cursor = self.db.cursor()
                cursor.execute('''
                    INSERT INTO quran_bookmarks 
                    (user_id, surah_number, surah_name, verse_number, verse_text, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    bookmark_data.get('user_id'),
                    bookmark_data.get('surah_number'),
                    bookmark_data.get('surah_name'),
                    bookmark_data.get('verse_number'),
                    bookmark_data.get('verse_text'),
                    bookmark_data.get('created_at')
                ))
                self.db.commit()
                return str(cursor.lastrowid)
        except Exception as e:
            print(f"❌ Error saving bookmark: {e}")
            return None
    
    def get_user_bookmarks(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's Quran bookmarks"""
        try:
            if self.using_mongodb:
                # MongoDB implementation
                bookmarks = list(self.db.quran_bookmarks.find(
                    {'user_id': user_id}
                ).sort('created_at', -1))
                
                # Convert ObjectId to string
                for bookmark in bookmarks:
                    if '_id' in bookmark:
                        bookmark['_id'] = str(bookmark['_id'])
                
                return bookmarks
            else:
                # SQLite implementation
                cursor = self.db.cursor()
                cursor.execute('''
                    SELECT * FROM quran_bookmarks 
                    WHERE user_id = ? 
                    ORDER BY created_at DESC
                ''', (user_id,))
                
                bookmarks = []
                for row in cursor.fetchall():
                    bookmarks.append({
                        'id': row[0],
                        '_id': row[0],
                        'user_id': row[1],
                        'surah_number': row[2],
                        'surah_name': row[3],
                        'verse_number': row[4],
                        'verse_text': row[5],
                        'created_at': row[6]
                    })
                
                return bookmarks
        except Exception as e:
            print(f"❌ Error getting bookmarks: {e}")
            return []


# Database initialization
def init_database():
    """Initialize database connection"""
    return DatabaseManager()


# Utility functions
def backup_database():
    """Backup database (placeholder for future implementation)"""
    print("🔄 Database backup feature coming soon...")


def migrate_database():
    """Migrate database schema (placeholder for future implementation)"""
    print("🔄 Database migration feature coming soon...")


def cleanup_old_data():
    """Clean up old data (placeholder for future implementation)"""
    print("🔄 Data cleanup feature coming soon...")


# Database health check
def check_database_health():
    """Check database health"""
    try:
        db_manager = DatabaseManager()
        
        if db_manager.using_mongodb:
            # MongoDB health check
            db_manager.mongodb_client.admin.command('ping')
            status = "healthy"
            database_type = "MongoDB"
        else:
            # SQLite health check
            cursor = db_manager.sqlite_conn.cursor()
            cursor.execute("SELECT 1")
            status = "healthy"
            database_type = "SQLite"
        
        db_manager.close()
        
        return {
            'status': status,
            'database_type': database_type,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
