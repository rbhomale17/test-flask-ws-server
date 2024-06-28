from flask import Blueprint, request, jsonify, session
from kiteconnect import KiteConnect

import json

app = Flask(__name__)
log_file_path = 'signal_log.json'

def create_log_blueprint(db, kite):
    log_bp = Blueprint('log', __name__)
    @app.route('/log', methods=['GET'])
    def get_log():
        try:
            with open(log_file_path, 'r') as f:
                logs = json.load(f)
            return jsonify(logs)
        except FileNotFoundError:
            return jsonify([]), 404

      return log_bp;
