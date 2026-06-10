# AI Agent - Intelligent macOS Automation

AI Agent is a powerful macOS automation tool that converts natural language requests into executable AppleScript or shell commands using Google's Gemini AI.

## 🚀 Features

- **Natural Language Processing**: Convert plain English requests into executable commands
- **Dual Execution Modes**: Supports both AppleScript (GUI) and shell (CLI) commands
- **Security First**: Built-in security validation prevents dangerous operations
- **Smart Detection**: Automatically determines the best execution method
- **Error Handling**: Comprehensive error handling and user-friendly messages
- **Logging**: Detailed logging for debugging and monitoring

## 📦 Installation

### Prerequisites
- macOS (required for AppleScript functionality)
- Python 3.7 or higher
- Google Gemini API key

### Setup

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**:
   ```bash
   export GEMINI_API_KEY='your-gemini-api-key-here'
   ```

4. **Test the installation**:
   ```bash
   python main.py 'test'
   ```

## 🏗️ Project Structure

```
ai-agent/
├── main.py                 # Entry point
├── __init__.py             # Package initialization
├── ai_agent.py             # Main orchestrator class
├── ai_service.py           # Google Gemini integration
├── config.py               # Configuration management
├── security.py             # Security validation
├── command_detector.py     # Command type detection
├── response_cleaner.py     # Response processing
├── executors.py            # Command execution
├── prompt_generator.py     # AI prompt generation
├── exceptions.py           # Custom exceptions
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
└── README.md              # This file
```

## 🎯 Usage

### Basic Usage

```bash
# Open an application
python main.py 'open chrome and go to google.com'

# File operations
python main.py 'create a folder named Projects on desktop'

# Email automation
python main.py 'send email to john@test.com with subject Hello'

# System controls
python main.py 'set volume to 50 percent'

# Screenshot
python main.py 'take a screenshot'
```

### Special Commands

```bash
# Run functionality tests
python main.py 'test'

# Show system information
python main.py 'info'

# Show help
python main.py 'help'
```

### Programmatic Usage

```python
from ai_agent import AIAgent

# Initialize the agent
agent = AIAgent()

# Execute a command
result = agent.execute_command("open terminal and list files")
print(result)

# Test functionality
test_result = agent.test_functionality()
print(test_result)
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Configuration Options
The `config.py` file contains various settings you can modify:
- Command timeout duration
- Security patterns
- Application bundle IDs
- AppleScript indicators

## 🛡️ Security

AI Agent includes multiple security layers:

1. **Command Validation**: Blocks potentially dangerous commands
2. **Path Restrictions**: Prevents operations on system directories
3. **Input Sanitization**: Cleans and validates all inputs
4. **Timeout Protection**: Prevents long-running commands
5. **Proper Escaping**: Handles special characters safely

### Blocked Operations
- System file deletion (`rm -rf /`, `sudo rm`, etc.)
- Disk formatting operations
- Privilege escalation attempts
- Code injection patterns
- Unsafe download and execute patterns

## 📊 Error Handling

The system provides detailed error messages for various scenarios:
- ✅ Success indicators
- ⚠️ Warning messages for issues
- ❌ Error messages for failures
- 🛡️ Security violation notifications
- 🤖 AI service status updates

## 🔍 Logging

Logs are written to:
- `ai_agent.log` file
- Console output (stdout)

Log levels include:
- INFO: General information
- WARNING: Security violations and issues
- ERROR: Execution failures
- DEBUG: Detailed debugging information

## 🧪 Testing

Run the built-in tests:
```bash
python main.py 'test'
```

This will test:
- AI service connectivity
- Shell command execution
- AppleScript execution
- Command type detection

## 📝 Examples

### GUI Operations (AppleScript)
```bash
# Browser automation
python main.py 'open safari and navigate to apple.com'

# Email management
python main.py 'create new email with subject Meeting and send to team@company.com'

# System preferences
python main.py 'open system preferences and go to displays'

# Application control
python main.py 'quit all chrome windows'
```

### CLI Operations (Shell)
```bash
# File system operations
python main.py 'list all python files in current directory'

# Git operations
python main.py 'check git status and show recent commits'

# System information
python main.py 'show disk usage and memory information'

# Process management
python main.py 'find all running python processes'
```

## ⚠️ Limitations

1. **macOS Only**: AppleScript functionality requires macOS
2. **API Dependency**: Requires active internet connection for AI service
3. **Permission Requirements**: Some operations may require system permissions
4. **Application Specific**: GUI automation depends on target applications being installed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `GEMINI_API_KEY` environment variable is set
2. **Permission Denied**: Some operations may require accessibility permissions
3. **Application Not Found**: Ensure target applications are installed
4. **Timeout Errors**: Large operations may need timeout adjustment

### Debug Mode
Set logging level to DEBUG for detailed information:
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs in `ai_agent.log`
3. Run the test command to verify functionality
4. Create an issue in the project repository

## 🔄 Version History

- **v1.0.0**: Initial release with core functionality
  - Natural language command processing
  - AppleScript and shell execution
  - Security validation
  - Comprehensive error handling