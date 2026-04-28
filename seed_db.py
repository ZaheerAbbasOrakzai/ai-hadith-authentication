import json
from pymongo import MongoClient, TEXT
from tqdm import tqdm
import sys

def connect_to_mongodb():
    """Establish connection to MongoDB and return the collection."""
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['AI_Hadith_DB']
        collection = db['hadiths']
        
        # Clear existing data
        print("Clearing existing hadiths collection...")
        collection.delete_many({})
        print("Existing data cleared successfully.")
        
        return collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        sys.exit(1)

def load_json_data(file_path):
    """Load and return JSON data from file."""
    try:
        print(f"Loading data from {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

def transform_hadith_data(hadith):
    """Transform raw hadith data to match our schema."""
    return {
        'source_book': hadith.get('book', 'Unknown'),
        'hadith_number': hadith.get('hadithnumber'),
        'arabic_number': hadith.get('arabicnumber'),
        'text_arabic': hadith.get('text_ar', ''),
        'text_english': hadith.get('text_en', ''),
        'grade': hadith.get('classification', 'Unknown'),
        'hadith_id': hadith.get('hadith_id'),
        'reference': hadith.get('reference', {}),
        'narrators': hadith.get('narrators', []),
        'source_url': hadith.get('source_url', '')
    }

def batch_insert(collection, data, batch_size=2000):
    """Insert data into MongoDB in batches."""
    total = len(data)
    print(f"Starting to insert {total} hadiths in batches of {batch_size}...")
    
    for i in tqdm(range(0, total, batch_size), desc="Inserting hadiths"):
        batch = data[i:i + batch_size]
        transformed_batch = [transform_hadith_data(h) for h in batch]
        collection.insert_many(transformed_batch, ordered=False)
        
    print(f"Successfully inserted {total} hadiths.")

def create_indexes(collection):
    """Create text indexes for search functionality."""
    print("Creating text indexes...")
    try:
        # Create text index for search
        collection.create_index(
            [('text_arabic', TEXT), ('text_english', TEXT)],
            name='search_index'
        )
        
        # Create unique index for hadith_id
        collection.create_index(
            'hadith_id',
            name='hadith_id_index',
            unique=True
        )
        
        # Create index for source_book
        collection.create_index(
            'source_book',
            name='book_index'
        )
        
        # Create index for hadith_number
        collection.create_index(
            'hadith_number',
            name='hadith_number_index'
        )
        
        print("Indexes created successfully.")
    except Exception as e:
        print(f"Error creating indexes: {e}")
        print("Some indexes might already exist. Continuing with the rest of the script...")

def main():
    # Configuration
    JSON_FILE = 'kutub_al_sittah_ara_fixed_v1__20251129_0951.json'
    
    # Connect to MongoDB
    collection = connect_to_mongodb()
    
    # Load and process data
    hadiths = load_json_data(JSON_FILE)
    print(f"Successfully loaded {len(hadiths)} hadiths from JSON file.")
    
    # Insert data in batches
    batch_insert(collection, hadiths)
    
    # Create indexes
    create_indexes(collection)
    
    # Print completion message
    print("\nDatabase seeding completed successfully!")
    print(f"Total hadiths in collection: {collection.count_documents({})}")

if __name__ == "__main__":
    main()
