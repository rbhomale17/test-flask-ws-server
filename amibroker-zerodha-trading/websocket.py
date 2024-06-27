# from flask_socketio import SocketIO, emit
# from flask import request
# from kiteconnect import KiteConnect
# from dbconfig import Database
# from dotenv import dotenv_values

# para = {key: value for key, value in dotenv_values('.env').items()}

# db = Database(para)
# kite = KiteConnect(api_key=para['api_key'])

# socketio = SocketIO()

# @socketio.on('connect')
# def handle_connect():
#     print('Client connected:', request.sid)
#     emit('response', {'message': 'Connected to server'})

# @socketio.on('disconnect')
# def handle_disconnect():
#     print('Client disconnected:', request.sid)

# @socketio.on('signal')
# def handle_signal(data):
#     try:
#         print('Received signal:', data)
#         # Process the signal and place an order using the KiteConnect API
#         access_token = data.get('access_token')
#         if not access_token:
#             emit('response', {'error': 'access token not found'})
#             return

#         kite.set_access_token(access_token)

#         # Extract order details from the signal data
#         tradingsymbol = data.get('tradingsymbol')
#         exchange = data.get('exchange')
#         transaction_type = data.get('transaction_type')
#         quantity = data.get('quantity')
#         product = data.get('product')
#         order_type = data.get('order_type')
#         price = data.get('price')
#         validity = data.get('validity')
#         disclosed_quantity = data.get('disclosed_quantity')
#         trigger_price = data.get('trigger_price')

#         # Place the order
#         order_id = kite.place_order(
#             exchange=exchange,
#             tradingsymbol=tradingsymbol,
#             transaction_type=transaction_type,
#             quantity=quantity,
#             product=product,
#             order_type=order_type,
#             price=price,
#             validity=validity,
#             disclosed_quantity=disclosed_quantity,
#             trigger_price=trigger_price
#         )
#         db.log_transaction(data['user_id'], exchange, tradingsymbol, transaction_type, quantity, product, order_type, price, validity, disclosed_quantity, trigger_price, order_id)
#         emit('response', {'message': 'Order placed successfully', 'order_id': order_id})
#     except Exception as e:
#         emit('response', {'error': str(e)})

# def init_app(app):
#     socketio.init_app(app)
#     return socketio

# websocket.py
'''------------------------------------------latest old------------------------------'''
# import json
# from flask_socketio import emit

# def handle_connect():
#     print('Client connected')

# def handle_disconnect():
#     print('Client disconnected')

# def handle_signal(data, app):
#     print(f"Received data: {data}")

#     with app.app_context():
#         parsed_data = json.loads(data)
#         signal_type = parsed_data.get("signal_type")

#         if signal_type == "placeorder":
#             print(parsed_data)
#             response = app.test_client().post("/placeorder", json=parsed_data)
#             result = response.get_json()
#             print(f"Place Order Response: {result}")
#         elif signal_type == "placegtt":
#             response = app.test_client().post("/placegtt", json=parsed_data)
#             result = response.get_json()
#             print(f"Place GTT Response: {result}")
#         else:
#             result = {"status": "error", "message": "Unknown signal type"}

#         emit('response', json.dumps(result))

# def register_websocket_handlers(socketio, app):
#     @socketio.on('connect')
#     def on_connect():
#         handle_connect()

#     @socketio.on('disconnect')
#     def on_disconnect():
#         handle_disconnect()

#     @socketio.on('signal')
#     def on_signal(data):
#         handle_signal(data, app)



# websocket.py

import json
from flask_socketio import emit

def handle_connect():
    print('Client connected')

def handle_disconnect():
    print('Client disconnected')

def process_signal(data, app):
    print(f"Received data: {data}")

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
