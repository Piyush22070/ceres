"""
AI prompt generation module for creating enhanced prompts.
"""


class PromptGenerator:
    """Generates comprehensive prompts for AI command generation"""
    
    @staticmethod
    def get_enhanced_prompt(user_request: str) -> str:
        """
        Generate comprehensive prompt for command generation
        
        Args:
            user_request: The user's natural language request
            
        Returns:
            Enhanced prompt for AI
        """
        return f"""
You are an expert macOS automation assistant. Convert this natural language request into executable commands.

USER REQUEST: {user_request}

CRITICAL REQUIREMENTS:
1. OUTPUT ONLY the raw command - no explanations, markdown, or JSON
2. Choose between AppleScript (GUI) or Shell (CLI) based on the task
3. Handle ALL edge cases properly

FOR APPLESCRIPT (GUI tasks):
- Use proper syntax: tell application "Name"...end tell
- Handle spaces in file paths: POSIX file "/path/with spaces/file.txt"
- Escape quotes in strings: "He said \\"Hello\\""
- Use delay statements for timing: delay 0.5
- Handle URLs: open location "https://example.com"
- Email automation: proper recipient/subject/content structure
- Window/tab management: tell front window, make new tab
- Error handling: try...on error...end try blocks
- Bundle IDs: use proper app bundle IDs when needed

FOR SHELL COMMANDS (CLI tasks):
- Properly quote paths with spaces: "file with spaces.txt"
- Chain commands safely: command1 && command2
- Handle special characters with proper escaping
- Use full paths when needed: /usr/bin/command
- Git operations: proper branch/remote handling
- File operations: check existence before acting
- Network commands: timeout and error handling
- Python/script execution: proper argument passing

COMMON EDGE CASES TO HANDLE:
- File/folder names with spaces, special chars, unicode
- Network timeouts and failures
- Application not running/installed
- Permission issues
- Multiple monitors/windows
- Clipboard operations
- System preferences access
- Background/foreground app states
- URL encoding for web searches
- Email addresses with + or . characters
- Time zones and date formatting
- Large file operations
- Concurrent operations

EXAMPLES:
Request: "Send email to john@test.com with subject Test"
AppleScript:
tell application "Mail"
    set newMessage to make new outgoing message with properties {{subject:"Test", visible:true}}
    tell newMessage
        make new to recipient at end of to recipients with properties {{address:"john@test.com"}}
        send
    end tell
end tell

Request: "Create folder named 'My Files' on desktop"
Shell: mkdir -p "$HOME/Desktop/My Files"

Request: "Open Chrome and search for python tutorials"
AppleScript:
tell application "Google Chrome"
    activate
    open location "https://www.google.com/search?q=python%20tutorials"
end tell

TASK: Generate the command for: {user_request}
"""
    
    @staticmethod
    def get_test_prompt() -> str:
        """Generate prompt for testing functionality"""
        return """
Generate a simple test command that will work on macOS.
Choose either:
1. A simple shell command like 'echo "test successful"'
2. A simple AppleScript like 'display dialog "test successful" buttons {"OK"}'

Output only the command, no explanations.
"""