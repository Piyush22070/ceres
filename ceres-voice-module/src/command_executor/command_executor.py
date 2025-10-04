"""
Command execution module for AppleScript and shell commands.
"""
import subprocess
import tempfile
import os
import shlex
from typing import Dict
from src.configs.configs import Config
from src.utils.security import SecurityValidator
from src.utils.response_cleaner import ResponseCleaner
from src.exceptions.exceptions import SecurityError



class AppleScriptExecutor:
    """Handles AppleScript execution"""
    
    def __init__(self):
        self.response_cleaner = ResponseCleaner()
    
    def execute(self, script: str) -> Dict:
        """
        Execute AppleScript with enhanced error handling
        
        Args:
            script: AppleScript code to execute
            
        Returns:
            Dictionary with execution results
        """
        try:
            # Validate script
            if not script.strip():
                return {"messages": [{"text": "Empty AppleScript provided", "type": "bot"}]}
            
            if not self.response_cleaner.validate_applescript_syntax(script):
                return {"messages": [{"text": "Invalid AppleScript syntax", "type": "bot"}]}
            
            # Create temporary file for complex scripts
            with tempfile.NamedTemporaryFile(mode='w', suffix='.scpt', delete=False) as f:
                f.write(script)
                temp_path = f.name
            
            try:
                # Execute via osascript with timeout
                result = subprocess.run(
                    ['osascript', temp_path],
                    capture_output=True,
                    text=True,
                    timeout=Config.COMMAND_TIMEOUT
                )
                
                if result.returncode == 0:
                    output = result.stdout.strip() or "AppleScript executed successfully"
                    return {"messages": [{"text": output, "type": "bot"}]}
                else:
                    error_msg = result.stderr.strip()
                    return self._handle_applescript_error(error_msg)
                    
            finally:
                # Clean up temp file
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass
                    
        except subprocess.TimeoutExpired:
            return {"messages": [{"text": f"AppleScript timed out ({Config.COMMAND_TIMEOUT}s limit)", "type": "bot"}]}
        except Exception as e:
            # logger.error(f"AppleScript execution error: {e}")
            return {"messages": [{"text": f"AppleScript execution failed: {str(e)}", "type": "bot"}]}
    
    def _handle_applescript_error(self, error_msg: str) -> Dict:
        """Handle AppleScript-specific errors"""
        if "execution error" in error_msg.lower():
            return {"messages": [{"text": f"AppleScript Error: {error_msg}", "type": "bot"}]}
        elif "application isn't running" in error_msg.lower():
            return {"messages": [{"text": "Target application is not running", "type": "bot"}]}
        elif "can't get" in error_msg.lower():
            return {"messages": [{"text": " AppleScript couldn't access the requested element", "type": "bot"}]}
        else:
            return {"messages": [{"text": f"Script failed: {error_msg}", "type": "bot"}]}

class ShellExecutor:
    """Handles shell command execution"""
    
    def __init__(self):
        print("Reached Security Validator ")
        self.security_validator = SecurityValidator()
        
    
    def execute(self, command: str) -> Dict:
        """
        Execute shell command with enhanced security and error handling
        
        Args:
            command: Shell command to execute
            
        Returns:
            Dictionary with execution results
        """
        try:
            # Security validation
            self.security_validator.validate_command(command)
            
            # Execute command based on complexity
            result = self._run_command(command)
            
            if result.returncode == 0:
                output = result.stdout.strip() or "Command executed successfully"
                return {"messages": [{"text": output, "type": "bot"}]}
            else:
                error_output = result.stderr.strip()
                return {"messages": [{"text": f"Command failed (exit {result.returncode}): {error_output}", "type": "bot"}]}
                
        except SecurityError as e:

            return {"messages": [{"text": f"🛡️ Security: {str(e)}", "type": "bot"}]}
        except subprocess.TimeoutExpired:
            return {"messages": [{"text": f" Command timed out ({Config.COMMAND_TIMEOUT}s limit)", "type": "bot"}]}
        except FileNotFoundError as e:
            return {"messages": [{"text": f"Command not found: {str(e)}", "type": "bot"}]}
        except Exception as e:

            return {"messages": [{"text": f"Execution failed: {str(e)}", "type": "bot"}]}
    
    def _run_command(self, command: str) -> subprocess.CompletedProcess:
        """
        Run shell command with appropriate method based on complexity
        
        Args:
            command: Command to execute
            
        Returns:
            CompletedProcess result
        """
        # Expand ~ and environment variables like $HOME
        command = os.path.expandvars(os.path.expanduser(command))
        # For complex commands with pipes, redirections, etc., use shell=True
        if any(char in command for char in ['|', '&&', '||', ';', '>', '<', '`', '$(']):
            return subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=Config.COMMAND_TIMEOUT,
                cwd=Config.get_home_directory()
            )
        else:
            # For simple commands, split and use shell=False (more secure)
            cmd_parts = shlex.split(command)
            return subprocess.run(
                cmd_parts,
                capture_output=True,
                text=True,
                timeout=Config.COMMAND_TIMEOUT,
                cwd=Config.get_home_directory()
            )

class CommandExecutor:
    """Main command executor that delegates to appropriate executor"""
    
    def __init__(self):
        print("Reached Command executor")
        self.applescript_executor = AppleScriptExecutor()
        print("Passed AppleExectore")
        self.shell_executor = ShellExecutor()
        print("Passed Shell Ecextore")
    
    def execute(self, command: str, command_type: str) -> Dict:
        """
        Execute command using appropriate executor
        
        Args:
            command: Command to execute
            command_type: 'applescript' or 'shell'
            
        Returns:
            Dictionary with execution results
        """
        try:
            if command_type == 'applescript':
                return self.applescript_executor.execute(command)
            elif command_type == 'shell':
                return self.shell_executor.execute(command)
            else:
                return {"messages": [{"text": f"⚠️ Unknown command type: {command_type}", "type": "bot"}]}
        
        except Exception as e:
            return {"messages": [{"text": f"⚠️ Execution failed: {str(e)}", "type": "bot"}]}