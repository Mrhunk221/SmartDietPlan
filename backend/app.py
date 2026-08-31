import os
from flask import Flask, send_from_directory, jsonify

# Initialize Flask app to serve frontend files from the root directory
app = Flask(__name__, static_folder='../', static_url_path='')

@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "SmartDiet AI Backend is running!"})

if __name__ == '__main__':
    app.run(debug=True)