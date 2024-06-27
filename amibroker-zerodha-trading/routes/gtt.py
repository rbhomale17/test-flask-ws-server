from flask import Blueprint, request, jsonify, session
from kiteconnect import KiteConnect

def create_gtt_blueprint(db, kite):
    gtt_bp = Blueprint('gtt', __name__)
    
    @gtt_bp.route('/gtts', methods=['GET'])
    @gtt_bp.route('/gtts/<int:trigger_id>', methods=['GET'])
    def handle_gtt(trigger_id = None):
        try:
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401
            
            # kite.set_access_token(access_token)
            if trigger_id is None: 
            # Fetch the orders
                gtts_order = kite.get_gtts()
                return gtts_order
            else:             
                gtt_order = kite.get_gtt(trigger_id)
                return gtt_order
        except Exception as e:
            return jsonify({"error": str(e)}), 400
            

    @gtt_bp.route('/placegtt', methods=['POST'])
    def place_gtt():
        try:
            # Ensure access token is set
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401

            # kite.set_access_token(access_token)

            # Parse the JSON request data
            order_data = request.get_json()

            # Extract individual fields from the JSON request
            trigger_type = order_data["trigger_type"]
            tradingsymbol = order_data["tradingsymbol"]
            exchange = order_data["exchange"]
            trigger_values = order_data["trigger_values"]
            last_price = order_data["last_price"]
            orders = order_data["orders"]

            # Place the GTT order
            order = kite.place_gtt(
                trigger_type=trigger_type,
                tradingsymbol=tradingsymbol,
                exchange=exchange,
                trigger_values=trigger_values,
                last_price=last_price,
                orders=orders
            )
            if order:
                trigger_id=order['data']['id']
                db.log_gtttransaction(session.get('user_id'), trigger_type,
                tradingsymbol,
                exchange,
                trigger_values,
                last_price,
                orders,
                trigger_id)
                return jsonify({"message": "GTT order placed successfully", "order": order})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    @gtt_bp.route('/modifygtt/<string:trigger_id>', methods=['PUT'])
    def modify_gtt(trigger_id):
        try:
            # Ensure access token is set
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401

            # kite.set_access_token(access_token)

            # Parse the JSON request data
            order_data = request.get_json()

            # Extract individual fields from the JSON request
            trigger_type = order_data["trigger_type"]
            tradingsymbol = order_data["tradingsymbol"]
            exchange = order_data["exchange"]
            trigger_values = order_data["trigger_values"]
            last_price = order_data["last_price"]
            orders = order_data["orders"]

            # Modify the GTT order
            order = kite.modify_gtt(
                trigger_id=trigger_id,
                trigger_type=trigger_type,
                tradingsymbol=tradingsymbol,
                exchange=exchange,
                trigger_values=trigger_values,
                last_price=last_price,
                orders=orders
            )
            if order:
                update_fields = {}
                optional_fields = ["trigger_type","tradingsymbol","exchange","trigger_values","last_price","orders"]
            
                for field in optional_fields:
                    if field in order_data:
                        update_fields[field] = order_data[field]
                db.update_gtttransaction(trigger_id, **update_fields)

                return jsonify({"message": "GTT order modified successfully", "order": order})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    @gtt_bp.route("/delete/<int:trigger_id>", methods = ['DELETE'])
    def delete_gtt(trigger_id):
        try:
            # Ensure access token is set
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401
            return kite.delete_gtt(trigger_id)
            
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    return gtt_bp