
# CERES - AI-Based OS Automation System

[![Demo Video](path_to_video_thumbnail)](path_to_video_link)

---

## **Overview**

CERES is a lightweight, AI-powered desktop automation system. It allows you to control your OS and applications using **voice commands** and **chat input**. The system converts **Natural Language (NLP)** commands into executable tasks using **GEMIN 2.0 Flash** and executes them seamlessly.

With CERES, you can automate everyday tasks such as:

- Opening and controlling applications  
- Sending emails  
- Checking system metrics (CPU, memory)  
- Killing processes or ports  
- Executing custom scripts  
- And much more via voice or chat  

---

## **Technology Stack**

- **Frontend:** Tauri (desktop), Tailwind CSS for UI  
- **Backend:** Rust + FastAPI for AI & WebSocket server  
- **AI Engine:** GEMIN 2.0 Flash for NLP → command conversion  
- **Voice Module:**  
  - Picovoice Porcupine for wake-word detection  
  - Silero VAD for voice activity detection  
  - OpenAI Whisper for speech-to-text  
  - pyttsx3 for text-to-speech  

---

## **Screenshots**

<!-- Add screenshots of the app here -->
![Screenshot 1](path_to_screenshot_1)
![Screenshot 2](path_to_screenshot_2)

---

## **Video Demo**

[![Watch Video](path_to_video_thumbnail)](path_to_video_link)

---

## **Running the Application**

The application is split into two main parts:

### **1. Desktop App**
- Located under `app/`  
- Navigate to the folder:  
```bash
cd app/
````

* Start the Tauri desktop app from there

### **2. Voice Module**

* Located under `ceres-voice-module/`
* Navigate to the folder:

```bash
cd ceres-voice-module/
```

* Run the voice client to start listening for commands

### **Backend**

* The FastAPI server (`main.py`) runs in `ceres-voice-module/src/`
* Navigate to the folder and run the server:

```bash
cd ceres-voice-module/
python -m src.main
```

---

## **Usage**

1. Start the **FastAPI server** (`main.py`)
2. Start the **voice client** (`voice_test.py`)
3. Say the wake word: **"Hey Ceres"**
4. Give any command via voice or chat, e.g.:

   * "Open Chrome"
   * "Send an email to John"
   * "Check CPU usage"
   * "Kill port 8000"
5. CERES will execute the task and provide feedback via voice and chat.

---

## **Future Work / Scope**

* Advanced scheduling of tasks
* Multi-language voice support
* Integration with external APIs
* GUI enhancements
* **Computer Vision Integration:**

  * Enable complex automation using camera input
  * Detect, recognize, and interact with on-screen elements
  * Perform tasks based on visual context, e.g., clicking buttons in apps or analyzing screenshots
  * Advanced object recognition to automate workflows more intelligently

---

## **Contributing**

Feel free to fork the repository and contribute. Please submit issues or pull requests for bug fixes and feature requests.

---

## **License**

MIT License


