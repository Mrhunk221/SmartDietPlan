import os
from flask import Flask, send_from_directory, jsonify, request
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app to serve frontend files from the root directory
app = Flask(__name__, static_folder='../', static_url_path='')

# Initialize Gemini Client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "SmartDiet AI Backend is running!"})

@app.route('/api/generate-plan', methods=['POST'])
def generate_plan():
    try:
        data = request.get_json() or {}
        goal = data.get('goal', 'Lose Weight')
        diet_type = data.get('diettype', 'Balanced')
        validity = data.get('validity', '1 Week')
        
        prompt = (
            f"Create a structured, healthy meal plan for a duration of {validity} "
            f"for someone whose goal is {goal} and prefers a {diet_type} diet. "
            f"You MUST provide a distinct, full daily breakdown for every single day "
            f"covered by {validity} (for example, Day 1, Day 2, Day 3, etc. up to the full duration). "
            f"Do not summarize or provide only one day."
        )
        
        if client:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt
            )
            plan_text = response.text
        else:
            plan_text = "Gemini API key not configured on backend."

        return jsonify({"success": True, "plan": plan_text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)