from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

# Configure the Gemini API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("No Gemini API key found. Make sure to add it to your .env file.")

genai.configure(api_key=api_key)

# Choose a specific model that we know is available
TEXT_MODEL = 'models/gemini-1.5-pro'
VISION_MODEL = 'models/gemini-1.5-pro-vision-latest'

# Initialize Flask app
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "ok", "message": "MCP server is running"})

@app.route('/list-models', methods=['GET'])
def list_models():
    """List available models."""
    try:
        models = genai.list_models()
        model_names = [model.name for model in models]
        return jsonify({"available_models": model_names})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/mcp', methods=['POST'])
def handle_mcp_request():
    """Handle MCP protocol requests."""
    # Get the request data
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    # Extract the necessary information from the MCP request
    action = data.get('action')
    parameters = data.get('parameters', {})
    
    # Handle different actions
    if action == 'generate_text':
        prompt = parameters.get('prompt')
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        # Get optional parameters with defaults
        max_tokens = parameters.get('max_tokens', 1024)
        temperature = parameters.get('temperature', 0.7)
        
        try:
            # Use the specified model
            model = genai.GenerativeModel(
                TEXT_MODEL,
                generation_config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens
                }
            )
            
            # Call Gemini API
            response = model.generate_content(prompt)
            
            # Format response according to MCP protocol
            return jsonify({
                'result': {
                    'text': response.text,
                    'model': TEXT_MODEL,
                    'usage': {
                        'prompt_tokens': len(prompt.split()),
                        'completion_tokens': len(response.text.split()),
                        'total_tokens': len(prompt.split()) + len(response.text.split())
                    }
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif action == 'analyze_text':
        text = parameters.get('text')
        analysis_type = parameters.get('analysis_type', 'general')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        try:
            # Construct a prompt based on the analysis type
            if analysis_type == 'sentiment':
                prompt = f"Analyze the sentiment of the following text and classify it as positive, negative, or neutral. Provide a brief explanation: {text}"
            elif analysis_type == 'summary':
                prompt = f"Provide a concise summary of the following text in 2-3 sentences: {text}"
            elif analysis_type == 'keywords':
                prompt = f"Extract and list the 5-7 most important keywords from this text: {text}"
            else:
                prompt = f"Analyze the following text and provide insights: {text}"
            
            # Use the model
            model = genai.GenerativeModel(TEXT_MODEL)
            response = model.generate_content(prompt)
            
            # Format response according to MCP protocol
            return jsonify({
                'result': {
                    'analysis': response.text,
                    'analysis_type': analysis_type,
                    'model': TEXT_MODEL
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    elif action == 'chat':
        messages = parameters.get('messages', [])
        
        if not messages or not isinstance(messages, list) or len(messages) == 0:
            return jsonify({'error': 'No valid messages provided'}), 400
        
        # Get optional parameters with defaults
        temperature = parameters.get('temperature', 0.7)
        
        try:
            # Use the model in chat mode
            model = genai.GenerativeModel(
                TEXT_MODEL,
                generation_config={"temperature": temperature}
            )
            
            # Format messages for Gemini
            chat = model.start_chat(history=[])
            
            # Add messages to chat
            formatted_messages = []
            for msg in messages:
                if msg.get('role') == 'user':
                    formatted_messages.append({"role": "user", "parts": [msg.get('content', '')]})
                elif msg.get('role') == 'assistant':
                    formatted_messages.append({"role": "model", "parts": [msg.get('content', '')]})
            
            # Get the last user message
            last_user_message = next((msg.get('content', '') for msg in reversed(messages) 
                                     if msg.get('role') == 'user'), None)
            
            if not last_user_message:
                return jsonify({'error': 'No user message found'}), 400
            
            # Send to Gemini
            response = chat.send_message(last_user_message)
            
            # Format response according to MCP protocol
            return jsonify({
                'result': {
                    'response': response.text,
                    'model': TEXT_MODEL,
                }
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    else:
        return jsonify({'error': f'Unknown action: {action}'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)