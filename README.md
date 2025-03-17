# MCP Gemini Server

A server implementation of the Model Context Protocol (MCP) to enable AI assistants like Claude to interact with Google's Gemini API.

## Project Overview

This project implements a server that follows the Model Context Protocol, allowing AI assistants to communicate with Google's Gemini models. With this MCP server, AI assistants can request text generation, text analysis, and maintain chat conversations through the Gemini API.

## Features

- **Client-Server Communication**: Implements MCP protocol for secure message exchange between client and server.  
- **Message Processing**: Handles and processes client requests, sending appropriate responses.  
- **Error Handling & Logging**: Logs server activities and ensures smooth error recovery.  
- **Environment Variables Support**: Uses `.env` file for storing sensitive information securely.  
- **API Testing & Debugging**: Supports manual and automated testing using Postman and test scripts.  

## Installation

### Prerequisites

- Python 3.7 or higher
- Google AI API key

### Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/mcp-gemini-server.git
cd mcp-gemini-server
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Create a `.env` file in the root directory with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

## Usage

1. Start the server:
```bash
python server.py
```

2. The server will run on `http://localhost:5000/` by default

3. Send MCP requests to the `/mcp` endpoint using POST method

### Example Request

```python
import requests

url = 'http://localhost:5000/mcp'
payload = {
    'action': 'generate_text',
    'parameters': {
        'prompt': 'Write a short poem about AI',
        'temperature': 0.7
    }
}

response = requests.post(url, json=payload)
print(response.json())
```

## API Reference

### Endpoints

- `GET /health`: Check if the server is running
- `GET /list-models`: List available Gemini models
- `POST /mcp`: Main endpoint for MCP requests

### MCP Actions

#### 1. generate_text

Generate text content with Gemini.

**Parameters:**
- `prompt` (required): The text prompt for generation
- `temperature` (optional): Controls randomness (0.0 to 1.0)
- `max_tokens` (optional): Maximum tokens to generate

**Example:**
```json
{
  "action": "generate_text",
  "parameters": {
    "prompt": "Write a short story about a robot",
    "temperature": 0.8,
    "max_tokens": 500
  }
}
```

#### 2. analyze_text

Analyze text content.

**Parameters:**
- `text` (required): The text to analyze
- `analysis_type` (optional): Type of analysis ('sentiment', 'summary', 'keywords', or 'general')

**Example:**
```json
{
  "action": "analyze_text",
  "parameters": {
    "text": "The weather today is wonderful! I love how the sun is shining.",
    "analysis_type": "sentiment"
  }
}
```

#### 3. chat

Have a conversation with Gemini.

**Parameters:**
- `messages` (required): Array of message objects with 'role' and 'content'
- `temperature` (optional): Controls randomness (0.0 to 1.0)

**Example:**
```json
{
  "action": "chat",
  "parameters": {
    "messages": [
      {"role": "user", "content": "Hello, how are you?"},
      {"role": "assistant", "content": "I'm doing well! How can I help?"},
      {"role": "user", "content": "Tell me about quantum computing"}
    ],
    "temperature": 0.7
  }
}
```

## Error Handling

The server returns appropriate HTTP status codes and error messages:

- `200`: Successful request
- `400`: Bad request (missing or invalid parameters)
- `500`: Server error (API issues, etc.)

## Testing

Use the included test script to test various functionalities:

```bash
# Test all functionalities
python test_client.py

# Test specific functionality
python test_client.py text     # Test text generation
python test_client.py analyze  # Test text analysis
python test_client.py chat     # Test chat functionality
```

## MCP Protocol Specification

The Model Context Protocol implemented here follows these specifications:

1. **Request Format**:
   - `action`: String specifying the operation
   - `parameters`: Object containing action-specific parameters

2. **Response Format**:
   - `result`: Object containing the operation result
   - `error`: String explaining any error (when applicable)

## License

MIT License
