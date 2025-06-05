import sys
import os
from pathlib import Path

# Add lib to path
addon_dir = Path(__file__).parent.parent
lib_path = addon_dir / "lib"
if str(lib_path) not in sys.path:
    sys.path.insert(0, str(lib_path))

print(f"GeminiTTS Debug: Attempting to import requests for HTTP API.")

try:
    import requests
    import json
    print("GeminiTTS Debug: requests imported successfully!")
except Exception as e:
    print(f"GeminiTTS Error: Failed to import requests: {e}")
    requests = None

class GeminiClient:
    def __init__(self, api_key):
        print(f"GeminiTTS Debug: GeminiClient.__init__ called. API key present: {bool(api_key)}")
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
        self.configured = bool(api_key and requests)
        
        if self.configured:
            print("GeminiTTS Debug: Gemini HTTP client configured successfully")
        else:
            print("GeminiTTS Error: Gemini client not initialized - missing API key or requests")
    
    def test_connection(self):
        """Test if API key works using HTTP API"""
        print("GeminiTTS Debug: test_connection called (HTTP API).")
        
        if not self.configured:
            print("GeminiTTS Error: test_connection - Client not initialized.")
            return False, "Client not initialized"
        
        try:
            # Simple test request using HTTP API
            url = f"{self.base_url}/models/gemini-2.5-flash-preview-05-20:generateContent"
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            }
            
            payload = {
                "contents": [{
                    "parts": [{"text": "Say 'Hello' in one word only."}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 50
                }
            }
            
            print("GeminiTTS Debug: Making HTTP request to Gemini API...")
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            print(f"GeminiTTS Debug: HTTP response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("GeminiTTS Debug: test_connection - API call successful")
                return True, "Connection successful"
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"GeminiTTS Error: API call failed: {error_msg}")
                return False, f"API call failed: {error_msg}"
                
        except Exception as e:
            print(f"GeminiTTS Error: test_connection failed: {e}")
            return False, f"Connection failed: {str(e)}"
    
    def generate_text(self, prompt, model="gemini-2.5-flash-preview-05-20"):
        """Generate text using HTTP API"""
        print("GeminiTTS Debug: generate_text called (HTTP API).")
        
        if not self.configured:
            return None, "Client not initialized"
        
        try:
            url = f"{self.base_url}/models/{model}:generateContent"
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            }
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1024
                }
            }
            
            print("GeminiTTS Debug: Making text generation request...")
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                
                # Extract text from response
                if 'candidates' in result and len(result['candidates']) > 0:
                    candidate = result['candidates'][0]
                    if 'content' in candidate and 'parts' in candidate['content']:
                        text = candidate['content']['parts'][0].get('text', '')
                        if text:
                            print("GeminiTTS Debug: Text generation successful")
                            return text, None
                
                return None, "No text generated"
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"GeminiTTS Error: Text generation failed: {error_msg}")
                return None, error_msg
                
        except Exception as e:
            print(f"GeminiTTS Error: generate_text failed: {e}")
            return None, f"Text generation failed: {str(e)}"
    
    def generate_tts_request(self, text):
        """Prepare TTS request (placeholder for future implementation)"""
        return f"TTS request prepared for: {text[:50]}..."

    def generate_tts_audio(self, text, voice_name="en-US-Wavenet-D"):
        """Generate TTS audio using Google Cloud Text-to-Speech API"""
        print("GeminiTTS Debug: generate_tts_audio called (Google Cloud TTS).")

        if not self.configured:
            return None, "Client not initialized"

        try:
            # Google Cloud TTS API endpoint
            url = "https://texttospeech.googleapis.com/v1/text:synthesize"
            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key  # Same API key works for both services
            }

            payload = {
                "input": {"text": text},
                "voice": {
                    "languageCode": "en-US",
                    "name": voice_name
                },
                "audioConfig": {
                    "audioEncoding": "MP3"
                }
            }

            print("GeminiTTS Debug: Making TTS request to Google Cloud...")
            response = requests.post(url, headers=headers, json=payload, timeout=60)

            if response.status_code == 200:
                result = response.json()

                # Extract base64 audio data
                if 'audioContent' in result:
                    import base64
                    audio_data = base64.b64decode(result['audioContent'])
                    print("GeminiTTS Debug: TTS generation successful")
                    return audio_data, None
                else:
                    return None, "No audio content in response"
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                print(f"GeminiTTS Error: TTS generation failed: {error_msg}")
                return None, error_msg

        except Exception as e:
            print(f"GeminiTTS Error: generate_tts_audio failed: {e}")
            return None, f"TTS generation failed: {str(e)}"