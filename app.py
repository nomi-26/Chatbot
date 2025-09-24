from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini AI
API_KEY = "AIzaSyBbzwF8qA_uSAa7aepdGfv9dNlqBBkRa2E"
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel("gemini-2.0-flash")
chat = model.start_chat()

@app.route('/')
def index():
    return render_template('genai.html')

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Send message to Gemini
        response = chat.send_message(message)
        
        return jsonify({
            'response': response.text,
            'success': True
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/reset', methods=['POST'])
def reset_chat():
    global chat
    chat = model.start_chat()
    return jsonify({'success': True, 'message': 'Chat reset successfully'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Move the HTML file to templates directory
    import shutil
    if os.path.exists('genai.html'):
        shutil.move('genai.html', 'templates/genai.html')
    
    app.run(debug=True, port=5000)
