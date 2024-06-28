from flask import Blueprint, request, jsonify, session,render_template_string
from kiteconnect import KiteConnect

def index_blueprint(db, kite):
    index_bp = Blueprint('index', __name__)
    
    @index_bp.route('/',)
    def home():
        return render_template_string('<h1>Welcome to NeuralHq auto-Trend</h1>')
    return index_bp