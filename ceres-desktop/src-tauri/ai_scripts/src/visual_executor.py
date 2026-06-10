"""
Visual command executor that combines PyAutoGUI actions with AI analysis.
"""
import json
import re
import time
# import logging
from typing import Dict, List, Optional, Tuple, Any
from .visual_automation import VisualAutomation
from .screenshot_analyzer import ScreenshotAnalyzer
from .ai_service import AIService
from .exceptions import CommandExecutionError


# logger = logging.getLogger(__name__)


class VisualExecutor:
    """Executes visual automation commands based on screenshots and AI analysis"""
    
    def __init__(self, ai_service: AIService):
        """
        Initialize visual executor
        
        Args:
            ai_service: AIService instance for AI analysis
        """
        self.visual_automation = VisualAutomation()
        self.screenshot_analyzer = ScreenshotAnalyzer(ai_service)
        self.ai_service = ai_service
        
    def execute_visual_command(self, user_request: str, screenshot_data: Optional[str] = None) -> Dict:
        """
        Execute a visual automation command based on user request and optional screenshot
        
        Args:
            user_request: Natural language request
            screenshot_data: Optional base64 screenshot data
            
        Returns:
            Dictionary with execution results
        """
        try:
            # logger.info(f"Processing visual command: {user_request}")
            
            # Take screenshot if not provided
            if not screenshot_data:
                screenshot_result = self.visual_automation.take_screenshot()
                if "screenshot_data" in screenshot_result:
                    screenshot_data = screenshot_result["screenshot_data"]["image_data"]
                else:
                    return {"messages": [{"text": "⚠️ Failed to capture screenshot", "type": "bot"}]}
            
            # Analyze screenshot and generate action plan
            analysis_result = self.screenshot_analyzer.analyze_screenshot(screenshot_data, user_request)
            
            # Parse the analysis to extract actionable commands
            action_commands = self._extract_action_commands(analysis_result.get("analysis", ""))
            
            if not action_commands:
                return {
                    "messages": [{
                        "text": f"🔍 Analysis completed but no specific actions identified.\n{analysis_result.get('analysis', '')}",
                        "type": "bot"
                    }],
                    "analysis": analysis_result.get("analysis", "")
                }
            
            # Execute the commands
            execution_results = []
            for command in action_commands:
                result = self._execute_single_command(command)
                execution_results.append(result)
                
                # Add small delay between commands
                time.sleep(0.5)
            
            # Summarize results
            success_count = sum(1 for r in execution_results if "✅" in str(r.get("messages", [])))
            total_commands = len(execution_results)
            
            summary = f"🤖 Visual Automation Complete: {success_count}/{total_commands} commands executed successfully"
            
            return {
                "messages": [{"text": summary, "type": "bot"}],
                "execution_results": execution_results,
                "analysis": analysis_result.get("analysis", ""),
                "commands_executed": action_commands
            }
            
        except Exception as e:
            # logger.error(f"Visual command execution failed: {e}")
            return {"messages": [{"text": f"⚠️ Visual execution failed: {str(e)}", "type": "bot"}]}
    
    def execute_with_feedback_loop(self, user_request: str, max_attempts: int = 3) -> Dict:
        """
        Execute visual command with feedback loop - take screenshot, analyze, act, verify
        
        Args:
            user_request: Natural language request
            max_attempts: Maximum number of attempts
            
        Returns:
            Dictionary with execution results
        """
        try:
            results = []
            
            for attempt in range(max_attempts):
                # logger.info(f"Visual execution attempt {attempt + 1}/{max_attempts}")
                
                # Take screenshot
                screenshot_result = self.visual_automation.take_screenshot()
                if "screenshot_data" not in screenshot_result:
                    return {"messages": [{"text": "⚠️ Failed to capture screenshot", "type": "bot"}]}
                
                screenshot_data = screenshot_result["screenshot_data"]["image_data"]
                
                # Analyze current state
                analysis = self.screenshot_analyzer.analyze_screenshot(screenshot_data, user_request)
                
                # Check if goal is already achieved
                if self._is_goal_achieved(analysis.get("analysis", ""), user_request):
                    return {
                        "messages": [{"text": f"✅ Goal achieved in {attempt + 1} attempt(s)", "type": "bot"}],
                        "attempts": attempt + 1,
                        "final_analysis": analysis.get("analysis", "")
                    }
                
                # Execute actions
                execution_result = self.execute_visual_command(user_request, screenshot_data)
                results.append({
                    "attempt": attempt + 1,
                    "screenshot": screenshot_data,
                    "analysis": analysis.get("analysis", ""),
                    "execution": execution_result
                })
                
                # Wait for UI to update
                time.sleep(1.0)
            
            return {
                "messages": [{"text": f"⚠️ Goal not achieved after {max_attempts} attempts", "type": "bot"}],
                "attempts": max_attempts,
                "results": results
            }
            
        except Exception as e:
            # logger.error(f"Feedback loop execution failed: {e}")
            return {"messages": [{"text": f"⚠️ Feedback loop failed: {str(e)}", "type": "bot"}]}
    
    def find_and_click(self, target_description: str, screenshot_data: Optional[str] = None) -> Dict:
        """
        Find and click on a specific UI element
        
        Args:
            target_description: Description of what to click
            screenshot_data: Optional screenshot data
            
        Returns:
            Dictionary with execution results
        """
        try:
            if not screenshot_data:
                screenshot_result = self.visual_automation.take_screenshot()
                if "screenshot_data" in screenshot_result:
                    screenshot_data = screenshot_result["screenshot_data"]["image_data"]
                else:
                    return {"messages": [{"text": "⚠️ Failed to capture screenshot", "type": "bot"}]}
            
            # Generate click coordinates
            coord_result = self.screenshot_analyzer.generate_click_coordinates(screenshot_data, target_description)
            
            # Extract coordinates if provided in the analysis
            coordinates = self._extract_coordinates_from_analysis(coord_result.get("suggestions", ""))
            
            if coordinates:
                # Click at the suggested coordinates
                click_result = self.visual_automation.click_coordinates(coordinates[0], coordinates[1])
                return click_result
            else:
                return {
                    "messages": [{
                        "text": f"🔍 Could not determine coordinates for '{target_description}'.\n{coord_result.get('suggestions', '')}",
                        "type": "bot"
                    }]
                }
                
        except Exception as e:
            # logger.error(f"Find and click failed: {e}")
            return {"messages": [{"text": f"⚠️ Find and click failed: {str(e)}", "type": "bot"}]}
    
    def execute_automation_plan(self, plan_text: str) -> Dict:
        """
        Execute a detailed automation plan
        
        Args:
            plan_text: Text containing automation plan with commands
            
        Returns:
            Dictionary with execution results
        """
        try:
            commands = self._extract_action_commands(plan_text)
            
            if not commands:
                return {"messages": [{"text": "⚠️ No executable commands found in plan", "type": "bot"}]}
            
            results = []
            for i, command in enumerate(commands):
                # logger.info(f"Executing step {i+1}/{len(commands)}: {command}")
                result = self._execute_single_command(command)
                results.append(result)
                
                # Wait between commands
                time.sleep(0.5)
            
            success_count = sum(1 for r in results if "✅" in str(r.get("messages", [])))
            
            return {
                "messages": [{
                    "text": f"🤖 Automation plan executed: {success_count}/{len(commands)} steps successful",
                    "type": "bot"
                }],
                "results": results,
                "total_steps": len(commands),
                "successful_steps": success_count
            }
            
        except Exception as e:
            # logger.error(f"Automation plan execution failed: {e}")
            return {"messages": [{"text": f"⚠️ Plan execution failed: {str(e)}", "type": "bot"}]}
    
    def _extract_action_commands(self, analysis_text: str) -> List[Dict]:
        """
        Extract actionable commands from AI analysis text
        
        Args:
            analysis_text: AI analysis containing suggested actions
            
        Returns:
            List of command dictionaries
        """
        commands = []
        
        # Look for common command patterns
        patterns = {
            'click': r'click\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)',
            'type': r'type(?:_text)?\s*\(\s*["\']([^"\']*)["\'\s*\)',
            'key': r'(?:key_press|press)\s*\(\s*["\']([^"\']*)["\'\s*\)',
            'scroll': r'scroll\s*\(\s*(-?\d+)\s*\)',
            'drag': r'drag\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)',
            'wait': r'(?:wait|sleep|delay)\s*\(\s*(\d+(?:\.\d+)?)\s*\)'
        }
        
        lines = analysis_text.split('\n')
        
        for line in lines:
            line = line.strip().lower()
            
            for command_type, pattern in patterns.items():
                matches = re.findall(pattern, line)
                for match in matches:
                    if command_type == 'click':
                        commands.append({
                            'type': 'click',
                            'x': int(match[0]),
                            'y': int(match[1])
                        })
                    elif command_type == 'type':
                        commands.append({
                            'type': 'type',
                            'text': match if isinstance(match, str) else match[0]
                        })
                    elif command_type == 'key':
                        commands.append({
                            'type': 'key',
                            'key': match if isinstance(match, str) else match[0]
                        })
                    elif command_type == 'scroll':
                        commands.append({
                            'type': 'scroll',
                            'clicks': int(match if isinstance(match, str) else match[0])
                        })
                    elif command_type == 'drag':
                        commands.append({
                            'type': 'drag',
                            'start_x': int(match[0]),
                            'start_y': int(match[1]),
                            'end_x': int(match[2]),
                            'end_y': int(match[3])
                        })
                    elif command_type == 'wait':
                        commands.append({
                            'type': 'wait',
                            'duration': float(match if isinstance(match, str) else match[0])
                        })
        
        return commands
    
    def _execute_single_command(self, command: Dict) -> Dict:
        """
        Execute a single visual automation command
        
        Args:
            command: Command dictionary
            
        Returns:
            Dictionary with execution results
        """
        try:
            cmd_type = command.get('type', '').lower()
            
            if cmd_type == 'click':
                return self.visual_automation.click_coordinates(command['x'], command['y'])
            
            elif cmd_type == 'type':
                return self.visual_automation.type_text(command['text'])
            
            elif cmd_type == 'key':
                return self.visual_automation.send_key(command['key'])
            
            elif cmd_type == 'scroll':
                return self.visual_automation.scroll(command['clicks'])
            
            elif cmd_type == 'drag':
                return self.visual_automation.drag_and_drop(
                    (command['start_x'], command['start_y']),
                    (command['end_x'], command['end_y'])
                )
            
            elif cmd_type == 'wait':
                time.sleep(command['duration'])
                return {"messages": [{"text": f"✅ Waited {command['duration']} seconds", "type": "bot"}]}
            
            else:
                return {"messages": [{"text": f"⚠️ Unknown command type: {cmd_type}", "type": "bot"}]}
                
        except Exception as e:
            # logger.error(f"Single command execution failed: {e}")
            return {"messages": [{"text": f"⚠️ Command failed: {str(e)}", "type": "bot"}]}
    
    def _extract_coordinates_from_analysis(self, analysis_text: str) -> Optional[Tuple[int, int]]:
        """
        Extract coordinates from analysis text
        
        Args:
            analysis_text: AI analysis text
            
        Returns:
            Tuple of (x, y) coordinates or None
        """
        # Look for coordinate patterns
        coord_patterns = [
            r'coordinates?\s*[:\-]?\s*\(?(\d+)\s*,\s*(\d+)\)?',
            r'click\s+at\s*[:\-]?\s*\(?(\d+)\s*,\s*(\d+)\)?',
            r'position\s*[:\-]?\s*\(?(\d+)\s*,\s*(\d+)\)?',
            r'\(?(\d+)\s*,\s*(\d+)\)?\s*(?:pixels?|px)?'
        ]
        
        for pattern in coord_patterns:
            matches = re.findall(pattern, analysis_text.lower())
            if matches:
                try:
                    x, y = int(matches[0][0]), int(matches[0][1])
                    # Validate coordinates are reasonable (not negative, not too large)
                    if 0 <= x <= 5000 and 0 <= y <= 5000:
                        return (x, y)
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def _is_goal_achieved(self, analysis_text: str, user_request: str) -> bool:
        """
        Determine if the goal has been achieved based on analysis
        
        Args:
            analysis_text: Current analysis text
            user_request: Original user request
            
        Returns:
            True if goal appears to be achieved
        """
        # Look for success indicators in the analysis
        success_indicators = [
            'goal achieved', 'task completed', 'successfully completed',
            'objective met', 'finished', 'done', 'complete'
        ]
        
        analysis_lower = analysis_text.lower()
        return any(indicator in analysis_lower for indicator in success_indicators)
    
    def get_visual_capabilities(self) -> Dict:
        """
        Get information about visual automation capabilities
        
        Returns:
            Dictionary with capability information
        """
        try:
            screen_info = self.visual_automation.get_screen_size()
            mouse_info = self.visual_automation.get_mouse_position()
            
            capabilities = [
                "🖱️ Mouse Operations:",
                "  - Click at coordinates",
                "  - Right-click, double-click, middle-click",
                "  - Drag and drop",
                "  - Mouse movement",
                "",
                "⌨️ Keyboard Operations:",
                "  - Type text",
                "  - Send key presses",
                "  - Keyboard shortcuts",
                "",
                "📸 Screenshot Operations:",
                "  - Full screen capture",
                "  - Region capture", 
                "  - Screenshot history",
                "  - Image annotation",
                "",
                "🔍 AI Analysis:",
                "  - Screenshot analysis",
                "  - UI element identification",
                "  - Action planning",
                "  - Coordinate suggestion",
                "",
                "🤖 Automation Features:",
                "  - Feedback loops",
                "  - Multi-step execution",
                "  - Error recovery",
                "  - Progress tracking"
            ]
            
            return {
                "messages": [{
                    "text": "🤖 Visual Automation Capabilities:\n\n" + "\n".join(capabilities),
                    "type": "bot"
                }],
                "screen_info": screen_info,
                "mouse_info": mouse_info
            }
            
        except Exception as e:
            # logger.error(f"Get capabilities failed: {e}")
            return {"messages": [{"text": f"⚠️ Failed to get capabilities: {str(e)}", "type": "bot"}]} 