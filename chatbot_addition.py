# --- SMART CHATBOT ADDITION ---
# Add this code to your app.py file before the final app.run() line

def get_relevant_hadiths(query, limit=5):
    """RAG Logic: Query MongoDB for relevant hadiths based on user query"""
    try:
        # Normalize the query for better Arabic matching
        normalized_query = normalize_arabic_text(query)
        
        # Build regex patterns
        regex_pattern = f'.*{re.escape(query)}.*'
        normalized_regex_pattern = f'.*{re.escape(normalized_query)}.*'
        
        # Search in multiple fields with priority
        query_filter = {
            '$or': [
                {'search_text': {'$regex': normalized_regex_pattern, '$options': 'i'}},  # Normalized Arabic
                {'text_arabic': {'$regex': regex_pattern, '$options': 'i'}},  # Original Arabic
                {'text_english': {'$regex': regex_pattern, '$options': 'i'}},  # English text
                {'source_book': {'$regex': regex_pattern, '$options': 'i'}},  # Book names
                {'chapter': {'$regex': regex_pattern, '$options': 'i'}}  # Chapters
            ]
        }
        
        # Get relevant hadiths with projection
        projection = {
            '_id': 0,
            'text_arabic': 1,
            'text_english': 1,
            'source_book': 1,
            'hadith_number': 1,
            'grade': 1,
            'chapter': 1
        }
        
        relevant_hadiths = list(hadiths_collection.find(query_filter, projection).limit(limit))
        
        # Format hadiths for context
        context_hadiths = []
        for hadith in relevant_hadiths:
            context_hadiths.append({
                'arabic': hadith.get('text_arabic', ''),
                'english': hadith.get('text_english', ''),
                'source': hadith.get('source_book', ''),
                'grade': hadith.get('grade', ''),
                'chapter': hadith.get('chapter', ''),
                'number': hadith.get('hadith_number', '')
            })
        
        return context_hadiths
        
    except Exception as e:
        print(f"RAG Error: {str(e)}")
        return []

@app.route('/chat', methods=['POST'])
@login_required
def chat():
    """Smart AI Chatbot with RAG and Gemini 1.5 Flash"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        print(f"🤖 User Message: {user_message}")
        
        # Step 1: Get relevant hadiths using RAG
        relevant_hadiths = get_relevant_hadiths(user_message, limit=5)
        print(f"📚 Found {len(relevant_hadiths)} relevant hadiths")
        
        # Step 2: Build context for Gemini
        context = ""
        if relevant_hadiths:
            context = "Relevant Hadiths from Database:\n\n"
            for i, hadith in enumerate(relevant_hadiths, 1):
                context += f"Hadith {i}:\n"
                context += f"Source: {hadith['source']}\n"
                context += f"Chapter: {hadith['chapter']}\n"
                context += f"Number: {hadith['number']}\n"
                context += f"Grade: {hadith['grade']}\n"
                context += f"Arabic: {hadith['arabic']}\n"
                context += f"English: {hadith['english']}\n\n"
        
        # Step 3: Generate response using Gemini
        if model:
            try:
                # System prompt for professional Islamic AI Assistant
                system_prompt = """You are a professional and respectful Islamic AI Assistant. Your goal is to provide authentic information about Islam, Hadiths, and Quran. Use the provided database context to answer accurately. If no relevant data is found in the context, use your general Islamic knowledge but always prioritize authenticity and avoid giving fatwas on complex legal matters. Be helpful, respectful, and provide balanced perspectives. Always mention your sources when possible."""
                
                # Prepare the full prompt
                full_prompt = f"{system_prompt}\n\nUser Question: {user_message}\n\n{context}\n\nPlease provide a helpful and accurate response based on the above context and your knowledge."
                
                # Generate response
                response = model.generate_content(full_prompt)
                ai_response = response.text
                
                print(f"✅ Gemini Response Generated")
                
                return jsonify({
                    'success': True,
                    'response': ai_response,
                    'sources_used': len(relevant_hadiths)
                })
                
            except Exception as e:
                print(f"❌ Gemini API Error: {str(e)}")
                return jsonify({
                    'success': False,
                    'error': 'I am unable to connect to my AI core. Please check your internet connection.'
                }), 500
        else:
            # Fallback response when Gemini is not available
            if relevant_hadiths:
                fallback_response = f"I found {len(relevant_hadiths)} relevant hadiths from our database, but I'm currently unable to process them with my AI. Here's one relevant hadith:\n\n{relevant_hadiths[0]['english']}\n\nSource: {relevant_hadiths[0]['source']}"
            else:
                fallback_response = "I apologize, but I'm currently unable to access my AI capabilities. Please try again later or search our hadith database directly."
            
            return jsonify({
                'success': True,
                'response': fallback_response,
                'sources_used': len(relevant_hadiths)
            })
            
    except Exception as e:
        print(f"❌ Chat Route Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'An error occurred while processing your request.'
        }), 500
