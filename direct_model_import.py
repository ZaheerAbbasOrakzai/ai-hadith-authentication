#!/usr/bin/env python3
"""
Direct Model Import for AI Hadith Authenticator
This shows how to import and use the model directly without Hugging Face Spaces
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

class DirectHadithModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
    def load_model(self, model_path="abbasorakzai777/ai-hadith-authentication/final_model"):
        """Load model directly from Hugging Face Hub"""
        try:
            print(f"Loading model from: {model_path}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            print("Tokenizer loaded successfully")
            
            # Load model
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            self.model.to(self.device)
            self.model.eval()
            print("Model loaded successfully")
            
            return True
            
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def predict(self, text, lang_mode="auto"):
        """Make prediction using the loaded model"""
        if not self.model or not self.tokenizer:
            return None
            
        try:
            # Preprocess text
            inputs = self.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            )
            
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Make prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                
            # Get predicted class and confidence
            predicted_class = torch.argmax(predictions, dim=-1).item()
            confidence = torch.max(predictions, dim=-1)[0].item()
            
            # Map class to grade
            grade_mapping = {0: "Sahih", 1: "Hasan", 2: "Da'if", 3: "Mawdu'", 4: "Not classified"}
            grade = grade_mapping.get(predicted_class, "Not classified")
            
            # Format result to match Hugging Face API
            result = [
                grade,                    # Grade
                f"{confidence*100:.1f}%", # Confidence
                "Direct model prediction", # Warning
                "Chain verification needed", # Isnad
                "Direct AI model analysis"   # Source
            ]
            
            return result
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

# Alternative: Local model loading
def load_local_model(model_folder="./hadith_model"):
    """Load model from local folder"""
    if os.path.exists(model_folder):
        print(f"Loading local model from: {model_folder}")
        model = DirectHadithModel()
        if model.load_model(model_folder):
            return model
    return None

# Usage example
if __name__ == "__main__":
    # Initialize model
    hadith_model = DirectHadithModel()
    
    # Try to load from Hugging Face
    if hadith_model.load_model():
        print("Model loaded successfully!")
        
        # Test prediction
        test_text = "Prophet Muhammad said: Actions are judged by intentions"
        result = hadith_model.predict(test_text, "auto")
        
        if result:
            print(f"Prediction result: {result}")
        else:
            print("Prediction failed")
    else:
        print("Failed to load model")
        
        # Try local fallback
        local_model = load_local_model()
        if local_model:
            print("Using local model instead")
