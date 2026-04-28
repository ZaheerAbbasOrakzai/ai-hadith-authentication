import re
import json
from pymongo import MongoClient
from tqdm import tqdm

def normalize_arabic_text(text):
    """
    Normalize Arabic text for searching:
    1. Remove tashkeel (vowels)
    2. Convert Alif variants (أ إ آ) to simple Alif (ا)
    3. Convert ta marbuta (ة) to ha (ه)
    4. Remove extra whitespace
    """
    if not isinstance(text, str):
        return ""
    
    # Define normalization mappings
    tashkeel_chars = 'ًٌٍَُِّّْـ'  # Common diacritics
    alif_variants = 'أإآ'  # Alif with hamza
    ta_marbuta = 'ة'  # Ta marbuta
    
    # Step 1: Remove tashkeel (diacritics)
    # This includes fatha, damma, kasra, sukun, shadda, tanween, etc.
    text = re.sub(r'[\u064B-\u065F\u0670]', '', text)
    
    # Step 2: Convert Alif variants to simple Alif
    alif_mapping = {
        'أ': 'ا',
        'إ': 'ا', 
        'آ': 'ا'
    }
    for variant, simple in alif_mapping.items():
        text = text.replace(variant, simple)
    
    # Step 3: Convert ta marbuta to ha
    text = text.replace('ة', 'ه')
    
    # Step 4: Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def process_json_dataset(input_file, output_file):
    """
    Process the JSON dataset and add search_text field to each hadith
    """
    print(f"Loading dataset from {input_file}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        hadiths = json.load(f)
    
    print(f"Processing {len(hadiths)} hadiths...")
    
    processed_hadiths = []
    
    for hadith in tqdm(hadiths):
        # Create a copy to avoid modifying original
        processed_hadith = hadith.copy()
        
        # Add search_text field with normalized Arabic text
        if 'text_ar' in hadith and hadith['text_ar']:
            processed_hadith['search_text'] = normalize_arabic_text(hadith['text_ar'])
        else:
            processed_hadith['search_text'] = ""
        
        processed_hadiths.append(processed_hadith)
    
    # Save the processed dataset
    print(f"Saving processed dataset to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_hadiths, f, ensure_ascii=False, indent=2)
    
    print(f"Dataset processed successfully! {len(processed_hadiths)} hadiths updated.")
    
    return processed_hadiths

def update_mongodb_with_search_text(processed_hadiths):
    """
    Update MongoDB collection with search_text field
    """
    print("Connecting to MongoDB...")
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['AI_Hadith_DB']
    hadiths_collection = db.hadiths
    
    print(f"Updating {len(processed_hadiths)} hadiths in MongoDB...")
    
    updated_count = 0
    
    for hadith in tqdm(processed_hadiths):
        # Use hadith_id as the unique identifier
        if 'hadith_id' in hadith:
            result = hadiths_collection.update_one(
                {'hadith_id': hadith['hadith_id']},
                {'$set': {'search_text': hadith['search_text']}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
    
    print(f"Successfully updated {updated_count} hadiths in MongoDB!")
    
    client.close()

if __name__ == "__main__":
    # File paths
    input_json = "kutub_al_sittah_ara_fixed_v1__20251129_0951.json"
    output_json = "kutub_al_sittah_with_search_text.json"
    
    # Process the dataset
    processed_hadiths = process_json_dataset(input_json, output_json)
    
    # Update MongoDB
    update_mongodb_with_search_text(processed_hadiths)
    
    print("\n=== Task completed successfully! ===")
    print("1. Arabic text normalization function created")
    print("2. JSON dataset processed with search_text field")
    print("3. MongoDB collection updated with search_text field")
    print("4. Ready to update app.py search function")
