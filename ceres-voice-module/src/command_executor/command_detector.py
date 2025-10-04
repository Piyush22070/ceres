"""
Command type detection module for determining AppleScript vs Shell execution.
"""

from src.configs.configs import Config

class CommandDetector:
     
     @staticmethod
     def detect_command_type(command: str, user_request: str)->str:
          
        """
            Intelligently detect if command should be AppleScript or shell
            comman
            Args:
                command: The generated command
                user_request: The original user request
                
            Returns:
                'applescript' or 'shell'
        """
        command_lower = command.lower()
        request_lower = user_request.lower()


        if any(indicator in command_lower for indicator in Config.APPLESCRIPT_INDICATORS):
            return 'applescript'
        

        if any(indicator in request_lower for indicator in Config.REQUEST_INDICATORS):
            return 'applescript'
        

        # Check for GUI-related keywords in the request
        gui_keywords = [
            'click', 'button', 'window', 'dialog', 'notification',
            'screenshot', 'volume', 'mute', 'browser', 'tab',
            'email', 'message', 'app', 'application'
        ]

        if any(keyword in request_lower for keyword in gui_keywords):
            return 'applescript'


        # Check for shell-specific patterns
        shell_patterns = [
            'ls', 'cd', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'grep',
            'find', 'ps', 'kill', 'git', 'npm', 'pip', 'brew'
        ]


        if any(pattern in command_lower for pattern in shell_patterns):
            return 'shell'
        

        #Default
        return 'shell'



    
