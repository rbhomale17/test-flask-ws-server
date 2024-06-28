import json
from flask_socketio import emit
###############
import json
from flask import Flask, request, jsonify

log_file_path = 'signal_log.json'

def handle_connect():
    print('Client connected')

def handle_disconnect():
    print('Client disconnected')

def log_data(data):
    try:
        # Read existing data
        with open(log_file_path, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    # Append new data
    logs.append(data)

    # Write updated data back to the file
    with open(log_file_path, 'w') as f:
        json.dump(logs, f, indent=4)
        
def process_signal(data, app):
    print(f"Received data: {data}")
    try:
        
        with app.app_context():
            parsed_data = json.loads(data)
            signal_type = parsed_data.get("signal_type")

            # Log the received data
            log_data(parsed_data)
######################
            if signal_type == "placeorder":
                response = app.test_client().post("/placeorder", json=parsed_data)
                result = response.get_json()
                print(f"Place Order Response: {result}")
            elif signal_type == "placegtt":
                response = app.test_client().post("/placegtt", json=parsed_data)
                result = response.get_json()
                print(f"Place GTT Response: {result}")
            else:
                result = {"status": "error", "message": "Unknown signal type"}

            emit('response', json.dumps(result))
    except Exception as e:
        print(f"Error processing signal: {e}")
        result = {"status": "error", "message": str(e)}
        emit('response', result, broadcast=False)

def handle_signal(data, app):
    process_signal(data, app)

def register_websocket_handlers(socketio, app):
    @socketio.on('connect')
    def on_connect():
        handle_connect()

    @socketio.on('disconnect')
    def on_disconnect():
        handle_disconnect()

    @socketio.on('signal')
    def on_signal(data):
        handle_signal(data, app)
