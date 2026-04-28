from flask import Flask, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'test_clear_session'

# Connect to MongoDB to clear any existing session data
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['AI_Hadith_DB']
    
    # This script will help clear any existing sessions
    print("Session clearing utility")
    print("Note: This will clear any existing user sessions in the database")
    print("Run this if you're experiencing authentication issues")
    
    # Optional: Clear any session collections if they exist
    if 'sessions' in db.list_collection_names():
        sessions_collection = db.sessions
        result = sessions_collection.delete_many({})
        print(f"Cleared {result.deleted_count} session records")
    
    print("Session clearing completed!")
    print("Now restart your app and it should redirect to login page")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'client' in locals():
        client.close()
