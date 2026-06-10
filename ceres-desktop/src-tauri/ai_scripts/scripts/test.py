# ai_agent_local.py
import subprocess
import sys
import json
from llama_cpp import Llama

# Load local GGUF model once
llm = Llama(
    model_path="./models/gemma-3n-E2B-it-Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=8,
    n_gpu_layers=-1
)

class AIAgent:
    def __init__(self):
        self.messages = []

    def run_command(self, command: str, shell: bool = False):
        """Run a shell or AppleScript command safely."""
        try:
            # AppleScript detection
            if command.lower().startswith("tell application"):
                result = subprocess.run(
                    ["osascript", "-e", command],
                    capture_output=True,
                    text=True,
                    timeout=20
                )
            else:
                result = subprocess.run(
                    command,
                    capture_output=True,
                    text=True,
                    timeout=20,
                    shell=shell
                )

            if result.returncode == 0:
                stdout_text = result.stdout.strip() if result.stdout else ""
                return {"messages": [{"text": stdout_text or "✅ Command executed successfully", "type": "bot"}]}
            else:
                stderr_text = result.stderr.strip() if result.stderr else "Unknown error"
                return {"messages": [{"text": f"⚠️ Error: {stderr_text}", "type": "bot"}]}
        except subprocess.TimeoutExpired:
            return {"messages": [{"text": "⚠️ Error: Command timed out", "type": "bot"}]}
        except Exception as e:
            return {"messages": [{"text": f"⚠️ Execution failed: {str(e)}", "type": "bot"}]}

    def sanitize_response(self, response_text: str) -> str:
        """Clean AI response: remove code fences and comments."""
        text = response_text.strip()
        if text.startswith("```"):
            text = text.strip("`")
            parts = text.split("\n", 1)
            if len(parts) > 1:
                text = parts.strip()
        # Remove comment lines starting with # (but keep AppleScript -- comments)
        lines = [line for line in text.splitlines() if not line.strip().startswith("#")]
        return "\n".join(lines)

    def generate_command(self, user_request: str) -> str:
        """Generate shell or AppleScript command using local LLM."""
        prompt = f"""You are a macOS/Linux CLI automation assistant.

USER REQUEST:
{user_request}

TASK:
- If the task is a macOS GUI automation, output only a valid AppleScript.
- If the task is command-line, output only a valid shell command.
- Do NOT return JSON, markdown, or backticks.
- Return only the raw AppleScript or shell command.
"""
        # Add conversation history if needed
        self.messages.append({"role": "user", "content": prompt})

        # Build full prompt for LLaMA
        full_prompt = "<bos>"
        for m in self.messages:
            role = m["role"]
            content = m["content"]
            full_prompt += f"<start_of_turn>{role}\n{content}<end_of_turn>\n"
        full_prompt += "<start_of_turn>model\n"

        output = llm(
            full_prompt,
            max_tokens=300,
            stop=["<end_of_turn>", "<start_of_turn>user"],
            echo=False
        )

        command_text = output["choices"]["text"].strip()
        
        # Debug output
        print("RAW MODEL OUTPUT:", command_text, file=sys.stderr)
        
        clean_command = self.sanitize_response(command_text)
        self.messages.append({"role": "model", "content": clean_command})
        
        # For shell commands, take the first non-empty line
        if not clean_command.lower().startswith("tell application"):
            lines = [line for line in clean_command.splitlines() if line.strip()]
            if lines:
                clean_command = lines.strip()
        
        return clean_command

    def execute_command(self, user_request: str):
        """Generate command from user request and execute it."""
        clean_command = self.generate_command(user_request)

        # Detect AppleScript
        if clean_command.lower().startswith("tell application"):
            return self.run_command(clean_command)
        else:
            return self.run_command(clean_command, shell=True)

def main():
    user_request = " ".join(sys.argv[1:])
    if not user_request:
        user_request = "open calculator"

    try:
        agent = AIAgent()
        result = agent.execute_command(user_request)
        print(json.dumps(result, indent=2))
    except Exception as e:
        error_result = {"messages": [{"text": f"Error: {str(e)}", "type": "bot"}]}
        print(json.dumps(error_result, indent=2))

if __name__ == "__main__":
    main()
