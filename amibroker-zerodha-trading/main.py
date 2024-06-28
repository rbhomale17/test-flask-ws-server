import eventlet
eventlet.monkey_patch()
from flask import Flask
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

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
