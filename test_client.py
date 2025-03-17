import requests
import json
import sys

# Server URL
url = 'http://localhost:5000/mcp'

def test_generate_text():
    payload = {
        'action': 'generate_text',
        'parameters': {
            'prompt': 'Write a short poem about AI and creativity',
            'temperature': 0.8,
            'max_tokens': 150
        }
    }
    
    response = requests.post(url, json=payload)
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

def test_analyze_text():
    payload = {
        'action': 'analyze_text',
        'parameters': {
            'text': 'The weather today is wonderful! I love how the sun is shining and the birds are singing.',
            'analysis_type': 'sentiment'
        }
    }
    
    response = requests.post(url, json=payload)
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

def test_chat():
    payload = {
        'action': 'chat',
        'parameters': {
            'messages': [
                {'role': 'user', 'content': 'Hello, how are you?'},
                {'role': 'assistant', 'content': 'I\'m doing well! How can I help you today?'},
                {'role': 'user', 'content': 'Tell me about the Model Context Protocol'}
            ],
            'temperature': 0.7
        }
    }
    
    response = requests.post(url, json=payload)
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
        if test_type == "text":
            test_generate_text()
        elif test_type == "analyze":
            test_analyze_text()
        elif test_type == "chat":
            test_chat()
        else:
            print(f"Unknown test type: {test_type}")
    else:
        print("Testing generate_text:")
        test_generate_text()
        
        print("\nTesting analyze_text:")
        test_analyze_text()
        
        print("\nTesting chat:")
        test_chat()