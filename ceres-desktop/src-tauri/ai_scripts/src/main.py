"""
WebSocket server for AI Agent with step-by-step execution AND voice transcription.
""" 
import os
import sys
import asyncio
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import numpy as np
import whisper

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from .ai_agent import AIAgent
from .exceptions import ConfigurationError

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

try:
    logger.info("Loading Whisper model...")
    whisper_model = whisper.load_model("base.en")
    logger.info("Whisper model loaded successfully.")
except Exception as e:
    logger.error(f"Fatal: Could not load Whisper model. Error: {e}")
    sys.exit(1)

app = FastAPI()

def handle_special_commands(command: str):
    command_lower = command.lower().strip()
    try:
        agent = AIAgent()
        if command_lower in ['test', '--test', 'self-test']:
            return agent.test_functionality()
        elif command_lower in ['info', '--info', 'system-info']:
            return agent.get_system_info()
        elif command_lower in ['help', '--help', '-h']:
            return {"messages": [{"text": "Help displayed", "type": "bot"}]}
        elif command_lower in ['screenshot', 'take-screenshot', 'capture']:
            return agent.take_screenshot()
        elif 'screenshot' in command_lower and ('analyze' in command_lower or 'click' in command_lower or 'find' in command_lower):
            return agent.execute_visual_command(command)
        else:
            return None
    except ConfigurationError as e:
        return {"messages": [{"text": f"Configuration error: {str(e)}", "type": "bot"}]}
    except Exception as e:
        logger.error(f"Special command failed: {e}")
        return {"messages": [{"text": f"Command failed: {str(e)}", "type": "bot"}]}


@app.websocket("/ws/execute")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    try:
        while True:
            command = await websocket.receive_text()
            logger.info(f"Received text command: {command}") 
            steps = ["Parsing...", "Executing..."]
            for step in steps:
                await websocket.send_text(step)
                await asyncio.sleep(1)
            try:
                special_result = handle_special_commands(command)
                if special_result is not None:
                    response = special_result
                else:
                    agent = AIAgent()
                    response = agent.execute_command(command)
            except Exception as e:
                response = {"messages": [{"text": f"Execution failed: {str(e)}", "type": "bot"}]}
            for msg in response.get("messages", []):
                text = msg.get("text", "")
                if text.strip():
                    await websocket.send_text(text)
                    await asyncio.sleep(0.2)
            await websocket.send_text("Finished execution!")
            await websocket.send_text("###DONE###")
    except WebSocketDisconnect:
        logger.info("UI Client disconnected")




@app.websocket("/listen")
async def websocket_listen_endpoint(websocket: WebSocket):
    """
    This new endpoint handles the audio stream from your wake word client.
    """
    await websocket.accept()
    logger.info("Voice client connected.")
    agent = AIAgent()  

    try:
        while True:
            # 1. Receive raw audio bytes from the client
            audio_bytes = await websocket.receive_bytes()

            # 2. Convert audio bytes to a NumPy array that Whisper can understand
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0

            # 3. Use Whisper to transcribe the audio to text
            result = whisper_model.transcribe(audio_np, fp16=False) # Use fp16=True if you have a GPU
            transcribed_text = result.get("text", "").strip()
            logger.info(f"Transcribed from voice: '{transcribed_text}'")

            # 4. If transcription is empty, send a default message
            if not transcribed_text:
                await websocket.send_text("Sorry, I didn't catch that.")
                continue

            # 5. Process the command using your existing AIAgent
            try:
                # Note: We are NOT using handle_special_commands here for simplicity,
                # but you could add it if you want the voice to trigger them.
                response_data = agent.execute_command(transcribed_text)
                messages = response_data.get("messages", [])
        
                chatbot_response = "I'm not sure how to respond." 
                if messages and messages[0].get("text"):
                    chatbot_response = messages[0].get("text")

            except Exception as e:
                logger.error(f"Error executing voice command: {e}")
                chatbot_response = "Sorry, an error occurred."

            # 6. Send the final text response back to the voice client
            await websocket.send_text(chatbot_response)

    except WebSocketDisconnect:
        logger.info("Voice client disconnected.")



if __name__ == "__main__":
    
    venv_python = os.path.join(os.path.dirname(__file__), "venv", "bin", "python")
    if os.path.exists(venv_python) and sys.executable != venv_python:
        os.execv(venv_python, [venv_python] + sys.argv)


    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False) 