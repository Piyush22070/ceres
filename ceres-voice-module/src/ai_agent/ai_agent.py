"""
This is Main Agent that orchestrates all components
"""

"""
Import Builtin libraries
"""
from typing import Dict,Optional,Tuple


"""
Import the Derived Libraries
"""
from src.exceptions.exceptions import AIServiceError
from src.utils.ApiResponse import ApiResponse
from src.ai_services.ai_service import AIService
from src.command_executor.command_detector import CommandDetector
from src.utils.response_cleaner import ResponseCleaner
from src.command_executor.command_executor import CommandExecutor
from src.utils.prompt_generator import PromptGenerator


class AIAgent:

    """
    Initialize the AIAgent 
    """
    def __init__(self,api_key:Optional[str]=None):
        """
        Initialize the AI Agent with all components
        
        Args:
            api_key: Optional API key for AI service
            
        Raises:
            ConfigurationError: If initialization fails
        """
        try:
            self.ai_service = AIService(api_key)
            print("Passed ai_service")
            self.command_detector = CommandDetector()
            print("Passed command_detector")
            self.response_cleaner = ResponseCleaner()
            print("Passed response_cleaner")
            
            self.executor = CommandExecutor()
            print("Passed executor")
            self.prompt_generator = PromptGenerator()
            print("Passed prompt_generator")
            
            print("App Initiated")
        except Exception as e:
            print("Failed Initiation")

    

    def execute_command(self,user_request:str)->Dict:

        """
        Main execution method with comprehensive error handling
        
        Args:
            user_request: Natural language request from user
            
        Returns:
            Dictionary with execution results and messages
        """

        try:

            # gets the use Prompt
            if not user_request.strip():
                return  ApiResponse.error("Command Empty !")
            

            # Get the inhance Prompt
            prompt = self.prompt_generator.get_enhanced_prompt(user_request)


            # Generate the conent wiht Ai
            try:
                response_text = self.ai_service.generate_content(prompt)
            except AIServiceError as e:
                return ApiResponse.error("AI service error")
            
            # IF no response is generated
            if not response_text:
                return ApiResponse.error("No Command Generated from AI")
            
            #Clean Command and chekc for safety
            clean_command = self.response_cleaner.sanitize_response(response_text)
            
            if not clean_command:
                return ApiResponse.error("Invalid command generated")
            

            # Check for apple script or shell command
            command_type = self.command_detector.detect_command_type(clean_command, user_request)

            if command_type == 'applescript':
                clean_command = self.response_cleaner.enhance_applescript_command(clean_command, user_request)

            # Final Execution
            return self.executor.execute(clean_command, command_type)
        
        except Exception as e:
            return ApiResponse.error("Unexpected Error while Executing")
        

    
    def test_test_functionality(self) -> Dict:
        return {"messages": [{"text": "This Functionality is Under Work", "type": "bot"}]}

    def get_system_info(self) -> Dict:
        return {"messages": [{"text": "This Functionality is Under Work", "type": "bot"}]}

    def execute_visual_command(self, user_request: str, screenshot_data: Optional[str] = None) -> Dict:
        return {"messages": [{"text": "This Functionality is Under Work", "type": "bot"}]}

    def take_screenshot(self, region: Optional[Tuple[int,int,int]] = None) -> Dict:
        return {"messages": [{"text": "This Functionality is Under Work", "type": "bot"}]}

    def analyze_screenshot(self, screenshot_data: str, user_request: str) -> Dict:
        return {"messages": [{"text": "This Functionality is Under Work", "type": "bot"}]}

    def execute_with_feedback(self, user_request: str, max_attempts: int = 3) -> Dict:
        return {"messages": [{"text": "This Functionality is Under Work", "type": "bot"}]}

    def find_and_click(self, target_description: str, screenshot_data: Optional[str] = None) -> Dict:
        return {"messages": [{"text": "This Functionality is Under Work", "type": "bot"}]}

    def get_visual_capabilities(self) -> Dict:
        return {"messages": [{"text": "This Functionality is Under Work", "type": "bot"}]}
