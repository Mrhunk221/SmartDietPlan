import os
from flask import Flask, send_from_directory, jsonify, request
from google import genai
from dotenv import load_dotenv

# Load environment variables (.env for local development)
load_dotenv()

# Initialize Flask app
# static_folder points to the root directory where index.html, script.js, and style.css live
app = Flask(__name__, static_folder='../', static_url_path='')

# Initialize Gemini Client using the environment variable
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

@app.route('/')
def serve_frontend():
    # Serves your main frontend web page
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "SmartDiet AI Backend is running!"})

# Add your diet plan generation or other API endpoints below as needed:
# @app.route('/api/generate-plan', methods=['POST'])
# def generate_plan():
#     ...

if __name__ == '__main__':
    app.run(debug=True)