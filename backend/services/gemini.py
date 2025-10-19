import os
from dotenv import load_dotenv

load_dotenv()

def summarize_text(text: str) -> str:
    """
    Summarize text using Google Gemini API.
    Falls back to a simple summary if API key is missing.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        # Fallback for demo purposes
        sentences = text.split('.')[:3]
        return '. '.join(s.strip() for s in sentences if s.strip()) + '.'
    
    try:
        import google.generativeai as genai
        
        genai.configure(api_key=api_key)
        
        # Use the latest stable flash model (fast and efficient)
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        
        prompt = f"""Provide a concise 2-3 sentence summary of the following text:

{text[:2000]}

Summary:"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except ImportError:
        sentences = text.split('.')[:3]
        return '. '.join(s.strip() for s in sentences if s.strip()) + '. (Install google-generativeai for AI summaries)'
    except Exception as e:
        # Graceful fallback: return first 3 sentences
        sentences = text.split('.')[:3]
        return '. '.join(s.strip() for s in sentences if s.strip()) + '.'