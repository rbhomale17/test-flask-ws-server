import json
from flask_socketio import emit

def handle_connect():
    print('Client connected')

def handle_disconnect():
    print('Client disconnected')

def process_signal(data, app):
    print(f"Received data: {data}")
    try:
        with app.app_context():
            parsed_data = json.loads(data)
            signal_type = parsed_data.get("signal_type")

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
