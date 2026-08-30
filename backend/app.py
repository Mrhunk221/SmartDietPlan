import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai

load_dotenv()

app = Flask(__name__)
CORS(app)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "SmartDiet AI Backend is running!"})

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "error": "No input data provided."}), 400

        height = data.get("height", "")
        weight = data.get("weight", "")
        age = data.get("age", "")
        gender = data.get("gender", "")
        goal = data.get("goal", "")
        diettype = data.get("diettype", "")
        validity = data.get("validity", "")
        restrictions = ", ".join(data.get("restrictions", []))

        prompt = (
            f"Create a personalized {diettype} diet plan for a {gender}, "
            f"age {age}, height {height}cm, weight {weight}kg. "
            f"Goal: {goal}. Duration: {validity}. Dietary restrictions: {restrictions}\n\n"
            f"Please format the response clearly using daily headers (e.g. ### Day 1) "
            f"and bullet points for Breakfast, Lunch, Dinner, and Snacks."
        )

        # Updated to the current gemini-3.6-flash model
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return jsonify({"success": True, "plan": response.text})

    except Exception as e:
        print("Backend error:", str(e))
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)