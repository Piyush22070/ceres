"""
AI service integration module for Google Gemini API.
"""
from typing import Optional
from ..configs.configs import Config
import google.generativeai as genai
from src.exceptions.exceptions import AIServiceError, ConfigurationError 


class AIService:
    """Handles AI service integration and content generation"""

    def __init__(self, api_key:Optional[str]=None):
        """
        Initialize AI service with API configuration
        
        Args:
            api_key: Optional API key, will use environment variable if not provided
            
        Raises:
            ConfigurationError: If API key is not available or configuration fails
        """

        try:
            self.api_key = Config.get_api_key(api_key)
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        except ValueError as e:
            raise ConfigurationError(str(e))

        except Exception as e:
            raise ConfigurationError(f"AI service initialization failed: {e}") 
       
    def generate_content(self,prompt:str) ->str:
        """
        Generate content using the AI model
        
        Args:
            prompt: The prompt to send to the AI
            
        Returns:
            Generated content as string
            
        Raises:
            AIServiceError: If content generation fails
        """
        try:
            if not prompt.strip():
                raise AIServiceError("Empty prompt provided")
        
            response = self.model.generate_content(prompt)

            if not response or not response.text:
                raise AIServiceError("Empty response from AI service")
            
            content = response.text.strip()

            return content
        
        except Exception as e:
            raise AIServiceError(f"Failed to generate content: {str(e)}")

    def test_connection(self) -> bool:
        """
        Test AI service connection
        
        Returns:
            True if connection is working, False otherwise
        """
        try:
            test_prompt = "Respond with 'Connection successful' if you receive this message."
            response = self.generate_content(test_prompt)
            return "successful" in response.lower()
            
        except Exception as e:
            #logger.error(f"AI service connection test failed: {e}")
            return False
    
    def get_model_info(self) -> dict:
        """
        Get information about the current AI model
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": "gemini-2.0-flash",
            "provider": "Google Generative AI",
            "api_key_configured": bool(self.api_key),
            "connection_status": self.test_connection()
        }