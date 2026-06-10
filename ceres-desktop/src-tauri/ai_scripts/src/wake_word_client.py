# File: wake_word_client.py

import asyncio
import websockets
import pyaudio
import torch
import pyttsx3
import numpy as np
import time
import struct
import pvporcupine

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WAKE_WORD_FILE = os.path.join(BASE_DIR, "Hey_Ceres_Wake_Word.ppn")

# --- ⚠️ IMPORTANT CONFIGURATION ---
# 1. Get your free AccessKey from Picovoice Console: https://console.picovoice.ai/
PICOVOICE_ACCESS_KEY = "sW+UUygd4q7fN+YJZJK/iHB66+SvYWuak0A9wYYvz4z5b8za3ocUbg=="
try:
    porcupine = pvporcupine.create(access_key=PICOVOICE_ACCESS_KEY, keyword_paths=[WAKE_WORD_FILE])
    print("Porcupine wake word engine loaded.")
except Exception as e:
    print(f"Error loading Porcupine. Did you add your AccessKey and .ppn file? Error: {e}")
    exit()

print("Loading VAD model...")
vad_model, _ = torch.hub.load(repo_or_dir='snakers4/silero-vad', model='silero_vad', force_reload=False)
print("VAD model loaded.")

tts_engine = pyttsx3.init()
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=porcupine.frame_length)


async def main_loop():
    uri = "ws://localhost:8000/listen"
    
    async with websockets.connect(uri) as websocket:
        print(f"\n--- Ready and listening for '{WAKE_WORD_FILE.split('_')[0]}' ---")
        stream.start_stream()
        
        while True:
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Wake word detected!")
                stream.stop_stream()
                tts_engine.say("Yes?")
                tts_engine.runAndWait()
                stream.start_stream()

                audio_buffer = []
                last_speech_time = time.time()
                print("Listening for command...")
                while time.time() - last_speech_time < 2.0: # Listen for 2 seconds of silence
                    audio_chunk_bytes = stream.read(512, exception_on_overflow=False)
                    audio_buffer.append(audio_chunk_bytes)
                    
                    audio_tensor = torch.from_numpy(np.frombuffer(audio_chunk_bytes, dtype=np.int16).astype(np.float32) / 32768.0)
                    if vad_model(audio_tensor, 16000).item() > 0.5:
                        last_speech_time = time.time()
                
                print("Finished listening.")
                stream.stop_stream()
                await websocket.send(b''.join(audio_buffer))
                
                response = await websocket.recv()
                print(f"Ceres says: {response}")
                tts_engine.say(response)
                tts_engine.runAndWait()

                print(f"\n--- Ready and listening for '{WAKE_WORD_FILE.split('_')[0]}' ---")
                stream.start_stream()

try:
    asyncio.run(main_loop())
except websockets.exceptions.ConnectionClosedError:
    print("Connection failed. Is the main.py server running?")
except KeyboardInterrupt:
    print("\nClient stopped.")
finally:
    if 'stream' in locals() and stream.is_active(): stream.stop_stream()
    if 'p' in locals(): p.terminate()
    if 'porcupine' in locals(): porcupine.delete()