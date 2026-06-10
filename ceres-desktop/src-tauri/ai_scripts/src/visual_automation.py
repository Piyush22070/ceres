"""
Visual automation module using PyAutoGUI for screenshot-based actions.
"""
import pyautogui
import cv2
import numpy as np
import base64
import io
import time
# import logging
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path
from .config import Config
from .exceptions import CommandExecutionError
from .security import SecurityValidator


# logger = logging.getLogger(__name__)


class VisualAutomation:
    """Handles screenshot-based automation using PyAutoGUI"""
    
    def __init__(self):
        """Initialize visual automation with safety settings"""
        # PyAutoGUI safety settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.5  # Pause between actions
        
        self.security_validator = SecurityValidator()
        self.screenshot_history = []
        self.max_history = 10
        
        # Confidence thresholds for image matching
        self.confidence_threshold = 0.8
        self.ocr_confidence_threshold = 60
        
        # logger.info("Visual automation initialized")
    
    def take_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict:
        """
        Take a screenshot of the entire screen or specific region
        
        Args:
            region: (left, top, width, height) tuple for specific region
            
        Returns:
            Dictionary with screenshot data and metadata
        """
        try:
            if region:
                screenshot = pyautogui.screenshot(region=region)
            else:
                screenshot = pyautogui.screenshot()
            
            # Convert to base64 for storage/transmission
            buffer = io.BytesIO()
            screenshot.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            # Store in history
            screenshot_data = {
                'timestamp': time.time(),
                'image_data': img_base64,
                'region': region,
                'size': screenshot.size
            }
            
            self.screenshot_history.append(screenshot_data)
            if len(self.screenshot_history) > self.max_history:
                self.screenshot_history.pop(0)
            
            return {
                "messages": [{
                    "text": f"✅ Screenshot captured ({screenshot.size[0]}x{screenshot.size[1]})",
                    "type": "bot"
                }],
                "screenshot_data": screenshot_data
            }
            
        except Exception as e:
            # logger.error(f"Screenshot capture failed: {e}")
            return {"messages": [{"text": f"⚠️ Screenshot failed: {str(e)}", "type": "bot"}]}
    
    def find_image_on_screen(self, template_path: str, confidence: float = None) -> Optional[Tuple[int, int, int, int]]:
        """
        Find an image on screen using template matching
        
        Args:
            template_path: Path to template image
            confidence: Confidence threshold (0.0 to 1.0)
            
        Returns:
            (left, top, width, height) tuple if found, None otherwise
        """
        try:
            confidence = confidence or self.confidence_threshold
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            
            # Try to locate the image
            try:
                box = pyautogui.locateOnScreen(template_path, confidence=confidence)
                if box:
                    return box
            except pyautogui.ImageNotFoundException:
                pass
            
            return None
            
        except Exception as e:
            logger.error(f"Image search failed: {e}")
            return None
    
    def click_image(self, template_path: str, confidence: float = None, 
                   click_type: str = 'left', offset: Tuple[int, int] = (0, 0)) -> Dict:
        """
        Click on an image found on screen
        
        Args:
            template_path: Path to template image
            confidence: Confidence threshold
            click_type: 'left', 'right', 'double', or 'middle'
            offset: (x, y) offset from image center
            
        Returns:
            Dictionary with operation results
        """
        try:
            box = self.find_image_on_screen(template_path, confidence)
            
            if not box:
                return {"messages": [{"text": f"⚠️ Image not found: {template_path}", "type": "bot"}]}
            
            # Calculate click position
            click_x = box.left + box.width // 2 + offset[0]
            click_y = box.top + box.height // 2 + offset[1]
            
            # Perform click
            if click_type == 'right':
                pyautogui.rightClick(click_x, click_y)
            elif click_type == 'double':
                pyautogui.doubleClick(click_x, click_y)
            elif click_type == 'middle':
                pyautogui.middleClick(click_x, click_y)
            else:  # default left click
                pyautogui.click(click_x, click_y)
            
            return {"messages": [{"text": f"✅ Clicked on image at ({click_x}, {click_y})", "type": "bot"}]}
            
        except Exception as e:
            # logger.error(f"Image click failed: {e}")
            return {"messages": [{"text": f"⚠️ Click failed: {str(e)}", "type": "bot"}]}
    
    def click_coordinates(self, x: int, y: int, click_type: str = 'left') -> Dict:
        """
        Click at specific coordinates
        
        Args:
            x: X coordinate
            y: Y coordinate
            click_type: Type of click ('left', 'right', 'double', 'middle')
            
        Returns:
            Dictionary with operation results
        """
        try:
            # Validate coordinates are within screen bounds
            screen_width, screen_height = pyautogui.size()
            
            if not (0 <= x <= screen_width and 0 <= y <= screen_height):
                return {"messages": [{"text": f"⚠️ Coordinates out of bounds: ({x}, {y})", "type": "bot"}]}
            
            # Perform click
            if click_type == 'right':
                pyautogui.rightClick(x, y)
            elif click_type == 'double':
                pyautogui.doubleClick(x, y)
            elif click_type == 'middle':
                pyautogui.middleClick(x, y)
            else:
                pyautogui.click(x, y)
            
            return {"messages": [{"text": f"✅ Clicked at coordinates ({x}, {y})", "type": "bot"}]}
            
        except Exception as e:
            logger.error(f"Coordinate click failed: {e}")
            return {"messages": [{"text": f"⚠️ Click failed: {str(e)}", "type": "bot"}]}
    
    def drag_and_drop(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int], 
                     duration: float = 1.0) -> Dict:
        """
        Drag from start position to end position
        
        Args:
            start_pos: (x, y) start coordinates
            end_pos: (x, y) end coordinates
            duration: Duration of drag operation in seconds
            
        Returns:
            Dictionary with operation results
        """
        try:
            pyautogui.drag(start_pos[0], start_pos[1], 
                          end_pos[0] - start_pos[0], 
                          end_pos[1] - start_pos[1], 
                          duration=duration)
            
            return {"messages": [{"text": f"✅ Dragged from {start_pos} to {end_pos}", "type": "bot"}]}
            
        except Exception as e:
            # logger.error(f"Drag and drop failed: {e}")
            return {"messages": [{"text": f"⚠️ Drag failed: {str(e)}", "type": "bot"}]}
    
    def type_text(self, text: str, interval: float = 0.01) -> Dict:
        """
        Type text at current cursor position
        
        Args:
            text: Text to type
            interval: Interval between keystrokes
            
        Returns:
            Dictionary with operation results
        """
        try:
            # Security check for text content
            if len(text) > 1000:
                return {"messages": [{"text": "⚠️ Text too long (max 1000 chars)", "type": "bot"}]}
            
            pyautogui.typewrite(text, interval=interval)
            return {"messages": [{"text": f"✅ Typed text: {text[:50]}{'...' if len(text) > 50 else ''}", "type": "bot"}]}
            
        except Exception as e:
            # logger.error(f"Text typing failed: {e}")
            return {"messages": [{"text": f"⚠️ Typing failed: {str(e)}", "type": "bot"}]}
    
    def send_key(self, key: str, presses: int = 1) -> Dict:
        """
        Send keyboard key presses
        
        Args:
            key: Key to press (e.g., 'enter', 'tab', 'ctrl', 'cmd', etc.)
            presses: Number of times to press the key
            
        Returns:
            Dictionary with operation results
        """
        try:
            # Validate key name
            valid_keys = [
                'enter', 'return', 'tab', 'space', 'backspace', 'delete',
                'shift', 'ctrl', 'alt', 'cmd', 'command', 'option',
                'up', 'down', 'left', 'right', 'home', 'end', 'pageup', 'pagedown',
                'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
                'escape', 'esc', 'capslock', 'numlock', 'scrolllock', 'insert',
                'printscreen', 'pause', 'menu', 'winleft', 'winright'
            ]
            
            if key.lower() not in valid_keys and len(key) != 1:
                return {"messages": [{"text": f"⚠️ Invalid key: {key}", "type": "bot"}]}
            
            for _ in range(presses):
                pyautogui.press(key)
                time.sleep(0.1)  # Small delay between presses
            
            return {"messages": [{"text": f"✅ Pressed '{key}' {presses} time(s)", "type": "bot"}]}
            
        except Exception as e:
            # logger.error(f"Key press failed: {e}")
            return {"messages": [{"text": f"⚠️ Key press failed: {str(e)}", "type": "bot"}]}
    
    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> Dict:
        """
        Scroll at current mouse position or specified coordinates
        
        Args:
            clicks: Number of scroll clicks (positive = up, negative = down)
            x: X coordinate (optional)
            y: Y coordinate (optional)
            
        Returns:
            Dictionary with operation results
        """
        try:
            if x is not None and y is not None:
                pyautogui.scroll(clicks, x=x, y=y)
                return {"messages": [{"text": f"✅ Scrolled {clicks} clicks at ({x}, {y})", "type": "bot"}]}
            else:
                pyautogui.scroll(clicks)
                return {"messages": [{"text": f"✅ Scrolled {clicks} clicks", "type": "bot"}]}
            
        except Exception as e:
            # logger.error(f"Scroll failed: {e}")
            return {"messages": [{"text": f"⚠️ Scroll failed: {str(e)}", "type": "bot"}]}
    
    def get_mouse_position(self) -> Dict:
        """
        Get current mouse position
        
        Returns:
            Dictionary with mouse coordinates
        """
        try:
            x, y = pyautogui.position()
            return {
                "messages": [{"text": f"🖱️ Mouse position: ({x}, {y})", "type": "bot"}],
                "coordinates": {"x": x, "y": y}
            }
            
        except Exception as e:
            # logger.error(f"Get mouse position failed: {e}")
            return {"messages": [{"text": f"⚠️ Failed to get mouse position: {str(e)}", "type": "bot"}]}
    
    def move_mouse(self, x: int, y: int, duration: float = 1.0) -> Dict:
        """
        Move mouse to specific coordinates
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            duration: Duration of movement in seconds
            
        Returns:
            Dictionary with operation results
        """
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return {"messages": [{"text": f"✅ Moved mouse to ({x}, {y})", "type": "bot"}]}
            
        except Exception as e:
            # logger.error(f"Mouse movement failed: {e}")
            return {"messages": [{"text": f"⚠️ Mouse movement failed: {str(e)}", "type": "bot"}]}
    
    def get_screen_size(self) -> Dict:
        """
        Get screen dimensions
        
        Returns:
            Dictionary with screen size information
        """
        try:
            width, height = pyautogui.size()
            return {
                "messages": [{"text": f"📺 Screen size: {width}x{height}", "type": "bot"}],
                "screen_size": {"width": width, "height": height}
            }
            
        except Exception as e:
            # logger.error(f"Get screen size failed: {e}")
            return {"messages": [{"text": f"⚠️ Failed to get screen size: {str(e)}", "type": "bot"}]}
    
    def find_text_on_screen(self, text: str, screenshot_data: Optional[str] = None) -> Dict:
        """
        Find text on screen using OCR (requires additional setup)
        Note: This is a placeholder - would need pytesseract for full OCR functionality
        
        Args:
            text: Text to search for
            screenshot_data: Optional base64 screenshot data
            
        Returns:
            Dictionary with search results
        """
        try:
            # This would require OCR implementation
            # For now, return a placeholder response
            return {"messages": [{"text": "⚠️ OCR text search not implemented yet", "type": "bot"}]}
            
        except Exception as e:
            # logger.error(f"Text search failed: {e}")
            return {"messages": [{"text": f"⚠️ Text search failed: {str(e)}", "type": "bot"}]}
    
    def annotate_screenshot(self, screenshot_data: str, annotations: List[Dict]) -> Dict:
        """
        Add annotations (rectangles, text) to a screenshot
        
        Args:
            screenshot_data: Base64 encoded screenshot
            annotations: List of annotation dictionaries
            
        Returns:
            Dictionary with annotated screenshot
        """
        try:
            # Decode base64 image
            img_bytes = base64.b64decode(screenshot_data)
            img = Image.open(io.BytesIO(img_bytes))
            draw = ImageDraw.Draw(img)
            
            # Add annotations
            for annotation in annotations:
                if annotation.get('type') == 'rectangle':
                    coords = annotation.get('coordinates', [])
                    if len(coords) == 4:
                        draw.rectangle(coords, outline='red', width=2)
                
                elif annotation.get('type') == 'text':
                    position = annotation.get('position', (10, 10))
                    text = annotation.get('text', '')
                    draw.text(position, text, fill='red')
            
            # Convert back to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            annotated_base64 = base64.b64encode(buffer.getvalue()).decode()
            
            return {
                "messages": [{"text": "✅ Screenshot annotated", "type": "bot"}],
                "annotated_screenshot": annotated_base64
            }
            
        except Exception as e:
            # logger.error(f"Screenshot annotation failed: {e}")
            return {"messages": [{"text": f"⚠️ Annotation failed: {str(e)}", "type": "bot"}]}
    
    def get_screenshot_history(self) -> Dict:
        """
        Get recent screenshot history
        
        Returns:
            Dictionary with screenshot history
        """
        try:
            history_info = []
            for i, screenshot in enumerate(self.screenshot_history):
                history_info.append(f"Screenshot {i+1}: {screenshot['size']} at {time.ctime(screenshot['timestamp'])}")
            
            return {
                "messages": [{"text": f"📸 Screenshot History ({len(self.screenshot_history)} items):\n" + "\n".join(history_info), "type": "bot"}],
                "history": self.screenshot_history
            }
            
        except Exception as e:
            # logger.error(f"Get screenshot history failed: {e}")
            return {"messages": [{"text": f"⚠️ Failed to get history: {str(e)}", "type": "bot"}]}