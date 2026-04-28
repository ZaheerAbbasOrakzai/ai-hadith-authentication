import json
import sys

def print_field(title, value, max_length=100):
    """Helper function to print field with value preview"""
    value_str = str(value)
    preview = value_str[:max_length] + ('...' if len(value_str) > max_length else '')
    print(f"\n{title}:")
    print("-" * (len(title) + 1))
    print(f"Type: {type(value).__name__}")
    print(f"Value: {preview}")
    if isinstance(value, dict):
        print(f"Keys: {', '.join(value.keys())}")
    elif isinstance(value, list):
        print(f"Length: {len(value)}")

def inspect_json_file(file_path):
    try:
        # Set console encoding to UTF-8
        sys.stdout.reconfigure(encoding='utf-8')
        
        print(f"Loading JSON file: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if not isinstance(data, list) or not data:
            print("Error: JSON file should contain a non-empty list of hadiths.")
            return
        
        first_hadith = data[0]
        total_hadiths = len(data)
        
        print("\n" + "="*50)
        print(f"TOTAL HADITHS IN FILE: {total_hadiths:,}")
        print("="*50)
        
        print("\n=== HADITH STRUCTURE ===")
        print("\nField names in each hadith:")
        for i, key in enumerate(first_hadith.keys(), 1):
            print(f"{i}. {key}")
        
        print("\n=== SAMPLE HADITH ===")
        for key, value in first_hadith.items():
            print_field(f"Field: {key}", value)
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in the file.")
    except Exception as e:
        print(f"An error occurred: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    json_file = "kutub_al_sittah_ara_fixed_v1__20251129_0951.json"
    inspect_json_file(json_file)
