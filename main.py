import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq
import json

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
CORS(app)

# Initialize Groq client
groq_api_key = os.environ.get("GROQ_API_KEY", "").strip()
if not groq_api_key:
    # Use the hardcoded key as fallback
    groq_api_key = "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"

if not groq_api_key:
    app.logger.error("GROQ_API_KEY is not set or is empty")
    groq_client = None
else:
    groq_client = Groq(api_key=groq_api_key)

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests and return AI responses"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Message is required'}), 400

        # Check if Groq client is available
        if not groq_client:
            return jsonify({'error': 'Groq API key not configured or invalid'}), 500

        # Create chat completion with Groq
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant. Provide concise, friendly responses suitable for voice conversation. Keep responses conversational and not too long."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=150
        )

        ai_response = chat_completion.choices[0].message.content

        return jsonify({
            'response': ai_response,
            'success': True
        })

    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': f'Failed to get AI response: {str(e)}',
            'success': False
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'groq_configured': bool(groq_client)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
