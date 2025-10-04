"""
This is Main Interface for Websocket and FastServer
main.py
"""


"""
Imports Inbuilt Libraries
"""
from fastapi import FastAPI,WebSocket,WebSocketDisconnect
import uvicorn
import logging
import asyncio
import numpy as np 
import whisper
import sys



"""
Import Derived Libraries
"""     
from src.ai_agent.ai_agent import AIAgent
from src.exceptions.exceptions import ConfigurationError
from src.utils.ApiResponse import ApiResponse




"""
Logger Initilisation
"""
logging.basicConfig(level=logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


"""
Apps Initilization
"""
app = FastAPI()
agent = AIAgent()



"""
Whisper Model Iniilization
"""
try:
    logger.info("Loading Whisper model...")
    whisper_model = whisper.load_model("base.en")
    logger.info("Whisper model loaded successfully.")
    print("Whisper model loaded successfully.")
except Exception as e:
    logger.error(f"Fatal: Could not load Whisper model. Error: {e}")
    print("Failed Model Loading")
    sys.exit(1)


"""
Helper Function For special execution
"""
def handle_special_commands(command : str):

    command = command.lower().strip()

    try:

        if command in ['test', '--test', 'self-test']:
            return agent.test_functionality()
        

        elif command in ['info', '--info', 'system-info']:
            return agent.get_system_info()
        

        elif command in ['help', '--help', '-h']:
            return {"messages": [{"text": "Help displayed", "type": "bot"}]}
        

        elif command in ['screenshot', 'take-screenshot', 'capture']:
            return agent.take_screenshot()
        

        elif 'screenshot' in command and ('analyze' in command or 'click' in command or 'find' in command):
            return agent.execute_visual_command(command)
        

        else:
            return None
        

    except ConfigurationError as e:
        return {"messages": [{"text": f"Configuration error: {str(e)}", "type": "bot"}]}
    

    except Exception as e:
        logger.error(f"Special command failed: {e}")
        return {"messages": [{"text": f"Command failed: {str(e)}", "type": "bot"}]}


"""
Task Exectution Socket
"""
@app.websocket('/ws/execute')
async def websocket_endpoint(websocket:WebSocket):
    
    # await till accept
    await websocket.accept()

    try:
        while True:
            
            #extract the commands
            command = await websocket.receive_text()

            logger.info(f"Received Commmand :{command}")
            await websocket.send_text("Received...")
            await asyncio.sleep(1)

            try:
          
                await websocket.send_text("Exectuting... ")

                special_result  = handle_special_commands(command)

                # Special Commands
                """
                If Any Specific command can be Executed in this way
                """
                if special_result is not None:
                    response = special_result
                
                # Generic Command
                else: 
                    """
                    AI Agent Will Perfrom the Further task
                    """
                    agent = AIAgent()
                    response = agent.execute_command(command)


            except Exception as e:
                response = ApiResponse.error("Execution Failed")

            # Sending response to Clent
            for msg in response.get("messages",[]):
                text = msg.get("text","")
                
                if text.strip():
                    await websocket.send_text(text)
                    await asyncio.sleep(0.2)

            await websocket.send_text("Execution Finished !")

    except WebSocketDisconnect:
        logger.info("UI Disconnected")
        


"""
Voice Assistance
"""
@app.websocket('/listen')
async def websocket_listen_endpoint(websocket:WebSocket):
    """
    This new endpoint handles the audio stream from your wake word client.
    """
    await websocket.accept()

    try:
        while True :
            # 1. Receive raw audio bytes from the client
            audio_bytes = await websocket.receive_bytes()


            # 2. Convert audio bytes to a Numpy array that whisper can understand
            # [-32768, 32767] -->  [-32768.0, 32767.0] --> [-1,0,1]
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0


            # 3. Use Whisper to transcribe the audio to text
            result = whisper_model.transcribe(audio_np, fp16=False) #True when GPU
            
            transcribed_text = result.get("text", "").strip()

            logger.info(f"Transcribed from voice: '{transcribed_text}'")

            print("Transcribe Sucesfully Done")



            # 4. If transcription is empty, send a default message
            if not transcribed_text:
                await websocket.send_text("Sorry, I didn't catch that.")
                continue



            # 5. Process the command using your existing AIAgent
            try:
                response_data = agent.execute_command(transcribed_text)
                messages = response_data.get("messages", [])
                
                chatbot_response = "I'm not sure how to respond." # Default
                if messages and messages[0].get("text"):
                    chatbot_response = messages[0].get("text")

            except Exception as e:
                logger.error(f"Error executing voice command: {e}")
                chatbot_response = "Sorry, an error occurred."


            # 6. Send the final text response back to the voice client
            await websocket.send_text(chatbot_response)

        
    except WebSocketDisconnect:
        logger.info("Voice client disconnected.")





"""
Health Function
"""

@app.get('/health')
def get_health():
    return "Working Fine"




"""
Main Function
"""
if __name__ == "__main__":

    #development
    uvicorn.run('src.main:app',host="127.0.0.1",port=8000,reload=True)


    #Production 
    # uvicorn.run(app,host="127.0.0.1",port=8000)

    
