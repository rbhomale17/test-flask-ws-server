from flask import Blueprint, request, jsonify, session
from kiteconnect import KiteConnect

def create_order_blueprint(db, kite):
    order_bp = Blueprint('order', __name__)
    
    @order_bp.route('/orders', methods=['GET'])
    @order_bp.route('/orders/<int:order_id>', methods=['GET'])
    def handle_orders(order_id=None):
        try:
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401

            # kite.set_access_token(access_token)

            if order_id is None:
                # If order_id is not provided, fetch all orders
                orders = kite.orders()
                return orders
            else:
                # If order_id is provided, fetch specific order details
                order = kite.order_history(order_id)
                return order
        except Exception as e:
            return jsonify({"error": str(e)}), 400


    @order_bp.route('/placeorder', methods=['POST'])
    def placeorder():
        try:
            #Ensure access token is set
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401
            
            # kite.set_access_token(access_token)

            # Parse the JSON request data
            order_data = request.get_json()
            print(order_data)

            # Extract individual fields from the JSON request
            variety = order_data.get("variety")
            exchange = order_data["exchange"]
            tradingsymbol = order_data["tradingsymbol"]
            transaction_type = order_data["transaction_type"]
            quantity = order_data["quantity"]
            product = order_data["product"]
            order_type = order_data["order_type"]
            price = order_data.get("price")  # Optional
            validity = order_data.get("validity")  # Optional
            validity_ttl = order_data.get("validity_ttl")  # Optional
            disclosed_quantity = order_data.get("disclosed_quantity")  # Optional
            trigger_price = order_data.get("trigger_price")  # Optional
            iceberg_legs = order_data.get("iceberg_legs")  # Optional
            iceberg_quantity = order_data.get("iceberg_quantity")  # Optional
            auction_number = order_data.get("auction_number")  # Optional
            tag = order_data.get("tag")  # Optional

            # Place the order
            order_id = kite.place_order(
                variety=variety,
                exchange=exchange,
                tradingsymbol=tradingsymbol,
                transaction_type=transaction_type,
                quantity=quantity,
                product=product,
                order_type=order_type,
                price=price,
                validity=validity,
                validity_ttl=validity_ttl,
                disclosed_quantity=disclosed_quantity,
                trigger_price=trigger_price,
                iceberg_legs=iceberg_legs,
                iceberg_quantity=iceberg_quantity,
                auction_number=auction_number,
                tag=tag
            )
            if order_id:
                db.log_transaction(session['user_id'], variety, exchange, tradingsymbol, transaction_type, quantity, product, order_type, price, validity, validity_ttl, disclosed_quantity, trigger_price, iceberg_legs, iceberg_quantity, auction_number, tag, order_id)
                return jsonify({"message": "Order placed successfully", "order_id": order_id})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @order_bp.route('/modifyorder', methods=['PUT'])
    def modifyorder():
        try:
            #Ensure access token is set
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401
            
            # kite.set_access_token(access_token)

            # Parse the JSON request data
            order_data = request.get_json()

            # Extract individual fields from the JSON request
            variety = order_data.get("variety")
            order_id = order_data["order_id"]
            parent_order_id = order_data.get("parent_order_id") # Optional
            quantity = order_data.get("quantity") # Optional
            price = order_data.get("price")  # Optional
            order_type = order_data.get("order_type")  # Optional
            trigger_price = order_data.get("trigger_price")  # Optional
            validity = order_data.get("validity")  # Optional
            disclosed_quantity = order_data.get("disclosed_quantity")  # Optional
            
            #modify the order
            order_id = kite.modify_order(
                variety=variety,
                order_id = order_id,
                parent_order_id = parent_order_id,
                quantity=quantity,
                price = price,
                order_type=order_type,
                trigger_price=trigger_price,
                validity=validity,
                disclosed_quantity=disclosed_quantity
            )
            # Extract fields to be updated
            if order_id:
                update_fields = {}
                optional_fields = ["variety", "parent_order_id", "quantity", "price", "order_type", 
                                "trigger_price", "validity", "disclosed_quantity", "iceberg_legs", 
                                "iceberg_quantity", "auction_number", "tag"]
                
                for field in optional_fields:
                    if field in order_data:
                        update_fields[field] = order_data[field]
                db.update_transaction(order_id, **update_fields)
                return jsonify({"message": "Order modified successfully", "order_id": order_id})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    @order_bp.route('/cancelorder', methods=['DELETE'])
    def cancelorder():
        try:
            # Ensure access token is set
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401
            
            # kite.set_access_token(access_token)

            # Parse the JSON request data
            order_data = request.get_json()

            # Extract individual fields from the JSON request
            variety = order_data.get("variety")
            order_id = order_data.get("order_id")
            parent_order_id = order_data.get("parent_order_id")
            
            order_id = kite.cancel_order(variety, order_id, parent_order_id)
            if order_id:
                return jsonify({"message": "Order canceled successfully", "order_id": order_id})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    @order_bp.route('/trades', methods=['GET'])
    @order_bp.route('/trades/<int:order_id>', methods=['GET'])
    def handle_trades(order_id=None):
        try:
            # Ensure access token is set
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401
            
            # kite.set_access_token(access_token)
            if order_id is None: 
            # Fetch the orders
                trades = kite.trades()
                return trades
            else:             
                trade = kite.order_trades(order_id)
                return trade
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    return order_bp