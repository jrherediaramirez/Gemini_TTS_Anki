import sys
import os
from pathlib import Path

# Add lib to path
addon_dir = Path(__file__).parent.parent
lib_path = addon_dir / "lib"
if str(lib_path) not in sys.path:
    sys.path.insert(0, str(lib_path))

try:
    from google import genai
    import requests
except ImportError as e:
    print(f"Import error: {e}")
    genai = None
    requests = None

class GeminiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = None
        if genai and api_key:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception as e:
                print(f"Failed to initialize Gemini client: {e}")
    
    def test_connection(self):
        """Test if API key works"""
        if not self.client:
            return False, "Client not initialized"
        
        try:
            # Simple test request
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents="Say 'Hello' in one word only."
            )
            return True, "Connection successful"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"
    
    def generate_text(self, prompt, model="gemini-2.5-flash"):
        """Generate text using Gemini"""
        if not self.client:
            return None, "Client not initialized"
        
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response.text, None
        except Exception as e:
            return None, f"Text generation failed: {str(e)}"
    
    def generate_tts_request(self, text):
        """Prepare TTS request (placeholder for future implementation)"""
        # Note: Direct TTS via Gemini API requires Live API WebSocket
        # This is a placeholder for HTTP-based TTS requests
        return f"TTS request prepared for: {text[:50]}..."
