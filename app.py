from flask import Flask, request, jsonify
import asyncio
import websockets
import json

app = Flask(__name__)

# Standard Flask routes
@app.route('/')
def index():
    return jsonify({"status": "success", "message": "Hello Boys."}), 200

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    # Process the data as needed
    print(f"Received data via HTTP: {data}")
    return jsonify({"status": "success", "message": "Data received"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)


