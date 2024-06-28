from flask import Blueprint, request, jsonify, session
from kiteconnect import KiteConnect

def create_query_blueprint(db, kite):
    query_bp = Blueprint('query', __name__)
    
    @query_bp.route('/query', methods=["GET"])
    def query():
        try:
            #Ensure access token is set
            access_token = session.get('access_token')
            if not access_token:
                return jsonify({"error": "access token not found"}), 401
        

            # Extract individual fields from the JSON request
            variety = request.args.get("variety")
            exchange = request.args.get("exchange")
            tradingsymbol = request.args.get("tradingsymbol")
            transaction_type = request.args.get("transaction_type")
            quantity = request.args.get("quantity")
            product = request.args.get("product")
            order_type = request.args.get("order_type")
            price = request.args.get("price")  # Optional
            validity = request.args.get("validity")  # Optional
            validity_ttl = request.args.get("validity_ttl")  # Optional
            disclosed_quantity = request.args.get("disclosed_quantity")  # Optional
            trigger_price = request.args.get("trigger_price")  # Optional
            iceberg_legs = request.args.get("iceberg_legs")  # Optional
            iceberg_quantity = request.args.get("iceberg_quantity")  # Optional
            auction_number = request.args.get("auction_number")  # Optional
            tag = request.args.get("tag")  # Optional
            
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

    return query_bp