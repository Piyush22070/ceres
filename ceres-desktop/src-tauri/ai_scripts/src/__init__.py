"""
AI Agent Package - macOS Automation Assistant

This package provides intelligent macOS automation through natural language commands.
It uses Google's Gemini AI to convert human requests into executable AppleScript or shell commands.

Main Components:
- AIAgent: Main orchestrator class
- AIService: Google Gemini API integration
- CommandExecutor: Handles command execution (AppleScript/Shell)
- SecurityValidator: Validates commands for safety
- ResponseCleaner: Cleans and processes AI responses

Usage:
    from ai_agent import AIAgent
    
    agent = AIAgent()
    result = agent.execute_command("open chrome and go to google.com")
    print(result)
"""

from .ai_agent import AIAgent
from .ai_service import AIService
from .config import Config, setup_logging
from .exceptions import (
    SecurityError,
    AIServiceError, 
    CommandExecutionError,
    ConfigurationError
)

__version__ = "1.0.0"
__author__ = "AI Agent Development Team"
__email__ = "contact@example.com"

__all__ = [
    "AIAgent",
    "AIService", 
    "Config",
    "setup_logging",
    "SecurityError",
    "AIServiceError",
    "CommandExecutionError", 
    "ConfigurationError"
]

# Package metadata
PACKAGE_INFO = {
    "name": "ai-agent",
    "version": __version__,
    "description": "Intelligent macOS automation through natural language",
    "author": __author__,
    "email": __email__,
    "requirements": [
        "google-generativeai>=0.3.0",
    ],
    "python_requires": ">=3.7",
    "platforms": ["macOS"],
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
        "Topic :: Desktop Environment :: Gnome"
    ]
}