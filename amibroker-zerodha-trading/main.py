import eventlet
eventlet.monkey_patch()
from flask import Flask, request, g
from kiteconnect import KiteConnect
from flask_socketio import SocketIO
from dotenv import dotenv_values
from dbconfig import Database
import routes
import websocket
import eventlet.wsgi
import os

para = {
        "user": os.getenv("user"),
        "password": os.getenv("password"),
        "host": os.getenv("host"),
        "port": os.getenv("port"),
        "database": os.getenv("database"),
        "api_key":os.getenv("api_key"),
        "session_secret_key":os.getenv("session_secret_key")
        }


db = Database(para)
kite = KiteConnect(api_key=para['api_key'])

app = Flask(__name__)
app.secret_key = para["session_secret_key"]
socketio = SocketIO(app, async_mode='eventlet')

routes.register_blueprints(app, db, kite)
websocket.register_websocket_handlers(socketio, app)


@app.after_request
def log_response_info(response):
    print(f"Route hit: {request.path}, Status: {response.status_code}")
    return response

@app.teardown_request
def log_request_teardown(exception=None):
    if exception:
        print(f"Route hit: {request.path}, Exception: {exception}")

# SocketIO logging
@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

@socketio.on('custom_event')
def handle_custom_event(data):
    print(f"Custom event received: {data}")
    # Handle the event and respond as needed
    socketio.emit('response', {'status': 'success'})

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
