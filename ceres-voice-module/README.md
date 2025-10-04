# CERES Voice Module

This module provides a **voice interface** for the CERES AI system. It integrates:

* **Wake-word detection** using Picovoice Porcupine
* **Voice command recognition** with Silero VAD
* **Speech-to-text transcription** using OpenAI Whisper
* **Text-to-speech** responses via `pyttsx3`
* **FastAPI server** for WebSocket communication with the voice client

---

# Interface of Voice Module

<img width="2374" height="1757" alt="image" src="https://github.com/user-attachments/assets/3c9c438f-5010-4efc-a778-19eb162341ee" />


## **Folder Structure**

```
ceres-voice-module/
│
├─ src/
│   ├─ main.py                 # FastAPI server and WebSocket endpoints
│   ├─ ai_agent/               # AI agent modules for command execution
│   ├─ exceptions/             # Custom exception handling
│   └─ utils/                  # Utilities like ApiResponse
│
├─ venv/                       # Python virtual environment
├─ voice_test.py               # Wake-word client and voice command handler
├─ Hey_Ceres_Wake_Word.ppn    # Wake-word model file
└─ .env                        # Environment variables, e.g., PICOVOICE_ACCESS_KEY
```

---

## **Prerequisites**

* Python 3.10+ (tested with 3.13)
* `pip` package manager
* Microphone access for voice input

---

## **1. Setting up Virtual Environment**

1. Create virtual environment (if not already created):

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

```bash
# Mac/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## **2. Configuration**

1. Add your **Picovoice Access Key** to `.env`:

```
PICOVOICE_ACCESS_KEY=YOUR_ACCESS_KEY_HERE
```

2. Ensure the **wake word file** is present:

```
Hey_Ceres_Wake_Word.ppn
```

---

## **3. Running the Server**

The FastAPI server handles **voice commands** and WebSocket connections.

```bash
# Activate virtual environment
source venv/bin/activate

# Start FastAPI server
python -m src.main
```

* Server endpoints:

  * `/listen` → Receives audio from the voice client
  * `/ws/execute` → Executes text commands
  * `/health` → Simple health check

---

## **4. Running the Voice Client**

The voice client detects your wake word, records commands, and sends them to the server.

```bash
# Activate virtual environment
source venv/bin/activate

# Start voice client
python voice_test.py
```

* Wake word: `Hey Ceres`
* Client automatically retries connection if the server is not available.

---

## **5. Running Both Together**

You can run both in **one terminal** using `&` (Mac/Linux):

```bash
python -m src.main & python voice_test.py
```

Or, use **separate terminal tabs** for cleaner output.

---

## **6. Troubleshooting**

* **Server not running:** Client retries every 3 seconds if connection fails.
* **Wake word not detected:** Check `Hey_Ceres_Wake_Word.ppn` and microphone permissions.
* **Dependencies missing:** Ensure all packages from `requirements.txt` are installed in the virtual environment.
* **TTS errors (`pyttsx3`)**: Occurs if engine fails during shutdown; usually harmless.

---

## **7. Notes**

* `voice_test.py` uses **Silero VAD** to detect when the user stops speaking.
* Whisper transcribes audio to text locally (offline).
* Special commands (e.g., `screenshot`, `test`) are handled before AI processing.

---
