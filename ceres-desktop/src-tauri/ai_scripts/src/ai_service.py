"""
AI service integration module for Google Gemini API.
"""
import logging
from typing import Optional
from google import genai
from .config import Config
from .exceptions import AIServiceError, ConfigurationError

class AIService:
    """Handles AI service integration and content generation"""
    
    def __init__(self, api_key: Optional[str] = None):
        try:
            self.api_key = Config.get_api_key(api_key)
            self.client = genai.Client(api_key=self.api_key)
            self.model_name = "gemini-2.5-flash"
            
        except ValueError as e:
            raise ConfigurationError(str(e))
        except Exception as e:
            raise ConfigurationError(f"AI service initialization failed: {e}")
    
    def generate_content(self, prompt: str) -> str:
        try:
            if not prompt.strip():
                raise AIServiceError("Empty prompt provided")
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            
            if not response or not response.text:
                raise AIServiceError("Empty response from AI service")
            
            return response.text.strip()
            
        except Exception as e:
            raise AIServiceError(f"Failed to generate content: {str(e)}")
    
    def test_connection(self) -> bool:
        try:
            test_prompt = "Respond with 'Connection successful' if you receive this message."
            response = self.generate_content(test_prompt)
            return "successful" in response.lower()
        except Exception:
            return False
    
    def get_model_info(self) -> dict:
        return {
            "model_name": self.model_name,
            "provider": "Google Generative AI",
            "api_key_configured": bool(self.api_key),
            "connection_status": self.test_connection()
        }
