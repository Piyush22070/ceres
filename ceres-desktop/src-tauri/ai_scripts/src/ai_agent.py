"""
Main AI Agent class that orchestrates all components.
"""
import logging
from typing import Dict, Optional, Tuple
from .config import Config, setup_logging
from .exceptions import AIServiceError, CommandExecutionError, ConfigurationError
from .ai_service import AIService
from .command_detector import CommandDetector
from .response_cleaner import ResponseCleaner
from .executors import CommandExecutor
from .prompt_generator import PromptGenerator


#logger = setup_logging()


class AIAgent:
    """Main AI Agent that orchestrates command generation and execution"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Agent with all components
        
        Args:
            api_key: Optional API key for AI service
            
        Raises:
            ConfigurationError: If initialization fails
        """
        try:
            # Initialize components
            self.ai_service = AIService(api_key)
            self.command_detector = CommandDetector()
            self.response_cleaner = ResponseCleaner()
            self.executor = CommandExecutor()
            self.prompt_generator = PromptGenerator()
            
            #logger.info("AI Agent initialized successfully")
            
        except Exception as e:
           # logger.error(f"Failed to initialize AI Agent: {e}")
            raise ConfigurationError(f"AI Agent initialization failed: {e}")
    
    def execute_command(self, user_request: str) -> Dict:
        """
        Main execution method with comprehensive error handling
        
        Args:
            user_request: Natural language request from user
            
        Returns:
            Dictionary with execution results and messages
        """
        try:
           # logger.info(f"Processing request: {user_request}")
            
            if not user_request.strip():
                return {"messages": [{"text": "⚠️ Empty request provided", "type": "bot"}]}
            
            # Generate command using AI
            prompt = self.prompt_generator.get_enhanced_prompt(user_request)
            
            try:
                response_text = self.ai_service.generate_content(prompt)
            except AIServiceError as e:
               # logger.error(f"AI generation failed: {e}")
                return {"messages": [{"text": f"⚠️ AI service error: {str(e)}", "type": "bot"}]}
            
            if not response_text:
                return {"messages": [{"text": "⚠️ No command generated", "type": "bot"}]}
            
            # Clean and process the response
            clean_command = self.response_cleaner.sanitize_response(response_text)
            
            if not clean_command:
                return {"messages": [{"text": "⚠️ Invalid command generated", "type": "bot"}]}
            
           # logger.info(f"Generated command: {clean_command[:100]}...")
            
            # Detect command type and execute
            command_type = self.command_detector.detect_command_type(clean_command, user_request)
            
            # Enhance AppleScript commands if needed
            if command_type == 'applescript':
                clean_command = self.response_cleaner.enhance_applescript_command(clean_command, user_request)
            
            # Execute the command
            return self.executor.execute(clean_command, command_type)
            
        except Exception as e:
           # logger.error(f"Command execution failed: {e}")
            return {"messages": [{"text": f"⚠️ Unexpected error: {str(e)}", "type": "bot"}]}
    
    def test_functionality(self) -> Dict:
        """
        Test basic functionality of all components
        
        Returns:
            Dictionary with test results
        """
        test_results = []
        
        # Test AI service connection
        try:
            if self.ai_service.test_connection():
                test_results.append("✅ AI Service: OK")
            else:
                test_results.append("❌ AI Service: Connection failed")
        except Exception as e:
            test_results.append(f"❌ AI Service: {e}")
        
        # Test shell command execution
        try:
            result = self.executor.execute("echo 'Shell test successful'", "shell")
            if "successful" in str(result).lower():
                test_results.append("✅ Shell Execution: OK")
            else:
                test_results.append("❌ Shell Execution: Failed")
        except Exception as e:
            test_results.append(f"❌ Shell Execution: {e}")
        
        # Test AppleScript execution
        try:
            simple_script = 'display dialog "Test successful" buttons {"OK"} default button "OK"'
            result = self.executor.execute(simple_script, "applescript")
            test_results.append("✅ AppleScript Execution: OK")
        except Exception as e:
            test_results.append(f"❌ AppleScript Execution: {e}")
        
        # Test command detection
        try:
            cmd_type = self.command_detector.detect_command_type("tell application", "open app")
            if cmd_type == "applescript":
                test_results.append("✅ Command Detection: OK")
            else:
                test_results.append("❌ Command Detection: Failed")
        except Exception as e:
            test_results.append(f"❌ Command Detection: {e}")
        
        return {"messages": [{"text": "\n".join(test_results), "type": "bot"}]}
    
    def get_system_info(self) -> Dict:
        """
        Get system information and configuration status
        
        Returns:
            Dictionary with system information
        """
        try:
            ai_info = self.ai_service.get_model_info()
            
            info = [
                "🤖 AI Agent System Information",
                "=" * 35,
                f"AI Model: {ai_info.get('model_name', 'Unknown')}",
                f"Provider: {ai_info.get('provider', 'Unknown')}",
                f"API Key: {'✅ Configured' if ai_info.get('api_key_configured') else '❌ Missing'}",
                f"Connection: {'✅ Working' if ai_info.get('connection_status') else '❌ Failed'}",
                f"Command Timeout: {Config.COMMAND_TIMEOUT}s",
                f"Security Patterns: {len(Config.DANGEROUS_PATTERNS)} active",
                f"Supported Apps: {len(Config.APP_BUNDLE_IDS)} configured"
            ]
            
            return {"messages": [{"text": "\n".join(info), "type": "bot"}]}
            
        except Exception as e:
            return {"messages": [{"text": f"⚠️ Failed to get system info: {str(e)}", "type": "bot"}]}
    
    def execute_visual_command(self, user_request: str, screenshot_data: Optional[str] = None) -> Dict:
        """
        Execute visual automation command based on screenshots
        
        Args:
            user_request: Natural language request
            screenshot_data: Optional base64 screenshot data
            
        Returns:
            Dictionary with execution results
        """
        try:
            return self.visual_executor.execute_visual_command(user_request, screenshot_data)
        except Exception as e:
            #logger.error(f"Visual command execution failed: {e}")
            return {"messages": [{"text": f"⚠️ Visual execution failed: {str(e)}", "type": "bot"}]}
    
    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict:
        """
        Take a screenshot
        
        Args:
            region: Optional (left, top, width, height) region
            
        Returns:
            Dictionary with screenshot data
        """
        try:
            return self.visual_executor.visual_automation.take_screenshot(region)
        except Exception as e:
            #logger.error(f"Screenshot capture failed: {e}")
            return {"messages": [{"text": f"⚠️ Screenshot failed: {str(e)}", "type": "bot"}]}
    
    def analyze_screenshot(self, screenshot_data: str, user_request: str) -> Dict:
        """
        Analyze screenshot with AI
        
        Args:
            screenshot_data: Base64 screenshot data
            user_request: User's request
            
        Returns:
            Dictionary with analysis results
        """
        try:
            return self.visual_executor.screenshot_analyzer.analyze_screenshot(screenshot_data, user_request)
        except Exception as e:
          #  logger.error(f"Screenshot analysis failed: {e}")
            return {"messages": [{"text": f"⚠️ Analysis failed: {str(e)}", "type": "bot"}]}
    
    def execute_with_feedback(self, user_request: str, max_attempts: int = 3) -> Dict:
        """
        Execute command with visual feedback loop
        
        Args:
            user_request: Natural language request
            max_attempts: Maximum number of attempts
            
        Returns:
            Dictionary with execution results
        """
        try:
            return self.visual_executor.execute_with_feedback_loop(user_request, max_attempts)
        except Exception as e:
           # logger.error(f"Feedback execution failed: {e}")
            return {"messages": [{"text": f"⚠️ Feedback execution failed: {str(e)}", "type": "bot"}]}
    
    def find_and_click(self, target_description: str, screenshot_data: Optional[str] = None) -> Dict:
        """
        Find and click on UI element
        
        Args:
            target_description: Description of what to click
            screenshot_data: Optional screenshot data
            
        Returns:
            Dictionary with execution results
        """
        try:
            return self.visual_executor.find_and_click(target_description, screenshot_data)
        except Exception as e:
           # logger.error(f"Find and click failed: {e}")
            return {"messages": [{"text": f"⚠️ Find and click failed: {str(e)}", "type": "bot"}]}
    
    def get_visual_capabilities(self) -> Dict:
        """
        Get visual automation capabilities
        
        Returns:
            Dictionary with capability information
        """
        try:
            return self.visual_executor.get_visual_capabilities()
        except Exception as e:
            #logger.error(f"Get visual capabilities failed: {e}")
            return {"messages": [{"text": f"⚠️ Failed to get capabilities: {str(e)}", "type": "bot"}]}