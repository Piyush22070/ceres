"""
Response cleaning and processing module.
"""
import re

class ResponseCleaner:
    @staticmethod
    def sanitize_response(response_text: str) -> str:
        """
        Enhanced response cleaning with better parsing
        
        Args:
            response_text: Raw response from AI
            
        Returns:
            Cleaned command text
        """
        text = response_text.strip()

        if not text:
            return ""
        

        # Remove markdown code blocks
        if '```' in text:
            code_block_pattern = r'```(?:[\w]*\n)?(.*?)```'
            match = re.search(code_block_pattern, text, re.DOTALL)
            if match:
                text = match.group(1).strip()

        # Normalize AI outputs like: osascript -e 'tell application "Calculator" to activate'
        osascript_match = re.match(r"^\s*osascript\s+-e\s+['\"](.+)['\"]\s*$", text)
        if osascript_match:
            text = osascript_match.group(1).strip()

        # Remove language identifiers at start
        first_line = text.split('\n', 1)[0].lower().strip()
        language_identifiers = ['bash', 'sh', 'zsh', 'applescript', 'python', 'shell', 'javascript', 'js']
       

        if first_line in language_identifiers:
                lines = text.split('\n', 1)
                if len(lines) > 1:
                    text = lines[1]

        # Clean up comments but preserve important AppleScript comments
        lines = text.splitlines()
        cleaned_lines = []
            
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                continue
                
            # Skip basic shell comments, but keep AppleScript structure
            if stripped.startswith('#') and 'applescript' not in stripped.lower():
                continue
                
            # Keep AppleScript comments that contain structural keywords
            if stripped.startswith('--'):
                applescript_keywords = ['tell', 'end', 'set', 'on', 'try', 'error']
                if not any(keyword in stripped.lower() for keyword in applescript_keywords):
                    continue
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
   
    @staticmethod
    def enhance_applescript_command(command: str, user_request: str) -> str:
        """
        Enhance AppleScript commands with better error handling and structure
        
        Args:
            command: The AppleScript command
            user_request: Original user request
            
        Returns:
            Enhanced AppleScript with error handling
        """
        # Don't add error handling if it already exists
        if any(keyword in command.lower() for keyword in ['try', 'on error', 'error']):
            return command
        
        # Add error handling wrapper for complex operations
        if len(command.splitlines()) > 1 or any(keyword in command.lower() for keyword in ['tell application', 'set', 'make']):
            enhanced = f"""try
    {command}
on error errMsg number errNum
    display dialog "Error " & errNum & ": " & errMsg buttons {{"OK"}} default button "OK"
end try"""
            return enhanced
        
        return command
    
    @staticmethod
    def validate_applescript_syntax(script: str) -> bool:
        """
        Basic AppleScript syntax validation
        
        Args:
            script: AppleScript to validate
            
        Returns:
            True if syntax appears valid
        """
        if not script.strip():
            return False
        
        # Check for basic AppleScript structure
        has_tell = 'tell' in script.lower()
        has_end = 'end' in script.lower()
        
        # If it has tell, it should have end
        if has_tell and not has_end:
            return False
        
        # Check for balanced quotes
        quote_count = script.count('"')
        if quote_count % 2 != 0:
            return False
        
        return True

