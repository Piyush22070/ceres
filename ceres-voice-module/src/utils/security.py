"""
Security validation module for command execution.
"""
import re
import shlex
from src.configs.configs import Config
from src.exceptions.exceptions import SecurityError


class SecurityValidator:
    """Handles security validation for commands"""
    
    def __init__(self):
        """Initialize security validator with patterns"""
        print("Passed till  Security Constructer")

        self.danger_regex = re.compile('|'.join(Config.DANGEROUS_PATTERN), re.IGNORECASE)

        print("Passed Security Constructer")
    
    def validate_command(self, command: str) -> None:
        """
        Check if command contains potentially dangerous operations
        
        Args:
            command: The command string to validate
            
        Raises:
            SecurityError: If dangerous patterns are detected
        """
        if self.danger_regex.search(command):
            raise SecurityError(f"Potentially dangerous command detected: {command}")
        
        # Additional checks for file operations on system directories
        if any(pattern in command.lower() for pattern in ['/system/', '/usr/bin/', '/etc/']):
            if any(op in command.lower() for op in ['rm', 'del', 'delete', 'format']):
                raise SecurityError(f"Attempt to modify system files detected: {command}")
    
    @staticmethod
    def escape_applescript_string(text: str) -> str:
        """
        Properly escape strings for AppleScript
        
        Args:
            text: The text to escape
            
        Returns:
            Escaped text wrapped in quotes
        """
        # Escape quotes and backslashes
        text = text.replace('\\', '\\\\')
        text = text.replace('"', '\\"')
        return f'"{text}"'
    
    @staticmethod
    def escape_shell_argument(arg: str) -> str:
        """
        Safely escape shell arguments
        
        Args:
            arg: The argument to escape
            
        Returns:
            Properly escaped shell argument
        """
        return shlex.quote(arg)
    
    def is_safe_path(self, path: str) -> bool:
        """
        Check if a path is safe to operate on
        
        Args:
            path: The file path to check
            
        Returns:
            True if path is safe, False otherwise
        """
        dangerous_paths = ['/system', '/usr/bin', '/etc', '/boot', '/dev']
        normalized_path = path.lower().strip()
        
        return not any(dangerous_path in normalized_path for dangerous_path in dangerous_paths)