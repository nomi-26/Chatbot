from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import os
import base64
import io
from PIL import Image
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure Gemini AI
API_KEY = "AIzaSyBbzwF8qA_uSAa7aepdGfv9dNlqBBkRa2E"  # Hardcoded API key
genai.configure(api_key=API_KEY)

# Initialize the models
text_model = genai.GenerativeModel("gemini-2.0-flash")
chat = text_model.start_chat()

# For image generation (using a different service since Gemini doesn't support direct image generation)
IMAGE_GEN_API = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"
IMAGE_GEN_TOKEN = os.getenv('HUGGINGFACE_TOKEN')  # Get from environment variables

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
        
        # Check if user wants to generate an image
        if message.lower().startswith('generate image:'):
            description = message[15:].strip()
            if description:
                # Generate image using external service
                image_data = generate_image(description)
                if image_data:
                    return jsonify({
                        'response': f"Here's your generated image for: {description}",
                        'image': image_data,
                        'is_image': True,
                        'success': True
                    })
                else:
                    return jsonify({
                        'response': "Sorry, I couldn't generate the image. Please try again later.",
                        'success': True
                    })
        
        # Regular text conversation
        response = chat.send_message(message)
        
        return jsonify({
            'response': response.text,
            'success': True,
            'is_image': False
        })
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

def generate_image(prompt):
    """
    Generate image using external service (Hugging Face Stable Diffusion)
    Note: You need to get a Hugging Face token and replace the placeholder
    """
    try:
        headers = {"Authorization": f"Bearer {IMAGE_GEN_TOKEN}"}
        payload = {"inputs": prompt}
        
        response = requests.post(IMAGE_GEN_API, headers=headers, json=payload)
        response.raise_for_status()
        
        # Convert image to base64 for web display
        image = Image.open(io.BytesIO(response.content))
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
        
    except Exception as e:
        print(f"Image generation error: {e}")
        return None

@app.route('/api/reset', methods=['POST'])
def reset_chat():
    global chat
    chat = text_model.start_chat()
    return jsonify({'success': True, 'message': 'Chat reset successfully'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
