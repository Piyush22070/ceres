"""
This is Testing of Voice Module 
"""


import asyncio
from asyncio import streams
import websockets
import pvporcupine
import torch
import pyttsx3
import pyaudio
import struct
import time
import numpy as np
from dotenv import load_dotenv
import os 


"""
Wake word and Picovoice Acces Key
"""
load_dotenv()


WAKE_WORD_FILE = 'Hey_Ceres_Wake_Word.ppn'
PICOVOICE_ACCESS_KEY = os.getenv("PICOVOICE_ACCESS_KEY")
try:
    porcupine = pvporcupine.create(access_key=PICOVOICE_ACCESS_KEY, keyword_paths=[WAKE_WORD_FILE])
    print("Porcupine wake word engine loaded.")
except Exception as e:
    print(f"Error loading Porcupine. Did you add your AccessKey and .ppn file? Error: {e}")
    exit()


"""
VAD Model
"""
print("Loading VAD model...")
vad_model, _ = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=False)
print("VAD model loaded.")




"""
TTS Engine 
"""
tts_engine = pyttsx3.init()
p = pyaudio.PyAudio()



async def main_loop():
    uri = "ws://localhost:8000/listen"

    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Successfully connected to the server.")
                
                while True:
                    # 1. Open a fresh stream just for wake word detection
                    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=porcupine.frame_length)
                    print(f"\n--- Ready and listening for Hey CERES word ---")

                    # Loop until wake word is detected
                    while True:
                        pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
                        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
                        keyword_index = porcupine.process(pcm)

                        if keyword_index >= 0:
                            break
                    
                    # 2. IMPORTANT: Close the wake-word stream completely
                    stream.close()
                    print("Wake word detected!")

                    # Acknowledge and wait for command
                    tts_engine.say("Yes?")
                    tts_engine.runAndWait()
                    
                    # 3. Open a NEW stream just for command recording
                    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=512)
                    print("Listening for command...")
                    
                    audio_buffer = []
                    last_speech_time = time.time()
                    while time.time() - last_speech_time < 2.0:
                        audio_chunk_bytes = stream.read(512, exception_on_overflow=False)
                        audio_buffer.append(audio_chunk_bytes)
                        
                        audio_tensor = torch.from_numpy(np.frombuffer(audio_chunk_bytes, dtype=np.int16).astype(np.float32) / 32768.0)
                        if vad_model(audio_tensor, 16000).item() > 0.5:
                            last_speech_time = time.time()

                    print("...Finished listening.")
                    
                    # 4. IMPORTANT: Close the command-recording stream
                    stream.close()

                    # Process command, get response, and speak
                    await websocket.send(b''.join(audio_buffer))
                    response = await websocket.recv()
                    print(f"Ceres says: {response}")
                    tts_engine.say(response)
                    tts_engine.runAndWait()
                    tts_engine.stop() 

        except OSError:
            print("Server not available. Retrying in 3 seconds...")
            await asyncio.sleep(3)
        except websockets.exceptions.ConnectionClosed:
            print("Connection lost. Attempting to reconnect in 3 seconds...")
            await asyncio.sleep(3)


try:
    asyncio.run(main_loop())
except websockets.exceptions.ConnectionClosedError:
    print("Connection Faliled with Socket !")
    print("Try to Check for Server is running !")
except KeyboardInterrupt:
    print("Client Stopped!")
finally:
    # This final cleanup is still a good safeguard
    if 'p' in locals(): p.terminate()
    if 'porcupine' in locals(): porcupine.delete()