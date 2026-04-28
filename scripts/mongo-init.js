// AI Hadith Authenticator - MongoDB Initialization Script
// Creates initial database structure and admin user

// Switch to the application database
db = db.getSiblingDB('hadith_auth');

// Create collections
db.createCollection('users');
db.createCollection('hadith_analyses');
db.createCollection('chat_history');
db.createCollection('search_history');
db.createCollection('quran_bookmarks');
db.createCollection('user_preferences');

// Create indexes for better performance
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "created_at": 1 });
db.users.createIndex({ "is_verified": 1 });

db.hadith_analyses.createIndex({ "user_id": 1 });
db.hadith_analyses.createIndex({ "created_at": 1 });
db.hadith_analyses.createIndex({ "grade": 1 });

db.chat_history.createIndex({ "user_id": 1 });
db.chat_history.createIndex({ "created_at": 1 });
db.chat_history.createIndex({ "session_id": 1 });

db.search_history.createIndex({ "user_id": 1 });
db.search_history.createIndex({ "created_at": 1 });
db.search_history.createIndex({ "search_query": "text" });

db.quran_bookmarks.createIndex({ "user_id": 1 });
db.quran_bookmarks.createIndex({ "surah_number": 1 });
db.quran_bookmarks.createIndex({ "created_at": 1 });

db.user_preferences.createIndex({ "user_id": 1 }, { unique: true });

// Insert sample data (optional)
db.users.insertOne({
    name: "Admin User",
    email: "admin@aihadithauthenticator.com",
    password: "$2b$12$LQv3c1yqBWVHxkd0LHAOqYqI5jE9i5dLg.Nj9CgQhLj7C1yC", // hashed "admin123"
    created_at: new Date(),
    is_verified: true,
    verification_token: null,
    last_login: null,
    login_count: 0,
    role: "admin"
});

// Insert sample hadith analyses
db.hadith_analyses.insertMany([
    {
        user_id: "admin@aihadithauthenticator.com",
        hadith_text: "Actions are judged by intentions.",
        grade: "Sahih",
        confidence: 95,
        warning: null,
        isnad: "Chain verified",
        source: "Sahih Bukhari 1:1",
        language: "en",
        created_at: new Date(),
        model_used: "direct_model"
    },
    {
        user_id: "admin@aihadithauthenticator.com",
        hadith_text: "The best among you are those who learn the Quran and teach it.",
        grade: "Sahih",
        confidence: 92,
        warning: null,
        isnad: "Chain verified",
        source: "Sahih Bukhari 6:545",
        language: "en",
        created_at: new Date(),
        model_used: "direct_model"
    }
]);

// Create database user for application
db.createUser({
    user: "hadith_user",
    pwd: "hadith_password_2024",
    roles: [
        {
            role: "readWrite",
            db: "hadith_auth"
        }
    ]
});

print("MongoDB initialization completed successfully!");
print("Collections created:");
print("- users");
print("- hadith_analyses");
print("- chat_history");
print("- search_history");
print("- quran_bookmarks");
print("- user_preferences");
print("");
print("Indexes created for performance optimization");
print("Sample data inserted");
print("Application user created: hadith_user");
