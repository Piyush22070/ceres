#!/bin/bash
if [[ "$HOME" ]]; then
    LOG_FILE="$HOME/Desktop/ceres_debug_log.txt"
else
    LOG_FILE="/tmp/ceres_debug_log.txt"
fi

echo "--- Starting Ceres Backend Script ---" > "$LOG_FILE"
date >> "$LOG_FILE"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "SCRIPT_DIR = $SCRIPT_DIR" >> "$LOG_FILE"

# Try to find ai_scripts directory in different locations
AI_SCRIPTS_DIR=""

# Check development directory FIRST to avoid corrupted venv copies
if [[ -d "$SCRIPT_DIR/../../ai_scripts" ]]; then
    AI_SCRIPTS_DIR="$SCRIPT_DIR/../../ai_scripts"
    echo "Found ai_scripts in dev dir: $AI_SCRIPTS_DIR" >> "$LOG_FILE"
elif [[ -d "$SCRIPT_DIR/ai_scripts" ]]; then
    AI_SCRIPTS_DIR="$SCRIPT_DIR/ai_scripts"
    echo "Found ai_scripts in bundle: $AI_SCRIPTS_DIR" >> "$LOG_FILE"
elif [[ -d "/Users/piyush/Desktop/ceres/src-tauri/ai_scripts" ]]; then
    AI_SCRIPTS_DIR="/Users/piyush/Desktop/ceres/src-tauri/ai_scripts"
    echo "Found ai_scripts in dev location: $AI_SCRIPTS_DIR" >> "$LOG_FILE"
else
    echo "ERROR: Could not find ai_scripts directory!" >> "$LOG_FILE"
    echo "Searched in:" >> "$LOG_FILE"
    echo "  - $SCRIPT_DIR/../../ai_scripts" >> "$LOG_FILE"
    echo "  - $SCRIPT_DIR/ai_scripts" >> "$LOG_FILE"
    echo "  - /Users/piyush/Desktop/ceres/src-tauri/ai_scripts" >> "$LOG_FILE"
    sleep 10
    exit 1
fi

echo "AI_SCRIPTS_DIR = $AI_SCRIPTS_DIR" >> "$LOG_FILE"

# Define the path to the python executable we are trying to run
PYTHON_EXEC="$AI_SCRIPTS_DIR/venv/bin/python"
echo "PYTHON_EXEC = $PYTHON_EXEC" >> "$LOG_FILE"

# Check if the python executable actually exists
if [ ! -f "$PYTHON_EXEC" ]; then
    echo "ERROR: Python executable not found at the path above!" >> "$LOG_FILE"
    if [ -d "$AI_SCRIPTS_DIR/venv/bin/" ]; then
        echo "Listing contents of venv/bin to see what's there:" >> "$LOG_FILE"
        ls -l "$AI_SCRIPTS_DIR/venv/bin/" >> "$LOG_FILE"
    else
        echo "venv/bin directory does not exist!" >> "$LOG_FILE"
    fi
    sleep 10
    exit 1
fi

echo "Python executable was found!" >> "$LOG_FILE"
# --- DEBUG END ---

# Use the python from the virtual environment and execute the uvicorn server.
echo "Attempting to start Uvicorn server..." >> "$LOG_FILE"
exec "$PYTHON_EXEC" -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --app-dir "$AI_SCRIPTS_DIR" >> "$LOG_FILE" 2>&1