import sqlite3
import os

db_path = "ar-tafsir-ibn-kathir.db"

if os.path.exists(db_path):
    print(f"✓ Database found at: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print(f"\nTables: {tables}")
    
    # Get schema for first table
    if tables:
        table_name = tables[0][0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()
        print(f"\nSchema for '{table_name}':")
        for col in schema:
            print(f"  {col}")
        
        # Get sample row
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        sample = cursor.fetchone()
        print(f"\nSample row: {sample}")
        
        # Count rows
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"\nTotal rows: {count}")
    
    conn.close()
else:
    print(f"✗ Database not found at: {db_path}")
