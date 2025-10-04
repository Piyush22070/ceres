"""
Custom exceptions for the AI Agent application.
"""


class SecurityError(Exception):
    """Raised when a potentially dangerous command is detected"""
    pass


class AIServiceError(Exception):
    """Raised when AI service fails to generate content"""
    pass


class CommandExecutionError(Exception):
    """Raised when command execution fails"""
    pass


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing"""
    pass