"""
Configuration management for the AI Agent application.
"""
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
     """Configuration class for AI Agent"""
     
     # Security patterns for dangerous commands
     DANGEROUS_PATTERN =[
        r'sudo\s+rm\s+-rf\s*/',
        r'rm\s+-rf\s*/',
        r'format\s+',
        r'del\s+/[qfs]',
        r'diskutil\s+eraseVolume',
        r'dd\s+if=.*of=/dev/',
        r'chmod\s+777',
        r'curl.*\|\s*bash',
        r'wget.*\|\s*sh',
        r'eval\s*\$\(',
        r'exec\s*\(',
        r'system\s*\(',
        r'__import__\s*\(', 
     ]

     # macOS application bundle IDs
     APP_BUNDLE_IDS = {
        'chrome': 'com.google.Chrome',
        'safari': 'com.apple.Safari',
        'firefox': 'org.mozilla.firefox',
        'mail': 'com.apple.mail',
        'messages': 'com.apple.iChat',
        'finder': 'com.apple.finder',
        'terminal': 'com.apple.Terminal',
        'notes': 'com.apple.Notes',
        'calendar': 'com.apple.iCal',
        'music': 'com.apple.Music',
        'photos': 'com.apple.Photos'
    }
     # Command execution settings
     COMMAND_TIMEOUT = 30

    # AppleScript indicators
     APPLESCRIPT_INDICATORS = [
        'tell application', 'tell app', 'activate application',
        'click', 'type text', 'key code', 'keystroke',
        'display dialog', 'display notification', 'choose file',
        'open location', 'set volume', 'get clipboard'
    ]
    
    # Request indicators for AppleScript
     REQUEST_INDICATORS = [
        'open app', 'launch app', 'send email', 'create email',
        'take screenshot', 'set volume', 'mute', 'unmute',
        'open url', 'browse to', 'search in', 'type in',
        'click on', 'press key', 'show notification'
    ]
     
     @classmethod
     def get_api_key(cls,api_key :Optional[str] = None):
        """Get API key from parameter or environment"""
        # For testing
        key = api_key or os.getenv('GEMINI_API_KEY')
        if not key:
            raise ValueError("GEMINI_API_KEY not provided. Set environment variable or pass as parameter.")
        return key
     
     @classmethod 
     def get_home_directory(cls) ->str:
         """Get user home directory"""
         return os.path.expanduser('~')