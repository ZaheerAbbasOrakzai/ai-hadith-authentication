from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import OperationFailure

def create_search_text_index():
    """
    Create a text index on the search_text field in the hadiths collection
    to improve search performance for Arabic text searches.
    """
    try:
        # Connect to MongoDB
        print("Connecting to MongoDB...")
        client = MongoClient('mongodb://localhost:27017/')
        db = client['AI_Hadith_DB']
        hadiths_collection = db.hadiths
        
        # Check existing indexes
        print("Checking existing indexes...")
        existing_indexes = hadiths_collection.list_indexes()
        index_names = [index['name'] for index in existing_indexes]
        print(f"Existing indexes: {index_names}")
        
        # Create text index on search_text field
        print("Creating text index on search_text field...")
        
        # Option 1: Simple text index on search_text only
        index_result = hadiths_collection.create_index([
            ("search_text", TEXT)
        ], name="search_text_index")
        
        print(f"Index created successfully! Index name: {index_result}")
        
        # Verify the index was created
        print("\nVerifying index creation...")
        updated_indexes = hadiths_collection.list_indexes()
        
        print("\nAll indexes in hadiths collection:")
        for index in updated_indexes:
            print(f"  - Name: {index['name']}")
            print(f"    Keys: {index['key']}")
            if 'weights' in index:
                print(f"    Weights: {index['weights']}")
            print()
        
        # Test the index with a sample search
        print("Testing search performance with index...")
        import time
        
        start_time = time.time()
        results = list(hadiths_collection.find(
            {"$text": {"$search": "السلام"}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(5))
        
        end_time = time.time()
        
        print(f"Found {len(results)} results in {(end_time - start_time)*1000:.2f}ms")
        if results:
            print("Sample result:")
            print(f"  Hadith ID: {results[0].get('hadith_id', 'N/A')}")
            print(f"  Search Text Preview: {results[0].get('search_text', '')[:100]}...")
        
        client.close()
        print("\n✅ Text index created and verified successfully!")
        
    except OperationFailure as e:
        print(f"❌ MongoDB operation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating index: {e}")
        return False
    
    return True

if __name__ == "__main__":
    create_search_text_index()
