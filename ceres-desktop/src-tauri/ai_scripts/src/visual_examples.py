#!/usr/bin/env python3
"""
Visual automation examples and usage demonstrations.
"""
import sys
import json
import time
from ai_agent import AIAgent


def example_basic_screenshot():
    """Example: Take a basic screenshot"""
    print("Example 1: Taking a screenshot")
    
    agent = AIAgent()
    result = agent.take_screenshot()
    
    print("Result:")
    print(json.dumps(result, indent=2))
    print("-" * 50)


def example_visual_analysis():
    """Example: Analyze screenshot and suggest actions"""
    print("Example 2: Visual analysis with action suggestions")
    
    agent = AIAgent()
    
    # Take screenshot first
    screenshot_result = agent.take_screenshot()
    
    if "screenshot_data" in screenshot_result:
        screenshot_data = screenshot_result["screenshot_data"]["image_data"]
        
        # Analyze with a specific request
        analysis_result = agent.analyze_screenshot(
            screenshot_data, 
            "Help me find and click the browser's address bar"
        )
        
        print("Analysis Result:")
        print(json.dumps(analysis_result, indent=2))
    
    print("-" * 50)


def example_find_and_click():
    """Example: Find and click on UI element"""
    print("Example 3: Find and click demonstration")
    
    agent = AIAgent()
    
    # This will take a screenshot and try to find/click the specified element
    result = agent.find_and_click("close button")
    
    print("Find and Click Result:")
    print(json.dumps(result, indent=2))
    print("-" * 50)


def example_visual_command_execution():
    """Example: Execute visual command with natural language"""
    print("Example 4: Visual command execution")
    
    agent = AIAgent()
    
    # Execute a natural language visual command
    result = agent.execute_visual_command("take a screenshot and find any text input fields")
    
    print("Visual Command Result:")
    print(json.dumps(result, indent=2))
    print("-" * 50)


def example_feedback_loop():
    """Example: Execute with feedback loop"""
    print("Example 5: Feedback loop execution")
    
    agent = AIAgent()
    
    # Execute with automatic feedback and retry
    result = agent.execute_with_feedback(
        "open the system preferences and navigate to display settings", 
        max_attempts=2
    )
    
    print("Feedback Loop Result:")
    print(json.dumps(result, indent=2))
    print("-" * 50)


def example_step_by_step_automation():
    """Example: Step-by-step automation plan"""
    print("Example 6: Step-by-step automation")
    
    agent = AIAgent()
    
    # Create an automation plan
    automation_plan = """
    Step-by-step plan:
    1. click(100, 50) - Click on menu
    2. type_text("preferences") - Type preferences
    3. key_press("enter") - Press enter
    4. wait(2) - Wait for dialog to open
    5. click(200, 150) - Click on display option
    """
    
    # Execute the plan
    result = agent.visual_executor.execute_automation_plan(automation_plan)
    
    print("Automation Plan Result:")
    print(json.dumps(result, indent=2))
    print("-" * 50)


def example_coordinate_operations():
    """Example: Direct coordinate operations"""
    print("Example 7: Direct coordinate operations")
    
    agent = AIAgent()
    
    # Get screen size first
    screen_info = agent.visual_executor.visual_automation.get_screen_size()
    print("Screen Info:", json.dumps(screen_info, indent=2))
    
    # Get mouse position
    mouse_info = agent.visual_executor.visual_automation.get_mouse_position()
    print("Mouse Info:", json.dumps(mouse_info, indent=2))
    
    # Click at specific coordinates (center of screen)
    if "screen_size" in screen_info:
        width = screen_info["screen_size"]["width"]
        height = screen_info["screen_size"]["height"]
        center_x = width // 2
        center_y = height // 2
        
        click_result = agent.visual_executor.visual_automation.click_coordinates(center_x, center_y)
        print("Center Click Result:", json.dumps(click_result, indent=2))
    
    print("-" * 50)


def example_text_and_keyboard():
    """Example: Text typing and keyboard operations"""
    print("Example 8: Text and keyboard operations")
    
    agent = AIAgent()
    
    # Type some text
    type_result = agent.visual_executor.visual_automation.type_text("Hello, World!")
    print("Type Result:", json.dumps(type_result, indent=2))
    
    # Send key presses
    key_result = agent.visual_executor.visual_automation.send_key("cmd+a")  # Select all
    print("Key Press Result:", json.dumps(key_result, indent=2))
    
    # Another key press
    enter_result = agent.visual_executor.visual_automation.send_key("enter")
    print("Enter Key Result:", json.dumps(enter_result, indent=2))
    
    print("-" * 50)


def example_screenshot_with_region():
    """Example: Screenshot with specific region"""
    print("Example 9: Regional screenshot")
    
    agent = AIAgent()
    
    # Take screenshot of specific region (left, top, width, height)
    region = (100, 100, 400, 300)  # 400x300 region starting at (100,100)
    result = agent.take_screenshot(region)
    
    print("Regional Screenshot Result:")
    print(json.dumps(result, indent=2))
    print("-" * 50)


def example_capabilities_overview():
    """Example: Show all visual capabilities"""
    print("Example 10: Visual capabilities overview")
    
    agent = AIAgent()
    
    capabilities = agent.get_visual_capabilities()
    
    print("Visual Capabilities:")
    print(json.dumps(capabilities, indent=2))
    print("-" * 50)


def main():
    """Run all examples or specific example"""
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        
        examples = {
            "1": example_basic_screenshot,
            "2": example_visual_analysis,
            "3": example_find_and_click,
            "4": example_visual_command_execution,
            "5": example_feedback_loop,
            "6": example_step_by_step_automation,
            "7": example_coordinate_operations,
            "8": example_text_and_keyboard,
            "9": example_screenshot_with_region,
            "10": example_capabilities_overview,
        }