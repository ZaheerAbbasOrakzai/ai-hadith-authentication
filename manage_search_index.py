from pymongo import MongoClient, ASCENDING, TEXT
from pymongo.errors import OperationFailure

def manage_search_text_index():
    """
    Manage text index for search_text field - either update existing or create new one
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
        
        print("\nCurrent indexes in hadiths collection:")
        for index in existing_indexes:
            print(f"  - Name: {index['name']}")
            print(f"    Keys: {index['key']}")
            if 'weights' in index:
                print(f"    Weights: {index['weights']}")
            print()
        
        # Option 1: Drop the existing search_index and create a new one with search_text
        print("Dropping existing search_index...")
        try:
            hadiths_collection.drop_index("search_index")
            print("✅ Existing search_index dropped successfully")
        except Exception as e:
            print(f"Could not drop search_index: {e}")
        
        # Create new text index with search_text included
        print("Creating new comprehensive text index...")
        index_result = hadiths_collection.create_index([
            ("search_text", TEXT),
            ("text_ar", TEXT),
            ("text_en", TEXT),
            ("book", TEXT)
        ], name="comprehensive_search_index", weights={
            "search_text": 10,  # Highest priority for normalized search text
            "text_ar": 5,       # Medium priority for original Arabic
            "text_en": 3,       # Lower priority for English
            "book": 1           # Lowest priority for book names
        })
        
        print(f"✅ New index created successfully! Index name: {index_result}")
        
        # Verify the new index
        print("\nVerifying new index creation...")
        updated_indexes = hadiths_collection.list_indexes()
        
        print("\nUpdated indexes in hadiths collection:")
        for index in updated_indexes:
            print(f"  - Name: {index['name']}")
            print(f"    Keys: {index['key']}")
            if 'weights' in index:
                print(f"    Weights: {index['weights']}")
            print()
        
        # Test the index with sample searches
        print("Testing search performance with new index...")
        import time
        
        # Test 1: Search using text search (with index)
        start_time = time.time()
        results_text = list(hadiths_collection.find(
            {"$text": {"$search": "السلام"}},
            {"score": {"$meta": "textScore"}}
        ).sort([("score", {"$meta": "textScore"})]).limit(3))
        
        text_search_time = (time.time() - start_time) * 1000
        
        # Test 2: Search using regex (without text index)
        start_time = time.time()
        results_regex = list(hadiths_collection.find(
            {"search_text": {"$regex": "السلام", "$options": "i"}}
        ).limit(3))
        
        regex_search_time = (time.time() - start_time) * 1000
        
        print(f"\nPerformance Comparison:")
        print(f"  Text Index Search: {text_search_time:.2f}ms (found {len(results_text)} results)")
        print(f"  Regex Search: {regex_search_time:.2f}ms (found {len(results_regex)} results)")
        print(f"  Performance Improvement: {((regex_search_time - text_search_time) / regex_search_time * 100):.1f}%")
        
        if results_text:
            print("\nSample result from text search:")
            result = results_text[0]
            print(f"  Hadith ID: {result.get('hadith_id', 'N/A')}")
            print(f"  Book: {result.get('book', 'N/A')}")
            print(f"  Search Text Preview: {result.get('search_text', '')[:100]}...")
            print(f"  Text Score: {result.get('score', 'N/A')}")
        
        client.close()
        print("\n✅ Text index management completed successfully!")
        
    except OperationFailure as e:
        print(f"❌ MongoDB operation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error managing index: {e}")
        return False
    
    return True

if __name__ == "__main__":
    manage_search_text_index()
