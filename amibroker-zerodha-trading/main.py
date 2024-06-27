from flask import Flask
from kiteconnect import KiteConnect
from flask_socketio import SocketIO
from dotenv import dotenv_values
from dbconfig import Database
import routes
import websocket
import eventlet
import eventlet.wsgi
import os



para = {key: value for key, value in dotenv_values('.env').items()}
print(para,os.getenv("user"))
db = Database(para)
kite = KiteConnect(api_key=para['api_key'])

app = Flask(__name__)
app.secret_key = para["session_secret_key"]
socketio = SocketIO(app, async_mode='eventlet')

routes.register_blueprints(app, db, kite)
websocket.register_websocket_handlers(socketio, app)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
